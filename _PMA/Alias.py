# -*- coding: utf-8 -*-
# Copyright (C) 2004-2015 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA.Alias
#
# Purpose
#    Model mail aliases
#
# Revision Dates
#    19-Sep-2004 (CT) Creation
#     1-May-2006 (CT) `Alias_Mgr.transitive_translation` added
#    16-Jun-2013 (CT) Correct import of `Regexp`
#     2-Apr-2015 (CT) Add `get`, `__getitem__` to `Alias_Mgr`
#     2-Apr-2015 (CT) Change `add_alias_file` to use `expanded_path`,
#                     ignore missing file
#     2-Apr-2015 (CT) Change `Alias.__str__` to return joined `email_addresses`
#    28-Oct-2015 (CT) Improve Python 3 compatibility
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _TFL                    import TFL
from   _PMA                    import PMA

from   _TFL.predicate          import split_hst
from   _TFL.pyk                import pyk
from   _TFL.Regexp             import *
from   _TFL                    import sos


from   _PMA                    import Lib

import _TFL._Meta.Object

@pyk.adapt__str__
class Alias (TFL.Meta.Object) :
    """Model a single alias"""

    def __init__ (self, key, values) :
        self.key    = key
        self.values = values
    # end def __init__

    def addresses (self) :
        return Lib.getaddresses (self.values)
    # end def addresses

    def email_addresses (self) :
        for n, v in self.addresses () :
            yield v
    # end def email_addresses

    def real_names (self) :
        for n, v in self.addresses () :
            yield n
    # end def real_names

    def __repr__ (self) :
        return "%s (%r, %r)" % (self.__class__.__name__, self.key, self.values)
    # end def __repr__

    def __str__ (self) :
        return ", ".join (self.email_addresses ())
    # end def __str__

# end class Alias

class Alias_Mgr (TFL.Meta.Object) :
    """Model a collection of aliases"""

    _alias_sep = Regexp ("\n(?!\\s)") ### a new-line followed by non-whitespace
    _alias_pat = Regexp \
        ( r"(?P<key> [-a-zA-Z0-9.]+)"
          r"\s* : \s*"
          r"(?P<value> .*)"
        , re.VERBOSE | re.DOTALL
        )

    def __init__ (self, * files) :
        self.aliases = {}
        for f in files :
            self.add_alias_file (f)
    # end def __init__

    def add_alias_buffer (self, buffer) :
        aliases = self.aliases
        pat     = self._alias_pat
        for entry in self._alias_sep.split (buffer) :
            entry = entry.strip ()
            if entry :
                if pat.match (entry) :
                    key  = pat.key
                    vals = filter \
                        (None, [v.strip () for v in pat.value.split (",")])
                    if vals :
                        aliases [key] = Alias (key, vals)
    # end def add_alias_buffer

    def add_alias_file (self, name) :
        path = sos.expanded_path (name)
        if sos.path.exists (path) :
            with open (path) as f :
                buffer = pyk.decoded (f.read ())
            self.add_alias_buffer (buffer)
    # end def add_alias_file

    def get (self, key, default = None) :
        try :
            return self [key]
        except KeyError :
            return default
    # end def get

    def transitive_translation (self, alias) :
        """Return transitive translation of `alias`"""
        result  = set ()
        aliases = self.aliases
        for v in alias.email_addresses () :
            if v in aliases :
                result.update (self.transitive_translation (aliases [v]))
            else :
                result.add (v)
        return result
    # end def transitive_translation

    def __getitem__ (self, key) :
        map     = self.aliases
        rn, ea  = Lib.parseaddr (key)
        l, s, d = split_hst (ea, "@")
        if s :
            try :
                return map [l]
            except KeyError :
                pass
        return map [ea]
    # end def __getitem__

# end class Alias_Mgr

"""
from   _PMA                    import PMA
import _PMA.Alias
amgr = PMA.Alias_Mgr ("/etc/aliases", "~/.aliases", "~/.mh_aliases")
a    = amgr ["mailer-daemon"]
list (a.addresses ())

"""
if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Alias

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
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
#    ««revision-date»»···
#--

from   Regexp                  import *
from   _TFL                    import TFL
from   _PMA                    import PMA
import _TFL._Meta.Object
from   _PMA                    import Lib

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
        return "%s: %s" % (self.key, ", ".join (self.values))
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
        f       = open (name)
        buffer  = f.read ()
        f.close ()
        self.add_alias_buffer (buffer)
    # end def add_alias_file

# end class Alias_Mgr

"""
from   _PMA                    import PMA
import _PMA.Alias
amgr = PMA.Alias_Mgr ("/etc/aliases", "/swing/private/tanzer/.mh_aliases")
a    = amgr.aliases ["baby-news"]
list (a.addresses ())

"""
if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Alias

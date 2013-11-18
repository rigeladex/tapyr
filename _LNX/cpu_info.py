# -*- coding: utf-8 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package LNX.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    LNX.cpu_info
#
# Purpose
#    Provide information about CPU a Linux system is running on
#
# Revision Dates
#    12-May-2009 (CT) Creation
#     8-Nov-2013 (CT) Improve `_ignore_rep` for `i[357]` CPUs
#    ««revision-date»»···
#--

from   __future__  import with_statement

from   _LNX import LNX
from   _TFL import TFL

import _TFL._Meta.Object
from   _TFL.Regexp import *

class _Cpu_Info_ (TFL.Meta.Object) :

    _dict = None
    _keys = set ()

    _paren_rep  = Re_Replacer (r"\s*\([^)]*\)\s*", " ")
    _ws_rep     = Re_Replacer (r"\s\s+",           " ")
    _ignore_rep = Multi_Re_Replacer \
        ( Re_Replacer (r"Intel\s+|CPU.*",  "")
        , Re_Replacer (r"(i\d)-\d+[A-Z]+", r"\1")
        )
    _space_rep  = Re_Replacer (r" ", "_")

    def items (self) :
        return list (self.iteritems ())
    # end def items

    def iteritems (self) :
        map  = self._dict
        for k in self.iterkeys () :
            yield k, map [k]
    # end def iteritems

    def iterkeys (self) :
        if self._dict is None :
            self._setup ()
        return iter (self._keys)
    # end def iterkeys

    def itervalues (self) :
        for k, v in self.iteritems () :
            yield v
    # end def itervalues

    def keys (self) :
        return list (self.iterkeys ())
    # end def keys

    def values (self) :
        return list (self.itervalues ())
    # end def values

    def _setup (self) :
        map  = self._dict = {}
        keys = self._keys
        with open ("/proc/cpuinfo") as f :
            for l in f :
                l = l.strip ()
                if not l :
                    continue
                k, v  = l.split (":")
                k     = k.strip ()
                if k not in keys :
                    v = v.strip ()
                    if k == "model name" :
                        v = self._paren_rep  (v)
                        v = self._ignore_rep (v)
                    if k == "cpu MHz" :
                        try :
                            v = float (v)
                        except :
                            pass
                        else :
                            v = "%5.0f" % (v, )
                    v = self._ws_rep (v).strip ()
                    map [k] = v
                    keys.add (k)
                    kk = self._space_rep (k)
                    if kk != k :
                        map [kk] = v
    # end def _setup

    def __getattr__ (self, name) :
        if self._dict is None :
            self._setup ()
        result = self._dict [name]
        setattr (self, name, result)
        return result
    # end def __getattr__

    def __getitem__ (self, key) :
        if self._dict is None :
            self._setup ()
        return self._dict [key]
    # end def __getitem__

# end class _Cpu_Info_

cpu_info = _Cpu_Info_ ()

if __name__ != "__main__" :
    LNX._Export ("cpu_info")
else :
    print "%(model name)s/%(cpu MHz)s" % cpu_info
### __END__ LNX.cpu_info

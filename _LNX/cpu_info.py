# -*- coding: utf-8 -*-
# Copyright (C) 2009-2018 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This module is part of the package LNX.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
#    22-Mar-2018 (CT) Make Python-3 compatible
#    ««revision-date»»···
#--

from   _LNX        import LNX
from   _TFL        import TFL

from   _TFL.Regexp import *

import _TFL._Meta.Object

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
    print ("%(model name)s/%(cpu MHz)s" % cpu_info)
### __END__ LNX.cpu_info

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    Ival_Map
#
# Purpose
#    Map intervals to values
#
# Revision Dates
#     5-Jul-2003 (CT) Creation
#    24-Apr-2009 (CT) `index` factored (and changed to use `bisect`)
#    24-Apr-2009 (CT) `keys`  added
#    11-Jun-2009 (CT) s/bisect_left/bisect_right/
#    ««revision-date»»···
#--

from   _TFL               import TFL
from   _TFL._Meta         import Meta
import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.predicate

from   bisect             import bisect_right

class Ival_Map (Meta.Object) :
    """Mapping of intervals to values.

       >>> ivm = Ival_Map ((500, 65), (1500, 85), (100000, 95), (1000, 75))
       >>> ivm
       [(500, 65), (1000, 75), (1500, 85), (100000, 95)]
       >>> ivm [100]
       65
       >>> ivm [499]
       65
       >>> ivm [500]
       75
       >>> ivm [1600]
       95
       >>> ivm [160000]
       95
       >>> ivm [2**31]
       95
       >>> ivm [-2**31]
       65
    """

    def __init__ (self, * iv_list) :
        self.iv_map = TFL.sorted (iv_list)
    # end def __init__

    def index (self, key) :
        result = bisect_right (self.keys, key)
        if result == len (self.iv_map) :
            result -= 1
        return result
    # end def index

    @TFL.Meta.Once_Property
    def keys (self) :
        return [i for (i, v) in self.iv_map]
    # end def keys

    def __getitem__ (self, key) :
        return self.iv_map [self.index (key)] [1]
    # end def __getitem__

    def __str__ (self) :
        return str (self.iv_map)
    # end def __str__

    def __repr__ (self) :
        return repr (self.iv_map)
    # end def __repr__

# end class Ival_Map

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Ival_Map

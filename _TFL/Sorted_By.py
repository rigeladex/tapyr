# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Sorted_By
#
# Purpose
#    Implement composite sort-key for list of sort criteria
#
# Revision Dates
#    18-Sep-2009 (CT) Creation
#    19-Sep-2009 (MG) `_desc_key` factored to avoind binding problems of the 
#                     `get` function
#    ««revision-date»»···
#--

from   _TFL import TFL

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Accessor

class Sorted_By (TFL.Meta.Object) :
    """Composite sort key for list of sort criteria.

       >>> from _TFL.Record import Record as R
       >>> NL = chr (10)
       >>> def show (l, key) :
       ...     print NL.join (str (s) for s in sorted (l, key = key))
       ...
       >>> l = [ R (a = 1, b = 1, c = "abcd")
       ...     , R (a = 1, b = 2, c = "ABCD")
       ...     , R (a = 1, b = 2, c = "efg")
       ...     , R (a = 2, b = 1, c = "xyz")
       ...     , R (a = 2, b = 1, c = " xyzz")
       ...     , R (a = 2, b = 1, c = "  xyzzz")
       ...     ]
       >>> show (l, key = Sorted_By (["a", "b"]))
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By (["a", "-b"]))
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By (["b", "a"]))
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       >>> show (l, key = Sorted_By (["-b", "a"]))
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By (["-b", "-a"]))
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       >>> show (l, key = Sorted_By (["b", "c"]))
       (a = 2, b = 1, c =   xyzzz)
       (a = 2, b = 1, c =  xyzz)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       >>> show (l, key = Sorted_By (["b", "-c"]))
       (a = 2, b = 1, c = xyz)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 2, c = ABCD)
       >>> show (l, key = Sorted_By (["-b", "c"]))
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By (["-b", "-c"]))
       (a = 2, b = 1, c = xyz)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = ABCD)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By (["c"]))
       (a = 2, b = 1, c =   xyzzz)
       (a = 2, b = 1, c =  xyzz)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c = xyz)
       >>> show (["1", 0, "42", 2.4], Sorted_By ([int]))
       0
       1
       2.4
       42
    """

    class Descending (TFL.Meta.Object) :

        def __init__ (self, key) :
            self.key = key
        # end def __init__

        def __lt__ (self, rhs) :
            return rhs.key < self.key
        # end def __lt__

    # end class Descending

    def __init__ (self, criteria) :
        self.criteria = criteria
    # end def __init__

    def __call__ (self, x) :
        return tuple (key (x) for key in self.keys)
    # end def __call__

    @Once_Property
    def keys (self) :
        result = []
        Desc   = self.Descending
        for c in self.criteria :
            if hasattr (c, "__call__") :
                key = c
            elif c.startswith ("-") :
                key = self._desc_key (c [1:])
            else :
                key = getattr (TFL.Getter, c)
            result.append (key)
        return result
    # end def keys

    def _desc_key (self, c) :
        get = getattr (TFL.Getter, c)
        return lambda x : self.Descending (get (x))
    # end def _desc_key

# end class Sorted_By

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Sorted_By

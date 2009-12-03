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
#    21-Sep-2009 (CT) `Descending.__lt__` fixed
#    21-Sep-2009 (CT) `Desc_Getter` added to improve introspection and to
#                     replace `_desc_key`
#    21-Sep-2009 (CT) `Descending.__eq__` added and doctests fixed
#    22-Sep-2009 (CT) `Descending` made `totally_ordered`
#                     `Descending.__eq__` removed again
#    14-Oct-2009 (CT) Signature of `Sorted_By` changed from `criteria`
#                     to `* criteria`
#     3-Dec-2009 (CT) `__iter__` added
#     3-Dec-2009 (CT) `keys` changed to allow `-` following `.`, too
#    ««revision-date»»···
#--

from   _TFL import TFL

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL._Meta.totally_ordered import totally_ordered

import _TFL.Accessor

class Desc_Getter (TFL.Meta.Object) :

    @totally_ordered
    class Descending (TFL.Meta.Object) :

        def __init__ (self, key) :
            self.key = key
        # end def __init__

        def __lt__ (self, rhs) :
            return self.key > rhs.key
        # end def __lt__

    # end class Descending

    def __init__ (self, getter) :
        self.getter = getter
    # end def __init__

    def __call__ (self, x) :
        return self.Descending (self.getter (x))
    # end def __call__

    def __repr__ (self) :
       return "%s-%s" % (self.Descending.__name__, self.getter)
    # end def __repr__

# end class Desc_Getter

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
       >>> print NL.join (str (s) for s in l)
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By ("a"))
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By ("a", "b"))
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By ("a", "-b"))
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By ("b", "a"))
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       >>> show (l, key = Sorted_By ("-b", "a"))
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By ("-b", "-a"))
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c = xyz)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       (a = 1, b = 1, c = abcd)
       >>> show (l, key = Sorted_By ("b", "c"))
       (a = 2, b = 1, c =   xyzzz)
       (a = 2, b = 1, c =  xyzz)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       >>> show (l, key = Sorted_By ("b", "-c"))
       (a = 2, b = 1, c = xyz)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       (a = 1, b = 2, c = efg)
       (a = 1, b = 2, c = ABCD)
       >>> show (l, key = Sorted_By ("-b", "c"))
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c =   xyzzz)
       (a = 2, b = 1, c =  xyzz)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c = xyz)
       >>> show (l, key = Sorted_By ("-b", "-c"))
       (a = 1, b = 2, c = efg)
       (a = 1, b = 2, c = ABCD)
       (a = 2, b = 1, c = xyz)
       (a = 1, b = 1, c = abcd)
       (a = 2, b = 1, c =  xyzz)
       (a = 2, b = 1, c =   xyzzz)
       >>> show (l, key = Sorted_By ("c"))
       (a = 2, b = 1, c =   xyzzz)
       (a = 2, b = 1, c =  xyzz)
       (a = 1, b = 2, c = ABCD)
       (a = 1, b = 1, c = abcd)
       (a = 1, b = 2, c = efg)
       (a = 2, b = 1, c = xyz)
       >>> show (["1", 0, "42", 2.4], Sorted_By (int))
       0
       1
       2.4
       42
    """

    def __init__ (self, * criteria) :
        self.criteria = criteria
    # end def __init__

    def __call__ (self, x) :
        return tuple (key (x) for key in self.keys)
    # end def __call__

    @Once_Property
    def keys (self) :
        result = []
        for c in self.criteria :
            if hasattr (c, "__call__") :
                key = c
            elif c.startswith ("-") or ".-" in c :
                key = Desc_Getter (getattr (TFL.Getter, c.replace ("-", "")))
            else :
                key = getattr (TFL.Getter, c)
            result.append (key)
        return result
    # end def keys

    def __iter__ (self) :
        return iter (self.criteria)
    # end def __iter__

    def __repr__ (self) :
       return "<%s: %s>" % \
          (self.__class__.__name__, ", ".join (str (key) for key in self.keys))
    # end def __repr__

# end class Sorted_By

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Sorted_By

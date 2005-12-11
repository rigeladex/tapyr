#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    TFL.Interval_Set
#
# Purpose
#    Model a sorted set of intervals
#
# Revision Dates
#     9-Dec-2005 (RSC) Creation
#    ««revision-date»»···
#--

from   _TFL                  import TFL

import _TFL._Meta.Object
from   bisect import bisect

class Interval_Set (TFL.Meta.Object) :
    """Class for modelling a sorted set of intervals.

       >>> from   _TFL   import TFL
       >>> import _TFL.Numeric_Interval
       >>> N = TFL.Numeric_Interval
       >>> i = Interval_Set (N (  0, 100))
       >>> j = Interval_Set (N (100, 200))
       >>> k = Interval_Set (N ( 20,  50))
       >>> l = i.union (j)
       >>> l
       Interval_Set ((0, 200))
       >>> m = Interval_Set (N (1, 2), N (5, 6), N (7, 9))
       >>> m.overlaps (m)
       True
       >>> n = Interval_Set (N (1, 5), N (6, 6), N (9, 11))
       >>> n.intersection (m)
       Interval_Set ((1, 2), (5, 5), (6, 6), (9, 9))
       >>> o = Interval_Set (N (1, 1))
       >>> o.is_empty ()
       False
       >>> p = Interval_Set ()
       >>> p.is_empty ()
       True
       >>> if     p : print "Ooops"
       >>> if not p : print not p
       True
       >>> l.overlaps (i)
       True
       >>> l.intersection (i)
       Interval_Set ((0, 100))
       >>> l.intersection (j)
       Interval_Set ((100, 200))
       >>> l.overlaps (i)
       True
       >>> i.overlaps (j)
       True
       >>> l.overlaps (l)
       True
       >>> l.contains_point (0)
       True
       >>> l.contains_point (100)
       True
       >>> l.contains_point (200)
       True
       >>> l.contains_point (50)
       True
       >>> l.contains_point (4711)
       False
       >>> l.next_point (4711)
       >>> m.next_point (1)
       1
       >>> m.next_point (3)
       5
       >>> m.next_point (9)
       9
       >>> m.next_point (10)
       >>> m.intersection (l)
       Interval_Set ((1, 2), (5, 6), (7, 9))
    """

    def __init__ (self, * args) :
        if args :
            self.intervals = args [0].__class__.union (*args)
        else :
            self.intervals = []
    # end def __init__

    def contains_point (self, point) :
        return point is not None and self.next_point (point) == point
    # end def contains_point

    def _element_class (self) :
        """ Will fail for self.is_empty """
        return self.intervals [0].__class__
    # end def _element_class
    element_class = property (_element_class)

    def intersection (self, other) :
        interval = []
        iterator = [(i for i in k.intervals) for k in (self, other)]
        try :
            item = [i.next () for i in iterator]
            while (True) :
                it         = item [0].intersection (item [1])
                if it.is_valid () : interval.append (it)
                idx        = item [1] < item [0]
                item [idx] = iterator [idx].next ()
        except StopIteration :
            for it in iterator :
                interval.extend (i for i in it if i.is_valid ())
        return self.__class__ (* interval)
    # end def intersection

    def is_empty (self) :
        return not self
    # end def is_empty

    def next_point (self, point) :
        i = bisect (self.intervals, self.element_class (point, point))
        try :
            # bisect might return i == len (self.intervals)
            if self.intervals [i - 1].contains_point (point) :
                return point
            if self.intervals     [i].contains_point (point) :
                return point
            return self.intervals [i].lower
        except IndexError :
            pass
        return None
    # end def next_point

    def overlaps (self, other) :
        return bool (self.intersection (other))
    # end def overlaps

    def union (self, * other) :
        intervals = sum ((i.intervals for i in other), self.intervals)
        return self.__class__ (* intervals)
    # end def union

    def __nonzero__ (self) :
        return bool (self.intervals)
    # end __nonzero__

    def __repr__ (self) :
        return \
            ( "Interval_Set (%s)"
            % ', '.join (repr (i) for i in self.intervals)
            )
    # end def __repr__

# end class Interval_Set

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Interval_Set


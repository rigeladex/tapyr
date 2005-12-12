# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
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
#    TFL.Interval_Set
#
# Purpose
#    Model a sorted set of intervals
#
# Revision Dates
#     9-Dec-2005 (RSC) Creation
#    12-Dec-2005 (RSC) Changed License to LGPL
#                      Added several new doctests for boundary cases
#                      Reordered doctests for easier viewing
#                      _element_class replaced with a lambda
#                      Introduced _intersection_iter and recode
#                      intersection and contains with it
#                      Factored _bisection and use it in next_point
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
       >>> m = Interval_Set (N (1, 2), N (5, 6), N (7, 9))
       >>> m.overlaps (m)
       True
       >>> n = Interval_Set (N (1, 5), N (6, 6), N (9, 11))
       >>> n.intersection (m)
       Interval_Set ((1, 2), (5, 5), (6, 6), (9, 9))
       >>> m.next_point (0)
       1
       >>> m.next_point (1)
       1
       >>> m.next_point (3)
       5
       >>> m.next_point (9)
       9
       >>> m.next_point (10)
       >>> m.intersection (l)
       Interval_Set ((1, 2), (5, 6), (7, 9))
       >>> o = Interval_Set (N (1, 1))
       >>> o.is_empty ()
       False
       >>> p = Interval_Set ()
       >>> p.is_empty ()
       True
       >>> p, bool (p)
       (Interval_Set (), False)
       >>> q = Interval_Set (N (1, 1))
       >>> r = Interval_Set (N (1, 1), N (3, 4))
       >>> q.intersection (r)
       Interval_Set ((1, 1))
    """

    def __init__ (self, * args) :
        if args :
            self.intervals = args [0].__class__.union (* args)
        else :
            self.intervals = []
    # end def __init__

    def contains_point (self, point) :
        return self.next_point (point) == point
    # end def contains_point

    element_class = property (lambda self : self.intervals [0].__class__)

    def intersection (self, other) :
        return self.__class__ (* self._intersection_iter (other))
    # end def intersection

    def is_empty (self) :
        return not self
    # end def is_empty

    def next_point (self, point) :
        ivals = self.intervals
        if ivals :
            i = bisect (ivals, self.element_class (point, point))
            if ivals [i - 1].contains_point (point) :
                return point
            elif i < len (ivals) :
                return ivals [i].lower
        return None
    # end def next_point

    # Using _bisection: FIXME: Really?
    def next_point (self, point) :
        idx, contained = self._bisection (point)
        if contained :
            return point
        if idx < len (self.intervals) :
            return self.intervals [idx].lower
        return None
    # end def next_point

    def overlaps (self, other) :
        try :
            self._intersection_iter (other).next ()
            return True
        except StopIteration :
            pass
        return False
    # end def overlaps

    def union (self, * other) :
        # dont use sum, for o in other extend
        # union soll self nicht aendern
        intervals = sum ((i.intervals for i in other), self.intervals)
        return self.__class__ (* intervals)
    # end def union

    # FIXME: Do we really need this one? Can it be done better?
    def _bisection (self, point) :
        ivals = self.intervals
        if not ivals :
            return 0, False
        i     = bisect (ivals, self.element_class (point, point))
        if ivals [i - 1].contains_point (point) :
            return i - 1, True
        return i, i < len (ivals) and ivals [i].lower == point
    # end def _bisection

    def _intersection_iter (self, other) :
        l_iter = iter (self.intervals)
        r_iter = iter (other.intervals)
        l      = l_iter.next ()
        r      = r_iter.next ()
        while (True) :
            it = r.intersection (l)
            if it.is_valid () :
                yield it
            if l.upper < r.upper :
                l = l_iter.next ()
            else :
                r = r_iter.next ()
    # end def _intersection_iter

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


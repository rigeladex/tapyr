# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2007 Dr. Ralf Schlatterbeck Open Source Consulting.
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
#    13-Dec-2005 (CT)  Small improvements (`_intersection_iter`, ...)
#    22-Jul-2006 (CED) `contains_interval` added
#    24-Nov-2006 (CED) `difference` added
#    19-Feb-2007 (CT)  `intersection_iter` added
#    19-Feb-2007 (CT)  `difference` done right
#    20-Feb-2007 (CT)  `contains_interval` changed to use `any_true`
#    21-Feb-2007 (CT)  `_difference_iter` factored
#    ««revision-date»»···
#--

from   _TFL                  import TFL

import _TFL._Meta.Object

from   _TFL.predicate        import any_true
from   bisect                import bisect

class Interval_Set (TFL.Meta.Object) :
    """Class for modelling a sorted set of intervals.

       >>> from   _TFL   import TFL
       >>> import _TFL.Numeric_Interval
       >>> N = TFL.Numeric_Interval
       >>> class IS (Interval_Set) : pass
       ...
       >>> i = IS (N (  0, 100))
       >>> j = IS (N (100, 200))
       >>> k = IS (N ( 20,  50))
       >>> l = i.union (j)
       >>> l
       IS ((0, 200))
       >>> [l.intersection (x) for x in (i, j, l)]
       [IS ((0, 100)), IS ((100, 200)), IS ((0, 200))]
       >>> [l.overlaps (x) for x in (i, j, l)]
       [True, True, True]
       >>> [l.contains_point (x) for x in (0, 50, 100, 200, 4711)]
       [True, True, True, True, False]
       >>> m = IS (N (1, 2), N (5, 6), N (7, 9))
       >>> m
       IS ((1, 2), (5, 6), (7, 9))
       >>> n = IS (N (1, 5), N (6, 6), N (9, 11), N (20, 30))
       >>> n.intersection (m)
       IS ((1, 2), (5, 5), (6, 6), (9, 9))
       >>> [m.next_point_up (x) for x in (0, 1, 3, 9, 10)]
       [1, 1, 5, 9, None]
       >>> m.intersection (l)
       IS ((1, 2), (5, 6), (7, 9))
       >>> o = IS (N (1, 1))
       >>> o, bool (o), o.is_empty ()
       (IS ((1, 1)), True, False)
       >>> p = IS ()
       >>> p, bool (p), p.is_empty ()
       (IS (), False, True)
       >>> o = IS (N (0, 5), N (10, 15), N (20, 25))
       >>> p = IS (N (3, 6), N (12, 13), N (20, 25))
       >>> o.difference (p)
       IS ((0, 3), (10, 12), (13, 15))

       >>> a = IS (N (0, 5), N (10, 20), N (40, 60), N (65, 70))
       >>> b = IS (N (7, 8), N (10, 12), N (18, 20), N (33, 37), N (45, 48))
       >>> c = a.difference (b)
       >>> c
       IS ((0, 5), (12, 18), (40, 45), (48, 60), (65, 70))
       >>> d = IS (N (10, 20), N (60,75))
       >>> c.difference (d)
       IS ((0, 5), (40, 45), (48, 60))
       >>> d.difference (IS ())
       IS ((10, 20), (60, 75))
       >>> d.difference (IS (N (30, 40)))
       IS ((10, 20), (60, 75))
       >>> d.difference (IS (N (80, 90)))
       IS ((10, 20), (60, 75))
       >>> d.difference (IS (N (0, 10)))
       IS ((10, 20), (60, 75))
       >>> d.difference (IS (N (0, 11)))
       IS ((11, 20), (60, 75))
       >>> c.union (d)
       IS ((0, 5), (10, 20), (40, 45), (48, 75))

       >>> list (IS.intersection_iter ((N (3, 6), N (12, 13)), min_size = 1))
       [(3, 6), (12, 13)]
       >>> list (IS.intersection_iter ((N (3, 6), N (12, 13)), min_size = 2))
       [(3, 6)]
       >>> list (IS.intersection_iter (o, p))
       [(3, 5), (12, 13), (20, 25)]
       >>> list (IS.intersection_iter (o, p, min_size = 2))
       [(3, 5), (20, 25)]
       >>> list (IS.intersection_iter (o, p, (N (4, 6), N (12, 12))))
       [(4, 5), (12, 12)]
    """

    element_class = property (lambda self : self.intervals [0].__class__)

    def __init__ (self, * args) :
        if args :
            self.intervals = args [0].__class__.union (* args)
        else :
            self.intervals = []
    # end def __init__

    def contains_interval (self, ival) :
        return bool (any_true (iv.contains (ival) for iv in self.intervals))
    # end def contains_interval

    def contains_point (self, point) :
        return self.next_point_up (point) == point
    # end def contains_point

    def difference (self, other) :
        return self.__class__ (* self._difference_iter (other))
    # end def difference

    def intersection (self, other) :
        return self.__class__ (* self._intersection_iter (other))
    # end def intersection

    @classmethod
    def intersection_iter (cls, * iv_sets, ** kw) :
        """Generates all intersections larger than `min_size` between the
           intervals of `iv_sets` (the default for `min_size` is 0).
        """
        min_size = kw.get ("min_size", 0)
        iv_iters = [iter     (ivs) for ivs in iv_sets]
        ivals    = [ivi.next ()    for ivi in iv_iters]
        while True :
            r = ivals [0]
            if r.length >= min_size :
                for i in ivals [1:] :
                    r = r.intersection (i)
                    if r.length < min_size :
                        break
                else :
                    yield r
            _, k = min ((iv.upper, k) for (k, iv) in enumerate (ivals))
            ivals [k] = iv_iters [k].next ()
    # end def intersection_iter

    def is_empty (self) :
        return not self
    # end def is_empty

    def next_point_up (self, point) :
        ivals = self.intervals
        if ivals :
            i = bisect (ivals, self.element_class (point, point))
            if ivals [i - 1].contains_point (point) :
                return point
            elif i < len (ivals) :
                return ivals [i].lower
    # end def next_point_up

    def overlaps (self, other) :
        try :
            self._intersection_iter (other).next ()
        except StopIteration :
            return False
        else :
            return True
    # end def overlaps

    def union (self, * other) :
        ivals = list (self)
        for o in other :
            ivals.extend (o)
        return self.__class__ (* ivals)
    # end def union

    def _difference_iter (self, other) :
        lit = iter     (self)
        l   = lit.next ()
        for r in other :
            while l.upper <= r.lower :
                yield l
                l = lit.next ()
            if l.lower < r.upper :
                if l.lower < r.lower :
                    yield l.__class__ (l.lower, r.lower)
                if r.upper < l.upper :
                    l   = l.__class__ (r.upper, l.upper)
                else :
                    l   = lit.next ()
        yield l
        for l in lit :
            yield l
    # end def _difference_iter

    def _intersection_iter (self, other) :
        l_iter = iter (self)
        r_iter = iter (other)
        l, r   = l_iter.next (), r_iter.next ()
        while True :
            i = r.intersection (l)
            if i.is_valid () :
                yield i
            if l.upper < r.upper :
                l = l_iter.next ()
            else :
                r = r_iter.next ()
    # end def _intersection_iter

    def __iter__ (self) :
        return iter (self.intervals)
    # end def __iter__

    def __nonzero__ (self) :
        return bool (self.intervals)
    # end __nonzero__

    def __repr__ (self) :
        name = self.__class__.__name__
        return "%s (%s)" % (name, ", ".join (repr (i) for i in self))
    # end def __repr__

# end class Interval_Set

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Interval_Set

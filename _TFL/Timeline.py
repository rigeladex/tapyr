# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003-2007 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Timeline
#
# Purpose
#    Timeline for scheduling
#
# Revision Dates
#    21-Aug-2003 (CT)  Creation
#    29-Aug-2003 (CT)  `Timeline.length` added
#    29-Aug-2003 (CT)  `orig` added
#    23-Sep-2003 (CT)  `snip` added
#    26-Sep-2003 (CED) `reset` added
#     2-Oct-2003 (CED) `epsilon` introduced and used to avoid rounding errors
#    23-Oct-2003 (CT)  Small changes to allow cutting of zero-length spans
#     5-Apr-2004 (CED) `__str__` added
#    29-Jun-2005 (CT)  Test scaffolding dumped
#    30-Jun-2005 (CT)  Style improvements
#    22-Jul-2006 (CED) `is_free` added
#    16-Feb-2007 (CT)  Factored to `TFL`
#    16-Feb-2007 (CT)  `is_free` removed
#    16-Feb-2007 (CT)  `bisect`-use and `break` added to `intersection`
#    16-Feb-2007 (CT)  `Timeline_Cut` simplified, `prepare_cut` added
#    16-Feb-2007 (CT)  `snip` simplified
#    16-Feb-2007 (CT)  `_sid` introduced
#    16-Feb-2007 (CT)  `intersection_p` added (and `cut` changed to deal with
#                      the resulting pieces)
#    17-Feb-2007 (CT)  `min_size` added to `intersection` (and
#                      `intersection_p`)
#    18-Feb-2007 (CT)  `Timeline_Cut` made compatible with
#                      `TFL.Numeric_Interval`
#    18-Feb-2007 (CT)  `Timeline_Cut.intersection` redefined (and
#                      `_update_result` added)
#    20-Feb-2007 (CT)  `Timeline_Cut_P` added
#    21-Feb-2007 (CT)  `Timeline_Cut.modulo` and
#                      `Timeline_Cut.prepare_cut_around` added
#    21-Feb-2007 (CT)  `Timeline.cut_p` added
#    22-Feb-2007 (CT)  `Timeline_Cut_P.minmax` added
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL.Interval_Set
import _TFL.Numeric_Interval
import _TFL._Meta.Object

from   _TFL.Generators       import enumerate_slice
from   bisect                import bisect

class Timeline_Cut (TFL.Numeric_Interval) :
    """Cut from Timeline"""

    Span       = TFL.Numeric_Interval
    parents    = []
    period     = None

    def __init__ (self, lower, upper, index = None, _sid = None) :
        self.__super.__init__ (lower, upper)
        self.index = index
        self._sid  = _sid
    # end def __init__

    def copy (self) :
        result = self.__super.copy ()
        self._update_result (None, result)
        return result
    # end def copy

    def intersection (self, other) :
        result = self.__super.intersection (other)
        self._update_result (other, result)
        return result
    # end def intersection

    def modulo (self, p) :
        result = self.__class__ (self.lower % p, self.upper % p)
        self._update_result (None, result)
        result.period = p
        return result
    # end def modulo

    def prepare_cut (self, span) :
        self.to_cut = self.__super.intersection (span)
        return self.to_cut
    # end def prepare_cut

    def prepare_cut_around (self, span, size) :
        jitter = size - span.length
        if jitter <= 0 :
            lower = span.lower
        else :
            lower = max (self.lower, span.lower - jitter)
        self.to_cut = self.Span (lower, lower + size)
        assert self.contains (self.to_cut)
        return self.to_cut
    # end def prepare_cut_around

    def prepare_cut_l (self, size) :
        lower       = self.lower
        self.to_cut = self.Span (lower, lower + size)
        return self.to_cut
    # end def prepare_cut_l

    def prepare_cut_u (self, size) :
        upper       = self.upper
        self.to_cut = self.Span (upper - size, upper)
        return self.to_cut
    # end def prepare_cut_u

    def _update_result (self, other, result) :
        result.index   = self.index
        result._sid    = self._sid
        result.parents = list (self.parents or [self])
        result.period  = self.period
        if other is not None :
            assert self._sid == other._sid
            result.parents.extend (other.parents or [other])
    # end def _update_result

# end class Timeline_Cut

class Timeline_Cut_P (TFL.Meta.Object) :
    """Periodic cut from Timeline"""

    def __init__ (self, period, min_size, _sid, generations) :
        self.period      = period
        self.min_size    = min_size
        self._sid        = _sid
        self.generations = generations
    # end def __init__

    @property
    def minmax (self) :
        return min \
            (max ([c.length for c in g] or [0]) for g in self.generations)
    # end def minmax

    def prepare_cut_mod_p (self, imp, size) :
        period = self.period
        shift  = 0
        for p in imp.parents :
            p.prepare_cut_around (imp.shifted (shift), size)
            shift += period
        self.to_cut = imp.parents
        return self.to_cut
    # end def prepare_cut_mod_p

    def intersections_mod_p (self, min_size = None) :
        if min_size is None :
            min_size = self.min_size
        p          = self.period
        normalized = [[c.modulo (p) for c in g] for g in self.generations]
        return list \
            ( TFL.Interval_Set.intersection_iter
                (* normalized, ** dict (min_size = min_size))
            )
    # end def intersections_mod_p

    def __iter__ (self) :
        return iter (self.generations)
    # end def __iter__

# end class Timeline_Cut_P

class Timeline (TFL.Meta.Object) :
    """Timeline for scheduling.

       >>> S  = Timeline.Span
       >>> tl = Timeline (0, 1000)
       >>> tl.free
       [(0, 1000)]
       >>> c = tl.intersection (S (100, 100)) [0] [0]
       >>> c.prepare_cut_l (0)
       (100, 100)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 1000)]
       >>> c = tl.intersection (S (100, 300)) [0] [0]
       >>> c.prepare_cut_l (50)
       (100, 150)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 100), (150, 1000)]
       >>> tl.intersection (S (80, 120))
       ([(80, 100)], 20)
       >>> c = tl.intersection (S (70, 100)) [0] [0]
       >>> c.prepare_cut_u (15)
       (85, 100)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 85), (150, 1000)]
       >>> c = tl.intersection (S (150, 200)) [0] [0]
       >>> c.prepare_cut_l (50)
       (150, 200)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 85), (200, 1000)]
       >>> c = tl.intersection (S (500, 600)) [0] [0]
       >>> c.prepare_cut_l (50)
       (500, 550)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 85), (200, 500), (550, 1000)]
       >>> c1, c2 = tl.intersection (S (50, 300)) [0]
       >>> c1, c2
       ((50, 85), (200, 300))
       >>> c1.prepare_cut_u (15)
       (70, 85)
       >>> c2.prepare_cut_l (15)
       (200, 215)
       >>> tl.cut (c1, c2)
       >>> tl.free
       [(0, 70), (215, 500), (550, 1000)]
       >>> tl.cut (c1, c2)
       Traceback (most recent call last):
       ...
       AssertionError: Wrong use of Timeline (intersection vs. cut)
           [(0, 70), (215, 500), (550, 1000)] <--> (200, 215)

       >>> tl = Timeline (0, 1000)
       >>> tl.snip (S (10, 20), S (25, 25), S (42, 400), S (900, 990))
       >>> tl.free
       [(0, 10), (20, 42), (400, 900), (990, 1000)]
       >>> tl.snip (S (995,1000), S (5, 7), S (400, 410), S (23, 37))
       >>> tl.free
       [(0, 5), (7, 10), (20, 23), (37, 42), (410, 900), (990, 995)]
       >>> tl.intersection (S (0, 50), min_size = 6)
       ([], 0)
       >>> tl.intersection (S (0, 50), min_size = 4)
       ([(0, 5), (37, 42)], 10)
       >>> tl.intersection (S (0, 50), min_size = 3)
       ([(0, 5), (7, 10), (20, 23), (37, 42)], 16)

       >>> tl = Timeline (0, 1000)
       >>> pieces = []
       >>> for (f, ) in tl.intersection_p (S (50, 100), 400) :
       ...     x = f.prepare_cut_l (50)
       ...     pieces.append (f)
       ...
       >>> [(p.to_cut, p.index) for p in pieces]
       [((50, 100), 0), ((450, 500), 0), ((850, 900), 0)]
       >>> tl.cut (* pieces)
       >>> tl.free
       [(0, 50), (100, 450), (500, 850), (900, 1000)]

       >>> tl = Timeline (0, 1000)
       >>> tl.intersection_p (S (50, 100), 40)
       Traceback (most recent call last):
       ...
           assert span.length < period, (span, period)
       AssertionError: ((50, 100), 40)

       >>> tl = Timeline (0, 1000)
       >>> tl.snip (S (100, 120), S (300, 330), S (360, 370), S (550, 590))
       >>> tl.free
       [(0, 100), (120, 300), (330, 360), (370, 550), (590, 1000)]
       >>> tcp = tl.intersection_p (S (50, 150), 250)
       >>> tcp.minmax
       30
       >>> tcp.generations
       [[(50, 100), (120, 150)], [(330, 360), (370, 400)], [(590, 650)], [(800, 900)]]
       >>> imp = tcp.intersections_mod_p ()
       >>> imp
       [(90, 100), (120, 150)]
       >>> tcp.prepare_cut_mod_p (imp [0], 30)
       [(50, 100), (330, 360), (590, 650), (800, 900)]
       >>> tl.cut_p (tcp)
       >>> tl.free
       [(0, 70), (120, 300), (370, 550), (620, 820), (850, 1000)]

       >>> tl = Timeline (0, 1000)
       >>> tl.snip (S (100, 120), S (300, 330), S (360, 370), S (550, 590))
       >>> tcp = tl.intersection_p (S (50, 150), 250)
       >>> imp = tcp.intersections_mod_p ()
       >>> tcp.prepare_cut_mod_p (imp [1], 30)
       [(120, 150), (370, 400), (590, 650), (800, 900)]
       >>> tl.cut_p (tcp)
       >>> tl.free
       [(0, 100), (150, 300), (330, 360), (400, 550), (590, 620), (650, 870), (900, 1000)]

       >>> tl = Timeline (0, 1000)
       >>> tl.snip (S (100, 120), S (300, 330), S (360, 370), S (550, 590))
       >>> tl.snip (S (70, 100), S (120, 130))
       >>> tl.free
       [(0, 70), (130, 300), (330, 360), (370, 550), (590, 1000)]
       >>> tcp = tl.intersection_p (S (50, 150), 250)
       >>> tcp.minmax
       20
       >>> tcp.generations
       [[(50, 70), (130, 150)], [(330, 360), (370, 400)], [(590, 650)], [(800, 900)]]

    """

    epsilon    = 0.001
    length     = property (lambda s : sum ((f.length for f in s.free), 0))
    Span       = TFL.Numeric_Interval
    _sid       = 0

    def __init__ (self, lower, upper) :
        self.orig = self.Span (lower, upper)
        self.reset ()
    # end def __init__

    def cut (self, * pieces) :
        """Cut `pieces` from `self.free`. Each element of `pieces` must be a
           `Timeline_Cut` as returned from `intersection` to which
           `prepare_cut_l` or `prepare_cut_u` was applied. Beware: don't
           interleave calls to `intersection` with multiple calls to `cut`.
        """
        try :
            pieces = sorted \
                (pieces, key = lambda p : (p.index, p.to_cut), reverse = True)
            for p in pieces :
                assert p._sid == self._sid, "%s\n    %s <--> %s" % \
                    ( "Wrong use of Timeline (intersection vs. cut)"
                    , self.free, p.to_cut
                    )
                if p.to_cut :
                    f = self.free [p.index]
                    if abs (f.lower - p.to_cut.lower) < self.epsilon :
                        f.lower = p.to_cut.upper
                    elif abs (f.upper - p.to_cut.upper) < self.epsilon :
                        f.upper = p.to_cut.lower
                    else :
                        head = self.Span (f.lower, p.to_cut.lower)
                        tail = self.Span (p.to_cut.upper, f.upper)
                        assert head and tail, \
                            "head = %s, tail = %s" % (head, tail)
                        self.free [p.index : p.index + 1] = [head, tail]
                    if not f :
                        del self.free [p.index]
        finally :
            self.__class__._sid += 1
    # end def cut

    def cut_p (self, tcp) :
        self.cut (* tcp.to_cut)
    # end def cut_p

    def intersection (self, span, min_size = 1) :
        if span.length == 0 :
            min_size = 0
        cuts, size   = [], 0
        free         = self.free
        lower, upper = span.lower, span.upper
        h            = bisect (free, self.Span (lower, lower))
        if h and free [h - 1].contains_point (lower) :
            h -= 1
        for i, f in enumerate_slice (free, h) :
            if f.lower > upper :
                break
            cut = f.intersection (span)
            if cut.length >= min_size :
                cuts.append (Timeline_Cut (cut.lower, cut.upper, i, self._sid))
                size += cut.length
        return cuts, size
    # end def intersection

    def intersection_p (self, span, period, min_size = 1) :
        assert span.length < period, (span, period)
        result = []
        upper  = self.free [-1].upper
        while span.lower < upper :
            cuts, size = self.intersection (span, min_size)
            result.append (cuts)
            span = span.shifted (period)
        return Timeline_Cut_P (period, min_size, self._sid, result)
    # end def intersection_p

    def reset (self) :
        self.free = [self.orig.copy ()]
    # end def reset

    def snip (self, * spans) :
        for s in spans :
            l = s.length
            if l > 0 :
                (free, ), size = self.intersection (s)
                if abs (size - l) > self.epsilon :
                    raise ValueError, (self.free, s, spans, free)
                free.prepare_cut_l (size)
                self.cut           (free)
    # end def snip

    def __str__ (self) :
        return "Timeline free: " + str (self.free)
    # end def __str__

# end class Timeline

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Timeline

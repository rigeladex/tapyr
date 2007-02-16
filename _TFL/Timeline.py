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
#     2-Oct-2003 (CED) `epsilon` introduced and used to avoid transient
#                      rounding errors
#    23-Oct-2003 (CT)  Small changes to allow cutting of zero-length spans
#     3-Nov-2003 (CT)  Inherit from `NDT.Sched2.Object`
#     5-Apr-2004 (CED) `__str__` added
#    29-Jun-2005 (CT)  Test scaffolding dumped
#    30-Jun-2005 (CT)  Style improvements
#    22-Jul-2006 (CED) `is_free` added
#    16-Feb-2007 (CT)  Factored to `TFL`
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL.Numeric_Interval
import _TFL._Meta.Object

class Timeline_Cut (TFL.Numeric_Interval) :
    """Cut from Timeline"""

    def __init__ (self, timeline, index, cut) :
        self.__super.__init__ (cut.lower, cut.upper)
        self.timeline = timeline
        self.index    = index
        self.cut      = cut
    # end def __init__

    def prepare_cut_l (self, size) :
        lower       = self.cut.lower
        self.to_cut = self.timeline.Span (lower, lower + size)
        return self.to_cut
    # end def prepare_cut_l

    def prepare_cut_u (self, size) :
        upper       = self.cut.upper
        self.to_cut = self.timeline.Span (upper - size, upper)
        return self.to_cut
    # end def prepare_cut_u

# end class Timeline_Cut

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
       >>> try :
       ...   tl.cut (c1, c2)
       ... except AssertionError, exc :
       ...   print exc.__class__.__name__, exc
       ...
       AssertionError head = (215, 200), tail = (215, 500)

       XXX add doctest for `snip`
    """

    Span       = TFL.Numeric_Interval
    epsilon    = 0.001
    length     = property (lambda s : sum ((f.length for f in s.free), 0))

    def __init__ (self, lower, upper) :
        self.orig = self.Span (lower, upper)
        self.reset ()
    # end def __init__

    def intersection (self, span) :
        free = []
        size = 0
        for i, f in enumerate (self.free) :
            cut = f.intersection (span)
            if cut or (cut.length == span.length == 0) :
                free.append (Timeline_Cut (self, i, cut))
                size += cut.length
        return free, size
    # end def intersection

    def is_free (self, span) :
        free, size = self.intersection (span)
        return (len (free) == 1) and (abs (size - span.length) < self.epsilon)
    # end def is_free

    def cut (self, * pieces) :
        """Cut `pieces` from `self.free`. Each element of `pieces` must be a
           `Timeline_Cut` as returned from `intersection` to which
           `prepare_cut_l` or `prepare_cut_u` was applied. Beware: don't
           interleave calls to `intersection` with multiple calls to `cut`.
        """
        for p in sorted (pieces, key = lambda p : p.index, reverse = True) :
            if p.to_cut :
                f = self.free [p.index]
                if abs (f.lower - p.to_cut.lower) < self.epsilon :
                    f.lower = p.to_cut.upper
                elif abs (f.upper - p.to_cut.upper) < self.epsilon :
                    f.upper = p.to_cut.lower
                else :
                    head = self.Span (f.lower, p.to_cut.lower)
                    tail = self.Span (p.to_cut.upper, f.upper)
                    assert head and tail, "head = %s, tail = %s" % (head, tail)
                    self.free [p.index : p.index + 1] = [head, tail]
                if not f :
                    del self.free [p.index]
    # end def cut

    def reset (self) :
        self.free = [self.orig.copy ()]
    # end def reset

    def snip (self, * spans) :
        ### XXX optimize to avoid repeated iteration over whole free list
        for s in spans :
            if s.length > 0 :
                free, size = self.intersection (s)
                if not self.is_free (s) :
                    raise ValueError, (self.free, s, spans, free)
                f = free [0]
                f.prepare_cut_l (size)
                self.cut        (f)
    # end def snip

    def __str__ (self) :
        return "Timeline free: " + str (self.free)
    # end def __str__

# end class Timeline

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Timeline

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    Timeline
#
# Purpose
#    Timeline for scheduling
#
# Revision Dates
#    21-Aug-2003 (CT) Creation
#    ««revision-date»»···
#--

from   _NDT                 import NDT
from   _TFL                 import TFL

import _NDT._Sched2.Window
import _TFL._Meta.Object

from   predicate            import *

class Timeline_Cut (NDT.Sched2.Span) :
    """Cut from Timeline"""

    def __init__ (self, timeline, index, cut) :
        self.__super.__init__ (cut.lower, cut.upper)
        self.timeline = timeline
        self.index    = index
        self.cut      = cut
    # end def __init__

    def prepare_cut_l (self, size) :
        lower       = self.cut.lower
        self.to_cut = NDT.Sched2.Span (lower, lower + size)
        return self.to_cut
    # end def prepare_cut_l

    def prepare_cut_u (self, size) :
        upper       = self.cut.upper
        self.to_cut = NDT.Sched2.Span (upper - size, upper)
        return self.to_cut
    # end def prepare_cut_u

# end class Timeline_Cut

class Timeline (TFL.Meta.Object) :
    """Timeline for scheduling.

       >>> tl = Timeline (1000)
       >>> tl.free
       [(0, 1000)]
       >>> S = NDT.Sched2.Span
       >>> c = tl.intersection (S (100, 300)) [0]
       >>> c.prepare_cut_l (50)
       (100, 150)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 100), (150, 1000)]
       >>> c = tl.intersection (S (70, 100)) [0]
       >>> c.prepare_cut_u (15)
       (85, 100)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 85), (150, 1000)]
       >>> c = tl.intersection (S (150, 200)) [0]
       >>> c.prepare_cut_l (50)
       (150, 200)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 85), (200, 1000)]
       >>> c = tl.intersection (S (500, 600)) [0]
       >>> c.prepare_cut_l (50)
       (500, 550)
       >>> tl.cut (c)
       >>> tl.free
       [(0, 85), (200, 500), (550, 1000)]
       >>> c1, c2 = tl.intersection (S (50, 300))
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
    """

    def __init__ (self, upper, lower = 0) :
        self.free = [NDT.Sched2.Span (lower, upper)]
    # end def __init__

    def intersection (self, span) :
        result = []
        for i, f in enumerate (self.free) :
            cut = f.intersection (span)
            if cut :
                result.append (Timeline_Cut (self, i, cut))
        return result
    # end def intersection

    def cut (self, * pieces) :
        """Cut `pieces` from `self.free`. Each element of `pieces` must be a
           `Timeline_Cut` as returned from `intersection` to which
           `prepare_cut_l` or `prepare_cut_u` was applied. Beware: don't
           interleave calls to `intersection` with multiple calls to `cut`.
        """
        for p in dusort (pieces, lambda p : - p.index) :
            f = self.free [p.index]
            if f.lower == p.to_cut.lower :
                f.lower = p.to_cut.upper
            elif f.upper == p.to_cut.upper :
                f.upper = p.to_cut.lower
            else :
                head = NDT.Sched2.Span (f.lower, p.to_cut.lower)
                tail = NDT.Sched2.Span (p.to_cut.upper, f.upper)
                assert head and tail, "head = %s, tail = %s" % (head, tail)
                self.free [p.index : p.index + 1] = [head, tail]
            if not f :
                del self.free [index]
    # end def cut

# end class Timeline

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        import Timeline
        return U_Test.run_module_doc_tests (Timeline)
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test

    if __name__ == "__main__" :
        _test ()
# end if __debug__

### end unit-test code ########################################################

if __name__ != "__main__" :
    NDT.Sched2._Export ("*")
### __END__ Timeline

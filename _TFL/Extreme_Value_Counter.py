# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    Extreme_Value_Counter
#
# Purpose
#    Classes for remembering the extreme values over a sequence of increments
#    and decrements
#
# Revision Dates
#    19-Feb-2004 (CED) Creation
#    26-Feb-2004 (CED) `set` added
#    ««revision-date»»···
#--
#

from _TFL import TFL

import _TFL._Meta.Object
import sys

class Extreme_Counter (object) :
    """
       >>> ec = Extreme_Counter ()
       >>> ec.inc ()
       >>> ec.dec ()
       >>> ec.dec ()
       >>> ec.current_val
       -1
       >>> ec.max_val
       1
       >>> ec.min_val
       -1
       >>> ec += 10
       >>> ec.set (5)
       >>> ec.current_val
       5
       >>> ec.max_val
       9
       >>> ec.min_val
       -1
    """

    def __init__ (self, init_val = 0) :
        self.init_val    = init_val
        self.reset ()
    # end def __init__

    def __iadd__ (self, rhs) :
        self.current_val += rhs
        if self.current_val > self.max_val :
            self.max_val = self.current_val
        return self
    # end def __iadd__

    def __isub__ (self, rhs) :
        self.current_val -= rhs
        if self.current_val < self.min_val :
            self.min_val = self.current_val
        return self
    # end def __isub__

    def inc (self) :
        self += 1
    # end def inc

    def dec (self) :
        self -= 1
    # end def dec

    def reset (self) :
        self.current_val = self.init_val
        self.max_val     = self.init_val
        self.min_val     = self.init_val
    # end def reset

    def set (self, value) :
        self.current_val = value
        if self.current_val < self.min_val :
            self.min_val = self.current_val
        if self.current_val > self.max_val :
            self.max_val = self.current_val
    # end def set

# end class Extreme_Counter

class Maximum_Counter (Extreme_Counter) :

    def __init__ (self, init_val = -sys.maxint) :
        self__super.__init__ (init_val)
    # end def __init__

# end class Maximum_Counter

class Minimum_Counter (Extreme_Counter) :

    def __init__ (self, init_val = sys.maxint) :
        self__super.__init__ (init_val)
    # end def __init__

# end class Minimum_Counter

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        import Extreme_Value_Counter
        return U_Test.run_module_doc_tests (Extreme_Value_Counter)
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test

    if __name__ == "__main__" :
        _test ()
# end if __debug__

### end unit-test code ########################################################

if __name__ != "__main__" :
    TFL._Export ("*")

### __END__ Extreme_Value_Counter



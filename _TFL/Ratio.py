#! /usr/bin/python
# Copyright (C) 2001 Mag. Christian Tanzer. All rights reserved
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
#    Ratio
#
# Purpose
#    Model ratio of two integer numbers
#
# Revision Dates
#     4-Sep-2001 (CT) Creation
#     5-Sep-2001 (CT) Error messages for `TypeError` improved
#    ««revision-date»»···
#--

from Regexp import *

class Ratio :
    """Model ratio of two integer numbers.

       
       >>> print Ratio (1,2)
       1 / 2
       >>> print Ratio (2)
       2 / 1
       >>> print Ratio ("3/4")
       3 / 4
       >>> print Ratio ("3")
       3 / 1
       >>> print Ratio (1,2) * Ratio (1,4)
       1 / 8
       >>> print Ratio (1,2) / Ratio (1,4)
       4 / 2
       >>> print Ratio (1,2) * Ratio ("3")
       3 / 2
       >>> print Ratio (1,2) * 3
       1
       >>> print Ratio (1,2) * 3.
       1.5
       >>> print 6 * Ratio (1,2)
       3
       >>> print 6 / Ratio (1,2)
       12
       >>> print Ratio (1,2) / 6 
       0
       >>> print Ratio (1,2) / 6.
       0.0833333333333
    """

    pattern = Regexp \
        ( r"^\s*"
          r"(?P<n> \d+)"
          r"(?: "
          r"\s* / \s*"
          r"(?P<d> \d+)"
          r")?"
          r"\s*$"
        , re.X
        )
    
    def __init__ (self, n, d = None) :
        if isinstance (n, type ("")) :
            if not d is None :
                raise TypeError, \
                      "Ratio() 2nd argument not allowed when 1st is a string"
            if self.pattern.match (n) :
                self.n = int (self.pattern.group ("n"))
                self.d = int (self.pattern.group ("d") or 1)
            else :
                raise ValueError, "invalid literal for Range(): %s" % (n, )
        elif isinstance (n, Ratio) :
            if not d is None :
                raise TypeError, \
                      "Ratio() 2nd argument not allowed when 1st is a Ratio"
            self.n = n.n
            self.d = n.d
        else :
            try :
                self.n = int (n)
                self.d = int (d or 1)
            except TypeError :
                print "invalid arguments for Ratio: (%r, %r)" % (n, d)
                raise
    # end def __init__

    def __int__ (self) :
        return int (self.n / self.d)
    # end def __int__

    def __float__ (self) :
        return float (self.n / (1.0 * self.d))
    # end def __float__
    
    def __str__ (self) :
        return "%s / %s" % (self.n, self.d)
    # end def __str__

    def __repr__ (self) :
        return "Ratio (%r)" % (str (self), )
    # end def __repr__

    def __mul__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        return self.__class__ (self.n * rhs.n, self.d * rhs.d)
    # end def __mul__

    __rmul__ = __mul__

    def __imul__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        self.n *= rhs.n
        self.d *= rhs.d
    # end def __imul__
    
    def __div__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        return self.__class__ (self.n * rhs.d, self.d * rhs.n)
    # end def __div__

    def __rdiv__ (self, rhs) :
        return (rhs * self.d) / self.n
    # end def __rdiv__

    def __idiv__ (self, rhs) :
        if not isinstance (rhs, Ratio) :
            rhs = self.__class__ (rhs)
        self.n *= rhs.d
        self.d *= rhs.n
    # end def __idiv__
    
    def __cmp__ (self, rhs) :
        if rhs is None :
            return cmp (float (self), rhs)
        else :
            if not isinstance (rhs, Ratio) :
                rhs = self.__class__ (rhs)
            return cmp (float (self), float (rhs))
    # end def __cmp__
    
# end class Ratio

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _test () :
        class Test_Case (U_Test.Case) :
            ### Each test case is implemented by a method 
            ### starting with `check_'

            pass

        # end class Test_Case

        ts = U_Test.make_suite (Test_Case, "check_")
        U_Test.Runner ().run (ts)
    # end def _test

    def _doc_test () :
        import Ratio
        return U_Test.run_module_doc_tests (Ratio)
    # end def _doc_test

    if __name__ == "__main__" :
        _test     ()
        _doc_test ()
# end if __debug__

### end unit-test code ########################################################

from _TFL import TFL
TFL._Export ("*")

### __END__ Ratio

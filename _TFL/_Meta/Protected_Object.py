# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 DI Christian Eder. All rights reserved
# eder@tttech.com
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
#    TFL.Meta.Protected_Object
#
# Purpose
#    Provide baseclass using access-protected attributes
#
# Revision Dates
#    20-Feb-2004 (CED) Creation
#    ««revision-date»»···
#--
#

from   _TFL             import TFL
import _TFL._Meta.M_Autoprotection
import _TFL._Meta.Object
from   U_Test           import *

class Protected_Object (TFL.Meta.Object) :
    """Baseclass using access-protected attributes"""

    __metaclass__ = TFL.Meta.M_Autoprotection
# end class Protected_Object

def private (initvalue = None) :
    return TFL.Meta.Private_Descriptor (initvalue)
# end def private

def protected (initvalue = None) :
    return TFL.Meta.Protected_Descriptor (initvalue)
# end def protected

### unit-test code
def _test () :
    """Unit test."""

    U_Test = Case

    class Protection_Test_Case (U_Test) :

        def _start_case (self) :
            class A (Protected_Object) :
                foo = private   ()
                baz = protected ()

                def __init__ (self) :
                    self.foo = 42
                    self.bar = 43
                    self.baz = 99
                # end def __init__

                def get_foo (self) :
                    return self.foo
                # end def get_foo

            # end class A

            class B (A) :

                def get_baz (self) :
                    return self.baz
                # end def get_baz

                def get_foo2 (self) :
                    return self.foo
                # end def get_foo2

            # end class B

            self.A = A
            self.B = B
        # end def _start_case


        def check_private (self) :
            a = self.A ()
            b = self.B ()

            a.bar = 1
            self.expect_exception \
                (AttributeError, setattr, a, "foo", 2)
            dummy = b.bar
            dummy = b.get_foo ()
            self.expect_exception \
                (AttributeError, getattr, a, "foo")
            self.expect_exception \
                (AttributeError, getattr, b, "foo")
            self.expect_exception \
                (AttributeError, b.get_foo2)
        # end def check_private

        def check_protected (self) :
            a = self.A ()
            b = self.B ()
            dummy = b.get_baz ()
            self.expect_exception \
                (AttributeError, getattr, a, "baz")
            self.expect_exception \
                (AttributeError, getattr, b, "baz")
        # end def check_protected

    # end class Protection_Test_Case

    ts = make_suite (Protection_Test_Case, "check")
    Runner ().run   (ts)
# end def _test

### end unit-test code

if __name__ == "__main__" :
    _test ()
else :
    TFL.Meta._Export ("*")

### __END__ Protected_Object



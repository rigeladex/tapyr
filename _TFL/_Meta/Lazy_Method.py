# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    Lazy_Method
#
# Purpose
#    Provide a wrapper for lazy evaluation of methods
#
# Revision Dates
#    15-Jul-2004 (CT) Creation
#    23-Sep-2004 (CT) `_Lazy_Wrapper_.__getattr__` added to make wrapped
#                     callables more similar to the real thing (e.g., avoid
#                     an AttributeError from `wrapped.func_code`)
#    ««revision-date»»···
#--

from   _TFL             import TFL
import _TFL._Meta.Property

class _Lazy_Wrapper_ (object) :

    ### `counter_name` is the name of the attribute which contains the number
    ### of changes to be considered by the lazy mechanism
    counter_name = "changes"

    def __init__ (self, fct, counter_name = None) :
        self.fct      = fct
        self.__name__ = getattr (fct, "__name__", None)
        self.__doc__  = getattr (fct, "__doc__", None)
        self.changes  = None
        self.result   = None
        if counter_name :
            self.counter_name = counter_name
    # end def __init__

    def __call__ (self, that, * args, ** kw) :
        if self.changes != getattr (that, self.counter_name) :
            self.result  = self.fct (that, * args, ** kw)
            self.changes = getattr (that, self.counter_name)
        return self.result
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self.fct, name)
    # end def __getattr__

# end class _Lazy_Wrapper_

class Lazy_Method (TFL.Meta.Method_Descriptor) :
    """Lazy evaluation wrapper: the wrapped method is executed only if the
       the object changed since the last call.

       Note that this wrapper is only applicable to methods which result does
       *not* depend on the arguments passed to the method.

       >>> class Test (object) :
       ...     changes = 0
       ...     def test (self) :
       ...         print "Test.test", self.changes
       ...     test = Lazy_Method (test)
       ...
       >>> t = Test ()
       >>> t.test ()
       Test.test 0
       >>> t.test ()
       >>> t.changes += 1
       >>> t.test ()
       Test.test 1
       >>> t.test ()
       >>> t.changes += 1
       >>> Test.test (t)
       Test.test 2
       >>> Test.test (t)
    """

    def __init__ (self, method, cls = None, counter_name = None) :
        super (Lazy_Method, self).__init__ \
            (_Lazy_Wrapper_ (method, counter_name), cls)
    # end def __init__

# end class Lazy_Method

### unit-test code ############################################################

if __debug__ :
    import U_Test

    def _doc_test () :
        return U_Test.run_module_doc_tests ("_TFL._Meta.Lazy_Method")
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test

    if __name__ == "__main__" :
        _test ()
# end if __debug__

### end unit-test code ########################################################

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ Lazy_Method

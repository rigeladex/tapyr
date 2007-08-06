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
#    24-Jan-2005 (MG) `_Lazy_Wrapper_.__call__`: conversion to an int added
#     2-Feb-2005 (MG) `_Lazy_Wrapper_.__call__`: store `int` of the change
#                     counter instead of the change object itself
#     2-Feb-2005 (MG) `_Lazy_Wrapper_RNC_` and `Lazy_Method_RNC` added,
#                     `Lazy_Method` renamed to `Lazy_Method_RLV`
#    26-Feb-2007 (CED) Fixed `self.changes` (is a dict now, since
#                      both change counters that are compared must
#                      work per instance ('that'))
#    28-Feb-2007 (CED) `self.result` also has to be per instance of course
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL             import TFL
import _TFL._Meta.Property
import _TFL.defaultdict

class _Lazy_Wrapper_RLV_ (object) :

    ### `counter_name` is the name of the attribute which contains the number
    ### of changes to be considered by the lazy mechanism
    counter_name = "changes"

    def __init__ (self, fct, counter_name = None) :
        self.fct      = fct
        self.__name__ = getattr (fct, "__name__", None)
        self.__doc__  = getattr (fct, "__doc__", None)
        self.changes  = TFL.defaultdict (lambda : -1)
        self.result   = TFL.defaultdict (lambda : None)
        if counter_name :
            self.counter_name = counter_name
    # end def __init__

    def __call__ (self, that, * args, ** kw) :
        if self.changes [that] != int (getattr (that, self.counter_name)) :
            self.result  [that] = self.fct (that, * args, ** kw)
            self.changes [that] = int (getattr (that, self.counter_name))
        return self.result [that]
    # end def __call__

    def __getattr__ (self, name) :
        return getattr (self.fct, name)
    # end def __getattr__

# end class _Lazy_Wrapper_RLV_

class _Lazy_Wrapper_RNC_ (_Lazy_Wrapper_RLV_) :

    def __call__ (self, that, * args, ** kw) :
        if self.changes [that] != int (getattr (that, self.counter_name)) :
            self.result  [that] = self.fct (that, * args, ** kw)
            self.changes [that] = int (getattr (that, self.counter_name))
            return self.result [that]
        return Lazy_Method.NC
    # end def __call__

# end class _Lazy_Wrapper_RNC_

class Lazy_Method_RLV (TFL.Meta.Method_Descriptor) :
    """Lazy evaluation wrapper: the wrapped method is executed only if the
       the object changed since the last call. In any case, the result of the
       last successfull run will be returned

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

    NC = object ()

    wrapper = _Lazy_Wrapper_RLV_

    def __init__ (self, method, cls = None, counter_name = None) :
        super (Lazy_Method, self).__init__ \
            (self.wrapper (method, counter_name), cls)
    # end def __init__

# end class Lazy_Method_RLV

class Lazy_Method_RNC (Lazy_Method_RLV) :
    """Lazy evaluation wrapper: the wrapped method is executed only if the
       the object changed since the last call. In case that the wrapped
       function has not been executed, the unique object
       `TFL.Meta.Lazy_Method_RNC.NC` will be return.
    """

    wrapper = _Lazy_Wrapper_RNC_

# end class Lazy_Method_RNC

Lazy_Method     = Lazy_Method_RLV ### provided for legacy, should not be used
                                  ### in new code !!!

if __name__ != "__main__" :
    TFL.Meta._Export ("*", "Lazy_Method")
### __END__ Lazy_Method

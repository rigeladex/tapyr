# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 DI Christian Eder. All rights reserved
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
#    Idempotent_Method
#
# Purpose
#    Provide a wrapper for idempotentify'ing methods
#
# Revision Dates
#    29-Mar-2005 (CED) Creation
#    ««revision-date»»···
#--
#

from   _TFL             import TFL
import _TFL._Meta.Property

class Idempotent_Method (TFL.Meta.Method_Descriptor) :
    """Method wrapper for idempotentify'ing method.

       >>> class A (object) :
       ...
       ...     _count = 1
       ...
       ...     def non_idempotent_method (self) :
       ...         result = self._count
       ...         self.__class__._count += 1
       ...         return result
       ...     idempotent_method = Idempotent_Method (non_idempotent_method)
       ...
       >>> a = A ()
       >>> b = A ()
       >>> a.idempotent_method     ()
       1
       >>> a.non_idempotent_method ()
       2
       >>> b.non_idempotent_method ()
       3
       >>> b.idempotent_method     ()
       1
    """

    class Bound_Method (TFL.Meta.Method_Descriptor.Bound_Method) :

        _Ancestor = TFL.Meta.Method_Descriptor.Bound_Method

        def __init__ (self, wrapper, * args, ** kw) :
            ### XXX Why does this `super` not work ?
            #super (Bound_Method, self).__init__ (* args, ** kw)
            self._Ancestor.__init__ (self, * args, ** kw)
            self.wrapper = wrapper
        # end def __init__


        def __call__ (self, * args, ** kw) :
            if not self.wrapper._called :
                self.wrapper._result = self.method (self.target, * args, ** kw)
                self.wrapper._called = True
            return self.wrapper._result
        # end def __call__

    # end class Bound_Method

    def __init__ (self, method, cls = None) :
        super (Idempotent_Method, self).__init__ (method, cls)
        self._called = False
        self._result = None
    # end def __init__

    def __get__ (self, obj, cls = None) :
        if obj is None :
            return self.method
        return self.Bound_Method (self, self.method, obj, self.cls or cls)
    # end def __get__

# end class Idempotent_Method

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ Idempotent_Method



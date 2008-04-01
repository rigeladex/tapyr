# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Decorator
#
# Purpose
#    Provide a decorator for defining well-behaved decorators
#
# Revision Dates
#    14-Apr-2006 (CT)  Creation
#    19-Apr-2006 (CT)  Set `__module__`, too
#    26-Sep-2006 (PGO) `wrapper` fixed to work with builtin functions, too
#    24-Jan-2008 (CT)  `Add_Method` and `Add_New_Method` added
#    26-Mar-2008 (CT)  `Add_Method` changed to use `_Added_Method_Descriptor_`
#    28-Mar-2008 (CT)  `_Added_Method_Descriptor_.__get__` corrected (`obj`
#                      needs to be passed as `head_args`)
#     1-Apr-2008 (CT)  `_Added_Method_Descriptor_` changed to be meta-class
#                      compatible, too
#    ««revision-date»»···
#--

from   _TFL         import TFL
import _TFL.Function
import _TFL.Functor

class _Added_Method_Descriptor_ (object) :
    """Descriptor supporting the monkey-patching of methods (supports
       inheritance and patching of the same method by different monkeys).
    """

    def __init__ (self, fct, orig_name) :
        self.__dict__.update (fct.__dict__)
        self.__doc__    = fct.__doc__
        self.__module__ = fct.__module__
        self.__name__   = fct.__name__
        self._chain     = None
        self._fct       = fct
        self._key       = "__%s_%08X_%s" % (fct.__name__, id (fct), orig_name)
        self._orig_name = orig_name
    # end def __init__

    def _add_to_class (self, cls) :
        name = self.__name__
        orig = getattr (cls, name, None)
        if orig is not None :
            assert not hasattr (orig, self._orig_name), \
                "%s, %s, %s" % (cls.__name__, self._key, orig)
            setattr (cls, self._key, orig)
            for b in cls.__mro__ :
                c = b.__dict__.get (name)
                if c is not None and isinstance (c, _Added_Method_Descriptor_) :
                    self._chain = c
                    break
        setattr (cls, name, self)
    # end def _add_to_class

    def __get__ (self, obj, cls = None) :
        if obj is None :
            result = TFL.Function (self._fct)
        else :
            result = TFL.Functor  (self._fct, head_args = (obj, ))
        c = self
        while c is not None :
            o = getattr (cls, c._key, None)
            if o is not None :
                setattr (result, c._orig_name, o)
                c = c._chain
            else :
                c = None
        return result
    # end def __get__

# end class _Added_Method_Descriptor_

def Add_Method (* classes, ** kw) :
    """Adds decorated function to `classes` (won't complains if any class
       already contains a function of that name).

       >>> class A (object) :
       ...     def foo (self) :
       ...         print self.__class__.__name__
       ...
       >>> class B (object) :
       ...     def foo (self) :
       ...         print self.__class__.__name__
       ...
       >>> class C (B) : pass
       ...
       >>> class D (B) : pass
       ...
       >>> class T (type) :
       ...     def foo (cls) :
       ...         print cls.__class__.__name__
       ...
       >>> @TFL.Add_Method (A, B)
       ... def foo (self) :
       ...     print "decorated",
       ...     return self.foo.orig (self)
       ...
       >>> @TFL.Add_Method (C, D, T, orig_name = "orig1")
       ... def foo (self) :
       ...     print "twice",
       ...     return self.foo.orig1 (self)
       ...
       >>> @TFL.Add_Method (D, orig_name = "orig2")
       ... def foo (self) :
       ...     print "more than",
       ...     return self.foo.orig2 (self)
       ...
       >>> @TFL.Add_Method (T)
       ... def foo (cls) :
       ...     print "meta-decorated",
       ...     return cls.foo.orig (cls)
       ...
       >>> for X in A, B, C, D :
       ...     o = X ()
       ...     print "Instance call:",
       ...     o.foo ()
       ...     print "Class    call:",
       ...     X.foo (o)
       ...
       Instance call: decorated A
       Class    call: decorated A
       Instance call: decorated B
       Class    call: decorated B
       Instance call: twice decorated C
       Class    call: twice decorated C
       Instance call: more than twice decorated D
       Class    call: more than twice decorated D

       >>> for X in T, :
       ...     c = T ("bar", (), {})
       ...     print "Class    call:",
       ...     c.foo ()
       ...     print "Meta     call:",
       ...     T.foo (c)
       Class    call: meta-decorated twice T
       Meta     call: meta-decorated twice T

    """
    def decorator (f) :
        orig_name = kw.pop ("orig_name", "orig")
        for cls in classes :
            _Added_Method_Descriptor_ (f, orig_name)._add_to_class (cls)
        return f
    return decorator
# end def Add_Method

def Add_New_Method (* classes) :
    """Adds decorated function to `classes` (complains if any class already
       contains a function of that name).
    """
    def decorator (f) :
        name = f.__name__
        for cls in classes :
            if hasattr (cls, name) :
                raise TypeError, "%s already has a property named `%s`" % \
                    (cls, name)
            setattr (cls, name, f)
        return f
    return decorator
# end def Add_New_Method

def Decorator (decorator) :
    """Decorate `decorator` so that `__name__`, `__doc__`, and `__dict__` of
       decorated functions/methods are preserved.

       >>> def deco (f) :
       ...     def wrapper () :
       ...         "Wrapper around decorated function"
       ...         return f ()
       ...     return wrapper
       ...
       >>> @deco
       ... def foo () :
       ...     "Function to test decoration"
       ...     pass
       ...
       >>> foo.__name__, foo.__doc__
       ('wrapper', 'Wrapper around decorated function')

       >>> @Decorator
       ... def deco (f) :
       ...     def wrapper () :
       ...         "Wrapper around decorated function"
       ...         return f ()
       ...     return wrapper
       ...
       >>> @deco
       ... def foo () :
       ...     "Function to test decoration"
       ...     pass
       ...
       >>> foo.__name__, foo.__doc__
       ('foo', 'Function to test decoration')
    """
    def wrapper (f) :
        decorated            = decorator (f)
        decorated.__name__   = f.__name__
        decorated.__module__ = getattr (f, "__module__", "<builtin>")
        decorated.__doc__    = f.__doc__
        decorated.__dict__.update (getattr (f, "__dict__", {}))
        return decorated
    wrapper.__name__   = decorator.__name__
    wrapper.__module__ = decorator.__module__
    wrapper.__doc__    = decorator.__doc__
    wrapper.__dict__.update (decorator.__dict__)
    return wrapper
# end def Decorator

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Decorator

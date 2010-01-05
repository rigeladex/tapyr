# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006-2009 Mag. Christian Tanzer. All rights reserved
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
#     4-Apr-2008 (CT)  Set `_globals` (unfortunately, both `__globals__` and
#                      `func_globals` are readonly)
#     4-Apr-2008 (CT)  `Contextmanager` added
#    17-Apr-2008 (CT)  `_Added_Method_Descriptor_` complexity revoked (didn't
#                      work for replacing a method that's overriden by a
#                      descendent of the class for which it is overriden)
#    17-Apr-2008 (CT)  `Override_Method` added (allows access to `orig`, but
#                      no multiple classes); `Add_Method` changed to not
#                      provide `orig`
#    18-Apr-2008 (CT)  `Decorator` decorator removed from `Add_Method` and
#                      `Override_Method`
#    19-Jun-2008 (CT)  `Attributed` added
#    23-Aug-2008 (CT)  `Annotated` added
#    12-Oct-2009 (CT)  `Add_To_Class` added
#     4-Nov-2009 (CT)  `decorator` keyword argument added to `Add_Method` and
#                      `Add_New_Method`
#    ««revision-date»»···
#--

from   _TFL         import TFL

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
        decorated             = decorator (f)
        decorated.__name__    = f.__name__
        decorated.__module__  = getattr (f, "__module__", "<builtin>")
        decorated.__doc__     = f.__doc__
        decorated.__dict__.update (getattr (f, "__dict__", {}))
        decorated._globals    = \
            getattr (f, "_globals", getattr (f, "__globals__", {}))
        return decorated
    wrapper.__name__   = decorator.__name__
    wrapper.__module__ = decorator.__module__
    wrapper.__doc__    = decorator.__doc__
    wrapper.__dict__.update (decorator.__dict__)
    wrapper._globals   = getattr \
        (decorator, "_globals", getattr (decorator, "__globals__", {}))
    return wrapper
# end def Decorator

_undefined = object ()

def Annotated (RETURN = _undefined, ** kw) :
    """Add dictionary `func_annotations` containing elements of `kw` and
       value of `RETURN` bound to key `return` as proposed by
       http://www.python.org/dev/peps/pep-3107/.

       Each key of `kw` must be the name of an argument of the function to be
       annotated.

       >>> @TFL.Annotated (bar = "Arg 1", baz = 42)
       ... def foo (bar, baz) : pass
       ...
       >>> sorted (foo.func_annotations.items ())
       [('bar', 'Arg 1'), ('baz', 42)]
       >>> @TFL.Annotated (bar = "Arg 1", baz = 42, RETURN = None)
       ... def foo (bar, baz) : pass
       ...
       >>> sorted (foo.func_annotations.items ())
       [('bar', 'Arg 1'), ('baz', 42), ('return', None)]
       >>> @TFL.Annotated (bar = "Arg 1", baz = 42, qux = None)
       ... def foo (bar, baz) : pass
       ...
       Traceback (most recent call last):
         ...
       TypeError: Function `foo` doesn't have an argument named `qux`
    """
    def decorator (f) :
        from inspect import getargspec
        f.func_annotations             = fa = {}
        args, varargs, varkw, defaults = getargspec (f)
        if varargs : args.append (varargs)
        if varkw   : args.append (varkw)
        arg_set = set (args)
        for k, v in kw.iteritems () :
            if k in arg_set :
                fa [k] = v
            else :
                raise TypeError, \
                    ( "Function `%s` doesn't have an argument named `%s`"
                    % (f.__name__, k)
                    )
        if RETURN is not _undefined :
            fa ["return"] = RETURN
        return f
    return decorator
# end def Annotated

def Attributed (** kw) :
    """Add all elements of `kw` as function attribute to decorated function.

       >>> from _TFL.Decorator import *
       >>> @Attributed (foo = 1, bar = 42)
       ... def f () :
       ...     pass
       ...
       >>> sorted (f.__dict__.iteritems ())
       [('bar', 42), ('foo', 1)]
       >>> @Attributed (a = "WTF", b = 137)
       ... def g () :
       ...     "Test `Attributed` decorator"
       ...
       >>> sorted (g.__dict__.iteritems ())
       [('a', 'WTF'), ('b', 137)]
       >>> g.__doc__
       'Test `Attributed` decorator'
    """
    def decorator (f) :
        for k, v in kw.iteritems () :
            setattr (f, k, v)
        return f
    return decorator
# end def Attributed

@Decorator
def Contextmanager (f) :
    """Decorate `f` so that it's usable as a contextmanager in `with`
       statements.
    """
    from contextlib import contextmanager
    return contextmanager (f)
# end def Contextmanager

def Add_Method (* classes, ** kw) :
    """Adds decorated function to `classes` (won't complain if any class
       already contains a function of that name, but the original function
       isn't available to the decorated function for chaining up to).
    """
    def decorator (f) :
        name = f.__name__
        deco = kw.get ("decorator")
        if deco :
            f = deco (f)
        for cls in classes :
            setattr (cls, name, f)
        return f
    return decorator
# end def Add_Method

def Add_New_Method (* classes, ** kw) :
    """Adds decorated function to `classes` (complains if any class already
       contains a function of that name).
    """
    def decorator (f) :
        name = f.__name__
        deco = kw.get ("decorator")
        if deco :
            f = deco (f)
        for cls in classes :
            if hasattr (cls, name) :
                raise TypeError \
                    ("%s already has a property named `%s`" % (cls, name))
            setattr (cls, name, f)
        return f
    return decorator
# end def Add_New_Method

def Add_To_Class (name, * classes) :
    """Adds decorated function/class to `classes` using `name`.
    """
    def decorator (x) :
        for cls in classes :
            setattr (cls, name, x)
        return x
    return decorator
# end def Add_To_Class

@Decorator
def Override_Method (cls) :
    """Adds decorated function to `cls` (original method if any is available
       inside the decorated function as function attribute `.orig`).
    """
    def decorator (f) :
        name = f.__name__
        if hasattr (cls, name) :
            setattr (f, "orig", getattr (cls, name))
        setattr (cls, name, f)
        return f
    return decorator
# end def Override_Method

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Decorator

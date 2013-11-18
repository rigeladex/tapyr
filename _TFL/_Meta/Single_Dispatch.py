# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.Meta.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.Meta.Single_Dispatch
#
# Purpose
#    Implement dispatch based on the type of a single argument
#
# Revision Dates
#    25-Jun-2013 (CT) Creation
#    27-Jun-2013 (CT) Add `Single_Dispatch_Method.__new__` to allow arguments
#                     when used as decorator
#    27-Jun-2013 (CT) Add `Single_Dispatch_Method.__call__` to allow calls of
#                     un-bound method
#    12-Sep-2013 (CT) Return `func`, not `self`, from
#                     `Single_Dispatch_Method.add_type` (decorator chaining)
#    12-Sep-2013 (CT) Allow more than one type arg for `add_type`
#    ««revision-date»»···
#--

from   __future__        import division, print_function
from   __future__        import absolute_import, unicode_literals

from   _TFL              import TFL
from   _TFL.pyk          import pyk

import _TFL._Meta.Object
import _TFL._Meta.Property

from   weakref           import WeakKeyDictionary

import functools

class Single_Dispatch (TFL.Meta.Object) :
    """Dispatch based on the type of a single argument."""

    dispatch_on = 0

    def __init__ (self, func, T = object, dispatch_on = None) :
        self.top_func = func
        self.top_type = T
        self.registry = { T : func }
        self.cache    = WeakKeyDictionary ()
        if dispatch_on is not None :
            self.dispatch_on = dispatch_on
        functools.wraps (func) (self)
    # end def __init__

    def __call__ (self, * args, ** kw) :
        try :
            da = args [self.dispatch_on]
        except IndexError as exc :
            raise TypeError \
                ( "Fucntion %r needs at least %s positional arguments; "
                  "got %s: %s, %s"
                % ( self.top_func.__name__
                  , self.dispatch_on + 1
                  , len (args), args, kw
                  )
                )
        func = self.dispatch (da.__class__)
        return func (* args, ** kw)
    # end def __call__

    def add_type (self, * Types, ** kw) :
        """Add implementations for `Types`"""
        func = kw.pop ("func", None)
        if func is None :
            return lambda func : self.add_type (* Types, func = func)
        else :
            for T in Types :
                registry = self.registry
                if T in registry :
                    raise TypeError \
                        ( "Duplicate implementation for function %r for type %s"
                        % (self.top_func.__name__, T)
                        )
                registry [T] = func
            self.cache.clear ()
            return func
    # end def add_type

    def dispatch (self, T) :
        """Return the function implementation matching type `T`."""
        try :
            result = self.cache [T]
        except KeyError :
            try :
                result = self.registry [T]
            except KeyError :
                result = self.registry [self._best_match (T)]
            self.cache [T] = result
        return result
    # end def dispatch

    def _best_match (self, T) :
        registry = self.registry
        matches  = tuple (b for b in T.__mro__ [1:] if b in registry)
        if not matches :
            raise TypeError ("No match for argument type %s" % (T, ))
        return matches [0]
    # end def _best_match

# end class Single_Dispatch

class Single_Dispatch_2nd (Single_Dispatch) :
    """Dispatch based on the type of the second argument."""

    dispatch_on = 1

# end class Single_Dispatch_2nd

class Single_Dispatch_Method (TFL.Meta.Method_Descriptor) :
    """Dispatch a method based on the type of the second, i.e., first
       non-self, argument.
    """

    def __new__ \
            ( sdm_cls
            , method = None, cls = None, T = object, dispatch_on = None
            ) :
        if method is None :
            return \
                ( lambda method, cls = cls, T = T, dispatch_on = dispatch_on
                    : sdm_cls
                          (method, cls = cls, T = T, dispatch_on = dispatch_on)
                )
        return super (Single_Dispatch_Method, sdm_cls).__new__ (sdm_cls)
    # end def __new__

    def __init__ (self, method, cls = None, T = object, dispatch_on = None) :
        func = method
        if isinstance (func, TFL.Meta.Method_Descriptor) :
            func = func.method
        self.__super.__init__ \
            ( Single_Dispatch_2nd (func, T = T, dispatch_on = dispatch_on)
            , cls = cls
            )
    # end def __init__

    def __call__ (self, * args, ** kw) :
        return self.method (* args, ** kw)
    # end def __call__

    def add_type (self, * Types, ** kw) :
        func = kw.pop ("func", None)
        if func is None :
            return lambda func : self.add_type (* Types, func = func)
        else :
            self.method.add_type (* Types, func = func)
            ### `add_type` needs to return `func` to allow decorator chaining
            return func
    # end def add_type

    def dispatch (self, T) :
        return self.method.dispatch (T)
    # end def dispatch

# end class Single_Dispatch_Method

__doc__ = """
:class:`Single_Dispatch` implements dispatch based on the type of a single
argument::

    >>> @Single_Dispatch
    ... def foo (x) :
    ...     print ("foo got generic argument", x)

    >>> foo.__name__, foo.__class__
    ('foo', <class 'Single_Dispatch.Single_Dispatch'>)

    >>> sorted ((k.__name__, v.__name__) for k, v in foo.registry.items ())
    [('object', 'foo')]

    >>> foo (23)
    foo got generic argument 23
    >>> foo ("42")
    foo got generic argument 42

    >>> @foo.add_type (int)
    ... def foo_int (x) :
    ...     print ("foo_int got integer argument", x)

    >>> sorted ((k.__name__, v.__name__) for k, v in foo.registry.items ())
    [('int', 'foo_int'), ('object', 'foo')]

    >>> foo (23)
    foo_int got integer argument 23

    >>> foo ("42")
    foo got generic argument 42

    >>> @foo.add_type (pyk.text_type)
    ... def foo_str (x) :
    ...     print ("foo_str got string argument '%s'" % (x, ))

    >>> foo (23)
    foo_int got integer argument 23

    >>> foo ("42")
    foo_str got string argument '42'

    >>> @Single_Dispatch_2nd
    ... def bar (* args) :
    ...     print ("bar got generic argument", args)

    >>> bar (1)
    Traceback (most recent call last):
    ...
    TypeError: Fucntion 'bar' needs at least 2 positional arguments; got 1: (1,), {}
    >>> bar (1, 2)
    bar got generic argument (1, 2)
    >>> bar (1, 2, 3)
    bar got generic argument (1, 2, 3)

    >>> @bar.add_type (int)
    ... def bar_int (* args) :
    ...     print ("bar_int got integer argument", args)

    >>> bar (1, 2)
    bar_int got integer argument (1, 2)

    >>> bar (1, 2.0)
    bar got generic argument (1, 2.0)

    >>> @bar.add_type (float)
    ... def bar_float (* args) :
    ...     print ("bar_float got float argument", args)

    >>> bar (1, 2)
    bar_int got integer argument (1, 2)
    >>> bar (1, 2.0)
    bar_float got float argument (1, 2.0)

:class:`Single_Dispatch_Method` implements dispatch based on the type of a
single, normally the second, argument of an instance method::

    >>> class Qux (object) :
    ...
    ...     @Single_Dispatch_Method
    ...     def qux (self, x, y) :
    ...         print ("qux got generic argument", x, y)
    ...
    ...     @qux.add_type (int)
    ...     def qux_int (self, x, y) :
    ...         print ("qux_int got integer argument", x, y)

    >>> baz = Qux ()
    >>> baz.qux (1, 2)
    qux_int got integer argument 1 2

    >>> baz.qux ('1', 2)
    qux got generic argument 1 2

    >>> @Qux.qux.add_type (pyk.text_type)
    ... def qux_str (self, x, y) :
    ...     print ("qux_str got string argument", x, y)

    >>> baz.qux (1, 2)
    qux_int got integer argument 1 2

    >>> baz.qux ('1', 2)
    qux_str got string argument 1 2

"""

if __name__ != "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.Single_Dispatch

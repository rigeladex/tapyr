# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Meta.totally_ordered
#
# Purpose
#    Add all missing rich comparison methods to a class
#
# Revision Dates
#    21-Sep-2009 (CT) Creation
#    22-Sep-2009 (CT) `__eq__` and `__ne__` removed from `_Orders_.__cmp__`
#    22-Sep-2009 (CT) `equality_operators ["__eq__"]` change to use only `<`
#    19-Nov-2009 (CT) `_Orders_.__hash__` added (3-compatibility)
#    ««revision-date»»···
#--

"""
`totally_ordered` is a class decorator adding all missing rich comparison
methods to a class, if at least one of the rich ordering methods or the
old-style `__cmp__` is defined.

>>> class T (TFL.Meta.Object) :
...     def __init__ (self, value) :
...         self.value = value
...
>>> @totally_ordered
... class T_ge (T) :
...     def __ge__ (self, rhs) : return self.value >= rhs.value
...
>>> @totally_ordered
... class T_gt (T) :
...     def __gt__ (self, rhs) : return self.value >  rhs.value
...
>>> @totally_ordered
... class T_gtr (T) :
...     def __gt__ (self, rhs) : return self.value <  rhs.value
...
>>> @totally_ordered
... class T_le (T) :
...     def __le__ (self, rhs) : return self.value <= rhs.value
...
>>> @totally_ordered
... class T_lt (T) :
...     def __lt__ (self, rhs) : return self.value <  rhs.value
...
>>> @totally_ordered
... class T_ltr (T) :
...     def __lt__ (self, rhs) : return self.value >  rhs.value
...
>>> @totally_ordered
... class T_cmp (T) :
...     def __cmp__ (self, rhs) : return self.value - rhs.value
...

>>> for C in T_cmp, T_ge, T_gt, T_le, T_lt, T_gtr, T_ltr :
...     a, b, c = C (1), C (2), C (2)
...     print C.__name__, a<b, a<=b, a>b, a>=b, b<a, b<=a, b>a, b>=a
...     print "    ", a==b, a!=b, b==c, b!=c
...
T_cmp True True False False False False True True
     False True True False
T_ge True True False False False False True True
     False True True False
T_gt True True False False False False True True
     False True True False
T_le True True False False False False True True
     False True True False
T_lt True True False False False False True True
     False True True False
T_gtr False False True True True True False False
     False True True False
T_ltr False False True True True True False False
     False True True False
>>> for C in T_lt, T_gtr, T_ltr :
...     a, b, c = C (1), C (2), C (2)
...     print C.__name__, (a, b) < (a, b), (a, b) <= (a, b), (a, b) == (a, b)
...     print "    ",     (a, b) > (a, b), (a, b) >= (a, b), (a, b) == (a, b)
...     print "    ",     (b, c) < (b, c), (b, c) <= (b, c), (b, c) == (b, c)
...     print "    ",     (b, c) > (b, c), (b, c) >= (b, c), (b, c) == (b, c)
...     print "    ",     (a, c) < (b, c), (a, c) <= (b, c), (a, c) == (b, c)
...     print "    ",     (a, c) > (b, c), (a, c) >= (b, c), (a, c) == (b, c)
T_lt False True True
     False True True
     False True True
     False True True
     True True False
     False False False
T_gtr False True True
     False True True
     False True True
     False True True
     False False False
     True True False
T_ltr False True True
     False True True
     False True True
     False True True
     False False False
     True True False
>>> totally_ordered (T)
Traceback (most recent call last):
  ...
TypeError: Totally ordered class `T` must define at least one of: __lt__, __gt__, __le__, __ge__, or __cmp__

"""

from   _TFL              import TFL
import _TFL._Meta.Object

import itertools

_order_operators = ("__lt__", "__gt__", "__le__", "__ge__")

def _base_operator (cls) :
    names = set (_order_operators + ("__cmp__", ))
    ops   = cls.operators = dict ()
    for name, func in cls.__dict__.iteritems () :
        if name in names :
            func.__doc__  = getattr (object, name).__doc__
            ops [name]    = func
    return cls
# end def _base_operator

class _Orders_ (TFL.Meta.Object) :
    """Helper defining the possible comparison methods derived from one given."""

    @_base_operator
    class __cmp__ :
        def __ge__ (self, rhs) : return self.__cmp__ (rhs) >= 0
        def __gt__ (self, rhs) : return self.__cmp__ (rhs) >  0
        def __le__ (self, rhs) : return self.__cmp__ (rhs) <= 0
        def __lt__ (self, rhs) : return self.__cmp__ (rhs) <  0

    @_base_operator
    class __ge__ :
        def __gt__ (self, rhs) : return not rhs  >= self
        def __le__ (self, rhs) : return     rhs  >= self
        def __lt__ (self, rhs) : return not self >= rhs

    @_base_operator
    class __gt__ :
        def __ge__ (self, rhs) : return not rhs  >  self
        def __le__ (self, rhs) : return not self >  rhs
        def __lt__ (self, rhs) : return     rhs  >  self

    @_base_operator
    class __le__ :
        def __ge__ (self, rhs) : return     rhs  <= self
        def __gt__ (self, rhs) : return not self <= rhs
        def __lt__ (self, rhs) : return not rhs  <= self

    @_base_operator
    class __lt__ :
        def __ge__ (self, rhs) : return not self <  rhs
        def __gt__ (self, rhs) : return     rhs  <  self
        def __le__ (self, rhs) : return not rhs  <  self

    ### Unfortunately, defining `__eq__` as a method here doesn't work due to
    ### the exception::
    ###     TypeError: unbound method __eq__() must be called with _Orders_
    ###         instance as first argument (got T_ge instance instead)
    ###
    ### Both `__eq__` and `__ne__` only use the `<` operator as that is the
    ### one most likely to be defined (being used by Pythons inbuilt `sort`)
    ###
    ### Using more than one operator for implementing `__eq__` (or `__ne__`)
    ### gives wrong results for some implementations of the base operator
    equality_operators = dict \
        ( __eq__ = lambda self, rhs : not (self < rhs or rhs < self)
        , __ne__ = lambda self, rhs :     (self < rhs or rhs < self)
        )

    for name, func in equality_operators.iteritems () :
        func.__name__ = name
        func.__doc__  = getattr (object, name).__doc__

    def __hash__ (self) :
        ### Define this just to silence `-3` deprecation warning about __cmp__
        raise NotImplementedError
    # end def __hash__

# end class _Orders_

def totally_ordered (cls) :
    """Class decorator adding missing comparison methods."""
    defined = set (cls.__dict__)
    oops    = set (_order_operators) & defined
    if oops :
        base = (k for k in _order_operators if k in oops).next ()
    elif "__cmp__" in defined :
        ### backwards compatibility for 2.x classes defining `__cmp__`
        base = "__cmp__"
    else :
        raise TypeError, \
            ( "Totally ordered class `%s` must define at least one of: "
              "%s, or __cmp__"
            % (cls.__name__, ", ".join (_order_operators))
            )
    for name, func in itertools.chain \
            ( getattr (_Orders_, base).operators.iteritems ()
            , _Orders_.equality_operators.iteritems ()
            ) :
        if name not in defined :
            setattr (cls, name, func)
    return cls
# end def totally_ordered

if __name__ == "__main__" :
    TFL.Meta._Export ("*")
### __END__ TFL.Meta.totally_ordered

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008-2011 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Filter
#
# Purpose
#    Classes for filtering
#
# Revision Dates
#    26-Jan-2008 (CT) Creation (started out as TOM.Entity_Dump_Filter)
#    27-Jan-2008 (CT) Creation continued
#    28-Jan-2008 (CT) Moved to TFL.Filter
#    28-Jan-2008 (CT) Creation continued..
#    13-Feb-2008 (CT) `filter_iter` added
#     6-May-2008 (CT) Use `all_true` and `any_true` instead of `all` and
#                     `any` to avoid errors from Python 2.4
#    17-Oct-2008 (CT) `* args, ** kw` added to filter functions
#     1-Dec-2009 (CT) `Attr_Query` and `Attr_Filter` added
#     1-Dec-2009 (MG) `Attr_Query.__mod__` added
#     2-Dec-2009 (CT) `_Filter_Q_.__init__` changed to not extract
#                     `predicate` of `Attr_Filter` instances
#     4-Dec-2009 (CT) `Attr_Query` based on `TFL.Q_Exp.Base` instead of
#                     home-grown code; `Attr_Filter` removed
#    19-Jan-2010 (CT) `Attr_Query.And` and `Attr_Query.Or` added
#    16-Jul-2011 (CT) `__repr__` added
#    ««revision-date»»···
#--

"""
This module provides some classes for filtering iterables.

    >>> def pprint (x) :
    ...     import textwrap
    ...     text = str (x)
    ...     sep  = chr (10) + "    "
    ...     print sep.join (textwrap.wrap (text, 70))
    ...
    >>> def is_even  (x) : return (x % 2) == 0
    ...
    >>> def div_7    (x) : return (x % 7) == 0
    ...
    >>> def is_prime (x) : return x in primes
    ...

    >>> primes                = [2, 3, 5, 7, 11, 13, 17, 19]
    >>> some_teens            = range (10, 20, 2)
    >>> fourties              = range (40, 50)
    >>> numbers               = primes + some_teens + fourties

    >>> Div_7                 = Filter     (div_7)
    >>> Is_Prime              = Filter     (is_prime)
    >>> Is_Even               = Filter     (is_even)
    >>> Is_Odd                = Filter_Not (Is_Even)
    >>> Is_Not_Odd            = Filter_Not (Is_Odd)
    >>> Div_7_and_Prime       = Filter_And (Div_7, Is_Prime)
    >>> Div_7_or_Prime        = Filter_Or  (Div_7, Is_Prime)
    >>> Div_7_not_Prime       = Filter_And (Div_7, ~ Is_Prime)
    >>> Div_7_not_Prime_Even  = Filter_And (Div_7_not_Prime, Is_Even)
    >>> Div_7_not_Prime_Odd   = Filter_And (Div_7_not_Prime, Is_Odd)
    >>> Is_Even_and_Prime     = Filter_And (Is_Even,  Is_Prime)

    >>> Div_7.filter (numbers)
    [7, 14, 42, 49]
    >>> Is_Prime.filter (numbers)
    [2, 3, 5, 7, 11, 13, 17, 19]
    >>> Is_Even.filter (numbers)
    [2, 10, 12, 14, 16, 18, 40, 42, 44, 46, 48]
    >>> Is_Odd.filter (numbers)
    [3, 5, 7, 11, 13, 17, 19, 41, 43, 45, 47, 49]
    >>> Is_Not_Odd.filter (numbers)
    [2, 10, 12, 14, 16, 18, 40, 42, 44, 46, 48]
    >>>
    >>> Div_7_and_Prime.filter (numbers)
    [7]
    >>> Div_7_or_Prime.filter (numbers)
    [2, 3, 5, 7, 11, 13, 17, 19, 14, 42, 49]
    >>> Div_7_not_Prime.filter (numbers)
    [14, 42, 49]
    >>> Div_7_not_Prime_Even.filter (numbers)
    [14, 42]
    >>> Div_7_not_Prime_Odd.filter (numbers)
    [49]
    >>> Is_Even_and_Prime.filter (numbers)
    [2]
    >>>
    >>> (~ Div_7).filter (numbers)
    [2, 3, 5, 11, 13, 17, 19, 10, 12, 16, 18, 40, 41, 43, 44, 45, 46, 47, 48]
    >>> (~ Is_Prime).filter (numbers)
    [10, 12, 14, 16, 18, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
    >>> (~ Is_Even).filter (numbers)
    [3, 5, 7, 11, 13, 17, 19, 41, 43, 45, 47, 49]
    >>> (~ Is_Odd).filter (numbers)
    [2, 10, 12, 14, 16, 18, 40, 42, 44, 46, 48]
    >>> (~ Is_Not_Odd).filter (numbers)
    [3, 5, 7, 11, 13, 17, 19, 41, 43, 45, 47, 49]
    >>>
    >>> pprint ((~ Div_7_and_Prime).filter (numbers))
    [2, 3, 5, 11, 13, 17, 19, 10, 12, 14, 16, 18, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49]
    >>> pprint ((~ Div_7_or_Prime).filter (numbers))
    [10, 12, 16, 18, 40, 41, 43, 44, 45, 46, 47, 48]
    >>> pprint ((~ Div_7_not_Prime).filter (numbers))
    [2, 3, 5, 7, 11, 13, 17, 19, 10, 12, 16, 18, 40, 41, 43, 44, 45, 46,
        47, 48]
    >>> pprint ((~ Div_7_not_Prime_Even).filter (numbers))
    [2, 3, 5, 7, 11, 13, 17, 19, 10, 12, 16, 18, 40, 41, 43, 44, 45, 46,
        47, 48, 49]
    >>> pprint ((~ Div_7_not_Prime_Odd).filter (numbers))
    [2, 3, 5, 7, 11, 13, 17, 19, 10, 12, 14, 16, 18, 40, 41, 42, 43, 44,
        45, 46, 47, 48]
    >>> pprint ((~ Is_Even_and_Prime).filter (numbers))
    [3, 5, 7, 11, 13, 17, 19, 10, 12, 14, 16, 18, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49]
    >>>
    >>> Is_Even.filter (numbers) == (~~Is_Even).filter (numbers)
    True

The filter operators `&` (logical and), `|` (logical or), and `~` (logical
not) are optimized to avoid intermediate level filter objects. The binary
operators short-circuit::

    >>> Is_Not_Odd is Is_Even
    True
    >>> Is_Even.predicate.__name__
    'is_even'
    >>> (~~Is_Even).predicate.__name__
    'is_even'
    >>> len ((Div_7_and_Prime & Div_7_and_Prime).predicates)
    4
    >>> len ((Div_7_or_Prime  | Div_7_or_Prime).predicates)
    4
    >>> len ((Div_7_and_Prime & Div_7_or_Prime).predicates)
    3
    >>> len ((Div_7_or_Prime  | Div_7_and_Prime).predicates)
    3
    >>> len ((Div_7_and_Prime | Div_7_and_Prime).predicates)
    2
    >>> len ((Div_7_or_Prime  & Div_7_or_Prime).predicates)
    2

    >>> for f in Div_7_and_Prime, Div_7_or_Prime :
    ...     for g in f, ~f, ~~f :
    ...         print g.__class__.__name__,
    ...     print
    ...
    Filter_And Filter_Or Filter_And
    Filter_Or Filter_And Filter_Or

"""

from   _TFL                     import TFL
from   _TFL.predicate           import first, all_true, any_true

import _TFL._Meta.Object
import _TFL.Q_Exp

import operator

class _Filter_ (TFL.Meta.Object) :
    """Base class for filters."""

    attrs = {}

    def filter (self, iterable, * args, ** kw) :
        return list (self.filter_iter (iterable, * args, ** kw))
    # end def filter

    def filter_iter (self, iterable, * args, ** kw) :
        return (item for item in iterable if self (item, * args, ** kw))
    # end def filter_iter

    def __call__ (self, item, * args, ** kw) :
        return self.predicate (item, * args, ** kw)
    # end def __call__

    def __and__ (self, rhs) :
        return Filter_And (self, rhs)
    # end def __add__

    def __getattr__ (self, name) :
        try :
            return self.attrs [name]
        except KeyError :
            raise AttributeError (name)
    # end def __getattr__

    def __invert__ (self) :
        return Filter_Not (self.predicate, ** self.attrs)
    # end def __invert__

    def __or__ (self, rhs) :
        return Filter_Or (self, rhs)
    # end def __or__

# end class _Filter_

class _Filter_S_ (_Filter_) :
    """Base class for simple predicate filters."""

# end class _Filter_S_

class Filter (_Filter_S_) :
    """Return all items from an iterable which satisfy the predicate."""

    def __new__ (cls, predicate, ** kw) :
        if isinstance (predicate, Filter) :
            return predicate
        else :
            return super (Filter, cls).__new__ (cls, predicate, ** kw)
    # end def __new__

    def __init__ (self, predicate, ** kw) :
        if self is not predicate :
            self.predicate = predicate
            self.attrs     = kw
    # end def __init__

    def __repr__ (self) :
        return "<%s %s>" % (self.__class__.__name__, self.predicate)
    # end def __repr__

# end class Filter

class Filter_Not (_Filter_S_) :
    """Return all items from an iterable which don't satisfy the predicate."""

    def __new__ (cls, predicate, ** kw) :
        if isinstance (predicate, Filter_Not) :
            return ~ predicate
        else :
            return super  (Filter_Not, cls).__new__ (cls, predicate, ** kw)
    # end def __new__

    def __init__ (self, predicate, ** kw) :
        self._not_predicate = predicate
        self.attrs          = kw
    # end def __init__

    def predicate (self, item, * args, ** kw) :
        return not self._not_predicate (item, * args, ** kw)
    # end def predicate

    def __invert__ (self) :
        return Filter (self._not_predicate, ** self.attrs)
    # end def __invert__

    def __repr__ (self) :
        return "<%s NOT %s>" % (self.__class__.__name__, self.predicate)
    # end def __repr__

# end class Filter_Not

class _Filter_Q_ (_Filter_) :
    """Base class for quantifying filters."""

    def __init__ (self, * pred_or_filters) :
        assert pred_or_filters
        self.predicates = preds = []
        add = preds.append
        ext = preds.extend
        for pof in pred_or_filters :
            if isinstance (pof, self.__class__) :
                ext (pof.predicates)
            elif getattr (pof, "predicate_precious_p", False) :
                add (pof)
            else :
                add (getattr (pof, "predicate", pof))
    # end def __init__

    def predicate (self, item, * args, ** kw) :
        return self.quant (p (item, * args, ** kw) for p in self.predicates)
    # end def predicate

    def _inverted_predicate (self) :
        return [Filter_Not (p) for p in self.predicates]
    # end def _inverted_predicate

    def __repr__ (self) :
        return "<%s %s>" % (self.__class__.__name__, self.predicates)
    # end def __repr__

# end class _Filter_Q_

class Filter_And (_Filter_Q_) :
    """Return all items from an iterable which satisfy all predicates."""

    quant = staticmethod (all_true)

    def __invert__ (self) :
        return Filter_Or (* self._inverted_predicate ())
    # end def __invert__

# end class Filter_And

class Filter_Or (_Filter_Q_) :
    """Return all items from an iterable which satisfy any of the predicates."""

    quant = staticmethod (any_true)

    def __invert__ (self) :
        return Filter_And (* self._inverted_predicate ())
    # end def __invert__

# end class Filter_Or

class Attr_Query (TFL.Q_Exp.Base) :
    """Syntactic sugar for creating Filter objects based on attribute queries.

       >>> from _TFL.Record import Record as R
       >>> Q  = Attr_Query ()
       >>> r1 = R (foo = 42, bar = 137, baz = 11)
       >>> q0 = Q.foo
       >>> q0
       Q.foo
       >>> q0._name
       'foo'
       >>> q0.predicate (r1)
       42

       >>> Q.fool.STARTSWITH ("bar") (R (fool = "barfly"))
       True
       >>> Q.fool.STARTSWITH ("fly") (R (fool = "barfly"))
       False
       >>> Q.fool.ENDSWITH ("fly") (R (fool = "barfly"))
       True
       >>> Q.fool.ENDSWITH ("bar") (R (fool = "barfly"))
       False
       >>> Q.fool.BETWEEN (2, 8) (R (fool = 1))
       False
       >>> Q.fool.BETWEEN (2, 8) (R (fool = 2))
       True
       >>> Q.fool.BETWEEN (2, 8) (R (fool = 3))
       True
       >>> Q.fool.BETWEEN (2, 8) (R (fool = 8))
       True
       >>> Q.fool.BETWEEN (2, 8) (R (fool = 9))
       False
       >>> (Q.fool == "barfly") (R (fool = "barfly"))
       True
       >>> (Q.fool != "barfly") (R (fool = "barfly"))
       False
       >>> (Q.fool != "barflyz") (R (fool = "barfly"))
       True
       >>> (Q.fool <= "barflyz") (R (fool = "barfly"))
       True
       >>> (Q.fool >= "barflyz") (R (fool = "barfly"))
       False
       >>> Q.fool.CONTAINS ("barf") (R (fool = "a barfly "))
       True
       >>> Q.fool.IN ([2,4,8]) (R (fool = 1))
       False
       >>> Q.fool.IN ([2,4,8]) (R (fool = 2))
       True
       >>> Q.fool.IN ([2,4,8]) (R (fool = 3))
       False
       >>> Q.fool.IN ([2,4,8]) (R (fool = 4))
       True
       >>> (Q.fool % 2) (R (fool = 20))
       0

    """

    Ignore_Exception = AttributeError

    And              = Filter_And
    Or               = Filter_Or

    class Bin_Bool (_Filter_S_, TFL.Q_Exp.Bin_Bool) :
        pass
    # end class Bin_Bool

    class Bin_Expr (_Filter_S_, TFL.Q_Exp.Bin_Expr) :
        pass
    # end class Bin_Expr

    class Call (_Filter_S_, TFL.Q_Exp.Call) :
        pass
    # end class Call

# end class Attr_Query

if __name__ != "__main__" :
    TFL._Export ("*", "_Filter_", "_Filter_Q_")
### __END__ TFL.Filter

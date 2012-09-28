# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer All rights reserved
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
#    TFL.Q_Result
#
# Purpose
#    Provide filtering and ordering functions over query result
#
# Revision Dates
#     1-Dec-2009 (CT) Creation
#     2-Dec-2009 (CT) Creation continued
#     3-Dec-2009 (CT) Creation continued..
#     7-Dec-2009 (CT) Usage of `TFL.Attr_Filter` replaced by `TFL.Attr_Query`
#    19-Feb-2010 (MG) `first` fixed
#     1-Sep-2010 (CT) `attr`, `attrs`, and `set` added
#     2-Sep-2010 (CT) `set` changed to use `SET` of `Q.Get`
#     7-Sep-2010 (MG) `attr` and `attrs` return a `Q_Result` instance instead
#                     of being an iterator
#    26-Jul-2011 (CT) Handling of `distinct` changed so that it is passed on
#                     to derived queries
#    13-Sep-2011 (MG) `group_by` and `_Q_Result_Group_By_` added
#    16-Sep-2011 (MG) `_Attr_` and `_Attrs_Tuple_` added and used
#    16-Sep-2011 (MG) `_Attr_` missing  compare functions added
#    16-Sep-2011 (CT) `_Attr_.__eq__` and `.__lt__` robustified
#    16-Sep-2011 (MG) `_Q_Result_Group_By_._fill_cache` support for `SUM`
#                     added
#    15-Nov-2011 (CT) Change `_Attrs_Tuple_.__init__` to not pass `* args` to
#                     `__super` to avoid: `DeprecationWarning:
#                         object.__init__() takes no parameters`
#    30-Jan-2012 (CT) Add `_Attr_.__nonzero__`, `__int__`, `.__float__`;
#                     define all `_Attr_` comparison operators explicitly
#    12-Jun-2012 (MG) `Q_Result_Composite._fill_cache`: check for
#                     `self._order_by` fixed
#     8-Aug-2012 (CT) Fix typo (`.__class__.__name__`, not `.__class__.__name`)
#    ««revision-date»»···
#--

"""
Module `Q_Result`
==================

Provide filtering and ordering functions over query result::

    >>> qr = Q_Result ([x for x in range (10)])
    >>> qr.count ()
    10
    >>> qr [5]
    5
    >>> qr [5:9].all ()
    [5, 6, 7, 8]
    >>> qr.slice (3).all ()
    [3, 4, 5, 6, 7, 8, 9]
    >>> qr.slice (3, 5).all ()
    [3, 4]
    >>> qr.slice (3, 8).all ()
    [3, 4, 5, 6, 7]
    >>> qq = qr.order_by (lambda x : x % 2)
    >>> qq [4]
    8
    >>> qq.all ()
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    >>> qq.filter (lambda x : x % 2).all ()
    [1, 3, 5, 7, 9]
    >>> qq.distinct (lambda x : x % 2).all ()
    [0, 1]
    >>> qq.all ()
    [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    >>> qq.distinct (lambda x : x % 3 == 0).all ()
    [0, 2]
    >>> qs = qr.filter (lambda x : x % 2 == 0)
    >>> qs.count ()
    5
    >>> qs.all ()
    [0, 2, 4, 6, 8]
    >>> qt = qs.filter (lambda x : x % 3 == 0)
    >>> qt.count ()
    2
    >>> qt.all ()
    [0, 6]
    >>> qt.first ()
    0
    >>> qt.one ()
    Traceback (most recent call last):
      ...
    IndexError: Query result contains 2 entries
    >>> qu = qt.limit (1)
    >>> qu.all ()
    [0]
    >>> qu.one ()
    0
    >>> qv = qt.offset (1)
    >>> qv.all ()
    [6]
    >>> qv.one ()
    6

    >>> qr = Q_Result (list (range (1, 100, 10)))
    >>> qs = Q_Result (list (range (10, 200, 20)))
    >>> qt = Q_Result (list (x*x for x in range (10)))
    >>> qc = Q_Result_Composite ((qr, qs, qt))
    >>> qr.count ()
    10
    >>> qs.count ()
    10
    >>> qt.count ()
    10
    >>> qc.count ()
    30
    >>> qc.all ()
    [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    >>> qc.distinct ().count ()
    28
    >>> qc.distinct ().all ()
    [1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 0, 4, 9, 16, 25, 36, 49, 64]
    >>> qc.distinct ().order_by (lambda x : x % 10).all ()
    [10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 0, 1, 11, 21, 31, 41, 51, 61, 71, 81, 91, 4, 64, 25, 16, 36, 9, 49]
    >>> qc.distinct (lambda x : x % 10).all ()
    [1, 10, 4, 9, 16, 25]
    >>> qc.distinct (lambda x : x % 10).count ()
    6
    >>> qc [5:15].all ()
    [51, 61, 71, 81, 91, 10, 30, 50, 70, 90]
    >>> qc.limit (5).all ()
    [1, 11, 21, 31, 41]
    >>> qc.distinct (lambda x : x % 10).limit (3).all ()
    [1, 10, 4]
    >>> qc.limit (15).distinct (lambda x : x % 10).all ()
    [1, 10]

    >>> qg = Q_Result ((1, 2, 3, 4, 2, 3, 4, 4,5))
    >>> qg.all        ()
    [1, 2, 3, 4, 2, 3, 4, 4, 5]
    >>> qg.group_by (lambda x : x).all ()
    [1, 2, 3, 4, 5]

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

"""

from   _TFL                       import TFL

import _TFL._Meta.Object
import _TFL.Decorator
import _TFL.Filter
from   _TFL.predicate             import first, uniq, uniq_p

import itertools
import operator

class _Attr_ (object) :
    """Wrapper for result of `.attr` method."""

    def __init__ (self, getter, value) :
        self._VALUE  = value
        p            = getter._name.split (".", 1)
        self._NAME   = p.pop              (0)
        self._REST   = p and p.pop        (0)
        self._IS_SUM = isinstance (getter, TFL.Q_Exp._Sum_) and getter
    # end def __init__

    def __eq__ (self, rhs) :
        if isinstance (rhs, _Attr_) :
            rhs = rhs._VALUE
        lhs = self._VALUE
        ### Compare `(x.__class__.__name__, x)` to avoid TypeError from some
        ### combinations, like `lhs == None`, `type (rhs) == datetime.date`
        return (lhs.__class__.__name__, lhs) == (rhs.__class__.__name__, rhs)
    # end def __eq__

    def __float__ (self) :
        return float (self._VALUE)
    # end def __float__

    def __getattr__ (self, name) :
        if name == self._NAME :
            if not self._REST :
                return self._VALUE
            return _Attr_ (getattr (Q_Result.Q, self._REST), self._VALUE)
        raise AttributeError (name)
    # end def __getattr__

    def __ge__ (self, rhs) :
        if isinstance (rhs, _Attr_) :
            rhs = rhs._VALUE
        lhs = self._VALUE
        ### Compare `(x.__class__.__name__, x)` to avoid TypeError for some
        ### combinations, like `lhs == None`, `type (rhs) == datetime.date`
        return (lhs.__class__.__name__, lhs) >= (rhs.__class__.__name__, rhs)
    # end def __ge__

    def __gt__ (self, rhs) :
        if isinstance (rhs, _Attr_) :
            rhs = rhs._VALUE
        lhs = self._VALUE
        ### Compare `(x.__class__.__name__, x)` to avoid TypeError for some
        ### combinations, like `lhs == None`, `type (rhs) == datetime.date`
        return (lhs.__class__.__name__, lhs) > (rhs.__class__.__name__, rhs)
    # end def __gt__

    def __hash__ (self) :
        lhs = self._VALUE
        return hash ((lhs.__class__.__name__, lhs))
    # end def __hash__

    def __int__ (self) :
        return int (self._VALUE)
    # end def __int__

    def __le__ (self, rhs) :
        if isinstance (rhs, _Attr_) :
            rhs = rhs._VALUE
        lhs = self._VALUE
        ### Compare `(x.__class__.__name__, x)` to avoid TypeError for some
        ### combinations, like `lhs == None`, `type (rhs) == datetime.date`
        return (lhs.__class__.__name__, lhs) <= (rhs.__class__.__name__, rhs)
    # end def __le__

    def __lt__ (self, rhs) :
        if isinstance (rhs, _Attr_) :
            rhs = rhs._VALUE
        lhs = self._VALUE
        ### Compare `(x.__class__.__name__, x)` to avoid TypeError for some
        ### combinations, like `lhs == None`, `type (rhs) == datetime.date`
        return (lhs.__class__.__name__, lhs) < (rhs.__class__.__name__, rhs)
    # end def __lt__

    def __ne__ (self, rhs) :
        if isinstance (rhs, _Attr_) :
            rhs = rhs._VALUE
        lhs = self._VALUE
        ### Compare `(x.__class__.__name__, x)` to avoid TypeError from some
        ### combinations, like `lhs == None`, `type (rhs) == datetime.date`
        return (lhs.__class__.__name__, lhs) != (rhs.__class__.__name__, rhs)
    # end def __ne__

    def __nonzero__ (self) :
        return bool (self._VALUE)
    # end def __nonzero__

    def __repr__ (self) :
        return repr (self._VALUE)
    # end def __repr__

    def __str__ (self) :
        return str (self._VALUE)
    # end def __str__

    def __unicode__ (self) :
        return unicode (self._VALUE)
    # end def __unicode__

# end class _Attr_

class _Attrs_Tuple_ (tuple) :
    """Wrapper for result of `.attrs` method."""

    _IS_SUM = None

    def __new__ (cls, getters, * args) :
        return super (_Attrs_Tuple_, cls).__new__ (cls, * args)
    # end def __new__

    def __init__ (self, getters, * args) :
        super (_Attrs_Tuple_, self).__init__ ()
        self._NAMES          = {}
        for i, g in enumerate (getters) :
            p                = g._name.split (".", 1)
            k                = p.pop         (0)
            self._NAMES [k]  = i, p and p.pop (0)
            if isinstance (g, TFL.Q_Exp._Sum_) :
                self._IS_SUM = g
                self._SUM_CO = i
    # end def __init__

    def __getattr__ (self, name) :
        idx, rest = self._NAMES.get (name, (-1, None))
        if rest is not None :
            result = self [idx]
            if rest :
                result = _Attr_ (getattr (Q_Result.Q, rest), result)
            return result
        raise AttributeError (name)
    # end def __getattr__

# end class _Attrs_Tuple_

class _Sum_Aggr_ (dict) :

    def __setitem__ (self, key, value) :
        if key in self :
            value += self [key]
        super (_Sum_Aggr_, self).__setitem__ (key, value)
    # end def __setitem__

# end class _Sum_Aggr_

class _Q_Filter_Distinct_ (TFL.Meta.Object) :

    def __init__ (self, criterion) :
        self.criterion = criterion
    # end def __init__

    def __call__ (self, iterable) :
        return uniq_p (iterable, self.criterion)
    # end def __call__

# end class _Q_Filter_Distinct_

class _Q_Result_ (TFL.Meta.Object) :

    Q = TFL.Attr_Query ()

    def __init__ (self, iterable, _distinct = False) :
        self.iterable  = iterable
        self._cache    = None
        self._distinct = _distinct
    # end def __init__

    def all (self) :
        return list (self)
    # end def all

    def attr (self, getter) :
        if isinstance (getter, basestring) :
            getter = getattr (self.Q, getter)
        return Q_Result \
            ((_Attr_ (getter, getter (r)) for r in self), self._distinct)
    # end def attr

    def attrs (self, * getters) :
        if not getters :
            raise TypeError \
                ( "%s.attrs() requires at least one argument"
                % self.__class__.__name__
                )
        def _g (getters) :
            Q = self.Q
            for getter in getters :
                if isinstance (getter, basestring) :
                    getter = getattr (Q, getter)
                yield getter
        getters = tuple (_g (getters))
        return Q_Result \
            ( (_Attrs_Tuple_ (getters, (g (r) for g in getters)) for r in self)
            , self._distinct
            )
    # end def attrs

    def count (self) :
        if self._cache is None :
            self._fill_cache ()
        return len (self._cache)
    # end def count

    def distinct (self, * criteria) :
        n = len (criteria)
        if n == 0 :
            _distinct = uniq
        else :
            if n == 1 :
                criterion = first (criteria)
            elif criteria :
                criterion = TFL.Filter_And  (* criteria)
            _distinct = _Q_Filter_Distinct_ (criterion)
        return _Q_Result_ (self, _distinct = _distinct)
    # end def distinct

    def filter (self, * criteria, ** kw) :
        if kw :
            criteria = list (criteria)
            Q = self.Q
            for k, v in kw.iteritems () :
                criteria.append (getattr (Q, k) == v)
            criteria = tuple (criteria)
        assert criteria
        if len (criteria) == 1 :
            criterion = first (criteria)
        else :
            criterion = TFL.Filter_And  (* criteria)
        return self._Q_Result_Filtered_ (self, criterion, self._distinct)
    # end def filter

    def first (self) :
        try :
            return first (self)
        except IndexError :
            return None
    # end def first

    def group_by (self, * criteria, ** kw) :
        if kw :
            criteria = list (criteria)
            Q = self.Q
            for k, v in kw.iteritems () :
                criteria.append (getattr (Q, k) == v)
            criteria = tuple (criteria)
        assert criteria
        if len (criteria) == 1 :
            criterion = first (criteria)
        else :
            criterion = TFL.Filter_And  (* criteria)
        return self._Q_Result_Group_By_ (self, criterion, self._distinct)
    # end def group_by

    def limit (self, limit) :
        return self._Q_Result_Limited_ (self, limit, self._distinct)
    # end def limit

    def offset (self, offset) :
        return self._Q_Result_Offset_ (self, offset, self._distinct)
    # end def offset

    def one (self) :
        result = first (self)
        if len (self._cache) > 1 :
            raise IndexError \
                ("Query result contains %s entries" % len (self._cache))
        return result
    # end def one

    def order_by (self, criterion) :
        return self._Q_Result_Ordered_ (self, criterion, self._distinct)
    # end def order_by

    def set (self, * args, ** kw) :
        def _g (args) :
            Q = self.Q
            for k, v in args :
                if isinstance (k, basestring) :
                    k = getattr (Q, k)
                yield k, v
        args = tuple (_g (args))
        for r in self :
            for k, v in kw.iteritems () :
                setattr (r, k, v)
            for k, v in args :
                k.SET (r, v)
    # end def set

    def slice (self, start, stop = None) :
        return self._Q_Result_Sliced_ (self, start, stop, self._distinct)
    # end def slice

    def _fill_cache (self) :
        iterable = self.iterable
        if self._distinct :
            iterable = self._distinct (iterable)
        self._cache = list (iterable)
    # end def _fill_cache

    def __getitem__ (self, key) :
        if isinstance (key, slice) :
            return self.slice (key.start, key.stop)
        if self._cache is None :
            self._fill_cache ()
        return self._cache [key]
    # end def __getitem__

    def __getslice__ (self, start, stop) :
        return self.slice (start, stop)
    # end def __getslice__

    def __iter__ (self) :
        if self._cache is None :
            self._fill_cache ()
        return iter (self._cache)
    # end def __iter__

    def __nonzero__ (self) :
        if self._cache is None :
            self._fill_cache ()
        return bool (self._cache)
    # end def __nonzero__

# end class _Q_Result_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Filtered_ (_Q_Result_) :

    def __init__ (self, iterable, criterion, _distinct = False) :
        self.__super.__init__ (iterable, _distinct = _distinct)
        self._criterion = criterion
    # end def __init__

    def _fill_cache (self) :
        pred     = self._criterion
        filtered = (x for x in self.iterable if pred (x))
        if self._distinct and not self.iterable._distinct :
            filtered = self._distinct (filtered)
        self._cache = list (filtered)
    # end def _fill_cache

# end class _Q_Result_Filtered_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Group_By_ (_Q_Result_Filtered_) :

    def _fill_cache (self) :
        pred        = self._criterion
        result      = dict        ()
        sums        = _Sum_Aggr_  ()
        sum_col     = None
        for row in self.iterable :
            key    = pred (row)
            is_sum = getattr (row, "_IS_SUM", False)
            if is_sum :
                sums [key] = is_sum (row)
                sum_col    = getattr (row, "_SUM_CO", None)
            result [key]   = row
        if sums :
            sum_fixed      = []
            for key, row in result.iteritems () :
                if sum_col is None :
                    sum_fixed.append (sums [key])
                else :
                    sum_fixed.append \
                        (row [:sum_col] + (sums [key], ) + row [sum_col + 1:])
            result         = sum_fixed
        else :
            result         = result.itervalues ()
        if self._distinct and not self.iterable._distinct :
            result  = self._distinct (result)
        self._cache = list (result)
    # end def _fill_cache

# end class _Q_Result_Group_By_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Limited_ (_Q_Result_) :

    def __init__ (self, iterable, limit, _distinct = False) :
        self.__super.__init__ (iterable, _distinct = _distinct)
        self._limit = limit
    # end def __init__

    def _fill_cache (self) :
        iterable = self.iterable
        if self._distinct and not iterable._distinct :
            iterable = self._distinct (iterable)
        self._cache = list (itertools.islice (iterable, None, self._limit))
    # end def _fill_cache

# end class _Q_Result_Limited_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Offset_ (_Q_Result_) :

    def __init__ (self, iterable, offset, _distinct = False) :
        self.__super.__init__ (iterable, _distinct = _distinct)
        self._offset = offset
    # end def __init__

    def _fill_cache (self) :
        iterable = self.iterable
        if self._distinct and not iterable._distinct :
            iterable = self._distinct (iterable)
        self._cache = list (itertools.islice (iterable, self._offset, None))
    # end def _fill_cache

# end class _Q_Result_Offset_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Ordered_ (_Q_Result_) :

    def __init__ (self, iterable, criterion, _distinct = False) :
        self.__super.__init__ (iterable, _distinct = _distinct)
        self._criterion = criterion
    # end def __init__

    def _fill_cache (self) :
        iterable = self.iterable
        if self._distinct and not iterable._distinct :
            iterable = self._distinct (iterable)
        self._cache = sorted (iterable, key = self._criterion)
    # end def _fill_cache

# end class _Q_Result_Ordered_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Sliced_ (_Q_Result_) :

    def __init__ (self, iterable, start, stop, _distinct = False) :
        self.__super.__init__ (iterable, _distinct = _distinct)
        self._start = start
        self._stop  = stop
    # end def __init__

    def _fill_cache (self) :
        iterable = self.iterable
        if self._distinct and not iterable._distinct :
            iterable = self._distinct (iterable)
        self._cache = list (itertools.islice (iterable, self._start, self._stop))
    # end def _fill_cache

# end class _Q_Result_Sliced_

class Q_Result (_Q_Result_) :

    def __init__ (self, iterable, _distinct = False) :
        self.iterable  = iterable
        self._distinct = _distinct
        try :
            len (iterable)
        except TypeError :
            self._cache = None
        else :
            if _distinct and not getattr (iterable, "_distinct", False) :
                iterable = list (_distinct (iterable))
            self._cache = iterable
    # end def __init__

# end class Q_Result

class Q_Result_Composite (_Q_Result_) :

    @TFL.Decorator
    def super_ordered (q) :
        def _ (self, * args, ** kw) :
            name = q.__name__
            result = getattr (self.__super, name) (* args, ** kw)
            if self._order_by :
                result = result.order_by (self._order_by)
            return result
        return _
    # end def super_ordered

    @TFL.Decorator
    def super_ordered_delegate (q) :
        def _ (self, * args, ** kw) :
            name   = q.__name__
            result = self.__class__ \
                ( [getattr (sq, name) (* args, ** kw) for sq in self.queries]
                , _distinct = self._distinct
                )
            result = getattr (result.__super, name) (* args, ** kw)
            if self._order_by :
                result = result.order_by (self._order_by)
            return result
        return _
    # end def super_ordered_delegate

    def __init__ (self, queries, order_by = None, _distinct = False) :
        self.queries   = queries
        self._order_by = order_by
        self.__super.__init__ \
            (itertools.chain (* queries), _distinct = _distinct)
    # end def __init__

    @super_ordered_delegate
    def distinct (self, * criteria) :
        pass
    # end def distinct

    def filter (self, * criteria, ** kw) :
        return self.__class__ \
            ( [q.filter (* criteria, ** kw) for q in self.queries]
            , self._order_by, self._distinct
            )
    # end def filter

    @super_ordered_delegate
    def limit (self, limit) :
        pass
    # end def limit

    @super_ordered
    def offset (self, offset) :
        pass
    # end def offset

    def order_by (self, criterion) :
        self._order_by = criterion
        return self
    # end def order_by

    @super_ordered
    def slice (self, start, stop = None) :
        pass
    # end def slice

    def _fill_cache (self) :
        if self._order_by is not None :
            iterable = self.iterable
            if self._distinct :
                iterable = self._distinct (iterable)
            self._cache = sorted (iterable, key = self._order_by)
        else :
            self.__super._fill_cache ()
    # end def _fill_cache

    def __nonzero__ (self) :
        return any (self.queries)
    # end def __nonzero__

# end class Q_Result_Composite

if __name__ != "__main__" :
    TFL._Export ("*", "_Q_Result_")
### __END__ TFL.Q_Result

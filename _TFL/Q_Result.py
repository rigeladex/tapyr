# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

"""
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
>>> qq.distinct (lambda x : x % 2).all ()
[0, 1]
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
>>> qc [5:15].all ()
[51, 61, 71, 81, 91, 10, 30, 50, 70, 90]
>>> qc.limit (5).all ()
[1, 11, 21, 31, 41]
>>> qc.distinct (lambda x : x % 10).limit (3).all ()
[1, 10, 4]
>>> qc.limit (15).distinct (lambda x : x % 10).all ()
[1, 10]

"""

from   _TFL                     import TFL

import _TFL._Meta.Object
import _TFL.Decorator
import _TFL.Filter

from   _TFL.predicate           import first, uniq, uniq_p

import itertools
import operator

class _Q_Result_ (TFL.Meta.Object) :

    Q = TFL.Attr_Query ()

    def __init__ (self, iterable) :
        self.iterable = iterable
        self._cache   = None
    # end def __init__

    def all (self) :
        return list (self)
    # end def all

    def attr (self, getter) :
        if isinstance (getter, basestring) :
            getter = getattr (self.Q, getter)
        for r in self :
            yield getter (r)
    # end def attr

    def attrs (self, * getters) :
        if not getters :
            raise TypeError \
                ( "%s.attrs() requires at least one argument"
                % self.__class__.__name
                )
        def _g (getters) :
            Q = self.Q
            for getter in getters :
                if isinstance (getter, basestring) :
                    getter = getattr (Q, getter)
                yield getter
        getters = tuple (_g (getters))
        for r in self :
            yield tuple (g (r) for g in getters)
    # end def attrs

    def count (self) :
        if self._cache is None :
            self._fill_cache ()
        return len (self._cache)
    # end def count

    def distinct (self, * criteria) :
        criterion = None
        if len (criteria) == 1 :
            criterion = first (criteria)
        elif criteria :
            criterion = TFL.Filter_And  (* criteria)
        return self._Q_Result_Distinct_ (self, criterion)
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
        return self._Q_Result_Filtered_ (self, criterion)
    # end def filter

    def first (self) :
        try :
            return first (self)
        except IndexError :
            return None
    # end def first

    def limit (self, limit) :
        return self._Q_Result_Limited_ (self, limit)
    # end def limit

    def offset (self, offset) :
        return self._Q_Result_Offset_ (self, offset)
    # end def offset

    def one (self) :
        result = first (self)
        if len (self._cache) > 1 :
            raise IndexError\
                ("Query result contains %s entries" % len (self._cache))
        return result
    # end def one

    def order_by (self, criterion) :
        return self._Q_Result_Ordered_ (self, criterion)
    # end def order_by

    def set (self, * args, ** kw) :
        return self._set (dict (args, ** kw))
    # end def set

    def slice (self, start, stop = None) :
        return self._Q_Result_Sliced_ (self, start, stop)
    # end def slice

    def _fill_cache (self) :
        self._cache = list (self.iterable)
    # end def _fill_cache

    def _set (self, kw) :
        for r in self :
            for k, v in kw.iteritems () :
                setattr (r, k, v)
    # end def _set

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
class _Q_Result_Distinct_ (_Q_Result_) :

    def __init__ (self, iterable, criterion) :
        self.__super.__init__ (iterable)
        self._criterion = criterion
    # end def __init__

    def _fill_cache (self) :
        if self._criterion is None :
            distinct = uniq   (self.iterable)
        else :
            distinct = uniq_p (self.iterable, self._criterion)
        self._cache  = list (distinct)
    # end def _fill_cache

# end class _Q_Result_Distinct_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Filtered_ (_Q_Result_) :

    def __init__ (self, iterable, criterion) :
        self.__super.__init__ (iterable)
        self._criterion = criterion
    # end def __init__

    def _fill_cache (self) :
        pred  = self._criterion
        self._cache = [x for x in self.iterable if pred (x)]
    # end def _fill_cache

# end class _Q_Result_Filtered_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Limited_ (_Q_Result_) :

    def __init__ (self, iterable, limit) :
        self.__super.__init__ (iterable)
        self._limit = limit
    # end def __init__

    def _fill_cache (self) :
        self._cache = self.iterable.all () [:self._limit]
    # end def _fill_cache

# end class _Q_Result_Limited_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Offset_ (_Q_Result_) :

    def __init__ (self, iterable, offset) :
        self.__super.__init__ (iterable)
        self._offset = offset
    # end def __init__

    def _fill_cache (self) :
        self._cache = self.iterable.all () [self._offset:]
    # end def _fill_cache

# end class _Q_Result_Offset_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Ordered_ (_Q_Result_) :

    def __init__ (self, iterable, criterion) :
        self.__super.__init__ (iterable)
        self._criterion = criterion
    # end def __init__

    def _fill_cache (self) :
        self._cache = sorted (self.iterable, key = self._criterion)
    # end def _fill_cache

# end class _Q_Result_Ordered_

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Sliced_ (_Q_Result_) :

    def __init__ (self, iterable, start, stop) :
        self.__super.__init__ (iterable)
        self._start = start
        self._stop   = stop
    # end def __init__

    def _fill_cache (self) :
        self._cache = self.iterable.all () [self._start:self._stop]
    # end def _fill_cache

# end class _Q_Result_Sliced_

class Q_Result (_Q_Result_) :

    def __init__ (self, iterable) :
        self.iterable = iterable
        try :
            len (iterable)
        except TypeError :
            self._cache = None
        else :
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
                ([getattr (sq, name) (* args, ** kw) for sq in self.queries])
            result = getattr (result.__super, name) (* args, ** kw)
            if self._order_by :
                result = result.order_by (self._order_by)
            return result
        return _
    # end def super_ordered_delegate

    def __init__ (self, queries, order_by = None) :
        self.queries   = queries
        self._order_by = order_by
        self.__super.__init__ (itertools.chain (* queries))
    # end def __init__

    @super_ordered_delegate
    def distinct (self, * criteria) :
        pass
    # end def distinct

    def filter (self, * criteria, ** kw) :
        return self.__class__ \
            ( [q.filter (* criteria, ** kw) for q in self.queries]
            , self._order_by
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
        if self._order_by :
            self._cache = sorted (self.iterable, key = self._order_by)
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

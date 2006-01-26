# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001-2003 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Ordered_Set
#
# Purpose
#    Ordered set of objects
#
# Revision Dates
#    16-Mar-2001 (CT)  Creation (factored from NO_List)
#    16-Mar-2001 (CT)  Aliase `pos', `contains', and `__contains__' added
#    16-Mar-2001 (CT)  `update' added
#    21-Mar-2001 (CT)  `_check_value' added to prevent duplicate values in
#                      Ordered_Set
#    16-Aug-2001 (CT)  `update` changed to overwrite existing values
#    11-Jun-2003 (CT)  s/== None/is None/
#    20-Nov-2003 (CT)  Minor face lifts
#    21-Nov-2003 (MG)  `__radd__` fixed (parameter rhs also a list)
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#    11-Nov-2004 (CED) `remove` implemented
#    11-Nov-2004 (CED) `remove` removed
#    27-Feb-2005 (MG)  `dusort` added
#     9-Jun-2005 (CT)  Arguments `key` and `reverse` added to `sort`
#    21-Jan-2006 (MG)  Moved into `TFL` package
#    ««revision-date»»···
#--

from  UserList      import UserList
from _TFL.predicate import *

class Duplicate_Key (KeyError) : pass

class Ordered_Set (UserList) :
    """Ordered set of objects. The objects are stored in a python list but
       additionally kept in a dictionary to allow fast access to the position
       in the list.
    """

    def __init__ (self, * elements) :
        UserList.__init__ (self)
        self.body       = self.data ### alias name for `self.data'
        self.index_dict = {}
        map (self.append, un_nested (elements))
    # end def __init__

    def append (self, value) :
        self._check_value (value)
        self.index_dict  [value] = len (self.data)
        self.data.append (value)
    # end def append

    def copy (self) :
        return self.__class__ (* self.data)
    # end def copy

    def extend (self, list) :
        map (self.append, tuple (list))
    # end def extend

    def insert (self, index, value, delta = 0) :
        self._check_value (value)
        if index is None :
            index = len (self.data)
        if not isinstance (index, int) :
            i = self.index_dict [index] + delta
        else :
            i = index                   + delta
        self.data [i:i] = [value]
        self._fix (i)
    # end def insert

    def get (self, index, default = None) :
        try :
            return self.__getitem__ (index)
        except (KeyError, IndexError) :
            return default
    # end def get

    def n_index (self, name) :
        return self.index_dict [name]
    # end def n_index

    pos = n_index

    def has_key (self, name) :
        return self.index_dict.has_key (name)
    # end def has_key

    contains = __contains__ = has_key

    def keys (self) :
        return self.index_dict.keys ()
    # end def keys

    def reverse (self) :
        self.data.reverse ()
        self._fix         (0)
    # end def reverse

    def remove (self, e) :
        del self.data       [self.index_dict [e]]
        del self.index_dict [e]
        self._fix (0)
    # end def remove

    def dusort (self, decorator = None) :
        self.data = dusort (self.data, decorator)
        self._fix          (0)
    # end def dusort

    def sort (self, cmp = cmp, key = None, reverse = False) :
        self.data.sort (cmp, key = key, reverse = reverse)
        self._fix      (0)
    # end def sort

    def update (self, other) :
        for o in other :
            if not self.has_key (o) :
                self.append (o)
            else :
                self.data [self.pos (o)] = o
    # end def update

    def _fix (self, from_index) :
        map ( lambda (e, i), d = self.index_dict : d.update ({e : i})
            , paired ( self.data [from_index:]
                     , range     (from_index, len (self.data))
                     )
            )
    # end def _fix

    def _indices (self, index) :
        if not isinstance (index, (int, long)) :
            i = self.index_dict [index]
            n = index
        else :
            if index < len (self.data) :
                i = index
                n = self.data [i]
            else :
                i = len (self.data)
                n = None
        return i, n
    # end def _indices

    def _check_value (self, value) :
        if self.has_key (value) :
            raise Duplicate_Key, (value, self.data [self.index_dict [value]])
    # end def _check_value

    def __getitem__ (self, index) :
        i, n = self._indices (index)
        return self.data [i]
    # end def __getitem__

    def __setitem__ (self, index, value) :
        i, n = self._indices (index)
        del self.index_dict  [n]
        self.index_dict [value] = i
        self.data       [i]     = value
    # end def __setitem__

    def __delitem__ (self, index) :
        i, n = self._indices (index)
        del self.index_dict  [n]
        del self.data        [i]
        self._fix (i)
    # end def __delitem__

    def __delslice__ (self, i, j) :
        h, n = self._indices (i)
        t, n = self._indices (j)
        if h - t < 0 :
            for index in range (h, t) :
                i, n = self._indices (h)
                del self.data        [i]
                del self.index_dict  [n]
            self._fix (h)
    # end def __delslice__

    def __getslice__ (self, i, j) :
        l, n   = self._indices  (i)
        u, n   = self._indices  (j)
        result = self.__class__ ()
        for index in range (l, u) :
            result.append (self.__getitem__ (index))
        return result
    # end def __getslice__

    def __add__ (self, rhs) :
        if isinstance (rhs, UserList) : rhs = rhs.data
        return self.__class__ (* (self.data + list (rhs)))
    # end def __add__

    def __radd__ (self, rhs) :
        return self.__class__ (* (list (rhs) + self.data))
    # end def __radd__

# end class Ordered_Set

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export ("*")
### __END__ TFL.Ordered_Set

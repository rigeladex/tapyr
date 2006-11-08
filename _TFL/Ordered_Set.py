# -*- coding: iso-8859-1 -*-
# Copyright (C) 2001-2006 Mag. Christian Tanzer. All rights reserved
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
#     8-Nov-2006 (PGO) Inheritance changed
#    ««revision-date»»···
#--

from _TFL import TFL

import _TFL._Meta.M_Class

class Duplicate_Key_Error (KeyError) : pass

class Ordered_Set (list) :
    """Ordered set of objects. The objects are stored in a python list but
       additionally kept in a dictionary to allow fast access to the position
       in the list.
    """
    __metaclass__        = TFL.Meta.M_Class
    _reverse_mapping_cls = dict
    _cannot_hold         = int

    def __init__ (self, values = None) :
        self.__super.__init__ ()
        self.index_dict = self._reverse_mapping_cls ()
        if values is not None :
            self.extend (values)
    # end def __init__

    def append (self, value) :
        self._check_value (value)
        self.index_dict [value] = len (self)
        self.__super.append (value)
    # end def append

    def copy (self) :
        return self.__class__ (self)
    # end def copy

    def count (self, value) :
        return (value in self) and 1 or 0
    # end def count

    def extend (self, values) :
        for value in values :
            self.append (value)
    # end def extend

    def get (self, index, default = None) :
        try :
            return self [index]
        except (KeyError, IndexError) :
            return default
    # end def get

    def index (self, value, start = None, stop = None) :
        pos = self.index_dict.get (value)
        if (   pos is not None
           and (start is None or stop is None or start <= pos <= stop)
           ) :
            return pos
        raise ValueError ("%s not in %s" % (value, self.__class__.__name__))
    # end def index
    n_index = pos = index

    def insert (self, index, value, offset = 0) :
        self._check_value (value)
        if index is None :
            index = len (self)
        elif not isinstance (index, int) :
            index = self.index_dict [index]
        index += offset
        self.index_dict [value] = index
        self.__super.insert (index, value)
        self._fix (index)
    # end def insert

    def pop (self, index = None) :
        value = self.__super.pop (index)
        del self.index_dict [value]
        if index is not None :
            self._fix (index)
        return value
    # end def pop

    def remove (self, value) :
        assert not isinstance (value, int), "use `del []` instead"
        index = self.index_dict [value]
        del self [index]
    # end def remove

    def reverse (self) :
        self.__super.reverse ()
        self._fix ()
    # end def reverse

    def sort (self, cmp = None, key = None, reverse = False) :
        self.__super.sort (cmp = cmp, key = key, reverse = reverse)
        self._fix ()
    # end def sort

    def update (self, values) :
        for value in values :
            if value in self :
                index = self.index (value)
                del self [index]
                self.insert (index, value)
            else :
                self.append (value)
    # end def update

    def _check_value_type (self, value) :
        assert not isinstance (value, self._cannot_hold), \
            ( "%s cannot hold %s"
            % (self.__class__.__name__, value.__class__.__name__)
            )
    # end def _check_value_type

    def _check_value_duplicate (self, value) :
        if value in self :
            raise Duplicate_Key_Error \
                (value.name, value, self [self.index (value)])
    # end def _check_value_duplicate

    def _check_value (self, value) :
        self._check_value_type      (value)
        self._check_value_duplicate (value)
    # end def _check_value

    def _fix (self, start = 0) :
        for pos in xrange (start, len (self)) :
            value = self [pos]
            self.index_dict [value] = pos
    # end def _fix

    def __add__ (self, other) :
        res = self.__class__ (self)
        res.extend (other)
        return res
    # end def __add__

    def __contains__ (self, value) :
        return self.index_dict.has_key (value)
    # end def __contains__
    contains = __contains__

    def __delitem__ (self, index) :
        assert isinstance (index, int), "use `remove` instead"
        value = self [index]
        self.__super.__delitem__ (index)
        del self.index_dict [value]
        self._fix (index)
    # end def __delitem__

    def __delslice__ (self, i, j) :
        raise NotImplementedError
    # end def __delslice__

    def __getslice__ (self, i, j) :
        return self.__class__ (self.__super.__getslice__ (i, j))
    # end def __getslice__

    def __radd__ (self, other) :
        res = self.__class__ (other)
        res.extend (self)
        return res
    # end def __radd__

    def __setitem__ (self, index, value) :
        self._check_value (value)
        old_value = self [index]
        del self.index_dict [old_value]
        self.index_dict [value] = index
        self.__super.__setitem__ (index, value)
    # end def __setitem__

    def __setslice__ (self, i, j, value) :
        raise NotImplementedError
    # end def __setslice__

# end class Ordered_Set

class Immutable_Ordered_Set (Ordered_Set) :
    """Immutable ordered set of objects. As opposed to the mutable version of
       the ordered set, it can also store values of the type that is used
       as an index.
    """
    _cannot_hold = ()

    def __init__ (self, values = None) :
        self.__super.__init__ (values)
        self.append = self._not_supported
        self.extend = self._not_supported
    # end def __init__

    def _not_supported (self, * args, ** kw) :
        raise TypeError \
            ("%s doesn't support modification" % self.__class__.__name__)
    # end def _not_supported

    __delitem__      = _not_supported
    __delslice__     = _not_supported
    insert           = _not_supported
    pop              = _not_supported
    remove           = _not_supported
    reverse          = _not_supported
    sort             = _not_supported
# end class Immutable_Ordered_Set

if __name__ != "__main__" :
    from _TFL import TFL
    TFL._Export ("*")
### __END__ TFL.Ordered_Set

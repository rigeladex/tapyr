# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.Attr.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Attr.Coll
#
# Purpose
#    Wrapper classes around Python lists/sets... to hold collection of
#    attributes
#
# Revision Dates
#     3-Sep-2010 (CT) Creation
#     4-Sep-2010 (CT) Creation continued
#    ««revision-date»»···
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _TFL._Meta.M_Class
import _TFL.Decorator

class M_Coll (TFL.Meta.M_Class) :

    _state_changers = ()

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        for mn in cls._state_changers :
            m = getattr (cls, mn, None)
            if m is not None :
                setattr (cls, mn, cls._override (m))
    # end def __init__

    @staticmethod
    @TFL.Decorator
    def _override (method) :
        def _ (self, * args, ** kw) :
            result = method (self, * args, ** kw)
            self.record_attr_change ()
            return result
        return _
    # end def _override

# end class M_Coll

class _Mixin_ (object) :

    __metaclass__   = M_Coll

    attr_name       = None
    owner           = None
    _attr_man       = property (lambda s : s.owner and s.owner._attr_man)

    def copy (self) :
        return self.__class__ (self)
    # end def copy

    @property
    def owner_attr (self) :
        """Return the attribute (kind property) of the `owner` object that
           holds `self`.
        """
        if self.owner and self.attr_name :
            return getattr (self.owner.__class__, self.attr_name)
    # end def owner_attr

    def record_attr_change (self, ** kw) :
        ### communicate change of `self` to `self.owner`
        if self.owner is not None :
            self.owner.record_attr_change ({self.attr_name : self})
    # end def record_attr_change

    def __getstate__ (self) :
        return self.P_Type (self)
    # end def __getstate__

# end class _Mixin_

class _Mixin_C_ (_Mixin_) :

    __metaclass__   = M_Coll

    is_primary      = False

    def __init__ (self, values = ()) :
        self.owner = None
        self.__super.__init__ (self._update_owner (v) for v in values)
    # end def __init__

    def _update_owner (self, value) :
        if value.owner is not None and value.owner is not self :
            value = value.copy ()
        value.owner     = self
        value.attr_name = self.attr_name
        return value
    # end def _update_owner

# end class _Mixin_C_

class List (_Mixin_, list) :
    """List of attribute values"""

    P_Type          = list
    _state_changers = \
        ( "__delitem__", "__delslice__"
        , "__iadd__", "__imul__"
        , "__setitem__", "__setslice__"
        , "append", "extend", "insert", "pop", "remove", "reverse", "sort"
        )

# end class List

class List_C (_Mixin_C_, List) :
    """List of composite attributes"""

    def append (self, value) :
        return self.__super.append (self._update_owner (value))
    # end def append

    def extend (self, values) :
        return self.__super.extend (self._update_owner (v) for v in values)
    # end def extend

    def insert (self, index, value) :
        return self.__super.insert (index, self._update_owner (value))
    # end def insert

    def __iadd__ (self, rhs) :
        return self.__super.__iadd__ (self._update_owner (v) for v in rhs)
    # end def __iadd__

    def __setitem__ (self, key, value) :
        return self.__super.__setitem__ (key, self._update_owner (value))
    # end def __setitem__

    def __setslice__ (self, i, j, seq) :
        return self.__super.__setslice__ \
            (i, j, (self._update_owner (v) for v in seq))
    # end def __setslice__

# end class List_C

class Set (_Mixin_, set) :
    """Set of attribute values"""

    P_Type          = set
    _state_changers = \
        ( "__iand__", "__ior__", "__isub__", "__ixor__"
        , "add", "clear", "difference_update", "discard"
        , "intersection_update", "pop", "remove"
        , "symmetric_difference_update", "update"
        )

# end class Set

class Set_C (_Mixin_C_, Set) :
    """Set of composite attributes."""

    def add (self, value) :
        return self.__super.add (self._update_owner (value))
    # end def add

    def symmetric_difference_update (self, rhs) :
        return self.__super.symmetric_difference_update \
            (self._update_owner (v) for v in rhs if v not in self)
    # end def symmetric_difference_update

    def update (self, rhs) :
        return self.__super.update (self._update_owner (v) for v in rhs)
    # end def update

    def __ior__ (self, rhs) :
        return self.__super.__ior__ (self._update_owner (v) for v in rhs)
    # end def __ior__

    def __ixor__ (self, rhs) :
        return self.__super.__ixor__ \
            (self._update_owner (v) for v in rhs if v not in self)
    # end def __ixor__

# end class Set_C

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Coll

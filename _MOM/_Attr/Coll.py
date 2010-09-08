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
#     6-Sep-2010 (CT) Creation continued..
#     7-Sep-2010 (CT) `Table` added
#     7-Sep-2010 (CT) `old` added to `_override` and passed to
#                     `record_attr_change`
#     8-Sep-2010 (CT) `M_Coll.__init__` changed to apply `_override` only once
#    ��revision-date�����
#--

from   __future__            import absolute_import, division
from   __future__            import print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _TFL._Meta.M_Class
import _TFL.Decorator

class M_Coll (TFL.Meta.M_Class) :

    _state_changers = ()
    Table           = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.P_Type is not None :
            if cls.P_Type not in cls.Table :
                cls.Table [cls.P_Type] = cls
                for mn in cls._state_changers :
                    m = getattr (cls, mn, None)
                    if m is not None :
                        setattr (cls, mn, cls._override (m))
            else :
                ### sub-class overrriding `attr_name`
                assert cls.Table [cls.P_Type] is bases [0]
    # end def __init__

    @staticmethod
    @TFL.Decorator
    def _override (method) :
        def _ (self, * args, ** kw) :
            old    = self.copy ()
            result = method (self, * args, ** kw)
            if old != self :
                self.record_attr_change (old)
            return result
        return _
    # end def _override

# end class M_Coll

class _Mixin_ (object) :

    __metaclass__   = M_Coll
    P_Type          = None

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

    def record_attr_change (self, old) :
        ### communicate change of `self` to `self.owner`
        if self.owner is not None :
            self.owner.record_attr_change ({self.attr_name : self.P_Type (old)})
    # end def record_attr_change

# end class _Mixin_

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

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Coll
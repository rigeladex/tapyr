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

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        result.owner = None
        return result
    # end def __call__

    @staticmethod
    @TFL.Decorator
    def _override (method) :
        def _ (self, * args, ** kw) :
            result = method (self, * args, ** kw)
            if self.owner is not None :
                ### communicate change of `self` to `self.owner`
                self.owner.set (** {self.attr_name : self})
            return result
        return _
    # end def _override

# end class M_Coll

class Dict (dict) :
    """Dict of attribute values"""

    __metaclass__   = M_Coll
    _state_changers = \
        ( "__delitem__", "__setitem__"
        , "clear", "pop", "popitem", "setdefault", "update"
        )

# end class Dict

class List (list) :
    """List of attribute values"""

    __metaclass__   = M_Coll
    _state_changers = \
        ( "__delitem__", "__delslice__"
        , "__iadd__", "__imul__"
        , "__setitem__", "__setslice__"
        , "append", "extend", "insert", "pop", "remove", "reverse", "sort"
        )

# end class List

class Set (set) :
    """Set of attribute values"""

    __metaclass__   = M_Coll
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

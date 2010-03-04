# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Attr.Spec
#
# Purpose
#    Attribute specification for essential entities of the MOM meta object model
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM.Attr.Spec)
#     2-Oct-2009 (CT) `_epk_attr` added
#     6-Oct-2009 (CT) `_epk_attr` removed (use `obj.primary` instead)
#     6-Oct-2009 (CT) Call of `_setup_alias` moved from `_setup_prop` to
#                     (newly redefined) `_add_prop`
#     8-Oct-2009 (CT) `sort` for `user_attr` added
#    13-Oct-2009 (CT) Don't append primary attributes to `_user_attr`
#    14-Oct-2009 (CT) `epk_sig` added
#    22-Oct-2009 (CT) `_effective_prop_kind_mixins` redefined to add
#                     `_Raw_Value_Mixin_` if necessary
#    22-Oct-2009 (CT) `_effective_prop_kind_mixins` changed to ignore
#                     electric kinds and to put `_Raw_Value_Mixin_` at end
#    22-Dec-2009 (CT) `__init__` changed to not set `epk_sig`
#     4-Feb-2010 (CT) Argument `e_type` added to `_effective_prop_kind_mixins`
#     4-Feb-2010 (CT) `_effective_prop_kind_mixins` changed to add
#                     `_Nested_Mixin_` to attributes of `An_Entity`
#    24-Feb-2010 (CT) `_add_prop` changed to replace `_A_Object_.Class` with
#                     app-type specific e-type
#     4-Mar-2010 (CT) `_add_prop` changed to not change `attr.Class` of
#                     `_A_Object_` (app_type doesn't have etypes yet)
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr.Type
import _MOM._Attr.Kind
import _MOM._Meta.M_Attr_Spec
import _MOM._Prop.Spec

import _TFL._Meta.Property
import _TFL.Alias_Dict
import _TFL.Sorted_By

from   _TFL.predicate        import callable, uniq

class Spec (MOM.Prop.Spec) :
    """Attribute specification for MOM entities (objects and links).

       A :class:`~_MOM.Entity.Entity` class contains a descendent of `Spec`
       with declarations for all attributes (which are descendents of
       :class:`~_MOM._Attr.Type.A_Attr_Type`) provided by that class.

       :class:`MOM.Meta.M_E_Type<_MOM._Meta.M_Entity.M_E_Type>` instantiates
       the `Spec`: this results in the assignment of all attribute
       properties, i.e., for all attributes `attr` defined in the `Spec` a
       property named by `attr.name` and instantiated as ::

           attr.kind (attr)

       is added to the `E_Type`.
    """

    __metaclass__   = MOM.Meta.M_Attr_Spec

    _Prop_Pkg       = MOM.Attr
    _Prop_Spec_Name = "_Attributes"
    _prop_dict_cls  = TFL.Alias_Dict
    _prop_dict      = TFL.Meta.Alias_Property ("_attr_dict")
    _prop_kind      = TFL.Meta.Alias_Property ("_attr_kind")

    def __init__ (self, e_type) :
        self._syncable    = []
        self._user_attr   = []
        self.__super.__init__ (e_type)
        e_type.attributes = self._prop_dict
        e_type.user_attr  = self._user_attr
        e_type.user_attr.sort (key = TFL.Sorted_By ("rank", "name"))
        self._setup_dependent_attrs ()
    # end def __init__

    def _add_prop (self, e_type, name, prop_type) :
        prop = self.__super._add_prop (e_type, name, prop_type)
        if prop and name != prop.name :
            self._setup_alias (e_type, name, prop.name)
        attr = prop.attr
        return prop
    # end def _add_prop

    def _effective_prop_kind_mixins (self, name, kind, prop_type, e_type) :
        result = self.__super._effective_prop_kind_mixins \
            (name, kind, prop_type, e_type)
        if prop_type.needs_raw_value and not kind.electric :
            result += (MOM.Attr._Raw_Value_Mixin_, )
        if prop_type.auto_up_depends :
            result += (MOM.Attr._Auto_Update_Mixin_, )
        if issubclass (e_type, MOM.An_Entity) :
            result = (MOM.Attr._Nested_Mixin_, ) + result
        return tuple (uniq (result))
    # end def _effective_prop_kind_mixins

    def _setup_alias (self, e_type, alias_name, real_name) :
        setattr (e_type, alias_name, TFL.Meta.Alias_Property (real_name))
        self._prop_dict.add_alias (alias_name, real_name)
    # end def _setup_alias

    def _setup_dependent_attrs (self) :
        attr_dict = self._attr_dict
        for a in attr_dict.itervalues () :
            for d in a.attr.auto_up_depends :
                attr_dict [d].dependent_attrs.add (a)
    # end def _setup_dependent_attrs

    def _setup_prop (self, e_type, name, kind, prop) :
        self.__super._setup_prop (e_type, name, kind, prop)
        if not (prop.electric or prop.is_primary) :
            self._user_attr.append (prop)
        if callable (prop.sync) :
            self._syncable.append (prop)
    # end def _setup_prop

# end class Spec

__doc__ = """
Class `MOM.Attr.Spec`
=====================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: Spec

"""

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Spec

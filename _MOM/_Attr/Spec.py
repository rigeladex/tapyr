# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
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
#    23-Mar-2010 (CT) `_add_prop` changed to pass names in `renameds` to
#                     `_setup_alias`
#     9-Apr-2010 (CT) `_effective_prop_kind_mixins` changed to filter
#                     `Sticky_Mixin`, if `Computed_Mixin` is in `result`
#    24-Jun-2010 (CT) `db_attr` added
#     9-Dec-2010 (CT) `_effective_prop_kind_mixins` changed to use
#                     `_Auto_Update_Lazy_Mixin_` if `Computed_Set_Mixin`
#    15-Sep-2011 (CT) s/_setup_dependent_attrs/_setup_attrs/
#    15-Sep-2011 (CT) `_setup_attrs` extended to setup `.completer`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    12-Apr-2012 (CT) Add `e_type.primary_required` and `.primary_optional`
#     7-May-2012 (CT) Add `e_type.edit_attr` and `.id_entity_attr`
#    14-Dec-2012 (CT) Add `KeyError` guard to `_setup_attrs` (`auto_up_depends`)
#    11-Jan-2013 (CT) Add support for `primary_ais`
#    28-Mar-2013 (CT) Add `e_type.ui_attr`
#    26-Apr-2013 (CT) Remove support for `primary_ais`
#    15-May-2013 (CT) Add `e_type.link_ref_attr`
#    16-May-2013 (CT) Use `Selector.A_Type` instead of home-grown code
#    16-May-2013 (CT) Add `e_type.rev_ref_attr`
#     3-Jun-2013 (CT) Factor `_prop_map_name`
#     5-Jun-2013 (CT) Add `e_type.own_surrogate` and sanity check
#     5-Jun-2013 (CT) Add `e_type.q_able`
#     6-Jun-2013 (CT) Add `e_type.surrogate_attr`
#     7-Jun-2013 (CT) Change `own_surrogate`, update `surrogate_map`
#    17-Jun-2013 (CT) Sort `rev_ref_attr` and `link_ref_attr`
#    12-Jul-2013 (CT) Change `rev_ref_attr` to select all `_A_Rev_Ref_` types
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

import _MOM._Attr.Type
import _MOM._Attr.Kind
import _MOM._Meta.M_Attr_Spec
import _MOM._Prop.Spec

import _TFL._Meta.Property
import _TFL.Alias_Dict
import _TFL.Sorted_By

from   _TFL.predicate        import callable, first, uniq

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
    _prop_map_name  = "attributes"

    def __init__ (self, e_type) :
        sk                      = TFL.Sorted_By ("rank", "name")
        self._syncable          = []
        self._db_attr           = e_type.db_attr    = []
        self._user_attr         = e_type.user_attr  = []
        self.__super.__init__     (e_type)
        e_type.db_attr.sort       (key = sk)
        e_type.user_attr.sort     (key = sk)
        self._setup_attrs         (e_type)
        e_type.q_able           = tuple \
            ( sorted
                ( (a for a in pyk.itervalues (e_type.attributes) if a.q_able)
                , key = sk
                )
            )
        e_type.edit_attr        = tuple (MOM.Attr.Selector.editable (e_type))
        e_type.id_entity_attr   = tuple \
            (  a for a in e_type.edit_attr
            if isinstance (a, MOM.Attr._EPK_Mixin_)
            )
        e_type.link_ref_attr    = tuple \
            ( sorted
                ( MOM.Attr.Selector.A_Type (MOM.Attr.A_Link_Ref_List) (e_type)
                , key = sk
                )
            )
        e_type.surrogate_attr   = tuple \
            (   a for a in e_type.db_attr
            if  isinstance (a.attr, MOM.Attr.A_Surrogate)
            )
        e_type.rev_ref_attr     = tuple \
            ( sorted
                ( MOM.Attr.Selector.A_Type (MOM.Attr._A_Rev_Ref_) (e_type)
                , key = sk
                )
            )
        e_type.primary_required = pr = list \
            (p for p in e_type.primary if p.is_required)
        e_type.primary_optional = list \
            (p for p in e_type.primary [len (pr): ] if not p.electric)
        e_type.ui_attr          = tuple (MOM.Attr.Selector.ui_attr (e_type))
        own_surrogates          = tuple \
            (a for a in e_type.surrogate_attr if a.name in self._own_names)
        if len (own_surrogates) > 1 :
            raise TypeError \
                ( "%s cannot have more than 1 own surrogate attributes; got %s"
                  "\n    %s"
                % ( e_type.type_name, len (own_surrogates)
                  , ", ".join (repr (a.name) for a in own_surrogates)
                  )
                )
        else :
            try :
                e_type.own_surrogate = s = first (own_surrogates)
            except LookupError :
                e_type.own_surrogate = None
            else :
                suid                 = s.surrogate_id
                app_type             = e_type.app_type
                if suid not in app_type.surrogate_map :
                    app_type.surrogate_t_map [suid]     = e_type
                    app_type.surrogate_map   [s.q_name] = s
    # end def __init__

    def _add_prop (self, e_type, name, prop_type) :
        prop = self.__super._add_prop (e_type, name, prop_type)
        if prop :
            if name != prop.name :
                self._setup_alias (e_type, name, prop.name)
            else :
                attr = prop.attr
                for alias in attr.renameds :
                    self._setup_alias (e_type, alias, name)
        return prop
    # end def _add_prop

    def _effective_prop_kind_mixins (self, name, kind, prop_type, e_type) :
        result = self.__super._effective_prop_kind_mixins \
            (name, kind, prop_type, e_type)
        if prop_type.needs_raw_value and not kind.electric :
            result += (MOM.Attr._Raw_Value_Mixin_, )
        if prop_type.auto_up_depends :
            MI = \
                ( MOM.Attr._Auto_Update_Lazy_Mixin_
                if   (MOM.Attr.Computed_Set_Mixin in result)
                else MOM.Attr._Auto_Update_Mixin_
                )
            result += (MI, )
        if issubclass (e_type, MOM.An_Entity) :
            result = (MOM.Attr._Nested_Mixin_, ) + result
        if MOM.Attr.Computed_Mixin in result :
            result = tuple (r for r in result if r != MOM.Attr.Sticky_Mixin)
        return tuple (uniq (result))
    # end def _effective_prop_kind_mixins

    def _setup_alias (self, e_type, alias_name, real_name) :
        setattr (e_type, alias_name, TFL.Meta.Alias_Property (real_name))
        self._prop_dict.add_alias (alias_name, real_name)
    # end def _setup_alias

    def _setup_attrs (self, e_type) :
        attr_dict = self._attr_dict
        for a in attr_dict.itervalues () :
            for d in a.attr.auto_up_depends :
                try :
                    x = attr_dict [d]
                except KeyError :
                    pass
                else :
                    x.dependent_attrs.add (a)
            if isinstance (a.completer, MOM.Attr.Completer_Spec) :
                a.attr.completer = a.completer (a, e_type)
    # end def _setup_attrs

    def _setup_prop (self, e_type, name, kind, prop) :
        self.__super._setup_prop (e_type, name, kind, prop)
        if not (prop.electric or prop.is_primary) :
            self._user_attr.append (prop)
        if prop.save_to_db :
            self._db_attr.append (prop)
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

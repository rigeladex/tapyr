# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Meta.M_Link
#
# Purpose
#    Meta class of link-types of MOM meta object model
#
# Revision Dates
#    23-Sep-2009 (CT) Creation (factored from `TOM.Meta.M_Link`)
#    27-Oct-2009 (CT) s/Scope_Proxy/E_Type_Manager/
#     4-Nov-2009 (CT) s/E_Type_Manager_L/E_Type_Manager.Link/
#     4-Nov-2009 (CT) `M_Link2` and `M_E_Type_Link2` added
#    18-Nov-2009 (CT) Major surgery (removed generic e-types [i.e., those for
#                     non-derived app_types])
#    19-Nov-2009 (CT) `cls.sorted_by` fixed for default case (3-compatibility)
#    19-Nov-2009 (CT) `_m_setup_roles` changed to set `role.attr.Class` to
#                     `role_type` (needed by MOM.Attr._A_Object_._to_cooked)
#    20-Nov-2009 (CT) `M_Link3`, `M_Link2_Ordered`, `M_E_Type_Link3`, and
#                     `M_E_Type_Link2_Ordered` added
#    24-Nov-2009 (CT) `_m_setup_roles` changed to add to `rt._own_link_map`
#    26-Nov-2009 (CT) `_m_setup_etype_auto_props` changed to handle
#                     `auto_cache`
#    26-Nov-2009 (CT) `other_role_name` added
#    27-Nov-2009 (CT) `_m_setup_etype_auto_props` adapted to change of
#                     `Role_Cacher`
#    27-Nov-2009 (CT) `destroy_dependency` added
#     3-Dec-2009 (CT) `sorted_by` hack removed from `_m_setup_roles`
#     3-Dec-2009 (CT) `M_Link3` and `M_Link2_Ordered` derived from `M_Link`
#                     instead of from `M_Link2`
#    22-Dec-2009 (CT) `M_Link2_Ordered` and `Sequence_Number` removed
#    18-Jan-2010 (CT) `M_Link2._m_setup_etype_auto_props` changed to handle
#                     `auto_cache` for `max_links != 1`, too
#    18-Feb-2010 (CT) `M_Link1` and `M_E_Type_Link1` added (`M_Link_n` factored)
#    19-Feb-2010 (CT) `M_Link_n._m_setup_auto_cache_role` changed to not
#                     create `A_Cached_Role` (done by `Role_Cacher`, now)
#     4-Mar-2010 (CT) `_m_setup_roles` changed to fix the `Class` of
#                     cached-role attributes
#    23-Mar-2010 (CT) `_m_setup_etype_auto_props` changed to set
#                     `role_type.is_relevant` only for non-partial link-types
#    11-May-2010 (CT) `_m_setup_etype_auto_props` changed to set
#                     `auto_cache_roles` depending on `_names`, not
#                     `_own_names` (otherwise, role cachers for inherited
#                     roles get lost)
#    22-Sep-2011 (CT) s/Class/P_Type/ for _A_Id_Entity_ attributes
#     7-Nov-2011 (CT) Redefine `_m_new_e_type_dict` to add `other_role_name`
#    19-Jan-2012 (CT) Remove `raise MOM.Error.No_Scope` from `M_E_Type.__call__`
#    23-Mar-2012 (CT) Change `_m_setup_etype_auto_props` to setup `auto_cache`
#                     properly even if `cls.type_name != rc.link_type_name`
#                     (i.e., for descendent classes)
#    24-Mar-2012 (CT) Change `_m_setup_etype_auto_props` to not overwrite
#                     `auto_cache` (don't rewrite ancestor's `auto_cache`)
#    18-Jun-2012 (CT) Add `M_E_Type_Link[123]_Reload`
#    23-Jul-2012 (CT) Change `M_Link._m_setup_etype_auto_props` to consider
#                     `a.Cacher_Type`
#     1-Aug-2012 (CT) Add `M_E_Type_Link[123]_Destroyed`
#    31-Aug-2012 (CT) Restrict `_m_setup_roles` to roles in `_own_names`
#    12-Sep-2012 (CT) Add `Partial_Roles`, `_m_create_auto_children`
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM._Meta.M_Entity
import _MOM.E_Type_Manager

from   _TFL.predicate import cartesian

import itertools

class M_Link (MOM.Meta.M_Id_Entity) :
    """Meta class of link-types of MOM meta object model."""

    _orn = {}

    def other_role_name (cls, role_name) :
        raise TypeError \
            ( "%s.%s.other_role_name needs to be explicitly defined"
            % (cls.type_name, role_name)
            )
    # end def other_role_name

    def _m_create_auto_child (cls, * role_etype_s) :
        rkw = dict (__module__ = cls.__module__)
        tn  = cls.type_name
        tbn = cls.type_base_name
        for role, etype in role_etype_s :
            tbn = tbn.replace (role.E_Type.type_base_name, etype.type_base_name)
            tn  = tn.replace  (role.E_Type.type_base_name, etype.type_base_name)
            rkw [role.name] = role.__class__ \
                ( role.name
                , (role, )
                , dict
                    ( auto_cache     = role.auto_cache_np
                    , auto_derive_np = role.auto_derive_npt
                    , role_type      = etype
                    , __module__     = cls.__module__
                    )
                )
        if tn == cls.type_name :
            TFL.Environment.exec_python_startup (); import pdb; pdb.set_trace ()
            raise NameError \
                ("Cannot auto-derive from %s for %s" % (cls, role_etype_s))
        if tn in cls._type_names :
            if __debug__ :
                print \
                    ( "Essential type %s is already defined [%s: %s]"
                    % (tn, cls, role_etype_s)
                    )
        else :
            result = cls.__class__ \
                ( tbn
                , (cls, )
                , dict
                    ( _Attributes    = cls._Attributes.__class__
                        ( "_Attributes"
                        , (cls._Attributes, )
                        , rkw
                        )
                    , __module__     = cls.__module__
                    )
                )
            return result
    # end def _m_create_auto_child

    def _m_create_auto_children (cls) :
        adrs = tuple \
            ( tuple
                ( (r, c)
                for c in sorted
                    ( r.E_Type.children_np.itervalues ()
                    , key = TFL.Getter.i_rank
                    )
                )
            for r in cls.Roles
            if  r.auto_derive_np and r.E_Type.children_np
            )
        if adrs :
            for adr in cartesian (* adrs) :
                cls._m_create_auto_child (* adr)
    # end def _m_create_auto_children

    def _m_new_e_type_dict (cls, app_type, etypes, bases, ** kw) :
        result = cls.__m_super._m_new_e_type_dict \
            ( app_type, etypes, bases
            , other_role_name = cls._orn
            , ** kw
            )
        return result
    # end def _m_new_e_type_dict

    def _m_setup_etype_auto_props (cls) :
        cls.__m_super._m_setup_etype_auto_props ()
        roles = set ()
        cls.Partial_Roles = PRs = []
        cls.Roles         = Rs  = []
        cls.acr_map = acr_map = dict (getattr (cls, "acr_map", {}))
        for a in cls._Attributes._names.itervalues () :
            if issubclass (a, MOM.Attr.A_Link_Role) :
                Rs.append (a)
                if a.role_type :
                    if a.auto_cache :
                        roles.add (a)
                    if a.role_type.is_partial :
                        PRs.append (a)
                else :
                    cls.is_partial = True
        for a in roles :
            rc = acr_map.get (a.name) or a.auto_cache
            if not isinstance (rc, MOM._.Link._Cacher_) :
                Cacher = a.Cacher_Type or cls.Cacher
                rc     = Cacher (a.auto_cache)
            if rc.link_type_name is None :
                rc.setup (cls, a)
            elif cls.type_name != rc.link_type_name :
                rc = rc.copy (cls, a)
            acr_map [a.name] = rc
        cls.auto_cache_roles = tuple (acr_map.get (a.name) for a in roles)
        cls._m_create_auto_children ()
    # end def _m_setup_etype_auto_props

# end class M_Link

class M_Link1 (M_Link) :
    """Meta class of unary link-types of MOM meta object model."""

    def other_role_name (cls, role_name) :
        raise TypeError \
            ( "%s: There is no other role than %s"
            % (cls.type_name, role_name)
            )
    # end def other_role_name

# end class M_Link1

class M_Link_n (M_Link) :
    """Meta class of link-types with more than 1 role."""

# end class M_Link_n

class M_Link2 (M_Link_n) :
    """Meta class of binary entity-based link-types of MOM meta object model."""

    _orn = dict (left = "right", right = "left")

    def other_role_name (cls, role_name) :
        return cls._orn [role_name]
    # end def other_role_name

# end class M_Link2

class M_Link3 (M_Link_n) :
    """Meta class of ternary link-types of MOM meta object model."""

# end class M_Link3

@TFL.Add_To_Class ("M_E_Type", M_Link)
class M_E_Type_Link (MOM.Meta.M_E_Type_Id) :
    """Meta class for essence of MOM.Link."""

    Manager = MOM.E_Type_Manager.Link

    ### `Alias_Property` makes `destroy_dependency` usable as class and as
    ### instance method
    ### - called as class method it refers to `destroy_links`
    ### - called as instance method it refers to `destroy_dependency` defined
    ###   in `Link` (or one of its ancestors)
    destroy_dependency = TFL.Meta.Alias_Property ("destroy_links")

    def destroy_links (cls, obj) :
        """Destroy all links where `obj` participates."""
        scope = obj.home_scope
        etm   = getattr (scope, cls.type_name)
        for l in etm.links_of (obj) :
            scope.remove (l)
    # end def destroy_links

    def _m_setup_attributes (cls, bases, dct) :
        cls.__m_super._m_setup_attributes (bases, dct)
        cls._m_setup_roles                (bases, dct)
    # end def _m_setup_attributes

    def _m_setup_roles (cls, bases, dct) :
        cls.Roles  = Roles  = tuple \
            (p for p in cls.primary if isinstance (p, MOM.Attr.Link_Role))
        role_types = tuple \
            (r.role_type for r in Roles if r.role_type is not None)
        if len (role_types) == len (Roles) :
            type_base_names = [rt.type_base_name for rt in role_types]
            cls.number_of_roles = nor      = len (Roles)
            cls.role_map        = role_map = {}
            for i, r in enumerate (Roles) :
                if r.attr.name in cls._Attributes._own_names :
                    ### Replace by app-type specific e-type
                    r.attr.assoc     = r.assoc       = cls
                    r.attr.role_type = r.attr.P_Type = rt = \
                        cls.app_type.entity_type (r.role_type)
                    r.attr.typ       = rt.type_base_name
                    ac      = cls.acr_map.get (r.attr.name)
                    cr_attr = ac and ac.cr_attr
                    if cr_attr and cr_attr.P_Type :
                        cr_attr.P_Type = cls.app_type.entity_type \
                            (cr_attr.P_Type)
                if r.role_name != r.generic_role_name :
                    setattr \
                        ( cls, r.role_name
                        , TFL.Meta.Alias_Property (r.generic_role_name)
                        )
                r.role_index = i
                for key in set \
                        (( r.default_role_name, r.generic_role_name
                         , r.role_name, r.role_type.type_name
                         , r.role_type.type_base_name
                        )) :
                    role_map [key] = r.role_index
    # end def _m_setup_roles

# end class M_E_Type_Link

@TFL.Add_To_Class ("M_E_Type", M_Link1)
class M_E_Type_Link1 (M_E_Type_Link) :
    """Meta class for essence of MOM.Link1."""

    Manager = MOM.E_Type_Manager.Link1

# end class M_E_Type_Link1

@TFL.Add_To_Class ("M_E_Type", M_Link2)
class M_E_Type_Link2 (M_E_Type_Link) :
    """Meta class for essence of MOM.Link2."""

    Manager = MOM.E_Type_Manager.Link2

# end class M_E_Type_Link2

@TFL.Add_To_Class ("M_E_Type", M_Link3)
class M_E_Type_Link3 (M_E_Type_Link2) :
    """Meta class for essence of MOM.Link2."""

    Manager = MOM.E_Type_Manager.Link3

# end class M_E_Type_Link3

class M_E_Type_Link1_Destroyed (MOM.Meta.M_E_Type_Id_Destroyed, M_E_Type_Link1) :
    """Meta class for `_Destroyed` classes of descendents of MOM.Link1."""

# end class M_E_Type_Link1_Destroyed

class M_E_Type_Link2_Destroyed (MOM.Meta.M_E_Type_Id_Destroyed, M_E_Type_Link2) :
    """Meta class for `_Destroyed` classes of descendents of MOM.Link2."""

# end class M_E_Type_Link2_Destroyed

class M_E_Type_Link3_Destroyed (MOM.Meta.M_E_Type_Id_Destroyed, M_E_Type_Link3) :
    """Meta class for `_Destroyed` classes of descendents of MOM.Link3."""

# end class M_E_Type_Link3_Destroyed

class M_E_Type_Link1_Reload (MOM.Meta.M_E_Type_Id_Reload, M_E_Type_Link1) :
    """Meta class for `_Reload` classes of descendents of MOM.Link1."""

# end class M_E_Type_Link1_Reload

class M_E_Type_Link2_Reload (MOM.Meta.M_E_Type_Id_Reload, M_E_Type_Link2) :
    """Meta class for `_Reload` classes of descendents of MOM.Link2."""

# end class M_E_Type_Link2_Reload

class M_E_Type_Link3_Reload (MOM.Meta.M_E_Type_Id_Reload, M_E_Type_Link3) :
    """Meta class for `_Reload` classes of descendents of MOM.Link3."""

# end class M_E_Type_Link3_Reload

__doc__ = """
Class `MOM.Meta.M_Link`
=========================

.. class:: M_Link

    `MOM.Meta.M_Link` provides the meta machinery for defining
    essential association types and link instances. It is based on
    :class:`~_MOM._Meta.M_Entity.M_Entity`.

    `M_Link` is the common base class for the arity-specific subclasses.

    `M_Link` provides the attribute:

    .. attribute:: Roles

      The tuple of role objects (contains as many role objects as the arity
      of the association specifies).

.. class:: M_Link1

    `MOM.Meta.M_Link1` provides the meta machinery for
    :class:`unary links<_MOM.Link.Link1>`.

.. class:: M_Link2

    `MOM.Meta.M_Link2` provides the meta machinery for
    :class:`binary links<_MOM.Link.Link2>`.

.. class:: M_Link3

    `MOM.Meta.M_Link3` provides the meta machinery for
    :class:`ternary links<_MOM.Link.Link3>`.

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Link

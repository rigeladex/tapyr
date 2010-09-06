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
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM._Meta.M_Entity
import _MOM.E_Type_Manager

import itertools

class M_Link (MOM.Meta.M_Id_Entity) :
    """Meta class of link-types of MOM meta object model."""

    def other_role_name (cls, role_name) :
        raise TypeError \
            ( "%s.%s.other_role_name needs to be explicitly defined"
            % (cls.type_name, role_name)
            )
    # end def other_role_name

    def _m_setup_etype_auto_props (cls) :
        cls.__m_super._m_setup_etype_auto_props ()
        roles = set ()
        for a in cls._Attributes._names.itervalues () :
            if issubclass (a, MOM.Attr.A_Link_Role) and a.role_type :


                if a.auto_cache :
                    roles.add (a)
                #if not cls.is_partial : a.role_type.is_relevant = True
        for a in cls._Attributes._own_names.itervalues () :
            if issubclass (a, MOM.Attr.A_Link_Role) and a.role_type :
                rc = a.auto_cache
                if rc :
                    if not isinstance (rc, MOM._.Link._Cacher_) :
                        rc = a.auto_cache = cls.Cacher (rc)
                    rc.setup (cls, a)
        cls.auto_cache_roles = tuple (a.auto_cache for a in roles)
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
            l.destroy () ### scope.ems.remove (l)
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
                r.role_index = i
                if r.role_type :
                    ### Replace by app-type specific e-type
                    r.attr.assoc     = r.assoc      = cls
                    r.attr.role_type = r.attr.Class = rt = \
                        cls.app_type.entity_type (r.role_type)
                    r.attr.typ       = rt.type_base_name
                    rt._own_link_map [cls].add (r)
                    cr_attr = r.attr.auto_cache and r.attr.auto_cache.cr_attr
                    if cr_attr and cr_attr.Class :
                        cr_attr.Class = cls.app_type.entity_type (cr_attr.Class)
                if r.role_name != r.generic_role_name :
                    setattr \
                        ( cls, r.role_name
                        , TFL.Meta.Alias_Property (r.generic_role_name)
                        )
                for key in set \
                        (( r.default_role_name, r.generic_role_name, r.role_name
                         , r.role_type.type_name, r.role_type.type_base_name
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

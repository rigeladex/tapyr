# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM._Meta.M_Entity
import _MOM.E_Type_Manager

class M_Link (MOM.Meta.M_Id_Entity) :
    """Meta class of link-types of MOM meta object model."""

    def _m_setup_etype_auto_props (cls) :
        cls.__m_super._m_setup_etype_auto_props ()
        for a in cls._Attributes._names.itervalues () :
            if issubclass (a, MOM.Attr.A_Link_Role) and a.role_type :
                a.role_type.is_relevant = True
        ### XXX setup auto cache roles
    # end def _m_setup_etype_auto_props

# end class M_Link

class M_Link2 (M_Link) :
    """Meta class of binary entity-based link-types of MOM meta object model."""

# end class M_Link2

@TFL.Add_To_Class ("M_E_Type", M_Link)
class M_E_Type_Link (MOM.Meta.M_E_Type_Id) :
    """Meta class for essence of MOM.Link."""

    Manager = MOM.E_Type_Manager.Link

    def _m_setup_attributes (cls, bases, dct) :
        cls.__m_super._m_setup_attributes (bases, dct)
        cls._m_setup_roles                (bases, dct)
    # end def _m_setup_attributes

    def _m_setup_roles (cls, bases, dct) :
        cls.Roles  = Roles  = tuple \
            (p for p in cls.primary if isinstance (p, MOM.Attr.Link_Role))
        role_types = tuple \
            (r.role_type for r in Roles if r.role_type is not None)
        if role_types and role_types [0] is not MOM.Sequence_Number :
            type_base_names = [rt.type_base_name for rt in role_types]
            if type_base_names [-1] == "Sequence_Number" :
                type_base_names = type_base_names [:-1]
            rltn_pat = TFL.Regexp (r"_(.*?)_".join (type_base_names))
            if rltn_pat.match (cls.type_base_name) :
                cls.rltn_names = rltn_pat.groups ()
            else :
                cls.rltn_names = None
                if __debug__ :
                    print "No match for relation names", \
                        cls.name, type_base_names, rltn_pat.pattern
            cls.number_of_roles = len (Roles)
            cls.role_map        = role_map = {}
            for i, r in enumerate (Roles) :
                r.role_index = i
                if r.role_type :
                    ### Replace by app-type specific e-type
                    r.assoc          = cls
                    r.attr.role_type = cls.app_type.entity_type (r.role_type)
                    r.attr.typ       = r.attr.role_type.type_base_name
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

@TFL.Add_To_Class ("M_E_Type", M_Link2)
class M_E_Type_Link2 (M_E_Type_Link) :
    """Meta class for essence of MOM.Link2."""

    Manager = MOM.E_Type_Manager.Link2

# end class M_E_Type_Link2

__doc__ = """
Class `MOM.Meta.M_Link`
=========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_Link

    `MOM.Meta.M_Link` provides the meta machinery for defining
    essential association types and link instances. It is based on
    :class:`~_MOM._Meta.M_Entity.M_Entity`.

    `M_Link` is the common base class for the arity-specific subclasses.

    `M_Link` provides the attribute:

    .. attribute:: Roles

      The tuple of role objects (contains as many role objects as the arity
      of the association specifies).

    `M_Link` provides the methods:

    .. automethod:: add
    .. automethod:: add_children_filters
    .. automethod:: applicable_objects
    .. automethod:: define_link

    .. method:: destroy()

        Destroy all links of the association.

    .. automethod:: destroy_links
    .. automethod:: link(* objs)
    .. automethod:: link_transitive(* objs)
    .. automethod:: links_of_obj(obj)
    .. automethod:: remove

.. class:: M_Link2

    `TOM.Meta.M_Link2` provides the meta machinery for
    :class:`binary links<_TOM.Link2.Link2>`.

    `M_Link2` provides the method:

    .. automethod:: links_of(l = None, r = None)


.. class:: M_Link2_Ordered

    `TOM.Meta.M_Link2_Ordered` provides the meta machinery for
    :class:`binary ordered links<_TOM.Link2_Ordered.Link2_Ordered>`.

    `M_Link2_Ordered` provides the method:

    .. automethod:: links_of(l = None, r = None, seq_no = None)

.. class:: M_Link3

    `TOM.Meta.M_Link3` provides the meta machinery for
    :class:`ternary links<_TOM.Link3.Link3>`.

    `M_Link3` provides the method:

    .. automethod:: links_of(l = None, m = None, r = None)

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Link

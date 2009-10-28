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
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM._Meta.M_Entity
import _MOM.E_Type_Manager

class M_Link (MOM.Meta.M_Id_Entity) :
    """Meta class of link-types of MOM meta object model."""

    def _m_new_e_type_dict (cls, app_type, etypes, bases, ** kw) :
        Roles  = [] ### XXX ??? can we do that here ???
        result = cls.__m_super._m_new_e_type_dict \
            ( app_type, etypes, bases
            , Roles = Roles
            , ** kw
            )
        return result
    # end def _m_new_e_type_dict

# end class M_Link

@TFL.Add_To_Class ("M_E_Type", M_Link)
class M_E_Type_Link (MOM.Meta.M_E_Type_Id) :
    """Meta class for essence of MOM.Link."""

    Manager = MOM.E_Type_Manager_L

# end class M_E_Type_Link

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

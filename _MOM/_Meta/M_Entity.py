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
#    MOM.Meta.M_Entity
#
# Purpose
#    Meta class for essential entity
#
# Revision Dates
#    23-Sep-2009 (CT) Creation (factored from `MOM.Meta.M_Entity`)
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _TFL._Meta.M_Class
import _MOM._Meta

class M_Entity (TFL.Meta.M_Class) :
    """Meta class for essential entity of MOM meta object model."""

    _M_Extension = []

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__  (name, bases, dict)
        cls._m_init_prop_specs  (name, bases, dict)
        cls._M_Extension.append (cls)
    # end def __init__

    ### XXX add methods to create app-type specific Etypes

    def _m_init_prop_specs (cls, name, bases, dct) :
        for psn in "_Attributes", "_Predicates" :
            if psn not in dct :
                prop_bases = tuple (getattr (b, psn) for b in bases)
                d          = dict  (__module__ = cls.__module__)
                ### `TFL.Meta.M_M_Class` will choose the right meta class
                ### (i.e., `M_Attr_Spec` or `M_Pred_Spec`)
                setattr (cls, psn, MOM.Meta.M_Prop_Spec (psn, prop_bases, d))
    # end def _m_init_prop_specs

# end class M_Entity

__doc__ = """
Class `MOM.Meta.M_Entity`
=========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_Entity

    `MOM.Meta.M_Entity` provides the meta machinery for defining the
    characteristics of essential object and link types of the MOM meta object
    model. It is the common base class for
    :class:`MOM.Meta.M_Object<_MOM._Meta.M_Object.M_Object>` and
    :class:`MOM.Meta.M_Link<_MOM._Meta.M_Link.M_Link>`.

    For each essential class, `M_Entity`:

    - Creates `_Attributes` and `_Predicates`, if they weren't already
      defined by the class definition.

    - Defines the class attributes

      .. attribute:: Essence

          Always points to the class defining the essence (even in the
          automatically generated ats-specific children of that class).

      .. attribute:: name

          Refers to the essential name of the class.

      .. attribute:: type_base_name

          Refers to the essential name of the class.

      .. attribute:: type_name

          Refers to the essential name of the class qualified by the
          name of defining :attr:`package namespace<_MOM.Entity.Package_NS>`.

      .. attribute:: ui_name

          Refers to the name of the class to be displayed by the user
          interface(s). Depending on the class variable
          :attr:`~_MOM.Entity.show_package_prefix`, `ui_name` might or
          might not be qualified by the name of defining
          :attr:`package namespace<_MOM.Entity.Package_NS>`.

    ### XXX ???
    `M_Entity` delegates two operations to the scope-specific type
    of the class:

    - object creation,

    - attribute access (for attributes not defined by the essential
      class itself).

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("M_Entity")
### __END__ MOM.Meta.M_Entity

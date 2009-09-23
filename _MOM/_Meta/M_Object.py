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
#    MOM.Meta.M_Object
#
# Purpose
#    Meta class of object-types of MOM meta object model
#
# Revision Dates
#    23-Sep-2009 (CT) Creation (factored from `MOM.Meta.M_Object`)
#    ««revision-date»»···
#--

from   _MOM import MOM
from   _TFL import TFL

import _MOM._Meta.M_Entity

class M_Object (MOM.Meta.M_Entity) :
    """Meta class of object-types of MOM meta object model."""


# end class M_Object

__doc__ = """
Class `MOM.Meta.M_Object`
=========================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. class:: M_Object

    `MOM.Meta.M_Object` provides the meta machinery for defining
    essential object types and instances. It is based on
    :class:`~_MOM._Meta.M_Entity.M_Entity`.

    `M_Object` provides the attribute:

    .. attribute:: root

      `root` gives to the root object, if any, in the `home_scope` or
      the currently active scope.

    `M_Object` provides the methods:

    .. automethod:: define
    .. automethod:: exists
    .. automethod:: extension
    .. automethod:: extension_strict
    .. automethod:: instance

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("M_Entity")
### __END__ MOM.Meta.M_Object

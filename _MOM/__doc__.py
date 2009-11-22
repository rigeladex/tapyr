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
#    MOM.__doc__
#
# Purpose
#    Test for MOM meta object model
#
# Revision Dates
#    18-Oct-2009 (CT) Creation
#     4-Nov-2009 (CT) Creation continued
#     4-Nov-2009 (MG) `Beaver` and `Otter` added
#    ««revision-date»»···
#--

"""
How to define essential object models
=====================================

Using `MOM`, an essential object model is specified by deriving
classes from :class:`MOM.Object<_MOM.Object.Object>`,
:class:`MOM.Named_Object<_MOM.Object.Named_Object>`, or from one of
the descendents of :class:`MOM.Link<_MOM.Link.Link>`.

Each essential class must be defined inside a
:class:`TFL.Package_Namespace<_TFL.Package_Namespace.Package_Namespace>`
and the class definition must contain an explicit or inherited
reference :attr:`Package_NS<_MOM.Entity.Package_NS>` to that package
namespace.

Normally, each essential class is defined in a module of its own. In
some cases, a single module might define more than one essential
class.

Essential objects and links have identity, i.e., each object or link
can be uniquely identified. This identity is specified by a set of (so
called `primary`) attributes that together define the `essential
primary key`, short `epk`, for the entity in question. If there is no
more than primary attribute, the sequence of the attributes is defined
by their :attr:`rank` and :attr:`name`.

Essential objects identified by a simple, unstructured `name` are
defined by classes derived from
:class:`MOM.Named_Object<_MOM.Object.Named_Object>`. All other
essential objects are defined by classes derived from
:class:`MOM.Object<_MOM.Object.Object>` that specify one or more
essential attributes of kind :class:`~_MOM._Attr.Kind.Primary`.

Essential links are identified by the associated objects (the link's
roles) and any other, if any, primary attributes defined for the link
in question:

- Binary links are derived from :class:`MOM.Link2<_MOM.Link.Link2>`
  and identified by the link roles :attr:`left<_MOM.Link.Link2.left>`
  and :attr:`right<_MOM.Link.Link2.right>` plus any other primary
  attributes.

- Binary ordered links are derived from
  :class:`MOM.Link2_Ordered<_MOM.Link.Link2_Ordered>`
  and identified by the link roles
  :attr:`left<_MOM.Link.Link2_Ordered.left>`,
  :attr:`right<_MOM.Link.Link2_Ordered.right>`, and
  :attr:`seq_no<_MOM.Link.Link2_Ordered.seq_no>` plus any other primary
  attributes.

- Ternary links are derived from :class:`MOM.Link3<_MOM.Link.Link3>`
  and identified by the link roles :attr:`left<_MOM.Link.Link3.left>`,
  :attr:`middle<_MOM.Link.Link3.middle>`,
  and :attr:`right<_MOM.Link.Link3.right>` plus any other primary
  attributes.


"""

from   _MOM.import_MOM       import *

class Rodent (MOM.Named_Object) :
    """Model a rodent of the Better Mouse Trap application."""

    class _Attributes (MOM.Named_Object._Attributes) :

        class color (A_String) :
            """Color of the rodent"""

            kind     = Attr.Optional

        # end class color

        class weight (A_Float) :
            """Weight of the rodent"""

            kind     = Attr.Required
            check    = ("value > 0", )

        # end class weight

    # end class _Attributes

# end class Rodent

class Mouse (Rodent) :
    """Model a mouse of the Better Mouse Trap application."""

    is_partial = False

# end class Mouse

class Rat (Rodent) :
    """Model a rat of the Better Mouse Trap application."""

    is_partial = False

# end class Rat

class Beaver (Mouse) :
    """Model a beaver of the Better Mouse Trap application."""

    class _Attributes (Mouse._Attributes) :

        class region (A_String) :
            """In wich are lives the beaver"""

            kind     = Attr.Optional

        # end class region

    # end class _Attributes

# end class Beaver

class Otter (Beaver) :

    class _Attributes (Beaver._Attributes) :

        class river (A_String) :

            kind       = Attr.Optional
            max_length = 20

        # end class river

    # end class _Attributes

# end class Otter

class Trap (MOM.Object) :
    """Model a trap of the Better Mouse Trap application."""

    is_partial = False

    class _Attributes (MOM.Object._Attributes) :

        class cat (A_String) :
            """Category of the trap"""

            kind     = Attr.Primary

        # end class cat

        class serial_no (A_Int) :
            """Serial number of the trap"""

            kind     = Attr.Primary

        # end class serial_no

        class max_weight (A_Float) :
            """Maximum weight of rodent the trap can hold"""

            kind     = Attr.Optional
            check    = ("value > 0", )

        # end class max_weight

    # end class _Attributes

# end class Trap

class Rodent_in_Trap (MOM.Link2) :
    """Model a rodent caught in a trap."""

    is_partial = False

    class _Attributes (MOM.Link2._Attributes) :

        class left (MOM.Link2._Attributes.left) :
            """Rodent caught in Trap."""

            role_type     = Rodent
            max_links     = 1

        # end class left

        class right (MOM.Link2._Attributes.right) :
            """Trap that caught a rodent."""

            role_type     = Trap
            max_links     = 1

        # end class right

    # end class _Attributes

# end class Rodent_in_Trap

### __END__ MOM.__doc__

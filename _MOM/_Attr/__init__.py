# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package _MOM.
#
# This package is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this package. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Attr.__init__
#
# Purpose
#    Initialize package `MOM.Attr`
#
# Revision Dates
#    17-Sep-2009 (CT) Creation (factored from TOM.Attr)
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _MOM                   import MOM

Attr = Package_Namespace ()
MOM._Export ("Attr")

del Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`MOM.Attr` provides a framework for the definition and
implementation of essential and non-essential attributes of
:class:`objects<_MOM.Object.Object>`
and :class:`links<_MOM.Link.Link>` of essential object models.

Each attribute is characterized by

- its :class:`type<_MOM._Attr.Type.A_Attr_Type>`

- its :class:`kind<_MOM._Attr.Kind.Kind>`

The attributes are defined inside the class definition of the
essential entity, i.e., object or link, and are encapsulated inside a
class named `_Attributes` that is derived from
:class:`~_MOM._Attr.Spec.Spec`, for instance::

    from _MOM._Attr import Attr

    class Some_Essence (MOM.Object) :

        class _Attributes (MOM.Object._Attributes) :

            class is_used (Attr.A_Int) :
                "Counts the number of users of this object."
                kind          = Attr.Cached
                default       = "1"
            # end class is_used

            ...

The attributes of a specific instance of an essential entity are
managed by an instance of :class:`~_MOM._Attr.Manager.Manager`.

"""

### __END__ MOM.Attr.__init__

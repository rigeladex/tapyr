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
#    MOM.__init__
#
# Purpose
#    Package implementing a simple meta object model in python
#
# Revision Dates
#    17-Sep-2009 (CT) Creation (factored from TOM)
#    ««revision-date»»···
#--

from _TFL.Package_Namespace import Package_Namespace

MOM = Package_Namespace ()

del Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`MOM` provides a framework for the definition and
implementation of essential object models.

An essential (see [McP84]_) object model is one, IMHO the best, way of
capturing the results of an object oriented analysis. An essential
object model comprises classes and associations.

Each essential class (modelled by the class
:class:`MOM.Object<_MOM.Object.Object>`)
describes one specific type of object, in particluar

- the attributes (modelled by the classes in the package namespace
  :mod:`MOM.Attr<_MOM._Attr>`),

- and the predicates (modelled by the classes in the package namespace
  :mod:`MOM.Pred<_MOM._Pred>`)

visible to the class' clients.

Each association (modelled by the classes :class:`MOM.Link<_MOM.Link.Link>` and
:class:`MOM.Meta.M_Link<_MOM._Meta.M_Link.M_Link`) describes the possible links
between the objects of a number of classes.

As the links of an association are also characterized by attributes
and predicates, most of the behavior of
:class:`MOM.Object<_MOM.Object.Object>` and
:class:`MOM.Link<_MOM.Link.Link>` is defined by their common ancestor
:class:`MOM.Entity<_MOM.Entity.Entity>`.

A specific meta object model is defined for a well-defined application. Each
instance of a meta object model is managed by a scope object (modelled by the
class :class:`MOM.Scope<_MOM.Scope.Scope>`).

"""

### __END__ MOM.__init__

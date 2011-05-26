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
# along with this package.  If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Prop.__init__
#
# Purpose
#    Initialize package `MOM.Prop`
#
# Revision Dates
#    24-Sep-2009 (CT) Creation (factored from TOM classes)
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _MOM                   import MOM

Prop = Package_Namespace ()
MOM._Export ("Prop")

del Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`MOM.Prop` provides a framework for the definition and
implementation of essential attributes and predicates of
:class:`objects<_MOM.Object.Object>`
and :class:`links<_MOM.Link.Link>` of essential object models.


"""

### __END__ MOM.Prop.__init__

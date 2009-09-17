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
#    MOM.Meta.__init__
#
# Purpose
#    Initialize package `MOM.Meta`
#
# Revision Dates
#    17-Sep-2009 (CT) Creation (factored from TOM.Meta)
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _TFL                   import TFL
from   _MOM                   import MOM

import _TFL._Meta

Meta = Derived_Package_Namespace (parent = TFL.Meta)
MOM._Export ("Meta")

del Derived_Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`MOM.Meta` provides meta classes for the definition and
implementation of essential object models (see :mod:`MOM<_MOM>`).

"""

### __END__ MOM.Meta.__init__

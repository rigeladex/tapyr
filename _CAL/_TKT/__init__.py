# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    CAL.TKT.__init__
#
# Purpose
#    Package providing (UI)-toolkit support for CAL
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _CAL                   import CAL
from   _TGL                   import TGL
import _TGL._TKT

TKT = Derived_Package_Namespace (parent = TGL.TKT)
CAL._Export ("TKT")

del Derived_Package_Namespace

### __END__ CAL.TKT.__init__

# -*- coding: iso-8859-1 -*-
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
#    TFL.TKT.Tk.__init__
#
# Purpose
#    Package providing Tk toolkit support for TFL
#
# Revision Dates
#    12-Jan-2005 (CT) Creation
#    18-Jan-2005 (CT) Set `TFL.TKT.Mixin.TNS_name` instead of calling
#                     `TFL.UI.set_TKT`
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _TFL                   import TFL
import _TFL._TKT

Tk = Package_Namespace ()
TFL.TKT._Export ("Tk")

import _TFL._TKT.Mixin
TFL.TKT.Mixin.TNS_name = "Tk"

del Package_Namespace

### __END__ TFL.TKT.Tk.__init__

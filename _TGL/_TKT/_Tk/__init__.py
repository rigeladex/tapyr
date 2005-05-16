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
#    TGL.TKT.Tk.__init__
#
# Purpose
#    Package providing Tk toolkit support for TGL
#
# Revision Dates
#    22-Mar-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _TFL                   import TFL
from   _TGL                   import TGL
import _TFL._TKT._Tk
import _TGL._TKT

Tk = Derived_Package_Namespace (parent = TFL.TKT.Tk)
TGL.TKT._Export ("Tk")

del Derived_Package_Namespace

import CT_TK
import Environment
import sos
CT_TK._std_pathes.insert \
    ( 0, sos.path.join
             (sos.path.dirname (Environment.module_path ("_TGL")), "-Images")
    )
### __END__ TGL.TKT.Tk.__init__

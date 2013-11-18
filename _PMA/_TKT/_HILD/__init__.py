# -*- coding: utf-8 -*-
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
#    PMA.TKT.HILD.__init__
#
# Purpose
#    Package providing HILD toolkit support for PMA
#
# Revision Dates
#    29-Mar-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Derived_Package_Namespace
from   _PMA                   import PMA
from   _TGL                   import TGL
import _TGL._TKT._HILD
import _PMA._TKT

HILD = Derived_Package_Namespace (parent = TGL.TKT.HILD)
PMA.TKT._Export ("HILD")

del Derived_Package_Namespace

from _PMA._TKT._GTK.Office import *
### __END__ PMA.TKT.HILD.__init__

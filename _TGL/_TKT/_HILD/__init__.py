# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TGL.TKT.HILD.__init__
#
# Purpose
#    Package providing hildon toolkit support for TGL
#
# Revision Dates
#    21-Jan-2006 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _TFL.Package_Namespace import Derived_Package_Namespace
import _TGL._TKT
import _TGL._TKT._GTK

HILD = Derived_Package_Namespace (parent = TGL.TKT.GTK)
TGL.TKT._Export         ("HILD")

import _TGL._TKT.Mixin
TGL.TKT.Mixin.set_TNS_name ("HILD", override = "GTK")

del Derived_Package_Namespace

import hildon
HILD.hildon = hildon

### __END__ TGL.TKT.HILD.__init__

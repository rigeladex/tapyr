# -*- coding: iso-8859-1 -*-
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
#    TGL.TKT.GTK.__init__
#
# Purpose
#    Package providing GTK toolkit support for TGL
#
# Revision Dates
#    21-Mar-2005 (MG) Creation
#    25-Mar-2005 (CT) Moved to `TGL`
#    20-May-2005 (MG) `Error` added
#    10-Aug-2005 (CT) Use `set_TNS_name` instead of home-grown code
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _TFL.Package_Namespace import Package_Namespace
import _TGL._TKT

GTK = Package_Namespace ()
TGL.TKT._Export         ("GTK")

GTK.stop_cb_chaining = True
GTK.Error            = Exception

import _TGL._TKT.Mixin
TGL.TKT.Mixin.set_TNS_name ("GTK")

del Package_Namespace

### __END__ TGL.TKT.GTK.__init__

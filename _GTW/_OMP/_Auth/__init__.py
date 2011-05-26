# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.OMP.Auth.__init__
#
# Purpose
#    Package defining a partial object model for Authentication
#
# Revision Dates
#    13-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW._OMP              import OMP
from   _MOM                   import MOM
from   _TFL.Package_Namespace import Derived_Package_Namespace

Auth = Derived_Package_Namespace (parent = MOM)
OMP._Export ("Auth")

del Derived_Package_Namespace

### __END__ GTW.OMP.Auth.__init__

# -*- coding: iso-8859-15 -*-
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
#    DJO.Apps.__init__
#
# Purpose
#    Package with Django applications
#
# Revision Dates
#    14-May-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _DJO                   import DJO

Apps = Package_Namespace ()
DJO._Export ("Apps")

del Package_Namespace

### __END__ DJO.Apps.__init__

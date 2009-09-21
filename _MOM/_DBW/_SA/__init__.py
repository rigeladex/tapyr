# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
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
#    MOM.DBW.SA.__init__
#
# Purpose
#    Package for the database wrapper using the sqlalchemy (www.sqlalchemy.org)
#    library
#
# Revision Dates
#    20-Sep-2009 (MG) Creation
#    ««revision-date»»···
#--



from   _MOM._DBW              import DBW
from   _TFL.Package_Namespace import Package_Namespace

SA = Package_Namespace ()
DBW._Export ("SA")

del Package_Namespace

### __END__ MOM.DBW.SA.__init__

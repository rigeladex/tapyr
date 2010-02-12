# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This package is part of the package _MOM.
#
# This package is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this package.  If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SQL.__init__
#
# Purpose
#    Package for the database wrapper using the SQL layer of sqlalchemy
#    (www.sqlalchemy.org)
#
# Revision Dates
#    11-Feb-2010 (MG) Creation (based on the full blown SQL backend)
#    ««revision-date»»···
#--

from   _MOM._DBW              import DBW
from   _TFL.Package_Namespace import Package_Namespace

SQL = Package_Namespace ()
DBW._Export ("SQL")

del Package_Namespace

### __END__ MOM.DBW.SQL.__init__

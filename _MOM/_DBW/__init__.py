# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Martin Glück. All rights reserved
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
#    MOM.DBW.__init__
#
# Purpose
#    Package for database wrappers
#
# Revision Dates
#    20-Sep-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM                   import MOM
from   _TFL.Package_Namespace import Package_Namespace

DBW = Package_Namespace ()
MOM._Export ("DBW")

del Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`MOM.DBW` contains packages with database wrappers for various backends.

"""

### __END__ MOM.DBW.__init__

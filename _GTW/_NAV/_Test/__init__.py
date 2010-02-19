# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This package is part of the package GTW.NAV.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.Test.__init__
#
# Purpose
#    Some test helpers
#
# Revision Dates
#    19-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL.Package_Namespace import Package_Namespace
from   _GTW                   import GTW

Test = Package_Namespace ()
GTW.NAV._Export ("Test")

del Package_Namespace

### __END__ GTW.NAV.Test.__init__

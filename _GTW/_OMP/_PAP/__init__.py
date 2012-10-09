# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This package is part of the package GTW.OMP.
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
#    GTW.OMP.PAP.__init__
#
# Purpose
#    Package defining a partial object model for Persons, Addresses, and
#    Phone-Numbers
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#     9-Oct-2012 (CT) Add `_desc_`
#    ««revision-date»»···
#--

from   _GTW._OMP              import OMP
from   _MOM                   import MOM
from   _TFL.Package_Namespace import Derived_Package_Namespace

_desc_ = """
Partial object model for (natural and legal) persons and their (contact)
properties.
"""

PAP = Derived_Package_Namespace (parent = MOM)
OMP._Export ("PAP")

del Derived_Package_Namespace

### __END__ GTW.OMP.PAP.__init__

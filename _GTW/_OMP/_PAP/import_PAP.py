# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.import_PAP
#
# Purpose
#    Import PAP object model
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    13-Oct-2010 (CT) `Entity_created_by_Person` added
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Address
import _GTW._OMP._PAP.Email
import _GTW._OMP._PAP.Entity
import _GTW._OMP._PAP.Phone
import _GTW._OMP._PAP.Person

import _GTW._OMP._PAP.Person_has_Address
import _GTW._OMP._PAP.Entity_created_by_Person
import _GTW._OMP._PAP.Person_has_Email
import _GTW._OMP._PAP.Person_has_Phone

### __END__ GTW.OMP.PAP.import_PAP

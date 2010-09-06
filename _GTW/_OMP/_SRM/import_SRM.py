# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.import_SRM
#
# Purpose
#    Import SRM object model
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#    19-Apr-2010 (CT) Creation continued
#    31-Aug-2010 (CT) `Team` and `Team_has_Boat_in_Regatta` added
#     6-Sep-2010 (CT) `Race_Result` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Attr_Type

import _GTW._OMP._SRM.Boat_Class
import _GTW._OMP._SRM.Boat
import _GTW._OMP._SRM.Entity
import _GTW._OMP._SRM.Page
import _GTW._OMP._SRM.Race_Result
import _GTW._OMP._SRM.Regatta_Event
import _GTW._OMP._SRM.Regatta
import _GTW._OMP._SRM.Sailor
import _GTW._OMP._SRM.Team

import _GTW._OMP._SRM.Boat_in_Regatta
import _GTW._OMP._SRM.Crew_Member
import _GTW._OMP._SRM.Team_has_Boat_in_Regatta


### __END__ GTW.OMP.SRM.import_SRM

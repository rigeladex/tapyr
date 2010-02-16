# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.NAV.
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
#    app_import
#
# Purpose
#    Import for the object model
#
# Revision Dates
#    20-Jan-2010 (MG) Creation
#    ««revision-date»»···
#--
from   _MOM            import MOM
from   _GTW            import GTW
import _GTW._OMP._Auth.import_Auth
import _GTW._OMP._PAP. import_PAP
import _GTW._OMP._SWP.Page

from   _MOM._EMS.Hash         import Manager as EMS
from   _MOM._DBW._HPS.Manager import Manager as DBW

app_type = MOM.App_Type \
    ( u"HWO", GTW
    , PNS_Aliases = dict
        ( Auth = GTW.OMP.Auth
        , PAP  = GTW.OMP.PAP
        , SWP  = GTW.OMP.SWP
        )
    ).Derived (EMS, DBW)

### __END__ app_import

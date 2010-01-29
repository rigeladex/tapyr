# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    29-Jan-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin

from   _GTW._Form._MOM.Inline_Description import Inline_Description as ID
from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )

_prim = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Person = dict \
        ( ETM     = "GTW.OMP.PAP.Person"
        , Type    = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (WF ("primary"), widget = "html/form.jnj, fg_tr")
            , FGD ()
            )
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.PAP._Export_Module ()
### __END__ GTW.OMP.PAP.Nav

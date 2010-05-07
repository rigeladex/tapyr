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
#    GTW.OMP.SRM.Crew_Member
#
# Purpose
#    Crew member of a `Boat_in_Regatta`
#
# Revision Dates
#    19-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._PAP.Person

import _GTW._OMP._SRM.Boat_in_Regatta
import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Crew_Member (_Ancestor_Essence) :
    """Crew member of a `Boat_in_Regatta`."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """`Boat_in_Regatta` the crew member sails on."""

            role_type          = GTW.OMP.SRM.Boat_in_Regatta
            auto_cache         = "crew"

        # end class left

        class member (A_Object) :
            """Person which sails as crew member on `boat_in_regatta`"""

            Class              = GTW.OMP.SRM.Sailor
            kind               = Attr.Primary

        # end class member

        ### Non-primary attributes

        class role (A_String) :
            """Role of crew member."""

            kind               = Attr.Optional
            max_length         = 32

        # end class role

    # end class _Attributes

# end class Crew_Member

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Crew_Member

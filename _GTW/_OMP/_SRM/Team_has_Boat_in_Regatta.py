# -*- coding: iso-8859-15 -*-
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
#    GTW.OMP.SRM.Team_has_Boat_in_Regatta
#
# Purpose
#    `Boat_in_Regatta` sailing for `Team`
#
# Revision Dates
#    31-Aug-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Boat_in_Regatta
import _GTW._OMP._SRM.Entity
import _GTW._OMP._SRM.Team

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link2

class Team_has_Boat_in_Regatta (_Ancestor_Essence) :
    """`Boat_in_Regatta` sailing for `Team`"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Sailing team boats sail for in regatta."""

            role_type          = GTW.OMP.SRM.Team
            auto_cache         = True

        # end class left

        class right (_Ancestor.right) :
            """`Boat_in_Regatta` sailing for team."""

            role_type          = GTW.OMP.SRM.Boat_in_Regatta
            role_name          = "boat"
            auto_cache         = True

        # end class right

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class valid_regatta (Pred.Condition) :

            kind               = Pred.Object
            assertion          = "team.regatta is boat.regatta"
            attributes         = ("team.regatta", "boat.regatta")

        # end class valid_regatta

    # end class _Predicates

# end class Team_has_Boat_in_Regatta

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Team_has_Boat_in_Regatta

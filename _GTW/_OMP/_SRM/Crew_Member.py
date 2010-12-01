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
#    13-Oct-2010 (CT) Derive from `Link2` instead of `Link1`
#     1-Dec-2010 (CT) `key` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._PAP.Person

import _GTW._OMP._SRM.Boat_in_Regatta
import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link2

class Crew_Member (_Ancestor_Essence) :
    """Crew member of a `Boat_in_Regatta`."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """`Boat_in_Regatta` the crew member sails on."""

            role_type          = GTW.OMP.SRM.Boat_in_Regatta

        # end class left

        class right (_Ancestor.right) :
            """Person which sails as crew member on `boat_in_regatta`"""

            role_type          = GTW.OMP.SRM.Sailor
            auto_cache         = "_crew"

        # end class right

        ### Non-primary attributes

        class key (A_Int) :
            """The crew members of a boat will be sorted by `key`, if
               defined, by order of creation otherwise.
            """

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = 0

        # end class key

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

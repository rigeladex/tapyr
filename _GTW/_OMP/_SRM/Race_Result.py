# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.SRM.Race_Result
#
# Purpose
#    Race result of a `Boat_in_Regatta`
#
# Revision Dates
#     6-Sep-2010 (CT) Creation
#     7-Oct-2011 (CT) `race.min_value` set to `1`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Boat_in_Regatta
import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Race_Result (_Ancestor_Essence) :
    """Race result of a `Boat_in_Regatta`."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """`Boat_in_Regatta` the crew member sails on."""

            role_type          = GTW.OMP.SRM.Boat_in_Regatta
            auto_cache         = "race_results"

        # end class left

        class race (A_Int) :
            """Number of race."""

            kind               = Attr.Primary
            min_value          = 1

        # end class race

        ### Non-primary attributes

        class discarded (A_Boolean) :
            """The result of this race is discarded."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = False
            rank               = 3

        # end class discarded

        class points (A_Int) :
            """Points of boat in this race."""

            kind               = Attr.Necessary
            min_value          = 1
            rank               = 1

        # end class points

        class status (A_String) :
            """Status of boat in this race (DNS, DNF, BFD, ...)"""

            kind               = Attr.Optional
            max_length         = 8
            rank               = 2

        # end class status

    # end class _Attributes

    @property
    def ui_display_format (self) :
        result = "%(points)s"
        if self.discarded :
            result = "[" + result + "]"
        if self.status :
            result += " %(status)s"
        return result
    # end def ui_display_format

# end class Race_Result

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Race_Result

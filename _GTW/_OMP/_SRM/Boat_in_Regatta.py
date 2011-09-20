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
#    GTW.OMP.SRM.Boat_in_Regatta
#
# Purpose
#    Boat racing in a regatta
#
# Revision Dates
#    19-Apr-2010 (CT) Creation
#    10-May-2010 (CT) `place` added
#     6-Sep-2010 (CT) `race_results` removed (now implemented as `Link1`)
#    20-Sep-2010 (CT) `rank` added
#    14-Oct-2010 (CT) `Init_Only_Mixin` added to `registration_date`
#     1-Dec-2010 (CT) `crew` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Boat
import _GTW._OMP._SRM.Entity
import _GTW._OMP._SRM.Regatta
import _GTW._OMP._SRM.Sailor

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link2

class Boat_in_Regatta (_Ancestor_Essence) :
    """Boat racing in a regatta."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Boat racing in a regatta."""

            role_type          = GTW.OMP.SRM.Boat
            auto_cache         = True

            completer          = Attr.E_Completer_Spec (Attr.Selector.primary)

        # end class left

        class right (_Ancestor.right) :
            """Regatta a boat races in."""

            role_type          = GTW.OMP.SRM.Regatta

            completer          = Attr.E_Completer_Spec (Attr.Selector.primary)

        # end class right

        ### Non-primary attributes

        class crew (A_Blob) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("_crew", )

            def computed (self, obj) :
                scope = obj.home_scope
                return \
                    [ cm.sailor for cm in scope.SRM.Crew_Member.r_query
                        ( left = obj
                        , sort_key = TFL.Sorted_By ("key", "pid")
                        )
                    ]
            # end def computed

        # end class crew

        class place (A_Int) :
            """Place of boat in this regatta."""

            kind               = Attr.Optional
            min_value          = 1

        # end class place

        class points (A_Int) :
            """Total points of boat in this regatta."""

            kind               = Attr.Optional
            min_value          = 1

        # end class points

        class rank (A_Int) :
            """Rank of registration of boat in regatta."""

            kind               = Attr.Internal
            default            = 0

        # end class rank

        class registration_date (A_Date) :
            """Date of registration."""

            kind               = Attr.Internal
            Kind_Mixins        = (Attr.Init_Only_Mixin, )

            def computed_default (self) :
                return self.now ()
            # end def computed_default

        # end class registration_date

        class skipper (A_Entity) :
            """Skipper of boat."""

            Class              = GTW.OMP.SRM.Sailor
            kind               = Attr.Required

        # end class skipper

    # end class _Attributes

# end class Boat_in_Regatta

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Boat_in_Regatta

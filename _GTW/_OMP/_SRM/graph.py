# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.SRM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.SRM.graph
#
# Purpose
#    Graph describing SRM (partial) object model
#
# Revision Dates
#    17-Aug-2012 (CT) Creation
#    21-Aug-2012 (CT) Add `Team_has_Boat_in_Regatta`, `Race_Result`
#    31-Aug-2012 (CT) Adapt to MOM.Graph.Spec API change
#     3-Sep-2012 (CT) Add `Page`, specify `source_side` for `Crew_Member`
#    24-Sep-2012 (CT) Add `Command`, rename from `Graph.py` to `graph.py`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _GTW._OMP._SRM

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD

def graph (app_type) :
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.SRM.Boat_in_Regatta
            ( Role.left
                ( Role.left (offset = CD.W)
                , offset = CD.W
                )
            , Role.right
                ( Role.left
                    ( Attr.club (offset = CD.N * 2)
                    , ET.SRM.Page
                        ( Attr.event
                        , offset = CD.S
                        )
                    , offset = CD.E
                    )
                , offset = CD.E
                )
            , ET.SRM.Crew_Member
                ( Role.left  (anchor = False, source_side = "W")
                , Role.right (anchor = False, source_side = "W")
                , offset = CD.NE
                )
            , ET.SRM.Team_has_Boat_in_Regatta
                ( Role.left
                    ( ET.SRM.Regatta_C
                        ( IS_A.SRM.Regatta
                        , offset = CD.E
                        )
                    , offset = CD.S
                    )
                , offset = CD.S
                )
            , ET.SRM.Race_Result (offset = CD.SW)
            , Attr.skipper
                ( Role.left
                    ( IS_A.PAP.Subject (offset = CD.E * 2)
                    , offset = CD.N
                    )
                , Attr.club (IS_A.PAP.Subject)
                , offset = CD.N * 2
                )
            )
        )
# end def graph

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
else :
    import _GTW._OMP._PAP.import_PAP
    import _GTW._OMP._SRM.import_SRM
    import _MOM._Graph.Command

    class Command (MOM.Graph.Command) :

        PNS                   = GTW.OMP.SRM

        PNS_Aliases           = dict \
            ( PAP             = GTW.OMP.PAP
            , SRM             = GTW.OMP.SRM
            )

    # end class Command

    command = Command ()
    command ()
### __END__ GTW.OMP.SRM.graph

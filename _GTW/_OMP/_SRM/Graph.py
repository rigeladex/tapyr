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
#    GTW.OMP.SRM.Graph
#
# Purpose
#    Graph describing SRM (partial) object model
#
# Revision Dates
#    17-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _GTW._OMP._SRM

from   _MOM._Graph.Spec       import ET
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD

def graph (app_type) :
    return MOM.Graph.Spec.Graph \
        ( app_type
        , ET.SRM.Boat_in_Regatta
            ( W      = ET.SRM.Boat    (left  = CD.W)
            , E      = ET.SRM.Regatta
                ( left   = ET.SRM.Regatta_Event
                    ( club   = ET.SRM.Club (offset = CD.N * 2)
                    , offset = CD.E
                    )
                )
            , N_E    = ET.SRM.Crew_Member
            , skipper  = ET.SRM.Sailor
                ( club   = ET.SRM.Club
                , offset = CD.N * 2
                , N      = ET.PAP.Person
                )
            )
        )
# end def graph

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Graph

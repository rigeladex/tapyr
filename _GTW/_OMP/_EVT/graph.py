# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.EVT.
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
#    GTW.OMP.EVT.graph
#
# Purpose
#    Graph describing EVT (partial) object model
#
# Revision Dates
#    24-Sep-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

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
        , ET.EVT.Event
            ( Role.left     (offset = CD.W)
            , Attr.calendar (offset = CD.N)
            , ET.EVT.Recurrence_Spec
                ( ET.EVT.Recurrence_Rule (offset = CD.E)
                , offset = CD.E
                )
            )
        )
# end def graph

if __name__ != "__main__" :
    GTW.OMP.EVT._Export ("*")
else :
    import _GTW._OMP._EVT.import_EVT
    import _GTW._OMP._SWP.import_SWP
    import _MOM._Graph.Command

    class Command (MOM.Graph.Command) :

        PNS                   = GTW.OMP.EVT

        PNS_Aliases           = dict \
            ( EVT             = GTW.OMP.EVT
            , SWP             = GTW.OMP.SWP
            )

    # end class Command

    command = Command ()
    command ()
### __END__ GTW.OMP.EVT.graph

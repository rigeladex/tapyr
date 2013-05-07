# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.graph
#
# Purpose
#    Graph describing PAP (partial) object model
#
# Revision Dates
#    24-Sep-2012 (CT) Creation
#    11-Oct-2012 (CT) Add `Address_Position`, `Url`
#    12-Oct-2012 (CT) Add `Nickname` if provided by `PAP`, i.e., was imported
#     9-Nov-2012 (CT) Add `IM_Handle` if provided by `PAP`, i.e., was imported
#     9-Nov-2012 (CT) Rotate graph by roughly 90 degrees
#     7-May-2013 (CT) Add `Association`, `Person_has_Account`, if imported
#     7-May-2013 (CT) Shift `Subject_has_Property` to center of graph
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM                   import MOM
from   _TFL                   import TFL

import _GTW._OMP._PAP

from   _MOM._Graph.Spec       import Attr, Child, ET, IS_A, Role, Skip

import _MOM._Graph.Command
import _MOM._Graph.Entity

from   _TFL._D2               import Cardinal_Direction as CD
from   _TFL.I18N              import _, _T

def graph (app_type) :
    result = MOM.Graph.Spec.Graph \
        ( app_type
        , ET.PAP.Subject_has_Property
            ( Role.left
                ( Child.PAP.Company
                    ( offset      = CD.NW
                    , source_side = "E"
                    , target_side = "W"
                    )
                , Child.PAP.Person
                    ( offset      = CD.N
                    , source_side = "W"
                    , target_side = "W"
                    )
                , offset = CD.W
                )
            , Role.right
                ( Child.PAP.Address
                    ( ET.PAP.Address_Position
                        ( label  = "_Position"
                        , offset = CD.W
                        )
                    , offset      = CD.S + 2 * CD.W
                    )
                , Child.PAP.Email
                    ( offset      = CD.SW
                    )
                , Child.PAP.Phone
                    ( offset      = CD.S
                    )
                , Child.PAP.Url
                    ( offset      = CD.SE
                    , source_side = "W"
                    , target_side = "E"
                    )
                , offset = CD.E
                )
            )
        , desc  = _T ("Graph displaying PAP partial object model")
        , title = _T ("PAP graph")
        )
    if hasattr (GTW.OMP.PAP, "Association") :
        result ["PAP.Subject"]._add \
            ( Child.PAP.Association
                ( offset      = CD.W
                )
            )
    if hasattr (GTW.OMP.PAP, "IM_Handle") :
        result ["PAP.Property"]._add \
            ( Child.PAP.IM_Handle
                ( offset      = CD.E
                )
            )
    if hasattr (GTW.OMP.PAP, "Nickname") :
        result ["PAP.Property"]._add \
            ( Child.PAP.Nickname
                ( offset      = CD.NE
                , source_side = "W"
                , target_side = "E"
                )
            )
    if hasattr (GTW.OMP.PAP, "Person_has_Account") :
        result ["PAP.Person"]._add \
            ( ET.PAP.Person_has_Account
                ( Role.left  (guide_offset = 1.0)
                , Role.right
                    ( offset  = CD.E
                    )
                , offset      = CD.E
                )
            )
    return result
# end def graph

class Command (MOM.Graph.Command) :

    @property
    def PNS (self) :
        return GTW.OMP.PAP
    # end def PNS

    @property
    def PNS_Aliases (self) :
        return dict \
            ( PAP             = GTW.OMP.PAP
            )
    # end def PNS_Aliases

# end class Command

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
else :
    import _GTW._OMP._PAP.import_PAP
    Command () ()
### __END__ GTW.OMP.PAP.graph

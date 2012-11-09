# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
                    ( offset      = CD.N
                    )
                , Child.PAP.Person
                    ( offset      = CD.NE
                    )
                , offset = CD.W
                )
            , Role.right
                ( Child.PAP.Address
                    ( ET.PAP.Address_Position
                        ( label  = "_Position"
                        , offset = CD.E
                        )
                    , offset      = CD.N
                    )
                , Child.PAP.Email
                    ( offset      = CD.E
                    )
                , Child.PAP.Phone
                    ( offset      = CD.SW
                    )
                , Child.PAP.Url
                    ( offset      = CD.S
                    )
                , offset = CD.E
                )
            , Child.PAP.Subject_has_Phone
                ( guide_offset = 1
                , offset       = CD.SW
                )
            )
        , desc  = _T ("Graph displaying PAP partial object model")
        , title = _T ("PAP graph")
        )
    if hasattr (GTW.OMP.PAP, "IM_Handle") :
        result ["PAP.Property"]._add \
            ( Child.PAP.IM_Handle
                ( offset      = CD.E * 2
                , source_side = "S"
                , target_side = "S"
                )
            )
    if hasattr (GTW.OMP.PAP, "Nickname") :
        result ["PAP.Property"]._add \
            ( Child.PAP.Nickname
                ( offset      = CD.SE
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

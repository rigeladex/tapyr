# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    29-Jan-2010 (CT) Creation
#     2-Feb-2010 (MG) `legend` and `title` added
#     3-Feb-2010 (MG) Completer added
#     3-Feb-2010 (MG) Use new `Role_Description`
#     5-Feb-2010 (MG) Adapted to new form handling
#     5-Feb-2010 (MG) First completer added
#     8-Feb-2010 (MG) Fixed `Person` form spec: `position` now is a
#                     composite attribute
#    ««revision-date»»···
#--

from   _TFL.I18N                import _
from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin
import _GTW._Form._MOM.Completer

from   _GTW._Form._MOM.Inline_Description      import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )
from  _GTW._Form.Widget_Spec  import Widget_Spec as WS

_prim = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Address         = dict \
        ( ETM       = "GTW.OMP.PAP.Address"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (WF ("primary"))
            , FGD ("desc")
            , AID
                ( "position"
                , FGD
                    ( "lon", "lat", "height"
                    , widget = "html/form.jnj, fg_tr"
                    )
                )
            )
        )

    Email           = dict \
        ( ETM       = "GTW.OMP.PAP.Email"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (WF ("primary"))
            , FGD ()
            )
        , list_display = ("ui_display", "desc")
        )

    Person          = dict \
        ( ETM       = "GTW.OMP.PAP.Person"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (WF ("primary"), widget = "html/form.jnj, fg_tr")
            , AID
                ( "date"
                , FGD (WF (), widget = "html/form.jnj, fg_tr")
                , legend    = _("Geburtstag")
                )
            , LID
                ( "PAP.Person_has_Address"
                , FGD ( "desc")
                , AID
                    ( "address"
                    , FGD (WF ("primary"))
                    , completer     = GTW.Form.MOM.Completer
                        ( fields    = ("street", "city", "zip", "country")
                        , triggers  = dict (street = dict (min_chars = 3))
                        , name      = "Personal_Contact_Info"
                        )
                    )
                , legend    = _("Addresses")
                , title     = _("Addresses")
                )
            , LID
                ( "PAP.Person_has_Phone"
                , FGD ( "desc")
                , AID ( "phone", FGD (WF ("primary"))
                      )
                , FGD ( "extension")
                , legend    = _("Phone numbers")
                , title     = _("Phone numbers")
                )
            )
        , list_display = ("ui_display", "date")
        )

    Phone           = dict \
        ( ETM       = "GTW.OMP.PAP.Phone"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (WF ("primary"))
            , FGD ()
            )
        , list_display = ("ui_display", "desc")
        )

    Person_has_Phone = dict \
        ( ETM       = "GTW.OMP.PAP.Person_has_Phone"
        , Type      = GTW.NAV.E_Type.Admin
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.PAP._Export_Module ()
### __END__ GTW.OMP.PAP.Nav

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
#    27-Feb-2010 (MG) Additional completers added
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin
import _GTW._Form._MOM.Javascript

from   _GTW._Form._MOM.Inline_Description      import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )
from  _GTW._Form.Widget_Spec    import Widget_Spec as WS

from   _TFL.I18N                import _

primary = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    address_completer = GTW.Form.Javascript.Multi_Completer \
        ( GTW.Form.MOM.Javascript.Completer
            ( fields    = ("street", "city", "zip", "country")
            , triggers  = dict (street = dict (min_chars = 3))
            )
        , zip       = GTW.Form.MOM.Javascript.Field_Completer
            ( "zip", ("zip", "city", "country", "region")
            , min_chars = 1
            )
        , city      = GTW.Form.MOM.Javascript.Field_Completer
            ( "city", ("city", "country", "region")
            , min_chars = 2
            )
        , name      = "GTW.OMP.PAP.Address"
        )

    email_completer = GTW.Form.MOM.Javascript.Completer \
        ( fields    = ("address", )
        , triggers  = dict (address = dict (min_chars = 2))
        , name      = "Email_Completer"
        )

    person_completer = GTW.Form.MOM.Javascript.Completer \
        ( fields    = ("last_name", "first_name", "middle_name", "title")
        , triggers  = dict (last_name = dict (min_chars = 2))
        , name      = "GTW.OMP.PAP.Person"
        )

    phone_completer = GTW.Form.MOM.Javascript.Completer \
        ( fields    = ("country_code", "area_code", "number")
        , triggers  = dict (number = dict (min_chars = 2))
        , name      = "Phone_Completer"
        )

    def Person_has_LID (link_type_name) :
        person_completer = GTW.Form.Javascript._Completer_ ["GTW.OMP.PAP.Person"]
        return LID \
            ( link_type_name
            , FGD ( "desc", "person")
            , legend      = _("Persons")
            , title       = _("Persons")
            , field_attrs = dict (person = dict (completer = person_completer))
            )
    # end def Person_has_LID

    Address         = dict \
        ( ETM       = "GTW.OMP.PAP.Address"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD ( primary, "desc", "position")
            , Person_has_LID ("PAP.Person_has_Address")
            )
        , list_display   = ("zip", "city", "street", "desc")
        , sort_key       = TFL.Sorted_By ( "zip", "street")
        )

    Email           = dict \
        ( ETM       = "GTW.OMP.PAP.Email"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD ()
            , Person_has_LID ("PAP.Person_has_Email")
            )
        , list_display = ("ui_display", "desc")
        )

    Person = dict \
        ( ETM       = "GTW.OMP.PAP.Person"
        , Form_args =
            [ FGD
                ( primary
                , completer = GTW.Form.MOM.Javascript.Field_Completer
                    ( "last_name", ("last_name", )
                    , min_chars = 2
                    )
                , render_mode = "table"
                )
            , FGD ("lifetime", WF ())
            , LID
                ( "GTW.OMP.PAP.Person_has_Phone"
                , FGD
                    ( "desc"
                    , AID
                        ( "phone", render_mode = "div_seq"
                        , legend = _ ("Phone")
                        )
                    )
                , list_display     = ("desc", "phone")
                , collapsable      = True
                )
            , LID
                ( "GTW.OMP.PAP.Person_has_Email"
                , FGD
                    ( "desc"
                    , AID
                        ("email", render_mode = "div_seq"
                        , legend = _ ("Email")
                        )
                    )
                , list_display     = ("desc", "email")
                , collapsable      = True
                )
            , LID
                ( "GTW.OMP.PAP.Person_has_Address"
                , FGD
                    ( "desc"
                    , AID
                        ("address", render_mode = "div_seq"
                        , legend = _ ("Address")
                        , completer = address_completer
                        )
                    )
                , list_display     = ("desc", "address")
                , collapsable      = True
                , popup            = False
                )
            ]
        )
    Phone           = dict \
        ( ETM       = "GTW.OMP.PAP.Phone"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (primary)
            , FGD ()
            , Person_has_LID ("PAP.Person_has_Phone")
            )
        , list_display = ("ui_display", "desc")
        )

    Person_has_Address = dict \
        ( ETM       = "GTW.OMP.PAP.Person_has_Address"
        , Type      = GTW.NAV.E_Type.Admin
        )

    Person_has_Email = dict \
        ( ETM       = "GTW.OMP.PAP.Person_has_Email"
        , Type      = GTW.NAV.E_Type.Admin
        )

    Person_has_Phone = dict \
        ( ETM       = "GTW.OMP.PAP.Person_has_Phone"
        , Type      = GTW.NAV.E_Type.Admin
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.PAP._Export_Module ()
### __END__ GTW.OMP.PAP.Nav

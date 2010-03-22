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
        , name      = "Address_Completer"
        )

    email_completer = GTW.Form.MOM.Javascript.Completer \
        ( fields    = ("address", )
        , triggers  = dict (address = dict (min_chars = 2))
        , name      = "Email_Completer"
        )

    person_completer = GTW.Form.MOM.Javascript.Completer \
        ( fields    = ("last_name", "first_name", "middle_name", "title")
        , triggers  = dict (last_name = dict (min_chars = 2))
        , name      = "Person_Completer"
        )

    phone_completer = GTW.Form.MOM.Javascript.Completer \
        ( fields    = ("country_code", "area_code", "number")
        , triggers  = dict (number = dict (min_chars = 2))
        , name      = "Phone_Completer"
        )

    Address         = dict \
        ( ETM       = "GTW.OMP.PAP.Address"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (primary)
            , FGD ("desc")
            , AID
                ( "position"
                , FGD
                    ( "lon", "lat", "height"
                    , widget = "html/form.jnj, fg_tr"
                    )
                )
            , LID
                ( "PAP.Person_has_Address"
                , FGD ( "desc")
                , AID
                    ( "person"
                    , FGD (primary)
                    , completer = person_completer
                    )
                , legend    = _("Persons")
                , title     = _("Persons")
                )
            )
        , list_display   = ("zip", "city", "street", "desc")
        , sort_key       = TFL.Sorted_By ( "zip", "street")
        )

    Email           = dict \
        ( ETM       = "GTW.OMP.PAP.Email"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (primary)
            , FGD ()
            , LID
                ( "PAP.Person_has_Email"
                , FGD ( "desc")
                , AID
                    ( "person"
                    , FGD (primary)
                    , completer = person_completer
                    )
                , legend    = _("Persons")
                , title     = _("Persons")
                )
            )
        , list_display = ("ui_display", "desc")
        )

    Person          = dict \
        ( ETM       = "GTW.OMP.PAP.Person"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD
                ( primary
                , completer = GTW.Form.MOM.Javascript.Field_Completer
                    ( "last_name", ("last_name", )
                    , min_chars = 2
                    )
                , widget    = "html/form.jnj, fg_tr"
                )
            , AID
                ( "lifetime"
                , FGD (widget = "html/form.jnj, fg_tr")
                , legend    = _("Lifetime")
                )
            , LID
                ( "PAP.Person_has_Phone"
                , FGD ( "desc")
                , AID
                    ( "phone"
                    , FGD (primary)
                    , completer = phone_completer
                    )
                , FGD ( "extension")
                , legend    = _("Phone numbers")
                , title     = _("Phone numbers")
                )
            , LID
                ( "PAP.Person_has_Email"
                , FGD ( "desc")
                , AID
                    ( "email"
                    , FGD (primary)
                    , completer = email_completer
                    )
                , legend    = _("Email addresses")
                , title     = _("Email addresses")
                )
            , LID
                ( "PAP.Person_has_Address"
                , FGD ( "desc")
                , AID
                    ( "address"
                    , FGD (primary)
                    , completer = address_completer
                    )
                , legend    = _("Addresses")
                , title     = _("Addresses")
                )
            )
        # list_display = ("ui_display", "lifetime")
        , list_display = ("last_name", "first_name", "middle_name", "title", "lifetime")
        )

    Phone           = dict \
        ( ETM       = "GTW.OMP.PAP.Phone"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD (primary)
            , FGD ()
            , LID
                ( "PAP.Person_has_Phone"
                , FGD ( "desc")
                , AID
                    ( "person"
                    , FGD (primary)
                    , completer = person_completer
                    )
                , FGD ( "extension")
                , legend    = _("Persons")
                , title     = _("Persons")
                )
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

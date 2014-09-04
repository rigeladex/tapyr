# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Mag. Christian Tanzer All rights reserved
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
#    13-Oct-2010 (CT) `Entity_created_by_Person` added
#    15-Mar-2011 (CT) Definitions for `GTW.AFS` added
#    19-May-2011 (CT) More definitions for `GTW.AFS` added
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Remove `Form_args`, `*_completer`,
#                     i.e., stuff related to non-AFS forms
#    22-Mar-2012 (CT) Add `Company` and its links
#    11-Oct-2012 (CT) Add `Address_Position`, `Url`
#     6-Dec-2012 (CT) Remove `Entity_created_by_Person`
#    12-Dec-2012 (CT) Add `Person_has_Account`
#    12-Dec-2012 (CT) Add `accounts` to `include_links` of `Person`
#     7-May-2013 (CT) Add `IM_Handle`, `Nickname`
#     7-May-2013 (CT) Add `Association`, `_import_association_cb`
#     7-May-2013 (CT) Add `urls` to `include_links` of `Person`
#    15-May-2013 (CT) Use `*_links` for `include_links`
#    21-Aug-2014 (CT) Replace `GTW.AFS` specification by `MF3_Form_Spec`
#     4-Sep-2014 (CT) Add `Adhoc_Group`, `Id_Entity_permits_Group`,
#                     `Person_in_Group`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    property_include_rev_refs = \
        ("persons", "companies", "associations")

    subject_include_rev_refs  = \
        ("addresses", "emails", "phones")

    Address              = dict \
        ( ETM            = "GTW.OMP.PAP.Address"
        , list_display   = ("zip", "city", "street", "desc")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = ("gps", ) + property_include_rev_refs
            )
        , sort_key       = TFL.Sorted_By ( "zip", "street")
        )

    Adhoc_Group          = dict \
        ( ETM            = "GTW.OMP.PAP.Adhoc_Group"
        )

    Association          = dict \
        ( ETM            = "GTW.OMP.PAP.Association"
        , list_display   = ("name", "short_name", "lifetime")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = subject_include_rev_refs
            )
        )

    Company              = dict \
        ( ETM            = "GTW.OMP.PAP.Company"
        , list_display   = ("name", "short_name", "lifetime")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = subject_include_rev_refs
            )
        )

    Email                = dict \
        ( ETM            = "GTW.OMP.PAP.Email"
        , list_display   = ("ui_display", "desc")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = property_include_rev_refs
            )
        )

    IM_Handle            = dict \
        ( ETM            = "GTW.OMP.PAP.IM_Handle"
        , list_display   = ("ui_display", "desc")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = property_include_rev_refs
            )
        )

    Nickname             = dict \
        ( ETM            = "GTW.OMP.PAP.Nickname"
        , list_display   = ("ui_display", "desc")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = property_include_rev_refs
            )
        )

    Person               = dict \
        ( ETM            = "GTW.OMP.PAP.Person"
        , list_display   =
            ( "last_name", "first_name", "middle_name", "title"
            , "lifetime", "sex"
            )
        , MF3_Form_Spec  = dict
            ( include_rev_refs =
                (subject_include_rev_refs + ("im_handles", "accounts"))
            )
        )

    Phone                = dict \
        ( ETM            = "GTW.OMP.PAP.Phone"
        , list_display   = ("ui_display", "desc")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = property_include_rev_refs
            )
        )

    Url                  = dict \
        ( ETM            = "GTW.OMP.PAP.Url"
        , list_display   = ("ui_display", "desc")
        , MF3_Form_Spec  = dict
            ( include_rev_refs = property_include_rev_refs
            )
        )

    Address_Position     = dict \
        ( ETM            = "GTW.OMP.PAP.Address_Position"
        )

    Company_has_Address  = dict \
        ( ETM            = "GTW.OMP.PAP.Company_has_Address"
        )

    Company_has_Email    = dict \
        ( ETM            = "GTW.OMP.PAP.Company_has_Email"
        )

    Company_has_Phone    = dict \
        ( ETM            = "GTW.OMP.PAP.Company_has_Phone"
        )

    Company_has_Url      = dict \
        ( ETM            = "GTW.OMP.PAP.Company_has_Url"
        )

    Id_Entity_permits_Group = dict \
        ( ETM            = "GTW.OMP.PAP.Id_Entity_permits_Group"
        )

    Person_has_Account   = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Account"
        )

    Person_has_Address   = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Address"
        )

    Person_has_Email     = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Email"
        )

    Person_has_IM_Handle = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_IM_Handle"
        )

    Person_has_Nickname  = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Nickname"
        )

    Person_has_Phone     = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Phone"
        )

    Person_has_Url       = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Url"
        )

    Person_in_Group      = dict \
        ( ETM            = "GTW.OMP.PAP.Person_in_Group"
        , sort_key       = TFL.Sorted_By ("pid") ### XXX remove this
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.PAP._Export_Module ()
### __END__ GTW.OMP.PAP.Nav

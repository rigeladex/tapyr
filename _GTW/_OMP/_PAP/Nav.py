# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Address              = dict \
        ( ETM            = "GTW.OMP.PAP.Address"
        , list_display   = ("zip", "city", "street", "desc")
        , sort_key       = TFL.Sorted_By ( "zip", "street")
        )

    Company              = dict \
        ( ETM            = "GTW.OMP.PAP.Company"
        , list_display   = ("name", "short_name", "lifetime")
        )

    Email                = dict \
        ( ETM            = "GTW.OMP.PAP.Email"
        , list_display   = ("ui_display", "desc")
        )

    Person               = dict \
        ( ETM            = "GTW.OMP.PAP.Person"
        , list_display   =
            ( "last_name", "first_name", "middle_name", "title"
            , "lifetime", "sex"
            )
        )

    Phone                = dict \
        ( ETM            = "GTW.OMP.PAP.Phone"
        , list_display   = ("ui_display", "desc")
        )

    Url                  = dict \
        ( ETM            = "GTW.OMP.PAP.Url"
        , list_display   = ("ui_display", "desc")
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

    Entity_created_by_Person = dict \
        ( ETM            = "GTW.OMP.PAP.Entity_created_by_Person"
        , list_display   = ("entity", "creator", "date")
        )

    Person_has_Address   = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Address"
        )

    Person_has_Email     = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Email"
        )

    Person_has_Phone     = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Phone"
        )

    Person_has_Url       = dict \
        ( ETM            = "GTW.OMP.PAP.Person_has_Url"
        )

# end class Admin

from   _GTW._AFS._MOM import Spec
import _GTW._OMP._PAP.Company
import _GTW._OMP._PAP.Person

GTW.OMP.PAP.Company.GTW.afs_spec = Spec.Entity \
    (include_links = ("addresses", "emails", "phones"))
GTW.OMP.PAP.Person.GTW.afs_spec = Spec.Entity \
    (include_links = ("addresses", "emails", "phones"))
GTW.OMP.PAP.Address.GTW.afs_spec = Spec.Entity \
    (include_links = ("persons", "companies", "PAP.Address_Position"))
GTW.OMP.PAP.Email.GTW.afs_spec = Spec.Entity \
    (include_links = ("persons", "companies"))
GTW.OMP.PAP.Phone.GTW.afs_spec = Spec.Entity \
    (include_links = ("persons", "companies"))
GTW.OMP.PAP.Url.GTW.afs_spec = Spec.Entity \
    (include_links = ("persons", "companies"))

from   _MOM import MOM
import _MOM._Attr.Date_Interval
import _MOM._Attr.Position
import _MOM._Attr.Time_Interval

MOM.Attr.Date_Interval.GTW.afs_kw = dict (renderer = "afs_fc_horizo")
MOM.Attr.Position.GTW.afs_kw      = dict (renderer = "afs_fc_horizo")
MOM.Attr.Time_Interval.GTW.afs_kw = dict (renderer = "afs_fc_horizo")

if __name__ != "__main__" :
    GTW.OMP.PAP._Export_Module ()
### __END__ GTW.OMP.PAP.Nav

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Attr_Type
#
# Purpose
#    Define attribute types for package GTW.OMP.SRM
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#    28-Apr-2010 (CT) `Race_Result.ui_display_format` redefined
#    11-May-2010 (CT) `A_Regatta_Result` added
#    12-May-2010 (CT) `A_Nation.Table` filled with `unicode` instead of `str`
#     6-Sep-2010 (CT) `Race_Result` removed (now implemented as `Link1`)
#    13-Oct-2010 (CT) `example` added
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Composite_, _A_Named_Object_

import _GTW._OMP._SRM

from   _TFL.I18N                import _, _T, _Tn

class A_Nation (_A_Named_Object_) :
    """Nation a boat or sailor sails for."""

    ### http://en.wikipedia.org/wiki/List_of_IOC_country_codes

    example    = u"AUT"
    typ        = "Nation"
    Table      = \
        { u"AUS" :  _(u"Australia")
        , u"AUT" :  _(u"Austria")
        , u"BEL" :  _(u"Belgium")
        , u"CAN" :  _(u"Canada")
        , u"CRO" :  _(u"Croatia")
        , u"CYP" :  _(u"Cyprus")
        , u"CZE" :  _(u"Czech Republic")
        , u"DEN" :  _(u"Denmark")
        , u"ESP" :  _(u"Spain")
        , u"EST" :  _(u"Estonia")
        , u"FIN" :  _(u"Finland")
        , u"FRA" :  _(u"France")
        , u"GBR" :  _(u"Great Britain")
        , u"GER" :  _(u"Germany")
        , u"GRE" :  _(u"Greece")
        , u"HUN" :  _(u"Hungary")
        , u"IRL" :  _(u"Ireland")
        , u"ISL" :  _(u"Iceland")
        , u"ITA" :  _(u"Italy")
        , u"LAT" :  _(u"Latvia")
        , u"LIE" :  _(u"Lichtenstein")
        , u"LTU" :  _(u"Lithuania")
        , u"LUX" :  _(u"Luxembourg")
        , u"MLT" :  _(u"Malta")
        , u"MNE" :  _(u"Montenegro")
        , u"MON" :  _(u"Monaco")
        , u"NED" :  _(u"Netherlands")
        , u"NOR" :  _(u"Norway")
        , u"NZL" :  _(u"New Zealand")
        , u"POL" :  _(u"Poland")
        , u"POR" :  _(u"Portugal")
        , u"ROU" :  _(u"Romania")
        , u"RUS" :  _(u"Russia")
        , u"SLO" :  _(u"Slovenia")
        , u"SRB" :  _(u"Serbia")
        , u"SUI" :  _(u"Switzerland")
        , u"SVK" :  _(u"Slovakia")
        , u"SWE" :  _(u"Sweden")
        , u"UKR" :  _(u"Ukraine")
        , u"USA" :  _(u"United States")
        }

# end class A_Nation

_Ancestor_Essence = MOM.An_Entity

class Regatta_Result (_Ancestor_Essence) :
    """Provide information about the result of a regatta."""

    PNS = GTW.OMP.SRM

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class date (A_Date_Time) :
            """Date of regatta result."""

            kind               = Attr.Necessary

        # end class date

        class software (A_String) :
            """Name of software used for managing the regatta."""

            kind               = Attr.Optional

        # end class software

        class status (A_String) :
            """Status of result (e.g., `preliminary` or `final`)."""

            kind               = Attr.Optional

        # end class status

    # end class _Attributes

# end class Regatta_Result

class A_Regatta_Result (_A_Composite_) :
    """Information about a regatta's result."""

    P_Type          = Regatta_Result
    typ             = "Regatta_Result"

# end class A_Regatta_Result

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Attr_Type

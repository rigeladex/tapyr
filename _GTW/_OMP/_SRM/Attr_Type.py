# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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

    typ        = "Nation"
    Table      = dict \
        ( AUS =  _("Australia")
        , AUT =  _("Austria")
        , BEL =  _("Belgium")
        , CAN =  _("Canada")
        , CRO =  _("Croatia")
        , CYP =  _("Cyprus")
        , CZE =  _("Czech Republic")
        , DEN =  _("Denmark")
        , ESP =  _("Spain")
        , EST =  _("Estonia")
        , FIN =  _("Finland")
        , FRA =  _("France")
        , GBR =  _("Great Britain")
        , GER =  _("Germany")
        , GRE =  _("Greece")
        , HUN =  _("Hungary")
        , IRL =  _("Ireland")
        , ISL =  _("Iceland")
        , ITA =  _("Italy")
        , LAT =  _("Latvia")
        , LIE =  _("Lichtenstein")
        , LTU =  _("Lithuania")
        , LUX =  _("Luxembourg")
        , MLT =  _("Malta")
        , MNE =  _("Montenegro")
        , MON =  _("Monaco")
        , NED =  _("Netherlands")
        , NOR =  _("Norway")
        , NZL =  _("New Zealand")
        , POL =  _("Poland")
        , POR =  _("Portugal")
        , ROU =  _("Romania")
        , RUS =  _("Russia")
        , SLO =  _("Slovenia")
        , SRB =  _("Serbia")
        , SUI =  _("Switzerland")
        , SVK =  _("Slovakia")
        , SWE =  _("Sweden")
        , UKR =  _("Ukraine")
        , USA =  _("United States")
        )

# end class A_Nation

_Ancestor_Essence = MOM.An_Entity

class Race_Result (_Ancestor_Essence) :
    """Model the result of a boat in a single race."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class discarded (A_Boolean) :
            """The result of this race is discarded."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            default            = False

        # end class discarded

        class rank (A_Int) :
            """Rank of boat in this race."""

            kind               = Attr.Required
            min_value          = 1

        # end class rank

        class status (A_String) :
            """Status of boat in this race (DNS, DNF, BFD, ...)"""

            kind               = Attr.Optional
            max_length         = 8

        # end class status

    # end class _Attributes

# end class Race_Result

class A_Race_Result (_A_Composite_) :
    """Result of a boat in a single race."""

    C_Type          = Race_Result
    typ             = "Race_Result"

# end class A_Race_Result

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Attr_Type



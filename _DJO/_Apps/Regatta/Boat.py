# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    DJO.Apps.Regatta.Boat
#
# Purpose
#    Django model for sail boat
#
# Revision Dates
#    26-May-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _DJO                       import DJO
import _DJO.Models
import _DJO.Model_Field           as     MF

from   _DJO._Apps.Regatta.Boat_Class import Boat_Class

from   django.utils.translation   import gettext_lazy as _

### http://en.wikipedia.org/wiki/List_of_IOC_country_codes
nations = \
    ( ("AUS", _("Australia"))
    , ("AUT", _("Austria"))
    , ("BEL", _("Belgium"))
    , ("CAN", _("Canada"))
    , ("CRO", _("Croatia"))
    , ("CYP", _("Cyprus"))
    , ("CZE", _("Czech Republic"))
    , ("DEN", _("Denmark"))
    , ("ESP", _("Spain"))
    , ("EST", _("Estonia"))
    , ("FIN", _("Finland"))
    , ("FRA", _("France"))
    , ("GBR", _("Great Britain"))
    , ("GER", _("Germany"))
    , ("GRE", _("Greece"))
    , ("HUN", _("Hungary"))
    , ("IRL", _("Ireland"))
    , ("ISL", _("Iceland"))
    , ("ITA", _("Italy"))
    , ("LAT", _("Latvia"))
    , ("LIE", _("Lichtenstein"))
    , ("LTU", _("Lithuania"))
    , ("LUX", _("Luxembourg"))
    , ("MLT", _("Malta"))
    , ("MNE", _("Montenegro"))
    , ("MON", _("Monaco"))
    , ("NED", _("Netherlands"))
    , ("NOR", _("Norway"))
    , ("NZL", _("New Zealand"))
    , ("POL", _("Poland"))
    , ("POR", _("Portugal"))
    , ("ROU", _("Romania"))
    , ("RUS", _("Russia"))
    , ("SLO", _("Slovenia"))
    , ("SRB", _("Serbia"))
    , ("SUI", _("Switzerland"))
    , ("SVK", _("Slovakia"))
    , ("SWE", _("Sweden"))
    , ("UKR", _("Ukraine"))
    , ("USA", _("United States"))
    )

class Boat (DJO.Model) :
    """Models a sail boat"""

    class Meta :
        ordering              = ["boat_class", "nation", "sailnumber"]
        verbose_name          = _("Boat")
        verbose_name_plural   = _("Boats")
    # end class Meta

    boat_class            = MF.Foreign_Key \
        ( Boat_Class
        , opt_proxy_args  = ("max_crew", "yardstick")
        , verbose_name    = _("Boat-Class")
        )
    nation                = MF.Choice \
        ( MF.Char, _("Nation")
        , choices         = nations
        , default         = "AUT"
        , help_text       = _("Nation for which the boat is registered")
        , max_length      = 3
        )
    sailnumber            = MF.Integer \
        ( _("Sail-Number")
        , blank           = True
        , help_text       = _("Sail number of the boat")
        , min_value       = 1
        , max_value       = 1000000
        , null            = True
        )
    vintage               = MF.Small_Integer \
        ( _("Vintage")
        , blank           = True
        , help_text       = _("Year of construction")
        , min_value       = 1850
        , max_value       = 2050
        , null            = True
        )
    name                  = MF.Char \
        ( _("Boat-Name")
        , blank           = True
        , help_text       = _("Name of the boat")
        , max_length      = 80
        )

    def __unicode__ (self) :
        if self.sailnumber :
            return "%s %s" % (self.nation, self.sailnumber)
        elif self.name :
            return self.name
        else :
            return "%s %s" % (self.nation, "Ohne Nr.")
    # end def __unicode__

    NAV_admin_args = dict \
        ( list_display =
            ( "boat_class", "nation", "sailnumber", "name", "vintage"
            , "max_crew"
            )
        )

# end class Boat

### __END__ Boat

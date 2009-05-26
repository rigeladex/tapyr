# -*- coding: iso-8859-1 -*-
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
#    DJO.Apps.Regatta.Boat_Class
#
# Purpose
#    Django model for sail boat class
#
# Revision Dates
#    26-May-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _DJO                       import DJO
import _DJO.Models
import _DJO.M_Field               as     MF

from   django.utils.translation   import gettext_lazy as _

class Boat_Class (DJO.Model) :
    """Models a sail boat class."""

    class Meta :
        ordering              = ["name"]
        verbose_name          = _("Boat-Class")
        verbose_name_plural   = _("Boat-Classes")
    # end class Meta

    name                  = MF.Char \
        ( _("Class-Name")
        , help_text       = _("Name of the sail boat class")
        , max_length      = 50
        )
    max_crew              = MF.Small_Integer \
        ( _("Max-Crew")
        , default         = 1
        , help_text       = _("Maximum number of crew")
        , min_value       = 1
        , max_value       = 5
        )
    yardstick             = MF.Small_Integer \
        ( _("Yardstick")
        , blank           = True
        , help_text       = _("Yardstick number")
        , min_value       = 50
        , max_value       = 200
        , null            = True
        )
    loa                   = MF.Decimal \
        ( _("LoA")
        , blank           = True
        , decimal_places  = 2
        , help_text       = _("Length overall in meters")
        , max_digits      = 4
        , min_value       = 2
        , max_value       = 25
        , null            = True
        )
    beam                  = MF.Decimal \
        ( _("Beam")
        , blank           = True
        , decimal_places  = 2
        , help_text       = _("Maximum beam in meters")
        , max_digits      = 3
        , min_value       = 0.25
        , max_value       = 5
        , null            = True
        )
    weight                = MF.Integer \
        ( _("Weight")
        , blank           = True
        , help_text       = _("Weight (fully rigged) in kilograms")
        , min_value       = 25
        , max_value       = 25000
        , null            = True
        )

    def __unicode__ (self) :
        return self.name
    # end def __unicode__

    NAV_admin_args = dict \
        ( list_display = ("name", "max_crew", "yardstick")
        )

# end class Boat_Class

### __END__ DJO.Apps.Regatta.Boat_Class

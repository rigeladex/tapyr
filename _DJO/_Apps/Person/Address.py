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
#    DJO.Apps.Person.Address
#
# Purpose
#    Django model for an address
#
# Revision Dates
#    18-May-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _DJO                          import DJO
import _DJO.Models
import _DJO.M_Field                  as     MF

from   _DJO._Apps.Person.Phone_Number import Phone_Number

from   django.db                     import models
from   django.utils.translation      import gettext_lazy as _

class Address (DJO.Model) :
    """Models an address"""

    class Meta :
        verbose_name          = _("Address")
        verbose_name_plural   = _("Addresses")
    # end class Meta

    street                =  MF.Char     \
        ( _("Street")
        , help_text       = _("Street (or place) and house number")
        , max_length      = 80
        )
    city                  =  MF.Char     \
        ( _("City")
        , max_length      = 30
        )
    zip                   = MF.Char \
        ( _("Zip")
        , max_length      = 10
        )
    region                =  MF.Char     \
        ( _("Region")
        , blank           = True
        , help_text       = _("State or province or region")
        , max_length      = 40
        , null            = True
        )
    country               =  MF.Char     \
        ( _("Country")
        , max_length      = 40
        )
    phone                 = models.ForeignKey \
        ( Phone_Number
        , blank           = True
        , null            = True
        , verbose_name    = "Phone_Number"
        )
    desc                  = MF.Char \
        ( _("Description")
        , blank           = True
        , help_text       = _("Short description of the address")
        , max_length      = 20
        )

    def components (self) :
        result = [self.street, ", ".join (self.zip, self.city)]
        if self.region :
            result.append (self.region)
        result.append (self.country)
        return result
    # end def components

    def __unicode__ (self) :
        return u"%s" % ("\n".join (str (c) for c in self.components ()), )
    # end def __unicode__

    NAV_admin_args = dict \
        ( list_display = ("street", "zip", "city", "desc")
        )

# end class Address

### __END__ DJO.Apps.Person.Address

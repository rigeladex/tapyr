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
#    DJO.Apps.Person.Person
#
# Purpose
#    Django model for persons
#
# Revision Dates
#    19-May-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _DJO                       import DJO
import _DJO.Models
import _DJO.M_Field               as     MF

from   django.utils.translation import gettext_lazy as _

class Person (DJO.Model) :
    """Models a person."""

    class Meta :
        verbose_name          = _("Person")
        verbose_name_plural   = _("Persons")
    # end class Meta

    user                  = MF.One_to_One \
        ( "auth.User"
        , editable        = False
        , verbose_name    = _("User")
        )
    emails                = MF.Many_to_Many \
        ( "Person.Email_Address"
        , blank           = True
        , verbose_name    = _("Email Addresses")
        )
    phones                = MF.Many_to_Many \
        ( "Person.Phone_Number"
        , blank           = False
        , verbose_name    = _("Phone Numbers")
        )
    addresses             = MF.Many_to_Many \
        ( "Person.Address"
        , blank           = True
        , verbose_name    = _("Addresses")
        )

# end class Person

### __END__ DJO.Apps.Person.Person

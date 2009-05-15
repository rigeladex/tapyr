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
#    DJO.Apps.Person.Phone_Number
#
# Purpose
#    Django model for phone numbers
#
# Revision Dates
#    15-May-2009 (CT) Creation
#    ««revision-date»»···
#--

### http://tools.ietf.org/html/rfc3966

from   _DJO                       import DJO
import _DJO.Forms
import _DJO.Models
import _DJO.M_Field               as     MF

from   django.utils.translation import gettext_lazy as _

class Phone_Number (DJO.Model) :
    """Models a phone number."""

    class Meta :
        verbose_name          = _("Phone_Number")
        verbose_name_plural   = _("Phone_Numbers")
    # end class Meta

    country_code          = MF.Positive_Small_Integer \
        ( _("Country-Code")
        )
    area_code             = MF.Positive_Integer \
        ( _("Area-Code")
        , blank           = True
        , null            = True
        )
    subscriber_number     = MF.Decimal \
        ( _("Subscriber-Number")
        , max_digits      = 14
        , decimal_places  = 0
        )
    extension             = MF.Positive_Integer \
        ( _("Extension")
        , blank           = True
        , help_text       = _("Extension number used in PBX")
        , null            = True
        )
    desc                  = MF.Char \
        ( _("Description")
        , blank           = True
        , help_text       = _("Short description of the phone number")
        , max_length      = 20
        )

    def components (self) :
        result = [self.country_code]
        if self.area_code :
            result.append (self.area_code)
        result.append (self.subscriber_number)
        if self.extension :
            result.append (self.extension)
        return result
    # end def components

    def __unicode__ (self) :
        return u"+%s" % ("-".join (str (c) for c in self.components ()), )
    # end def __unicode__

    display = property (__unicode__)

    NAV_admin_args = dict \
        ( list_display = ("desc", )
        )

# end class Phone_Number

### __END__ DJO.Apps.Person.Phone_Number

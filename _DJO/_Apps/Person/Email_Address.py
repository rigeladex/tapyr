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
#    DJO.Apps.Person.Email_Address
#
# Purpose
#    Django model for email addresses
#
# Revision Dates
#    18-May-2009 (CT) Creation
#    21-Aug-2009 (CT) `Nested_Form_Group_Description` added
#    ««revision-date»»···
#--

from   _DJO                       import DJO
import _DJO.Field_Group_Description
import _DJO.Models
import _DJO.Model_Field           as     MF
import _DJO.Nested_Form_Completer

from   django.utils.translation import gettext_lazy as _

class Email_Address (DJO.Model) :
    """Models an email address"""

    class Meta :
        verbose_name          = _("Email-Address")
        verbose_name_plural   = _("Email-Addresses")
    # end class Meta

    email                = MF.Email \
        ( _("Email Address")
        )

    desc                  = MF.Char \
        ( _("Description")
        , blank           = True
        , help_text       = _("Short description of the email address")
        , max_length      = 20
        )

    def __unicode__ (self) :
        return unicode (self.email)
    # end def __unicode__

    NAV_admin_args = dict \
        ( list_display = ("email", "desc")
        )

    ### Saves the `Nested_Form_Group_Description` as
    ###   `DJO.Nested_Form_Group_Description._.Personal_Email_Info`
    DJO.Nested_Form_Group_Description \
        ( "emails"
        , field_group_descriptions =
            ( DJO.Field_Group_Description
                ( "email", "desc"
                , template  = DJO.Template ["field_group_horizontal.html"]
                )
            ,
            )
        , completer = DJO.Nested_Form_Completer
            ( fields    = ("email", )
            , triggers  = dict (email = dict (min_chars = 3))
            , name      = "Personal_Email_Info"
            )
        , legend    = _("Email-Addresses")
        , template  = DJO.Template ["nested_model_form_table.html"]
        , name      = "Personal_Email_Info"
        )

# end class Email_Address

### __END__ DJO.Apps.Person.Email_Address

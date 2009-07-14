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
#    DJO.Apps.Regatta.Sailor
#
# Purpose
#    Django model for sailor
#
# Revision Dates
#    27-May-2009 (CT) Creation
#    28-May-2009 (CT) Creation continued
#     6-Jun-2009 (MG) `s/Form_Set/Field_Group/g`
#    11-Jun-2009 (CT) Use `name` for `Field_Group_Description` and reuse
#                     `Field_Group_Descriptions` defined by `Person`
#    14-Jul-2009 (CT) Use `Template` objects instead of strings
#    ««revision-date»»···
#--

from   _DJO                       import DJO
import _DJO.Field_Group_Description
import _DJO.Models
import _DJO.Model_Field           as     MF
import _DJO.Template
import _DJO._Apps.Base

from   django.utils.translation   import gettext_lazy as _

from   _DJO._Apps.Person.Person   import Person

class Sailor (DJO.Model) :
    """Modelliert die Person eines Seglers (oder Angehörigen eines Seglers)."""

    class Meta :
        verbose_name        = _("Sailor")
        verbose_name_plural = _("Sailors")
    # end class Meta

    person             = MF.One_to_One \
        ( Person
        , editable        = True
        , verbose_name    = _("Person")
        )
    club               = MF.Char \
        ( u"Club"
        , help_text    = _("Sailing club the sailor starts for")
        , max_length   = 10
        )
    oesv_nr            = MF.Integer \
        ( u"ÖSV-Nr."
        , blank        = True
        , null         = True
        , unique       = True
        )

    def __unicode__ (self) :
        return unicode (self.person)
    # end def __unicode__

    display = property (__unicode__)

    NAV_admin_args = dict \
        ( list_display = ("birth_date", "sex", "club", "oesv_nr")
        , field_group_descriptions =
              ( DJO.Field_Group_Description._.Personal_Info
              , DJO.Field_Group_Description
                  ( "club", "oesv_nr"
                  , legend    = _("Sailing club info")
                  , template  = DJO.Template ["field_group_horizontal.html"]
                  , name      = "Sailing_Club_Info"
                  )
              , DJO.Field_Group_Description
                  ( "sex"
                  , legend    = _("Sailor details")
                  , template  = DJO.Template ["field_group_horizontal.html"]
                  , name      = "Sailor_Details"
                  )
              , DJO.Field_Group_Description._.Personal_Contact_Info
              )
        )

# end class Sailor

### __END__ DJO.Apps.Regatta.Sailor

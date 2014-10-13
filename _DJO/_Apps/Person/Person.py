# -*- coding: utf-8 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#     6-Jun-2009 (MG) `s/Form_Set/Field_Group/g`
#    10-Jun-2009 (MG) `Nested_Form_Description` used for phone numbers
#    11-Jun-2009 (CT) Use `name` for `Field_Group_Description`
#    14-Jul-2009 (CT) Use `Template` objects instead of strings
#    21-Aug-2009 (CT) `Nested_Form_Group_Description` for `Phone_Number`,
#                     `Email_Address`, and `Addresses` factored
#    ««revision-date»»···
#--

from   _DJO                       import DJO
import _DJO.Field_Group_Description
import _DJO.Models
import _DJO.Model_Field           as     MF
import _DJO.Nested_Form_Completer
import _DJO.Template
import _DJO._Apps.Base

from   django.utils.translation   import gettext_lazy as _

class Person (DJO.Model) :
    """Models a person."""

    class Meta :
        ordering              = ["user"]
        verbose_name          = _("Person")
        verbose_name_plural   = _("Persons")
    # end class Meta

    user                  = MF.One_to_One \
        ( "auth.User"
        , editable        = True
        , verbose_name    = _("User")
        )
    title                 = MF.Char \
        ( _("Title")
        , blank           = True
        , help_text       = _("Academic title")
        , max_length      = 20
        )
    birth_date            = MF.Date \
        ( _("Birth-Date")
        , blank           = True
        , null            = True
        )
    sex                   = MF.Choice \
        ( MF.Char, _("Sex")
        , blank           = True
        , choices         = (("F", _("Female")), ("M", _("Male")))
        , max_length      = 1
        )
    emails                = MF.Many_to_Many \
        ( "Person.Email_Address"
        , blank           = True
        , null            = True
        , verbose_name    = _("Email Addresses")
        )
    phones                = MF.Many_to_Many \
        ( "Person.Phone_Number"
        , blank           = False
        , null            = True
        , verbose_name    = _("Phone Numbers")
        )
    addresses             = MF.Many_to_Many \
        ( "Person.Address"
        , blank           = True
        , null            = True
        , verbose_name    = _("Addresses")
        )

    @property
    def first_name (self) :
        return self.user.first_name
    # end def first_name

    @property
    def last_name (self) :
        return self.user.last_name
    # end def last_name

    def __unicode__ (self) :
        u = self.user
        result = " ".join \
            (x for x in (self.title, u.first_name, u.last_name) if x)
        if not result :
            result = u.username
        return result
    # end def __unicode__

    display = property (__unicode__)

    NAV_admin_args = dict \
        ( list_display = ("birth_date", "sex")
        , field_group_descriptions =
            ( DJO.Field_Group_Description
                ( DJO.Field_Description ("last_name",  required = True)
                , DJO.Field_Description ("first_name", required = True)
                , "title"
                , legend    = _("Personal info")
                , template  = DJO.Template ["field_group_horizontal.html"]
                , name      = "Personal_Info"
                )
            , DJO.Field_Group_Description
                ( "sex", "birth_date"
                , legend    = _("Personal details")
                , template  = DJO.Template ["field_group_horizontal.html"]
                , name      = "Personal_Details"
                )
            , DJO.Nested_Form_Group_Description._.Personal_Phone_Info
            , DJO.Nested_Form_Group_Description._.Personal_Email_Info
            , DJO.Nested_Form_Group_Description._.Personal_Contact_Info
            )
        )

# end class Person

### __END__ DJO.Apps.Person.Person

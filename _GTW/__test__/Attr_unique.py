# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Attr_unique
#
# Purpose
#    Test unique-ness predicates
#
# Revision Dates
#     4-Aug-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW.__test__.model import *
from   _MOM.inspect        import children_trans_iter

_test_unique = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...


    >>> for ET in scope.app_type._T_Extension :
    ...     ems_ps = ET._Predicates.uniqueness_ems
    ...     dbw_ps = ET._Predicates.uniqueness_dbw
    ...     if (ems_ps or dbw_ps) and ET.is_relevant :
    ...         print (ET.type_name)
    ...         print (" ".join ((" " * 3, "EMS", ", ".join (str (p) for p in ems_ps))).rstrip ())
    ...         print (" ".join ((" " * 3, "DBW", ", ".join (str (p) for p in dbw_ps))).rstrip ())
    Auth._Account_
        EMS
        DBW Uniqueness predicate: unique_epk ('name',)
    Auth.Account_Anonymous
        EMS Uniqueness predicate: unique_epk ('name',)
        DBW
    Auth.Account
        EMS Uniqueness predicate: unique_epk ('name',)
        DBW
    Auth.Certificate
        EMS
        DBW Uniqueness predicate: unique_epk ('email', 'validity', 'desc')
    Auth.Group
        EMS
        DBW Uniqueness predicate: unique_epk ('name',)
    Auth.Account_in_Group
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'right')
    Auth.Account_Activation
        EMS
        DBW Uniqueness predicate: unique_epk ('left',)
    Auth.Account_Password_Change_Required
        EMS
        DBW Uniqueness predicate: unique_epk ('left',)
    Auth.Account_EMail_Verification
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'token')
    Auth.Account_Password_Reset
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'token')
    EVT.Calendar
        EMS
        DBW Uniqueness predicate: unique_epk ('name',)
    SWP.Page
        EMS Uniqueness predicate: unique_epk ('perma_name',)
        DBW
    SWP.Page_Y
        EMS Uniqueness predicate: unique_epk ('perma_name', 'year')
        DBW
    EVT.Event
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'date', 'time', 'calendar')
    EVT.Event_occurs
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'date', 'time')
    EVT.Recurrence_Spec
        EMS
        DBW Uniqueness predicate: unique_epk ('left',)
    EVT.Recurrence_Rule
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'is_exception', 'desc')
    PAP.Address
        EMS
        DBW Uniqueness predicate: unique_epk ('street', 'zip', 'city', 'country')
    PAP.Company
        EMS
        DBW Uniqueness predicate: unique_epk ('name', 'registered_in')
    PAP.Email
        EMS
        DBW Uniqueness predicate: unique_epk ('address',)
    PAP.Phone
        EMS
        DBW Uniqueness predicate: unique_epk ('country_code', 'area_code', 'number')
    PAP.Person
        EMS
        DBW Uniqueness predicate: unique_epk ('last_name', 'first_name', 'middle_name', 'title')
    PAP.Url
        EMS
        DBW Uniqueness predicate: unique_epk ('value',)
    PAP.Address_Position
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'position')
    PAP.Subject_has_Property
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Person_has_Account
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'right')
    SRM._Boat_Class_
        EMS
        DBW Uniqueness predicate: unique_epk ('name',)
    SRM.Boat_Class
        EMS Uniqueness predicate: unique_epk ('name',)
        DBW
    SRM.Handicap
        EMS Uniqueness predicate: unique_epk ('name',)
        DBW
    SRM.Boat
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'sail_number', 'nation', 'sail_number_x')
    SRM.Club
        EMS
        DBW Uniqueness predicate: unique_epk ('name',)
    SRM.Regatta_Event
        EMS
        DBW Uniqueness predicate: unique_epk ('name', 'date')
    SWP.Clip_O
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'date_x')
    SWP.Clip_X
        EMS Uniqueness predicate: unique_epk ('perma_name',)
        DBW
    SWP.Gallery
        EMS
        DBW Uniqueness predicate: unique_epk ('perma_name',)
    SWP.Picture
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'number')
    SRM.Page
        EMS Uniqueness predicate: unique_epk ('perma_name', 'event')
        DBW
    SRM.Regatta
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'boat_class')
    SRM.Regatta_C
        EMS Uniqueness predicate: unique_epk ('left', 'boat_class')
        DBW
    SRM.Regatta_H
        EMS Uniqueness predicate: unique_epk ('left', 'boat_class')
        DBW
    SRM.Sailor
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'nation', 'mna_number', 'club')
    SRM.Boat_in_Regatta
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'right'), Uniqueness predicate: unique_regatta_skipper (u'regatta', u'skipper')
    SRM.Race_Result
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'race')
    SRM.Team
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'name')
    SRM.Crew_Member
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'right')
    SRM.Team_has_Boat_in_Regatta
        EMS
        DBW Uniqueness predicate: unique_epk ('left', 'right')
    PAP.Subject_has_Address
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Subject_has_Email
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Subject_has_Phone
        EMS Uniqueness predicate: unique_epk ('left', 'right', 'extension')
        DBW
    PAP.Subject_has_Url
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Company_has_Url
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Person_has_Url
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Company_has_Phone
        EMS Uniqueness predicate: unique_epk ('left', 'right', 'extension')
        DBW
    PAP.Person_has_Phone
        EMS Uniqueness predicate: unique_epk ('left', 'right', 'extension')
        DBW
    PAP.Company_has_Email
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Person_has_Email
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Company_has_Address
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW
    PAP.Person_has_Address
        EMS Uniqueness predicate: unique_epk ('left', 'right')
        DBW


"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_unique      = _test_unique
        )
    , ignore = ("HPS", )
    )

### __END__ GTW.__test__.Attr_unique

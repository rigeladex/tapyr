# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.__test__.SAS_SQL
#
# Purpose
#    Test the generated SQL expression for queries
#
# Revision Dates
#    22-Jul-2011 (MG) Creation
#     2-Apr-2013 (CT) Adapt to change of `MOM.DBW.SAS.Q_Result.__str__`
#    30-May-2013 (CT) Add `test_select` and `test_tables`
#    ««revision-date»»···
#--

from   __future__          import print_function
from   __future__          import unicode_literals

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q
from   _MOM.inspect        import children_trans_iter

_test_filters = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> print (scope.PAP.Person.query (Q.last_name == "h"))
    SQL: SELECT
           "PAP__Person".__lifetime_finish AS "PAP__Person___lifetime_finish",
           "PAP__Person".__lifetime_start AS "PAP__Person___lifetime_start",
           "PAP__Person".__raw_first_name AS "PAP__Person___raw_first_name",
           "PAP__Person".__raw_last_name AS "PAP__Person___raw_last_name",
           "PAP__Person".__raw_middle_name AS "PAP__Person___raw_middle_name",
           "PAP__Person".__raw_title AS "PAP__Person___raw_title",
           "PAP__Person".electric AS "PAP__Person_electric",
           "PAP__Person".first_name AS "PAP__Person_first_name",
           "PAP__Person".last_cid AS "PAP__Person_last_cid",
           "PAP__Person".last_name AS "PAP__Person_last_name",
           "PAP__Person".middle_name AS "PAP__Person_middle_name",
           "PAP__Person".pid AS "PAP__Person_pid",
           "PAP__Person".salutation AS "PAP__Person_salutation",
           "PAP__Person".sex AS "PAP__Person_sex",
           "PAP__Person".title AS "PAP__Person_title",
           "PAP__Person".type_name AS "PAP__Person_type_name",
           "PAP__Person".x_locked AS "PAP__Person_x_locked"
         FROM "PAP__Person"
         WHERE "PAP__Person".last_name = :last_name_1

    >>> print (scope.PAP.Person.query (Q.RAW.last_name == "H"))
    SQL: SELECT
           "PAP__Person".__lifetime_finish AS "PAP__Person___lifetime_finish",
           "PAP__Person".__lifetime_start AS "PAP__Person___lifetime_start",
           "PAP__Person".__raw_first_name AS "PAP__Person___raw_first_name",
           "PAP__Person".__raw_last_name AS "PAP__Person___raw_last_name",
           "PAP__Person".__raw_middle_name AS "PAP__Person___raw_middle_name",
           "PAP__Person".__raw_title AS "PAP__Person___raw_title",
           "PAP__Person".electric AS "PAP__Person_electric",
           "PAP__Person".first_name AS "PAP__Person_first_name",
           "PAP__Person".last_cid AS "PAP__Person_last_cid",
           "PAP__Person".last_name AS "PAP__Person_last_name",
           "PAP__Person".middle_name AS "PAP__Person_middle_name",
           "PAP__Person".pid AS "PAP__Person_pid",
           "PAP__Person".salutation AS "PAP__Person_salutation",
           "PAP__Person".sex AS "PAP__Person_sex",
           "PAP__Person".title AS "PAP__Person_title",
           "PAP__Person".type_name AS "PAP__Person_type_name",
           "PAP__Person".x_locked AS "PAP__Person_x_locked"
         FROM "PAP__Person"
         WHERE "PAP__Person".__raw_last_name = :__raw_last_name_1

    >>> print (scope.PAP.Person.query (Q.RAW.last_name.LOWER == "h"))
    SQL: SELECT
           "PAP__Person".__lifetime_finish AS "PAP__Person___lifetime_finish",
           "PAP__Person".__lifetime_start AS "PAP__Person___lifetime_start",
           "PAP__Person".__raw_first_name AS "PAP__Person___raw_first_name",
           "PAP__Person".__raw_last_name AS "PAP__Person___raw_last_name",
           "PAP__Person".__raw_middle_name AS "PAP__Person___raw_middle_name",
           "PAP__Person".__raw_title AS "PAP__Person___raw_title",
           "PAP__Person".electric AS "PAP__Person_electric",
           "PAP__Person".first_name AS "PAP__Person_first_name",
           "PAP__Person".last_cid AS "PAP__Person_last_cid",
           "PAP__Person".last_name AS "PAP__Person_last_name",
           "PAP__Person".middle_name AS "PAP__Person_middle_name",
           "PAP__Person".pid AS "PAP__Person_pid",
           "PAP__Person".salutation AS "PAP__Person_salutation",
           "PAP__Person".sex AS "PAP__Person_sex",
           "PAP__Person".title AS "PAP__Person_title",
           "PAP__Person".type_name AS "PAP__Person_type_name",
           "PAP__Person".x_locked AS "PAP__Person_x_locked"
         FROM "PAP__Person"
         WHERE lower("PAP__Person".__raw_last_name) = :lower_1

    >>> print (scope.PAP.Person.query (Q.RAW.last_name.STARTSWITH ("H")))
    SQL: SELECT
           "PAP__Person".__lifetime_finish AS "PAP__Person___lifetime_finish",
           "PAP__Person".__lifetime_start AS "PAP__Person___lifetime_start",
           "PAP__Person".__raw_first_name AS "PAP__Person___raw_first_name",
           "PAP__Person".__raw_last_name AS "PAP__Person___raw_last_name",
           "PAP__Person".__raw_middle_name AS "PAP__Person___raw_middle_name",
           "PAP__Person".__raw_title AS "PAP__Person___raw_title",
           "PAP__Person".electric AS "PAP__Person_electric",
           "PAP__Person".first_name AS "PAP__Person_first_name",
           "PAP__Person".last_cid AS "PAP__Person_last_cid",
           "PAP__Person".last_name AS "PAP__Person_last_name",
           "PAP__Person".middle_name AS "PAP__Person_middle_name",
           "PAP__Person".pid AS "PAP__Person_pid",
           "PAP__Person".salutation AS "PAP__Person_salutation",
           "PAP__Person".sex AS "PAP__Person_sex",
           "PAP__Person".title AS "PAP__Person_title",
           "PAP__Person".type_name AS "PAP__Person_type_name",
           "PAP__Person".x_locked AS "PAP__Person_x_locked"
         FROM "PAP__Person"
         WHERE "PAP__Person".__raw_last_name LIKE :__raw_last_name_1 || '%%%%'

    >>> print (scope.PAP.Person.query (Q.RAW.last_name.LOWER.STARTSWITH ("h")))
    SQL: SELECT
           "PAP__Person".__lifetime_finish AS "PAP__Person___lifetime_finish",
           "PAP__Person".__lifetime_start AS "PAP__Person___lifetime_start",
           "PAP__Person".__raw_first_name AS "PAP__Person___raw_first_name",
           "PAP__Person".__raw_last_name AS "PAP__Person___raw_last_name",
           "PAP__Person".__raw_middle_name AS "PAP__Person___raw_middle_name",
           "PAP__Person".__raw_title AS "PAP__Person___raw_title",
           "PAP__Person".electric AS "PAP__Person_electric",
           "PAP__Person".first_name AS "PAP__Person_first_name",
           "PAP__Person".last_cid AS "PAP__Person_last_cid",
           "PAP__Person".last_name AS "PAP__Person_last_name",
           "PAP__Person".middle_name AS "PAP__Person_middle_name",
           "PAP__Person".pid AS "PAP__Person_pid",
           "PAP__Person".salutation AS "PAP__Person_salutation",
           "PAP__Person".sex AS "PAP__Person_sex",
           "PAP__Person".title AS "PAP__Person_title",
           "PAP__Person".type_name AS "PAP__Person_type_name",
           "PAP__Person".x_locked AS "PAP__Person_x_locked"
         FROM "PAP__Person"
         WHERE lower("PAP__Person".__raw_last_name) LIKE :lower_1 || '%%%%'
"""

_test_select = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> show_select (scope)
    Auth.Account_in_Group
        SELECT "Auth__Account_in_Group".pid,
               "Auth__Account_in_Group".electric,
               "Auth__Account_in_Group".last_cid,
               "Auth__Account_in_Group".left_pid,
               "Auth__Account_in_Group".right_pid,
               "Auth__Account_in_Group".type_name,
               "Auth__Account_in_Group".x_locked
        FROM "Auth__Account_in_Group"
    Auth.Certificate
        SELECT "Auth__Certificate".pid,
               "Auth__Certificate"."desc",
               "Auth__Certificate".__validity_finish,
               "Auth__Certificate".__validity_start,
               "Auth__Certificate".electric,
               "Auth__Certificate".email,
               "Auth__Certificate".last_cid,
               "Auth__Certificate".pem,
               "Auth__Certificate".revocation_date,
               "Auth__Certificate".type_name,
               "Auth__Certificate".x_locked
        FROM "Auth__Certificate"
    Auth.Group
        SELECT "Auth__Group".pid,
               "Auth__Group"."desc",
               "Auth__Group".electric,
               "Auth__Group".last_cid,
               "Auth__Group".name,
               "Auth__Group".type_name,
               "Auth__Group".x_locked
        FROM "Auth__Group"
    Auth._Account_
        SELECT "Auth___Account_".pid,
               "Auth___Account_".electric,
               "Auth___Account_".enabled,
               "Auth___Account_".last_cid,
               "Auth___Account_".name,
               "Auth___Account_".superuser,
               "Auth___Account_".suspended,
               "Auth___Account_".type_name,
               "Auth___Account_".x_locked
        FROM "Auth___Account_"
    Auth.Account Auth._Account_
        SELECT "Auth__Account"."Auth___Account__pid",
               "Auth__Account".password,
               "Auth__Account".ph_name
        FROM "Auth__Account"
    EVT.Event
        SELECT "EVT__Event".pid,
               "EVT__Event".__date_finish,
               "EVT__Event".__date_start,
               "EVT__Event".__time_finish,
               "EVT__Event".__time_start,
               "EVT__Event".calendar_pid,
               "EVT__Event".detail,
               "EVT__Event".electric,
               "EVT__Event".last_cid,
               "EVT__Event".left_pid,
               "EVT__Event".short_title,
               "EVT__Event".type_name,
               "EVT__Event".x_locked
        FROM "EVT__Event"
    EVT.Event_occurs
        SELECT "EVT__Event_occurs".pid,
               "EVT__Event_occurs".__time_finish,
               "EVT__Event_occurs".__time_start,
               "EVT__Event_occurs".date,
               "EVT__Event_occurs".last_cid,
               "EVT__Event_occurs".left_pid,
               "EVT__Event_occurs".type_name,
               "EVT__Event_occurs".x_locked
        FROM "EVT__Event_occurs"
    EVT.Recurrence_Rule
        SELECT "EVT__Recurrence_Rule".pid,
               "EVT__Recurrence_Rule"."desc",
               "EVT__Recurrence_Rule".count,
               "EVT__Recurrence_Rule".easter_offset,
               "EVT__Recurrence_Rule".electric,
               "EVT__Recurrence_Rule".finish,
               "EVT__Recurrence_Rule".is_exception,
               "EVT__Recurrence_Rule".last_cid,
               "EVT__Recurrence_Rule".left_pid,
               "EVT__Recurrence_Rule".month,
               "EVT__Recurrence_Rule".month_day,
               "EVT__Recurrence_Rule".period,
               "EVT__Recurrence_Rule".restrict_pos,
               "EVT__Recurrence_Rule".start,
               "EVT__Recurrence_Rule".type_name,
               "EVT__Recurrence_Rule".unit,
               "EVT__Recurrence_Rule".week,
               "EVT__Recurrence_Rule".week_day,
               "EVT__Recurrence_Rule".x_locked,
               "EVT__Recurrence_Rule".year_day
        FROM "EVT__Recurrence_Rule"
    EVT.Recurrence_Spec
        SELECT "EVT__Recurrence_Spec".pid,
               "EVT__Recurrence_Spec".date_exceptions,
               "EVT__Recurrence_Spec".dates,
               "EVT__Recurrence_Spec".electric,
               "EVT__Recurrence_Spec".last_cid,
               "EVT__Recurrence_Spec".left_pid,
               "EVT__Recurrence_Spec".type_name,
               "EVT__Recurrence_Spec".x_locked
        FROM "EVT__Recurrence_Spec"
    EVT.Calendar
        SELECT "EVT__Calendar".pid,
               "EVT__Calendar"."desc",
               "EVT__Calendar".electric,
               "EVT__Calendar".last_cid,
               "EVT__Calendar".name,
               "EVT__Calendar".type_name,
               "EVT__Calendar".x_locked
        FROM "EVT__Calendar"
    PAP.Address_Position
        SELECT "PAP__Address_Position".pid,
               "PAP__Address_Position".__position___raw_lat,
               "PAP__Address_Position".__position___raw_lon,
               "PAP__Address_Position".__position_height,
               "PAP__Address_Position".__position_lat,
               "PAP__Address_Position".__position_lon,
               "PAP__Address_Position".electric,
               "PAP__Address_Position".last_cid,
               "PAP__Address_Position".left_pid,
               "PAP__Address_Position".type_name,
               "PAP__Address_Position".x_locked
        FROM "PAP__Address_Position"
    SRM.Boat
        SELECT "SRM__Boat".pid,
               "SRM__Boat".__raw_sail_number,
               "SRM__Boat".__raw_sail_number_x,
               "SRM__Boat".electric,
               "SRM__Boat".last_cid,
               "SRM__Boat".left_pid,
               "SRM__Boat".name,
               "SRM__Boat".nation,
               "SRM__Boat".sail_number,
               "SRM__Boat".sail_number_x,
               "SRM__Boat".type_name,
               "SRM__Boat".x_locked
        FROM "SRM__Boat"
    SRM.Race_Result
        SELECT "SRM__Race_Result".pid,
               "SRM__Race_Result".discarded,
               "SRM__Race_Result".electric,
               "SRM__Race_Result".last_cid,
               "SRM__Race_Result".left_pid,
               "SRM__Race_Result".points,
               "SRM__Race_Result".race,
               "SRM__Race_Result".status,
               "SRM__Race_Result".type_name,
               "SRM__Race_Result".x_locked
        FROM "SRM__Race_Result"
    SRM.Regatta
        SELECT "SRM__Regatta".pid,
               "SRM__Regatta".__result_date,
               "SRM__Regatta".__result_software,
               "SRM__Regatta".__result_status,
               "SRM__Regatta".boat_class_pid,
               "SRM__Regatta".discards,
               "SRM__Regatta".electric,
               "SRM__Regatta".is_cancelled,
               "SRM__Regatta".kind,
               "SRM__Regatta".last_cid,
               "SRM__Regatta".left_pid,
               "SRM__Regatta".perma_name,
               "SRM__Regatta".races,
               "SRM__Regatta".type_name,
               "SRM__Regatta".x_locked
        FROM "SRM__Regatta"
    SRM.Regatta_C SRM.Regatta
        SELECT "SRM__Regatta_C"."SRM__Regatta_pid",
               "SRM__Regatta_C".is_team_race
        FROM "SRM__Regatta_C"
    SRM.Regatta_H SRM.Regatta
        SELECT "SRM__Regatta_H"."SRM__Regatta_pid"
        FROM "SRM__Regatta_H"
    SRM.Sailor
        SELECT "SRM__Sailor".pid,
               "SRM__Sailor".__raw_mna_number,
               "SRM__Sailor".club_pid,
               "SRM__Sailor".electric,
               "SRM__Sailor".last_cid,
               "SRM__Sailor".left_pid,
               "SRM__Sailor".mna_number,
               "SRM__Sailor".nation,
               "SRM__Sailor".type_name,
               "SRM__Sailor".x_locked
        FROM "SRM__Sailor"
    SRM.Team
        SELECT "SRM__Team".pid,
               "SRM__Team"."desc",
               "SRM__Team".__raw_name,
               "SRM__Team".club_pid,
               "SRM__Team".electric,
               "SRM__Team".last_cid,
               "SRM__Team".leader_pid,
               "SRM__Team".left_pid,
               "SRM__Team".name,
               "SRM__Team".place,
               "SRM__Team".registration_date,
               "SRM__Team".type_name,
               "SRM__Team".x_locked
        FROM "SRM__Team"
    SWP.Clip_O
        SELECT "SWP__Clip_O".pid,
               "SWP__Clip_O".__date_finish,
               "SWP__Clip_O".__date_start,
               "SWP__Clip_O".__date_x_finish,
               "SWP__Clip_O".__date_x_start,
               "SWP__Clip_O".abstract,
               "SWP__Clip_O".contents,
               "SWP__Clip_O".electric,
               "SWP__Clip_O".last_cid,
               "SWP__Clip_O".left_pid,
               "SWP__Clip_O".prio,
               "SWP__Clip_O".type_name,
               "SWP__Clip_O".x_locked
        FROM "SWP__Clip_O"
    SWP.Picture
        SELECT "SWP__Picture".pid,
               "SWP__Picture".__photo_extension,
               "SWP__Picture".__photo_height,
               "SWP__Picture".__photo_width,
               "SWP__Picture".__thumb_extension,
               "SWP__Picture".__thumb_height,
               "SWP__Picture".__thumb_width,
               "SWP__Picture".electric,
               "SWP__Picture".last_cid,
               "SWP__Picture".left_pid,
               "SWP__Picture".name,
               "SWP__Picture".number,
               "SWP__Picture".type_name,
               "SWP__Picture".x_locked
        FROM "SWP__Picture"
    PAP.Person_has_Account
        SELECT "PAP__Person_has_Account".pid,
               "PAP__Person_has_Account".electric,
               "PAP__Person_has_Account".last_cid,
               "PAP__Person_has_Account".left_pid,
               "PAP__Person_has_Account".right_pid,
               "PAP__Person_has_Account".type_name,
               "PAP__Person_has_Account".x_locked
        FROM "PAP__Person_has_Account"
    PAP.Company_has_Address
        SELECT "PAP__Company_has_Address".pid,
               "PAP__Company_has_Address"."desc",
               "PAP__Company_has_Address".electric,
               "PAP__Company_has_Address".last_cid,
               "PAP__Company_has_Address".left_pid,
               "PAP__Company_has_Address".right_pid,
               "PAP__Company_has_Address".type_name,
               "PAP__Company_has_Address".x_locked
        FROM "PAP__Company_has_Address"
    PAP.Person_has_Address
        SELECT "PAP__Person_has_Address".pid,
               "PAP__Person_has_Address"."desc",
               "PAP__Person_has_Address".electric,
               "PAP__Person_has_Address".last_cid,
               "PAP__Person_has_Address".left_pid,
               "PAP__Person_has_Address".right_pid,
               "PAP__Person_has_Address".type_name,
               "PAP__Person_has_Address".x_locked
        FROM "PAP__Person_has_Address"
    PAP.Company_has_Email
        SELECT "PAP__Company_has_Email".pid,
               "PAP__Company_has_Email"."desc",
               "PAP__Company_has_Email".electric,
               "PAP__Company_has_Email".last_cid,
               "PAP__Company_has_Email".left_pid,
               "PAP__Company_has_Email".right_pid,
               "PAP__Company_has_Email".type_name,
               "PAP__Company_has_Email".x_locked
        FROM "PAP__Company_has_Email"
    PAP.Person_has_Email
        SELECT "PAP__Person_has_Email".pid,
               "PAP__Person_has_Email"."desc",
               "PAP__Person_has_Email".electric,
               "PAP__Person_has_Email".last_cid,
               "PAP__Person_has_Email".left_pid,
               "PAP__Person_has_Email".right_pid,
               "PAP__Person_has_Email".type_name,
               "PAP__Person_has_Email".x_locked
        FROM "PAP__Person_has_Email"
    PAP.Company_has_Phone
        SELECT "PAP__Company_has_Phone".pid,
               "PAP__Company_has_Phone"."desc",
               "PAP__Company_has_Phone".electric,
               "PAP__Company_has_Phone".extension,
               "PAP__Company_has_Phone".last_cid,
               "PAP__Company_has_Phone".left_pid,
               "PAP__Company_has_Phone".right_pid,
               "PAP__Company_has_Phone".type_name,
               "PAP__Company_has_Phone".x_locked
        FROM "PAP__Company_has_Phone"
    PAP.Person_has_Phone
        SELECT "PAP__Person_has_Phone".pid,
               "PAP__Person_has_Phone"."desc",
               "PAP__Person_has_Phone".electric,
               "PAP__Person_has_Phone".extension,
               "PAP__Person_has_Phone".last_cid,
               "PAP__Person_has_Phone".left_pid,
               "PAP__Person_has_Phone".right_pid,
               "PAP__Person_has_Phone".type_name,
               "PAP__Person_has_Phone".x_locked
        FROM "PAP__Person_has_Phone"
    PAP.Company_has_Url
        SELECT "PAP__Company_has_Url".pid,
               "PAP__Company_has_Url"."desc",
               "PAP__Company_has_Url".electric,
               "PAP__Company_has_Url".last_cid,
               "PAP__Company_has_Url".left_pid,
               "PAP__Company_has_Url".right_pid,
               "PAP__Company_has_Url".type_name,
               "PAP__Company_has_Url".x_locked
        FROM "PAP__Company_has_Url"
    PAP.Person_has_Url
        SELECT "PAP__Person_has_Url".pid,
               "PAP__Person_has_Url"."desc",
               "PAP__Person_has_Url".electric,
               "PAP__Person_has_Url".last_cid,
               "PAP__Person_has_Url".left_pid,
               "PAP__Person_has_Url".right_pid,
               "PAP__Person_has_Url".type_name,
               "PAP__Person_has_Url".x_locked
        FROM "PAP__Person_has_Url"
    SRM.Boat_in_Regatta
        SELECT "SRM__Boat_in_Regatta".pid,
               "SRM__Boat_in_Regatta".electric,
               "SRM__Boat_in_Regatta".last_cid,
               "SRM__Boat_in_Regatta".left_pid,
               "SRM__Boat_in_Regatta".place,
               "SRM__Boat_in_Regatta".points,
               "SRM__Boat_in_Regatta".rank,
               "SRM__Boat_in_Regatta".registration_date,
               "SRM__Boat_in_Regatta".right_pid,
               "SRM__Boat_in_Regatta".skipper_pid,
               "SRM__Boat_in_Regatta".type_name,
               "SRM__Boat_in_Regatta".x_locked
        FROM "SRM__Boat_in_Regatta"
    SRM.Crew_Member
        SELECT "SRM__Crew_Member".pid,
               "SRM__Crew_Member".electric,
               "SRM__Crew_Member".key,
               "SRM__Crew_Member".last_cid,
               "SRM__Crew_Member".left_pid,
               "SRM__Crew_Member".right_pid,
               "SRM__Crew_Member".role,
               "SRM__Crew_Member".type_name,
               "SRM__Crew_Member".x_locked
        FROM "SRM__Crew_Member"
    SRM.Team_has_Boat_in_Regatta
        SELECT "SRM__Team_has_Boat_in_Regatta".pid,
               "SRM__Team_has_Boat_in_Regatta".electric,
               "SRM__Team_has_Boat_in_Regatta".last_cid,
               "SRM__Team_has_Boat_in_Regatta".left_pid,
               "SRM__Team_has_Boat_in_Regatta".right_pid,
               "SRM__Team_has_Boat_in_Regatta".type_name,
               "SRM__Team_has_Boat_in_Regatta".x_locked
        FROM "SRM__Team_has_Boat_in_Regatta"
    PAP.Address
        SELECT "PAP__Address".pid,
               "PAP__Address"."desc",
               "PAP__Address".__raw_city,
               "PAP__Address".__raw_country,
               "PAP__Address".__raw_region,
               "PAP__Address".__raw_street,
               "PAP__Address".__raw_zip,
               "PAP__Address".city,
               "PAP__Address".country,
               "PAP__Address".electric,
               "PAP__Address".last_cid,
               "PAP__Address".region,
               "PAP__Address".street,
               "PAP__Address".type_name,
               "PAP__Address".x_locked,
               "PAP__Address".zip
        FROM "PAP__Address"
    PAP.Email
        SELECT "PAP__Email".pid,
               "PAP__Email"."desc",
               "PAP__Email".__raw_address,
               "PAP__Email".address,
               "PAP__Email".electric,
               "PAP__Email".last_cid,
               "PAP__Email".type_name,
               "PAP__Email".x_locked
        FROM "PAP__Email"
    PAP.Phone
        SELECT "PAP__Phone".pid,
               "PAP__Phone"."desc",
               "PAP__Phone".area_code,
               "PAP__Phone".country_code,
               "PAP__Phone".electric,
               "PAP__Phone".last_cid,
               "PAP__Phone".number,
               "PAP__Phone".type_name,
               "PAP__Phone".x_locked
        FROM "PAP__Phone"
    PAP.Url
        SELECT "PAP__Url".pid,
               "PAP__Url"."desc",
               "PAP__Url".electric,
               "PAP__Url".last_cid,
               "PAP__Url".type_name,
               "PAP__Url".value,
               "PAP__Url".x_locked
        FROM "PAP__Url"
    PAP.Company
        SELECT "PAP__Company".pid,
               "PAP__Company".__lifetime_finish,
               "PAP__Company".__lifetime_start,
               "PAP__Company".__raw_name,
               "PAP__Company".__raw_registered_in,
               "PAP__Company".__raw_short_name,
               "PAP__Company".electric,
               "PAP__Company".last_cid,
               "PAP__Company".name,
               "PAP__Company".registered_in,
               "PAP__Company".short_name,
               "PAP__Company".type_name,
               "PAP__Company".x_locked
        FROM "PAP__Company"
    PAP.Person
        SELECT "PAP__Person".pid,
               "PAP__Person".__lifetime_finish,
               "PAP__Person".__lifetime_start,
               "PAP__Person".__raw_first_name,
               "PAP__Person".__raw_last_name,
               "PAP__Person".__raw_middle_name,
               "PAP__Person".__raw_title,
               "PAP__Person".electric,
               "PAP__Person".first_name,
               "PAP__Person".last_cid,
               "PAP__Person".last_name,
               "PAP__Person".middle_name,
               "PAP__Person".salutation,
               "PAP__Person".sex,
               "PAP__Person".title,
               "PAP__Person".type_name,
               "PAP__Person".x_locked
        FROM "PAP__Person"
    SRM.Club
        SELECT "SRM__Club".pid,
               "SRM__Club".__raw_name,
               "SRM__Club".electric,
               "SRM__Club".last_cid,
               "SRM__Club".long_name,
               "SRM__Club".name,
               "SRM__Club".type_name,
               "SRM__Club".x_locked
        FROM "SRM__Club"
    SRM.Page SWP.Page
        SELECT "SRM__Page"."SWP__Page_pid",
               "SRM__Page"."desc",
               "SRM__Page".event_pid
        FROM "SRM__Page"
    SRM.Regatta_Event
        SELECT "SRM__Regatta_Event".pid,
               "SRM__Regatta_Event"."desc",
               "SRM__Regatta_Event".__date_finish,
               "SRM__Regatta_Event".__date_start,
               "SRM__Regatta_Event".__raw_name,
               "SRM__Regatta_Event".club_pid,
               "SRM__Regatta_Event".electric,
               "SRM__Regatta_Event".is_cancelled,
               "SRM__Regatta_Event".last_cid,
               "SRM__Regatta_Event".name,
               "SRM__Regatta_Event".perma_name,
               "SRM__Regatta_Event".type_name,
               "SRM__Regatta_Event".x_locked
        FROM "SRM__Regatta_Event"
    SRM._Boat_Class_
        SELECT "SRM___Boat_Class_".pid,
               "SRM___Boat_Class_".__raw_name,
               "SRM___Boat_Class_".electric,
               "SRM___Boat_Class_".last_cid,
               "SRM___Boat_Class_".name,
               "SRM___Boat_Class_".type_name,
               "SRM___Boat_Class_".x_locked
        FROM "SRM___Boat_Class_"
    SRM.Boat_Class SRM._Boat_Class_
        SELECT "SRM__Boat_Class"."SRM___Boat_Class__pid",
               "SRM__Boat_Class".beam,
               "SRM__Boat_Class".loa,
               "SRM__Boat_Class".max_crew,
               "SRM__Boat_Class".sail_area
        FROM "SRM__Boat_Class"
    SRM.Handicap SRM._Boat_Class_
        SELECT "SRM__Handicap"."SRM___Boat_Class__pid"
        FROM "SRM__Handicap"
    SWP.Gallery
        SELECT "SWP__Gallery".pid,
               "SWP__Gallery".__date_finish,
               "SWP__Gallery".__date_start,
               "SWP__Gallery".directory,
               "SWP__Gallery".electric,
               "SWP__Gallery".last_cid,
               "SWP__Gallery".perma_name,
               "SWP__Gallery".short_title,
               "SWP__Gallery".title,
               "SWP__Gallery".type_name,
               "SWP__Gallery".x_locked
        FROM "SWP__Gallery"
    SWP.Page
        SELECT "SWP__Page".pid,
               "SWP__Page".__date_finish,
               "SWP__Page".__date_start,
               "SWP__Page".contents,
               "SWP__Page".electric,
               "SWP__Page".format,
               "SWP__Page".head_line,
               "SWP__Page".hidden,
               "SWP__Page".last_cid,
               "SWP__Page".perma_name,
               "SWP__Page".prio,
               "SWP__Page".short_title,
               "SWP__Page".text,
               "SWP__Page".title,
               "SWP__Page".type_name,
               "SWP__Page".x_locked
        FROM "SWP__Page"
    SWP.Clip_X SWP.Page
        SELECT "SWP__Clip_X"."SWP__Page_pid",
               "SWP__Clip_X".link_to
        FROM "SWP__Clip_X"
    SWP.Page_Y SWP.Page
        SELECT "SWP__Page_Y"."SWP__Page_pid",
               "SWP__Page_Y".year
        FROM "SWP__Page_Y"

"""

_test_tables = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> show_tables (scope)
    Auth.Account_in_Group <Table Auth__Account_in_Group>
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    Auth.Certificate <Table Auth__Certificate>
        Column __validity_finish         : Datetime
        Column __validity_start          : Datetime
        Column desc                      : Varchar(40)
        Column electric                  : Boolean
        Column email                     : Varchar(80)
        Column last_cid                  : Integer
        Column pem                       : Blob
        Column pid                       : Integer              primary
        Column revocation_date           : Datetime
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    Auth.Group <Table Auth__Group>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column name                      : Varchar(32)
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    Auth._Account_ <Table Auth___Account_>
        Column electric                  : Boolean
        Column enabled                   : Boolean
        Column last_cid                  : Integer
        Column name                      : Varchar(80)
        Column pid                       : Integer              primary
        Column superuser                 : Boolean
        Column suspended                 : Boolean
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    Auth.Account Auth._Account_ <Table Auth__Account>
        Column Auth___Account__pid       : Integer              primary ForeignKey(u'Auth___Account_.pid')
        Column password                  : Varchar(120)
        Column ph_name                   : Varchar(64)
    EVT.Event <Table EVT__Event>
        Column __date_finish             : Date
        Column __date_start              : Date
        Column __time_finish             : Time
        Column __time_start              : Time
        Column calendar_pid              : Integer
        Column detail                    : Varchar(160)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column short_title               : Varchar(64)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    EVT.Event_occurs <Table EVT__Event_occurs>
        Column __time_finish             : Time
        Column __time_start              : Time
        Column date                      : Date
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    EVT.Recurrence_Rule <Table EVT__Recurrence_Rule>
        Column count                     : Integer
        Column desc                      : Varchar(20)
        Column easter_offset             : Blob
        Column electric                  : Boolean
        Column finish                    : Date
        Column is_exception              : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column month                     : Blob
        Column month_day                 : Blob
        Column period                    : Integer
        Column pid                       : Integer              primary
        Column restrict_pos              : Blob
        Column start                     : Date
        Column type_name                 : Varchar(60)
        Column unit                      : Integer
        Column week                      : Blob
        Column week_day                  : Blob
        Column x_locked                  : Boolean
        Column year_day                  : Blob
    EVT.Recurrence_Spec <Table EVT__Recurrence_Spec>
        Column date_exceptions           : Blob
        Column dates                     : Blob
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    EVT.Calendar <Table EVT__Calendar>
        Column desc                      : Varchar(80)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column name                      : Varchar(32)
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Address_Position <Table PAP__Address_Position>
        Column __position___raw_lat      : Varchar(60)
        Column __position___raw_lon      : Varchar(60)
        Column __position_height         : Float
        Column __position_lat            : Float
        Column __position_lon            : Float
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Boat <Table SRM__Boat>
        Column __raw_sail_number         : Varchar(60)
        Column __raw_sail_number_x       : Varchar(60)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column name                      : Varchar(48)
        Column nation                    : Varchar(3)
        Column pid                       : Integer              primary
        Column sail_number               : Integer
        Column sail_number_x             : Varchar(8)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Race_Result <Table SRM__Race_Result>
        Column discarded                 : Boolean
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column points                    : Integer
        Column race                      : Integer
        Column status                    : Varchar(8)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Regatta <Table SRM__Regatta>
        Column __result_date             : Datetime
        Column __result_software         : Varchar(64)
        Column __result_status           : Varchar(64)
        Column boat_class_pid            : Integer
        Column discards                  : Integer
        Column electric                  : Boolean
        Column is_cancelled              : Boolean
        Column kind                      : Varchar(32)
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column perma_name                : Varchar(64)
        Column pid                       : Integer              primary
        Column races                     : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Regatta_C SRM.Regatta <Table SRM__Regatta_C>
        Column SRM__Regatta_pid          : Integer              primary ForeignKey(u'SRM__Regatta.pid')
        Column is_team_race              : Boolean
    SRM.Regatta_H SRM.Regatta <Table SRM__Regatta_H>
        Column SRM__Regatta_pid          : Integer              primary ForeignKey(u'SRM__Regatta.pid')
    SRM.Sailor <Table SRM__Sailor>
        Column __raw_mna_number          : Varchar(60)
        Column club_pid                  : Integer
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column mna_number                : Integer
        Column nation                    : Varchar(3)
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Team <Table SRM__Team>
        Column __raw_name                : Varchar(60)
        Column club_pid                  : Integer
        Column desc                      : Varchar(160)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column leader_pid                : Integer
        Column left_pid                  : Integer
        Column name                      : Varchar(64)
        Column pid                       : Integer              primary
        Column place                     : Integer
        Column registration_date         : Date
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SWP.Clip_O <Table SWP__Clip_O>
        Column __date_finish             : Date
        Column __date_start              : Date
        Column __date_x_finish           : Date
        Column __date_x_start            : Date
        Column abstract                  : Text
        Column contents                  : Text
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column prio                      : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SWP.Picture <Table SWP__Picture>
        Column __photo_extension         : Varchar(10)
        Column __photo_height            : Smallint
        Column __photo_width             : Smallint
        Column __thumb_extension         : Varchar(10)
        Column __thumb_height            : Smallint
        Column __thumb_width             : Smallint
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column name                      : Varchar(100)
        Column number                    : Integer
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Person_has_Account <Table PAP__Person_has_Account>
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Company_has_Address <Table PAP__Company_has_Address>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Person_has_Address <Table PAP__Person_has_Address>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Company_has_Email <Table PAP__Company_has_Email>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Person_has_Email <Table PAP__Person_has_Email>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Company_has_Phone <Table PAP__Company_has_Phone>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column extension                 : Varchar(5)
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Person_has_Phone <Table PAP__Person_has_Phone>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column extension                 : Varchar(5)
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Company_has_Url <Table PAP__Company_has_Url>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Person_has_Url <Table PAP__Person_has_Url>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Boat_in_Regatta <Table SRM__Boat_in_Regatta>
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column place                     : Integer
        Column points                    : Integer
        Column rank                      : Integer
        Column registration_date         : Date
        Column right_pid                 : Integer
        Column skipper_pid               : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Crew_Member <Table SRM__Crew_Member>
        Column electric                  : Boolean
        Column key                       : Integer
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column role                      : Varchar(32)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Team_has_Boat_in_Regatta <Table SRM__Team_has_Boat_in_Regatta>
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column left_pid                  : Integer
        Column pid                       : Integer              primary
        Column right_pid                 : Integer
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Address <Table PAP__Address>
        Column __raw_city                : Varchar(60)
        Column __raw_country             : Varchar(60)
        Column __raw_region              : Varchar(60)
        Column __raw_street              : Varchar(60)
        Column __raw_zip                 : Varchar(60)
        Column city                      : Varchar(30)
        Column country                   : Varchar(20)
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column pid                       : Integer              primary
        Column region                    : Varchar(20)
        Column street                    : Varchar(60)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
        Column zip                       : Varchar(6)
    PAP.Email <Table PAP__Email>
        Column __raw_address             : Varchar(60)
        Column address                   : Varchar(80)
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Phone <Table PAP__Phone>
        Column area_code                 : Varchar(5)
        Column country_code              : Varchar(3)
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column number                    : Varchar(14)
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Url <Table PAP__Url>
        Column desc                      : Varchar(20)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column value                     : Varchar(160)
        Column x_locked                  : Boolean
    PAP.Company <Table PAP__Company>
        Column __lifetime_finish         : Date
        Column __lifetime_start          : Date
        Column __raw_name                : Varchar(60)
        Column __raw_registered_in       : Varchar(60)
        Column __raw_short_name          : Varchar(60)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column name                      : Varchar(64)
        Column pid                       : Integer              primary
        Column registered_in             : Varchar(64)
        Column short_name                : Varchar(12)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    PAP.Person <Table PAP__Person>
        Column __lifetime_finish         : Date
        Column __lifetime_start          : Date
        Column __raw_first_name          : Varchar(60)
        Column __raw_last_name           : Varchar(60)
        Column __raw_middle_name         : Varchar(60)
        Column __raw_title               : Varchar(60)
        Column electric                  : Boolean
        Column first_name                : Varchar(32)
        Column last_cid                  : Integer
        Column last_name                 : Varchar(48)
        Column middle_name               : Varchar(32)
        Column pid                       : Integer              primary
        Column salutation                : Varchar(80)
        Column sex                       : Varchar(1)
        Column title                     : Varchar(20)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Club <Table SRM__Club>
        Column __raw_name                : Varchar(60)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column long_name                 : Varchar(64)
        Column name                      : Varchar(8)
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Page SWP.Page <Table SRM__Page>
        Column SWP__Page_pid             : Integer              primary ForeignKey(u'SWP__Page.pid')
        Column desc                      : Varchar(30)
        Column event_pid                 : Integer
    SRM.Regatta_Event <Table SRM__Regatta_Event>
        Column __date_finish             : Date
        Column __date_start              : Date
        Column __raw_name                : Varchar(60)
        Column club_pid                  : Integer
        Column desc                      : Varchar(160)
        Column electric                  : Boolean
        Column is_cancelled              : Boolean
        Column last_cid                  : Integer
        Column name                      : Varchar(64)
        Column perma_name                : Varchar(64)
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM._Boat_Class_ <Table SRM___Boat_Class_>
        Column __raw_name                : Varchar(60)
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column name                      : Varchar(48)
        Column pid                       : Integer              primary
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SRM.Boat_Class SRM._Boat_Class_ <Table SRM__Boat_Class>
        Column SRM___Boat_Class__pid     : Integer              primary ForeignKey(u'SRM___Boat_Class_.pid')
        Column beam                      : Float
        Column loa                       : Float
        Column max_crew                  : Smallint
        Column sail_area                 : Float
    SRM.Handicap SRM._Boat_Class_ <Table SRM__Handicap>
        Column SRM___Boat_Class__pid     : Integer              primary ForeignKey(u'SRM___Boat_Class_.pid')
    SWP.Gallery <Table SWP__Gallery>
        Column __date_finish             : Date
        Column __date_start              : Date
        Column directory                 : Text
        Column electric                  : Boolean
        Column last_cid                  : Integer
        Column perma_name                : Varchar(80)
        Column pid                       : Integer              primary
        Column short_title               : Varchar(30)
        Column title                     : Varchar(120)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SWP.Page <Table SWP__Page>
        Column __date_finish             : Date
        Column __date_start              : Date
        Column contents                  : Text
        Column electric                  : Boolean
        Column format                    : Varchar(8)
        Column head_line                 : Varchar(256)
        Column hidden                    : Boolean
        Column last_cid                  : Integer
        Column perma_name                : Varchar(80)
        Column pid                       : Integer              primary
        Column prio                      : Integer
        Column short_title               : Varchar(30)
        Column text                      : Text
        Column title                     : Varchar(120)
        Column type_name                 : Varchar(60)
        Column x_locked                  : Boolean
    SWP.Clip_X SWP.Page <Table SWP__Clip_X>
        Column SWP__Page_pid             : Integer              primary ForeignKey(u'SWP__Page.pid')
        Column link_to                   : Varchar(160)
    SWP.Page_Y SWP.Page <Table SWP__Page_Y>
        Column SWP__Page_pid             : Integer              primary ForeignKey(u'SWP__Page.pid')
        Column year                      : Integer

"""

def formatted_select (T, nl, indent) :
    sep   = nl + indent
    text  = str (T._sa_table.select ())
    lines = text.split (nl)
    def _gen () :
        s = "," + sep + (" " * 7)
        for l in lines :
            if "," in l :
                comps = list (c.strip () for c in l.split (","))
                comps = [comps [0]] + sorted (comps [1:])
                yield s.join (comps)
            else :
                yield l
    return sep.join (_gen ())
# end def formatted_select

def formatted_table (T, nl, indent) :
    sep   = nl + indent
    SQ    = T._SAQ
    ST    = T._sa_table
    def _gen () :
        for c in ST.columns :
            tail = []
            if c.primary_key :
                tail.append ("primary")
            if c.foreign_keys :
                tail.extend (str (fk) for fk in sorted (c.foreign_keys))
            r = ( "Column %-25s : %-20s %s"
                % (c.name, str (c.type).capitalize (), " ".join (tail))
                ).strip ()
            yield r
    return sep.join (sorted (_gen ()))
# end def formatted_table

nl     = chr (10)
indent = "  " * 2
sk     = lambda x : (x.type_name, x.i_rank, )

def show_select (scope) :
    for T, l in (children_trans_iter (scope.MOM.Id_Entity, sort_key = sk)) :
        if T.relevant_root and T.show_in_ui :
            second = "" if T.relevant_root is T \
                      else T.relevant_root.type_name
            head   = ("%s %s" % (T.type_name, second)).strip ()
            print (head, nl, "  ", formatted_select (T, nl, indent))
# end def show_select

def show_tables (scope) :
    for T, l in (children_trans_iter (scope.MOM.Id_Entity, sort_key = sk)) :
        if T.relevant_root and T.show_in_ui :
            ST = T._sa_table
            second = "" if T.relevant_root is T \
                      else T.relevant_root.type_name
            head   = ("%s %s" % (T.type_name, second)).strip ()
            head   = ("%s <Table %s>" % (head, T._sa_table)).strip ()
            print (head, nl, "  ", formatted_table (T, nl, indent))
# end def show_tables

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_filters = _test_filters
        , test_select  = _test_select
        , test_tables  = _test_tables
        )
    , ignore = "HPS"
    )

### __END__ GTW.__test__.SAS_SQL

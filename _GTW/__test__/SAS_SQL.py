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
#     3-Jun-2013 (CT) Add `MOM_Kind` to `formatted_table`
#    18-Jun-2013 (CT) Add `test_joins`; factor `_SAS_test_functions`
#    ««revision-date»»···
#--

from   __future__          import print_function
from   __future__          import unicode_literals

from   _GTW.__test__.model               import *
from   _GTW.__test__._SAS_test_functions import *

from   _MOM.import_MOM                   import Q

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

    >>> print (scope.PAP.Person_has_Phone.query (Q.extension == None))
    SQL: SELECT
           "PAP__Person_has_Phone"."desc" AS "PAP__Person_has_Phone_desc",
           "PAP__Person_has_Phone".electric AS "PAP__Person_has_Phone_electric",
           "PAP__Person_has_Phone".extension AS "PAP__Person_has_Phone_extension",
           "PAP__Person_has_Phone".last_cid AS "PAP__Person_has_Phone_last_cid",
           "PAP__Person_has_Phone".left_pid AS "PAP__Person_has_Phone_left_pid",
           "PAP__Person_has_Phone".pid AS "PAP__Person_has_Phone_pid",
           "PAP__Person_has_Phone".right_pid AS "PAP__Person_has_Phone_right_pid",
           "PAP__Person_has_Phone".type_name AS "PAP__Person_has_Phone_type_name",
           "PAP__Person_has_Phone".x_locked AS "PAP__Person_has_Phone_x_locked"
         FROM "PAP__Person_has_Phone"
         WHERE "PAP__Person_has_Phone".extension IS NULL

    >>> print (scope.PAP.Person_has_Phone.query (Q.left.last_name.STARTSWITH ("H")))
    SQL: SELECT
           "PAP__Person_has_Phone"."desc" AS "PAP__Person_has_Phone_desc",
           "PAP__Person_has_Phone".electric AS "PAP__Person_has_Phone_electric",
           "PAP__Person_has_Phone".extension AS "PAP__Person_has_Phone_extension",
           "PAP__Person_has_Phone".last_cid AS "PAP__Person_has_Phone_last_cid",
           "PAP__Person_has_Phone".left_pid AS "PAP__Person_has_Phone_left_pid",
           "PAP__Person_has_Phone".pid AS "PAP__Person_has_Phone_pid",
           "PAP__Person_has_Phone".right_pid AS "PAP__Person_has_Phone_right_pid",
           "PAP__Person_has_Phone".type_name AS "PAP__Person_has_Phone_type_name",
           "PAP__Person_has_Phone".x_locked AS "PAP__Person_has_Phone_x_locked"
         FROM "PAP__Person_has_Phone"
           JOIN "PAP__Person" ON "PAP__Person_has_Phone".left_pid = "PAP__Person".pid
         WHERE "PAP__Person".last_name LIKE :last_name_1 || '%%%%'

    >>> print (scope.PAP.Person_has_Phone.query ().attrs (Q.pid, Q.left, Q.right))
    SQL: SELECT
           "PAP__Person_has_Phone".left_pid,
           "PAP__Person_has_Phone".pid,
           "PAP__Person_has_Phone".right_pid
         FROM "PAP__Person_has_Phone"

    >>> print (scope.PAP.Person_has_Phone.query ().attrs (Q.pid, Q.left.last_name, Q.right.number))
    SQL: SELECT
           "PAP__Person".last_name,
           "PAP__Person_has_Phone".pid,
           "PAP__Phone".number
         FROM "PAP__Person_has_Phone", "PAP__Person", "PAP__Phone"

    >>> print (scope.SRM.Boat_in_Regatta.query (Q.right.left.date.start > "2009/05/21"))
    SQL: SELECT
           "SRM__Boat_in_Regatta".electric AS "SRM__Boat_in_Regatta_electric",
           "SRM__Boat_in_Regatta".last_cid AS "SRM__Boat_in_Regatta_last_cid",
           "SRM__Boat_in_Regatta".left_pid AS "SRM__Boat_in_Regatta_left_pid",
           "SRM__Boat_in_Regatta".pid AS "SRM__Boat_in_Regatta_pid",
           "SRM__Boat_in_Regatta".place AS "SRM__Boat_in_Regatta_place",
           "SRM__Boat_in_Regatta".points AS "SRM__Boat_in_Regatta_points",
           "SRM__Boat_in_Regatta".rank AS "SRM__Boat_in_Regatta_rank",
           "SRM__Boat_in_Regatta".registration_date AS "SRM__Boat_in_Regatta_registration_date",
           "SRM__Boat_in_Regatta".right_pid AS "SRM__Boat_in_Regatta_right_pid",
           "SRM__Boat_in_Regatta".skipper_pid AS "SRM__Boat_in_Regatta_skipper_pid",
           "SRM__Boat_in_Regatta".type_name AS "SRM__Boat_in_Regatta_type_name",
           "SRM__Boat_in_Regatta".x_locked AS "SRM__Boat_in_Regatta_x_locked"
         FROM "SRM__Boat_in_Regatta"
           JOIN "SRM__Regatta" ON "SRM__Boat_in_Regatta".right_pid = "SRM__Regatta".pid
           JOIN "SRM__Regatta_Event" ON "SRM__Regatta".left_pid = "SRM__Regatta_Event".pid
         WHERE "SRM__Regatta_Event".__date_start > :__date_start_1

    >>> print (scope.SWP.Clip_O.query (Q.left.type_name == "SWP.Page"))
    SQL: SELECT
           "SWP__Clip_O".__date_finish AS "SWP__Clip_O___date_finish",
           "SWP__Clip_O".__date_start AS "SWP__Clip_O___date_start",
           "SWP__Clip_O".__date_x_finish AS "SWP__Clip_O___date_x_finish",
           "SWP__Clip_O".__date_x_start AS "SWP__Clip_O___date_x_start",
           "SWP__Clip_O".abstract AS "SWP__Clip_O_abstract",
           "SWP__Clip_O".contents AS "SWP__Clip_O_contents",
           "SWP__Clip_O".electric AS "SWP__Clip_O_electric",
           "SWP__Clip_O".last_cid AS "SWP__Clip_O_last_cid",
           "SWP__Clip_O".left_pid AS "SWP__Clip_O_left_pid",
           "SWP__Clip_O".pid AS "SWP__Clip_O_pid",
           "SWP__Clip_O".prio AS "SWP__Clip_O_prio",
           "SWP__Clip_O".type_name AS "SWP__Clip_O_type_name",
           "SWP__Clip_O".x_locked AS "SWP__Clip_O_x_locked"
         FROM "SWP__Clip_O"
           JOIN pids ON "SWP__Clip_O".left_pid = pids.pid
         WHERE pids.type_name = :type_name_1

"""

_test_joins = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> show_joins (scope)
    Auth._Account_ ['Auth__Account', 'Auth__Account_Anonymous', 'Auth___Account_']
        SQL: SELECT
           "Auth__Account"."Auth___Account__pid" AS "Auth__Account_Auth___Account__pid",
           "Auth__Account".password AS "Auth__Account_password",
           "Auth__Account".ph_name AS "Auth__Account_ph_name",
           "Auth__Account_Anonymous"."Auth___Account__pid" AS "Auth__Account_Anonymous_Auth___Account__pid",
           "Auth___Account_".electric AS "Auth___Account__electric",
           "Auth___Account_".enabled AS "Auth___Account__enabled",
           "Auth___Account_".last_cid AS "Auth___Account__last_cid",
           "Auth___Account_".name AS "Auth___Account__name",
           "Auth___Account_".pid AS "Auth___Account__pid",
           "Auth___Account_".superuser AS "Auth___Account__superuser",
           "Auth___Account_".suspended AS "Auth___Account__suspended",
           "Auth___Account_".type_name AS "Auth___Account__type_name",
           "Auth___Account_".x_locked AS "Auth___Account__x_locked"
         FROM "Auth___Account_"
           LEFT OUTER JOIN "Auth__Account" ON "Auth___Account_".pid = "Auth__Account"."Auth___Account__pid"
           LEFT OUTER JOIN "Auth__Account_Anonymous" ON "Auth___Account_".pid = "Auth__Account_Anonymous"."Auth___Account__pid"
    Auth.Account ['Auth__Account', 'Auth___Account_']
        SQL: SELECT
           "Auth__Account"."Auth___Account__pid" AS "Auth__Account_Auth___Account__pid",
           "Auth__Account".password AS "Auth__Account_password",
           "Auth__Account".ph_name AS "Auth__Account_ph_name",
           "Auth___Account_".electric AS "Auth___Account__electric",
           "Auth___Account_".enabled AS "Auth___Account__enabled",
           "Auth___Account_".last_cid AS "Auth___Account__last_cid",
           "Auth___Account_".name AS "Auth___Account__name",
           "Auth___Account_".pid AS "Auth___Account__pid",
           "Auth___Account_".superuser AS "Auth___Account__superuser",
           "Auth___Account_".suspended AS "Auth___Account__suspended",
           "Auth___Account_".type_name AS "Auth___Account__type_name",
           "Auth___Account_".x_locked AS "Auth___Account__x_locked"
         FROM "Auth__Account"
           JOIN "Auth___Account_" ON "Auth___Account_".pid = "Auth__Account"."Auth___Account__pid"
    Auth.Account_Anonymous ['Auth__Account_Anonymous', 'Auth___Account_']
        SQL: SELECT
           "Auth__Account_Anonymous"."Auth___Account__pid" AS "Auth__Account_Anonymous_Auth___Account__pid",
           "Auth___Account_".electric AS "Auth___Account__electric",
           "Auth___Account_".enabled AS "Auth___Account__enabled",
           "Auth___Account_".last_cid AS "Auth___Account__last_cid",
           "Auth___Account_".name AS "Auth___Account__name",
           "Auth___Account_".pid AS "Auth___Account__pid",
           "Auth___Account_".superuser AS "Auth___Account__superuser",
           "Auth___Account_".suspended AS "Auth___Account__suspended",
           "Auth___Account_".type_name AS "Auth___Account__type_name",
           "Auth___Account_".x_locked AS "Auth___Account__x_locked"
         FROM "Auth__Account_Anonymous"
           JOIN "Auth___Account_" ON "Auth___Account_".pid = "Auth__Account_Anonymous"."Auth___Account__pid"
    SRM.Regatta ['SRM__Regatta', 'SRM__Regatta_C', 'SRM__Regatta_H']
        SQL: SELECT
           "SRM__Regatta".__result_date AS "SRM__Regatta___result_date",
           "SRM__Regatta".__result_software AS "SRM__Regatta___result_software",
           "SRM__Regatta".__result_status AS "SRM__Regatta___result_status",
           "SRM__Regatta".boat_class_pid AS "SRM__Regatta_boat_class_pid",
           "SRM__Regatta".discards AS "SRM__Regatta_discards",
           "SRM__Regatta".electric AS "SRM__Regatta_electric",
           "SRM__Regatta".is_cancelled AS "SRM__Regatta_is_cancelled",
           "SRM__Regatta".kind AS "SRM__Regatta_kind",
           "SRM__Regatta".last_cid AS "SRM__Regatta_last_cid",
           "SRM__Regatta".left_pid AS "SRM__Regatta_left_pid",
           "SRM__Regatta".perma_name AS "SRM__Regatta_perma_name",
           "SRM__Regatta".pid AS "SRM__Regatta_pid",
           "SRM__Regatta".races AS "SRM__Regatta_races",
           "SRM__Regatta".type_name AS "SRM__Regatta_type_name",
           "SRM__Regatta".x_locked AS "SRM__Regatta_x_locked",
           "SRM__Regatta_C"."SRM__Regatta_pid" AS "SRM__Regatta_C_SRM__Regatta_pid",
           "SRM__Regatta_C".is_team_race AS "SRM__Regatta_C_is_team_race",
           "SRM__Regatta_H"."SRM__Regatta_pid" AS "SRM__Regatta_H_SRM__Regatta_pid"
         FROM "SRM__Regatta"
           LEFT OUTER JOIN "SRM__Regatta_C" ON "SRM__Regatta".pid = "SRM__Regatta_C"."SRM__Regatta_pid"
           LEFT OUTER JOIN "SRM__Regatta_H" ON "SRM__Regatta".pid = "SRM__Regatta_H"."SRM__Regatta_pid"
    SRM.Regatta_C ['SRM__Regatta', 'SRM__Regatta_C']
        SQL: SELECT
           "SRM__Regatta".__result_date AS "SRM__Regatta___result_date",
           "SRM__Regatta".__result_software AS "SRM__Regatta___result_software",
           "SRM__Regatta".__result_status AS "SRM__Regatta___result_status",
           "SRM__Regatta".boat_class_pid AS "SRM__Regatta_boat_class_pid",
           "SRM__Regatta".discards AS "SRM__Regatta_discards",
           "SRM__Regatta".electric AS "SRM__Regatta_electric",
           "SRM__Regatta".is_cancelled AS "SRM__Regatta_is_cancelled",
           "SRM__Regatta".kind AS "SRM__Regatta_kind",
           "SRM__Regatta".last_cid AS "SRM__Regatta_last_cid",
           "SRM__Regatta".left_pid AS "SRM__Regatta_left_pid",
           "SRM__Regatta".perma_name AS "SRM__Regatta_perma_name",
           "SRM__Regatta".pid AS "SRM__Regatta_pid",
           "SRM__Regatta".races AS "SRM__Regatta_races",
           "SRM__Regatta".type_name AS "SRM__Regatta_type_name",
           "SRM__Regatta".x_locked AS "SRM__Regatta_x_locked",
           "SRM__Regatta_C"."SRM__Regatta_pid" AS "SRM__Regatta_C_SRM__Regatta_pid",
           "SRM__Regatta_C".is_team_race AS "SRM__Regatta_C_is_team_race"
         FROM "SRM__Regatta_C"
           JOIN "SRM__Regatta" ON "SRM__Regatta".pid = "SRM__Regatta_C"."SRM__Regatta_pid"
    SRM.Regatta_H ['SRM__Regatta', 'SRM__Regatta_H']
        SQL: SELECT
           "SRM__Regatta".__result_date AS "SRM__Regatta___result_date",
           "SRM__Regatta".__result_software AS "SRM__Regatta___result_software",
           "SRM__Regatta".__result_status AS "SRM__Regatta___result_status",
           "SRM__Regatta".boat_class_pid AS "SRM__Regatta_boat_class_pid",
           "SRM__Regatta".discards AS "SRM__Regatta_discards",
           "SRM__Regatta".electric AS "SRM__Regatta_electric",
           "SRM__Regatta".is_cancelled AS "SRM__Regatta_is_cancelled",
           "SRM__Regatta".kind AS "SRM__Regatta_kind",
           "SRM__Regatta".last_cid AS "SRM__Regatta_last_cid",
           "SRM__Regatta".left_pid AS "SRM__Regatta_left_pid",
           "SRM__Regatta".perma_name AS "SRM__Regatta_perma_name",
           "SRM__Regatta".pid AS "SRM__Regatta_pid",
           "SRM__Regatta".races AS "SRM__Regatta_races",
           "SRM__Regatta".type_name AS "SRM__Regatta_type_name",
           "SRM__Regatta".x_locked AS "SRM__Regatta_x_locked",
           "SRM__Regatta_H"."SRM__Regatta_pid" AS "SRM__Regatta_H_SRM__Regatta_pid"
         FROM "SRM__Regatta_H"
           JOIN "SRM__Regatta" ON "SRM__Regatta".pid = "SRM__Regatta_H"."SRM__Regatta_pid"
    SRM.Page ['SRM__Page', 'SWP__Page']
        SQL: SELECT
           "SRM__Page"."SWP__Page_pid" AS "SRM__Page_SWP__Page_pid",
           "SRM__Page"."desc" AS "SRM__Page_desc",
           "SRM__Page".event_pid AS "SRM__Page_event_pid",
           "SWP__Page".__date_finish AS "SWP__Page___date_finish",
           "SWP__Page".__date_start AS "SWP__Page___date_start",
           "SWP__Page".contents AS "SWP__Page_contents",
           "SWP__Page".electric AS "SWP__Page_electric",
           "SWP__Page".format AS "SWP__Page_format",
           "SWP__Page".head_line AS "SWP__Page_head_line",
           "SWP__Page".hidden AS "SWP__Page_hidden",
           "SWP__Page".last_cid AS "SWP__Page_last_cid",
           "SWP__Page".perma_name AS "SWP__Page_perma_name",
           "SWP__Page".pid AS "SWP__Page_pid",
           "SWP__Page".prio AS "SWP__Page_prio",
           "SWP__Page".short_title AS "SWP__Page_short_title",
           "SWP__Page".text AS "SWP__Page_text",
           "SWP__Page".title AS "SWP__Page_title",
           "SWP__Page".type_name AS "SWP__Page_type_name",
           "SWP__Page".x_locked AS "SWP__Page_x_locked"
         FROM "SRM__Page"
           JOIN "SWP__Page" ON "SWP__Page".pid = "SRM__Page"."SWP__Page_pid"
    SRM._Boat_Class_ ['SRM__Boat_Class', 'SRM__Handicap', 'SRM___Boat_Class_']
        SQL: SELECT
           "SRM__Boat_Class"."SRM___Boat_Class__pid" AS "SRM__Boat_Class_SRM___Boat_Class__pid",
           "SRM__Boat_Class".beam AS "SRM__Boat_Class_beam",
           "SRM__Boat_Class".loa AS "SRM__Boat_Class_loa",
           "SRM__Boat_Class".max_crew AS "SRM__Boat_Class_max_crew",
           "SRM__Boat_Class".sail_area AS "SRM__Boat_Class_sail_area",
           "SRM__Handicap"."SRM___Boat_Class__pid" AS "SRM__Handicap_SRM___Boat_Class__pid",
           "SRM___Boat_Class_".__raw_name AS "SRM___Boat_Class____raw_name",
           "SRM___Boat_Class_".electric AS "SRM___Boat_Class__electric",
           "SRM___Boat_Class_".last_cid AS "SRM___Boat_Class__last_cid",
           "SRM___Boat_Class_".name AS "SRM___Boat_Class__name",
           "SRM___Boat_Class_".pid AS "SRM___Boat_Class__pid",
           "SRM___Boat_Class_".type_name AS "SRM___Boat_Class__type_name",
           "SRM___Boat_Class_".x_locked AS "SRM___Boat_Class__x_locked"
         FROM "SRM___Boat_Class_"
           LEFT OUTER JOIN "SRM__Boat_Class" ON "SRM___Boat_Class_".pid = "SRM__Boat_Class"."SRM___Boat_Class__pid"
           LEFT OUTER JOIN "SRM__Handicap" ON "SRM___Boat_Class_".pid = "SRM__Handicap"."SRM___Boat_Class__pid"
    SRM.Boat_Class ['SRM__Boat_Class', 'SRM___Boat_Class_']
        SQL: SELECT
           "SRM__Boat_Class"."SRM___Boat_Class__pid" AS "SRM__Boat_Class_SRM___Boat_Class__pid",
           "SRM__Boat_Class".beam AS "SRM__Boat_Class_beam",
           "SRM__Boat_Class".loa AS "SRM__Boat_Class_loa",
           "SRM__Boat_Class".max_crew AS "SRM__Boat_Class_max_crew",
           "SRM__Boat_Class".sail_area AS "SRM__Boat_Class_sail_area",
           "SRM___Boat_Class_".__raw_name AS "SRM___Boat_Class____raw_name",
           "SRM___Boat_Class_".electric AS "SRM___Boat_Class__electric",
           "SRM___Boat_Class_".last_cid AS "SRM___Boat_Class__last_cid",
           "SRM___Boat_Class_".name AS "SRM___Boat_Class__name",
           "SRM___Boat_Class_".pid AS "SRM___Boat_Class__pid",
           "SRM___Boat_Class_".type_name AS "SRM___Boat_Class__type_name",
           "SRM___Boat_Class_".x_locked AS "SRM___Boat_Class__x_locked"
         FROM "SRM__Boat_Class"
           JOIN "SRM___Boat_Class_" ON "SRM___Boat_Class_".pid = "SRM__Boat_Class"."SRM___Boat_Class__pid"
    SRM.Handicap ['SRM__Handicap', 'SRM___Boat_Class_']
        SQL: SELECT
           "SRM__Handicap"."SRM___Boat_Class__pid" AS "SRM__Handicap_SRM___Boat_Class__pid",
           "SRM___Boat_Class_".__raw_name AS "SRM___Boat_Class____raw_name",
           "SRM___Boat_Class_".electric AS "SRM___Boat_Class__electric",
           "SRM___Boat_Class_".last_cid AS "SRM___Boat_Class__last_cid",
           "SRM___Boat_Class_".name AS "SRM___Boat_Class__name",
           "SRM___Boat_Class_".pid AS "SRM___Boat_Class__pid",
           "SRM___Boat_Class_".type_name AS "SRM___Boat_Class__type_name",
           "SRM___Boat_Class_".x_locked AS "SRM___Boat_Class__x_locked"
         FROM "SRM__Handicap"
           JOIN "SRM___Boat_Class_" ON "SRM___Boat_Class_".pid = "SRM__Handicap"."SRM___Boat_Class__pid"
    SWP.Page ['SRM__Page', 'SWP__Clip_X', 'SWP__Page', 'SWP__Page_Y']
        SQL: SELECT
           "SRM__Page"."SWP__Page_pid" AS "SRM__Page_SWP__Page_pid",
           "SRM__Page"."desc" AS "SRM__Page_desc",
           "SRM__Page".event_pid AS "SRM__Page_event_pid",
           "SWP__Clip_X"."SWP__Page_pid" AS "SWP__Clip_X_SWP__Page_pid",
           "SWP__Clip_X".link_to AS "SWP__Clip_X_link_to",
           "SWP__Page".__date_finish AS "SWP__Page___date_finish",
           "SWP__Page".__date_start AS "SWP__Page___date_start",
           "SWP__Page".contents AS "SWP__Page_contents",
           "SWP__Page".electric AS "SWP__Page_electric",
           "SWP__Page".format AS "SWP__Page_format",
           "SWP__Page".head_line AS "SWP__Page_head_line",
           "SWP__Page".hidden AS "SWP__Page_hidden",
           "SWP__Page".last_cid AS "SWP__Page_last_cid",
           "SWP__Page".perma_name AS "SWP__Page_perma_name",
           "SWP__Page".pid AS "SWP__Page_pid",
           "SWP__Page".prio AS "SWP__Page_prio",
           "SWP__Page".short_title AS "SWP__Page_short_title",
           "SWP__Page".text AS "SWP__Page_text",
           "SWP__Page".title AS "SWP__Page_title",
           "SWP__Page".type_name AS "SWP__Page_type_name",
           "SWP__Page".x_locked AS "SWP__Page_x_locked",
           "SWP__Page_Y"."SWP__Page_pid" AS "SWP__Page_Y_SWP__Page_pid",
           "SWP__Page_Y".year AS "SWP__Page_Y_year"
         FROM "SWP__Page"
           LEFT OUTER JOIN "SRM__Page" ON "SWP__Page".pid = "SRM__Page"."SWP__Page_pid"
           LEFT OUTER JOIN "SWP__Clip_X" ON "SWP__Page".pid = "SWP__Clip_X"."SWP__Page_pid"
           LEFT OUTER JOIN "SWP__Page_Y" ON "SWP__Page".pid = "SWP__Page_Y"."SWP__Page_pid"
    SWP.Clip_X ['SWP__Clip_X', 'SWP__Page']
        SQL: SELECT
           "SWP__Clip_X"."SWP__Page_pid" AS "SWP__Clip_X_SWP__Page_pid",
           "SWP__Clip_X".link_to AS "SWP__Clip_X_link_to",
           "SWP__Page".__date_finish AS "SWP__Page___date_finish",
           "SWP__Page".__date_start AS "SWP__Page___date_start",
           "SWP__Page".contents AS "SWP__Page_contents",
           "SWP__Page".electric AS "SWP__Page_electric",
           "SWP__Page".format AS "SWP__Page_format",
           "SWP__Page".head_line AS "SWP__Page_head_line",
           "SWP__Page".hidden AS "SWP__Page_hidden",
           "SWP__Page".last_cid AS "SWP__Page_last_cid",
           "SWP__Page".perma_name AS "SWP__Page_perma_name",
           "SWP__Page".pid AS "SWP__Page_pid",
           "SWP__Page".prio AS "SWP__Page_prio",
           "SWP__Page".short_title AS "SWP__Page_short_title",
           "SWP__Page".text AS "SWP__Page_text",
           "SWP__Page".title AS "SWP__Page_title",
           "SWP__Page".type_name AS "SWP__Page_type_name",
           "SWP__Page".x_locked AS "SWP__Page_x_locked"
         FROM "SWP__Clip_X"
           JOIN "SWP__Page" ON "SWP__Page".pid = "SWP__Clip_X"."SWP__Page_pid"
    SWP.Page_Y ['SWP__Page', 'SWP__Page_Y']
        SQL: SELECT
           "SWP__Page".__date_finish AS "SWP__Page___date_finish",
           "SWP__Page".__date_start AS "SWP__Page___date_start",
           "SWP__Page".contents AS "SWP__Page_contents",
           "SWP__Page".electric AS "SWP__Page_electric",
           "SWP__Page".format AS "SWP__Page_format",
           "SWP__Page".head_line AS "SWP__Page_head_line",
           "SWP__Page".hidden AS "SWP__Page_hidden",
           "SWP__Page".last_cid AS "SWP__Page_last_cid",
           "SWP__Page".perma_name AS "SWP__Page_perma_name",
           "SWP__Page".pid AS "SWP__Page_pid",
           "SWP__Page".prio AS "SWP__Page_prio",
           "SWP__Page".short_title AS "SWP__Page_short_title",
           "SWP__Page".text AS "SWP__Page_text",
           "SWP__Page".title AS "SWP__Page_title",
           "SWP__Page".type_name AS "SWP__Page_type_name",
           "SWP__Page".x_locked AS "SWP__Page_x_locked",
           "SWP__Page_Y"."SWP__Page_pid" AS "SWP__Page_Y_SWP__Page_pid",
           "SWP__Page_Y".year AS "SWP__Page_Y_year"
         FROM "SWP__Page_Y"
           JOIN "SWP__Page" ON "SWP__Page".pid = "SWP__Page_Y"."SWP__Page_pid"

"""

_test_select = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> show_select (scope)
    Auth.Account_in_Group
        SELECT "Auth__Account_in_Group".electric,
               "Auth__Account_in_Group".last_cid,
               "Auth__Account_in_Group".left_pid,
               "Auth__Account_in_Group".pid,
               "Auth__Account_in_Group".right_pid,
               "Auth__Account_in_Group".type_name,
               "Auth__Account_in_Group".x_locked
        FROM "Auth__Account_in_Group"
    Auth.Certificate
        SELECT "Auth__Certificate"."desc",
               "Auth__Certificate".__validity_finish,
               "Auth__Certificate".__validity_start,
               "Auth__Certificate".cert_id,
               "Auth__Certificate".electric,
               "Auth__Certificate".email,
               "Auth__Certificate".last_cid,
               "Auth__Certificate".pem,
               "Auth__Certificate".pid,
               "Auth__Certificate".revocation_date,
               "Auth__Certificate".type_name,
               "Auth__Certificate".x_locked
        FROM "Auth__Certificate"
    Auth.Group
        SELECT "Auth__Group"."desc",
               "Auth__Group".electric,
               "Auth__Group".last_cid,
               "Auth__Group".name,
               "Auth__Group".pid,
               "Auth__Group".type_name,
               "Auth__Group".x_locked
        FROM "Auth__Group"
    Auth._Account_
        SELECT "Auth___Account_".electric,
               "Auth___Account_".enabled,
               "Auth___Account_".last_cid,
               "Auth___Account_".name,
               "Auth___Account_".pid,
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
        SELECT "EVT__Event".__date_finish,
               "EVT__Event".__date_start,
               "EVT__Event".__time_finish,
               "EVT__Event".__time_start,
               "EVT__Event".calendar_pid,
               "EVT__Event".detail,
               "EVT__Event".electric,
               "EVT__Event".last_cid,
               "EVT__Event".left_pid,
               "EVT__Event".pid,
               "EVT__Event".short_title,
               "EVT__Event".type_name,
               "EVT__Event".x_locked
        FROM "EVT__Event"
    EVT.Event_occurs
        SELECT "EVT__Event_occurs".__time_finish,
               "EVT__Event_occurs".__time_start,
               "EVT__Event_occurs".date,
               "EVT__Event_occurs".last_cid,
               "EVT__Event_occurs".left_pid,
               "EVT__Event_occurs".pid,
               "EVT__Event_occurs".type_name,
               "EVT__Event_occurs".x_locked
        FROM "EVT__Event_occurs"
    EVT.Recurrence_Rule
        SELECT "EVT__Recurrence_Rule"."desc",
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
               "EVT__Recurrence_Rule".pid,
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
        SELECT "EVT__Recurrence_Spec".date_exceptions,
               "EVT__Recurrence_Spec".dates,
               "EVT__Recurrence_Spec".electric,
               "EVT__Recurrence_Spec".last_cid,
               "EVT__Recurrence_Spec".left_pid,
               "EVT__Recurrence_Spec".pid,
               "EVT__Recurrence_Spec".type_name,
               "EVT__Recurrence_Spec".x_locked
        FROM "EVT__Recurrence_Spec"
    EVT.Calendar
        SELECT "EVT__Calendar"."desc",
               "EVT__Calendar".electric,
               "EVT__Calendar".last_cid,
               "EVT__Calendar".name,
               "EVT__Calendar".pid,
               "EVT__Calendar".type_name,
               "EVT__Calendar".x_locked
        FROM "EVT__Calendar"
    PAP.Address_Position
        SELECT "PAP__Address_Position".__position___raw_lat,
               "PAP__Address_Position".__position___raw_lon,
               "PAP__Address_Position".__position_height,
               "PAP__Address_Position".__position_lat,
               "PAP__Address_Position".__position_lon,
               "PAP__Address_Position".electric,
               "PAP__Address_Position".last_cid,
               "PAP__Address_Position".left_pid,
               "PAP__Address_Position".pid,
               "PAP__Address_Position".type_name,
               "PAP__Address_Position".x_locked
        FROM "PAP__Address_Position"
    SRM.Boat
        SELECT "SRM__Boat".__raw_sail_number,
               "SRM__Boat".__raw_sail_number_x,
               "SRM__Boat".electric,
               "SRM__Boat".last_cid,
               "SRM__Boat".left_pid,
               "SRM__Boat".name,
               "SRM__Boat".nation,
               "SRM__Boat".pid,
               "SRM__Boat".sail_number,
               "SRM__Boat".sail_number_x,
               "SRM__Boat".type_name,
               "SRM__Boat".x_locked
        FROM "SRM__Boat"
    SRM.Race_Result
        SELECT "SRM__Race_Result".discarded,
               "SRM__Race_Result".electric,
               "SRM__Race_Result".last_cid,
               "SRM__Race_Result".left_pid,
               "SRM__Race_Result".pid,
               "SRM__Race_Result".points,
               "SRM__Race_Result".race,
               "SRM__Race_Result".status,
               "SRM__Race_Result".type_name,
               "SRM__Race_Result".x_locked
        FROM "SRM__Race_Result"
    SRM.Regatta
        SELECT "SRM__Regatta".__result_date,
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
               "SRM__Regatta".pid,
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
        SELECT "SRM__Sailor".__raw_mna_number,
               "SRM__Sailor".club_pid,
               "SRM__Sailor".electric,
               "SRM__Sailor".last_cid,
               "SRM__Sailor".left_pid,
               "SRM__Sailor".mna_number,
               "SRM__Sailor".nation,
               "SRM__Sailor".pid,
               "SRM__Sailor".type_name,
               "SRM__Sailor".x_locked
        FROM "SRM__Sailor"
    SRM.Team
        SELECT "SRM__Team"."desc",
               "SRM__Team".__raw_name,
               "SRM__Team".club_pid,
               "SRM__Team".electric,
               "SRM__Team".last_cid,
               "SRM__Team".leader_pid,
               "SRM__Team".left_pid,
               "SRM__Team".name,
               "SRM__Team".pid,
               "SRM__Team".place,
               "SRM__Team".registration_date,
               "SRM__Team".type_name,
               "SRM__Team".x_locked
        FROM "SRM__Team"
    SWP.Clip_O
        SELECT "SWP__Clip_O".__date_finish,
               "SWP__Clip_O".__date_start,
               "SWP__Clip_O".__date_x_finish,
               "SWP__Clip_O".__date_x_start,
               "SWP__Clip_O".abstract,
               "SWP__Clip_O".contents,
               "SWP__Clip_O".electric,
               "SWP__Clip_O".last_cid,
               "SWP__Clip_O".left_pid,
               "SWP__Clip_O".pid,
               "SWP__Clip_O".prio,
               "SWP__Clip_O".type_name,
               "SWP__Clip_O".x_locked
        FROM "SWP__Clip_O"
    SWP.Picture
        SELECT "SWP__Picture".__photo_extension,
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
               "SWP__Picture".pid,
               "SWP__Picture".type_name,
               "SWP__Picture".x_locked
        FROM "SWP__Picture"
    PAP.Person_has_Account
        SELECT "PAP__Person_has_Account".electric,
               "PAP__Person_has_Account".last_cid,
               "PAP__Person_has_Account".left_pid,
               "PAP__Person_has_Account".pid,
               "PAP__Person_has_Account".right_pid,
               "PAP__Person_has_Account".type_name,
               "PAP__Person_has_Account".x_locked
        FROM "PAP__Person_has_Account"
    PAP.Company_has_Address
        SELECT "PAP__Company_has_Address"."desc",
               "PAP__Company_has_Address".electric,
               "PAP__Company_has_Address".last_cid,
               "PAP__Company_has_Address".left_pid,
               "PAP__Company_has_Address".pid,
               "PAP__Company_has_Address".right_pid,
               "PAP__Company_has_Address".type_name,
               "PAP__Company_has_Address".x_locked
        FROM "PAP__Company_has_Address"
    PAP.Person_has_Address
        SELECT "PAP__Person_has_Address"."desc",
               "PAP__Person_has_Address".electric,
               "PAP__Person_has_Address".last_cid,
               "PAP__Person_has_Address".left_pid,
               "PAP__Person_has_Address".pid,
               "PAP__Person_has_Address".right_pid,
               "PAP__Person_has_Address".type_name,
               "PAP__Person_has_Address".x_locked
        FROM "PAP__Person_has_Address"
    PAP.Company_has_Email
        SELECT "PAP__Company_has_Email"."desc",
               "PAP__Company_has_Email".electric,
               "PAP__Company_has_Email".last_cid,
               "PAP__Company_has_Email".left_pid,
               "PAP__Company_has_Email".pid,
               "PAP__Company_has_Email".right_pid,
               "PAP__Company_has_Email".type_name,
               "PAP__Company_has_Email".x_locked
        FROM "PAP__Company_has_Email"
    PAP.Person_has_Email
        SELECT "PAP__Person_has_Email"."desc",
               "PAP__Person_has_Email".electric,
               "PAP__Person_has_Email".last_cid,
               "PAP__Person_has_Email".left_pid,
               "PAP__Person_has_Email".pid,
               "PAP__Person_has_Email".right_pid,
               "PAP__Person_has_Email".type_name,
               "PAP__Person_has_Email".x_locked
        FROM "PAP__Person_has_Email"
    PAP.Company_has_Phone
        SELECT "PAP__Company_has_Phone"."desc",
               "PAP__Company_has_Phone".electric,
               "PAP__Company_has_Phone".extension,
               "PAP__Company_has_Phone".last_cid,
               "PAP__Company_has_Phone".left_pid,
               "PAP__Company_has_Phone".pid,
               "PAP__Company_has_Phone".right_pid,
               "PAP__Company_has_Phone".type_name,
               "PAP__Company_has_Phone".x_locked
        FROM "PAP__Company_has_Phone"
    PAP.Person_has_Phone
        SELECT "PAP__Person_has_Phone"."desc",
               "PAP__Person_has_Phone".electric,
               "PAP__Person_has_Phone".extension,
               "PAP__Person_has_Phone".last_cid,
               "PAP__Person_has_Phone".left_pid,
               "PAP__Person_has_Phone".pid,
               "PAP__Person_has_Phone".right_pid,
               "PAP__Person_has_Phone".type_name,
               "PAP__Person_has_Phone".x_locked
        FROM "PAP__Person_has_Phone"
    PAP.Company_has_Url
        SELECT "PAP__Company_has_Url"."desc",
               "PAP__Company_has_Url".electric,
               "PAP__Company_has_Url".last_cid,
               "PAP__Company_has_Url".left_pid,
               "PAP__Company_has_Url".pid,
               "PAP__Company_has_Url".right_pid,
               "PAP__Company_has_Url".type_name,
               "PAP__Company_has_Url".x_locked
        FROM "PAP__Company_has_Url"
    PAP.Person_has_Url
        SELECT "PAP__Person_has_Url"."desc",
               "PAP__Person_has_Url".electric,
               "PAP__Person_has_Url".last_cid,
               "PAP__Person_has_Url".left_pid,
               "PAP__Person_has_Url".pid,
               "PAP__Person_has_Url".right_pid,
               "PAP__Person_has_Url".type_name,
               "PAP__Person_has_Url".x_locked
        FROM "PAP__Person_has_Url"
    SRM.Boat_in_Regatta
        SELECT "SRM__Boat_in_Regatta".electric,
               "SRM__Boat_in_Regatta".last_cid,
               "SRM__Boat_in_Regatta".left_pid,
               "SRM__Boat_in_Regatta".pid,
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
        SELECT "SRM__Crew_Member".electric,
               "SRM__Crew_Member".key,
               "SRM__Crew_Member".last_cid,
               "SRM__Crew_Member".left_pid,
               "SRM__Crew_Member".pid,
               "SRM__Crew_Member".right_pid,
               "SRM__Crew_Member".role,
               "SRM__Crew_Member".type_name,
               "SRM__Crew_Member".x_locked
        FROM "SRM__Crew_Member"
    SRM.Team_has_Boat_in_Regatta
        SELECT "SRM__Team_has_Boat_in_Regatta".electric,
               "SRM__Team_has_Boat_in_Regatta".last_cid,
               "SRM__Team_has_Boat_in_Regatta".left_pid,
               "SRM__Team_has_Boat_in_Regatta".pid,
               "SRM__Team_has_Boat_in_Regatta".right_pid,
               "SRM__Team_has_Boat_in_Regatta".type_name,
               "SRM__Team_has_Boat_in_Regatta".x_locked
        FROM "SRM__Team_has_Boat_in_Regatta"
    PAP.Address
        SELECT "PAP__Address"."desc",
               "PAP__Address".__raw_city,
               "PAP__Address".__raw_country,
               "PAP__Address".__raw_region,
               "PAP__Address".__raw_street,
               "PAP__Address".__raw_zip,
               "PAP__Address".city,
               "PAP__Address".country,
               "PAP__Address".electric,
               "PAP__Address".last_cid,
               "PAP__Address".pid,
               "PAP__Address".region,
               "PAP__Address".street,
               "PAP__Address".type_name,
               "PAP__Address".x_locked,
               "PAP__Address".zip
        FROM "PAP__Address"
    PAP.Email
        SELECT "PAP__Email"."desc",
               "PAP__Email".__raw_address,
               "PAP__Email".address,
               "PAP__Email".electric,
               "PAP__Email".last_cid,
               "PAP__Email".pid,
               "PAP__Email".type_name,
               "PAP__Email".x_locked
        FROM "PAP__Email"
    PAP.Phone
        SELECT "PAP__Phone"."desc",
               "PAP__Phone".area_code,
               "PAP__Phone".country_code,
               "PAP__Phone".electric,
               "PAP__Phone".last_cid,
               "PAP__Phone".number,
               "PAP__Phone".pid,
               "PAP__Phone".type_name,
               "PAP__Phone".x_locked
        FROM "PAP__Phone"
    PAP.Url
        SELECT "PAP__Url"."desc",
               "PAP__Url".electric,
               "PAP__Url".last_cid,
               "PAP__Url".pid,
               "PAP__Url".type_name,
               "PAP__Url".value,
               "PAP__Url".x_locked
        FROM "PAP__Url"
    PAP.Company
        SELECT "PAP__Company".__lifetime_finish,
               "PAP__Company".__lifetime_start,
               "PAP__Company".__raw_name,
               "PAP__Company".__raw_registered_in,
               "PAP__Company".__raw_short_name,
               "PAP__Company".electric,
               "PAP__Company".last_cid,
               "PAP__Company".name,
               "PAP__Company".pid,
               "PAP__Company".registered_in,
               "PAP__Company".short_name,
               "PAP__Company".type_name,
               "PAP__Company".x_locked
        FROM "PAP__Company"
    PAP.Person
        SELECT "PAP__Person".__lifetime_finish,
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
               "PAP__Person".pid,
               "PAP__Person".salutation,
               "PAP__Person".sex,
               "PAP__Person".title,
               "PAP__Person".type_name,
               "PAP__Person".x_locked
        FROM "PAP__Person"
    SRM.Club
        SELECT "SRM__Club".__raw_name,
               "SRM__Club".electric,
               "SRM__Club".last_cid,
               "SRM__Club".long_name,
               "SRM__Club".name,
               "SRM__Club".pid,
               "SRM__Club".type_name,
               "SRM__Club".x_locked
        FROM "SRM__Club"
    SRM.Page SWP.Page
        SELECT "SRM__Page"."SWP__Page_pid",
               "SRM__Page"."desc",
               "SRM__Page".event_pid
        FROM "SRM__Page"
    SRM.Regatta_Event
        SELECT "SRM__Regatta_Event"."desc",
               "SRM__Regatta_Event".__date_finish,
               "SRM__Regatta_Event".__date_start,
               "SRM__Regatta_Event".__raw_name,
               "SRM__Regatta_Event".club_pid,
               "SRM__Regatta_Event".electric,
               "SRM__Regatta_Event".is_cancelled,
               "SRM__Regatta_Event".last_cid,
               "SRM__Regatta_Event".name,
               "SRM__Regatta_Event".perma_name,
               "SRM__Regatta_Event".pid,
               "SRM__Regatta_Event".type_name,
               "SRM__Regatta_Event".x_locked
        FROM "SRM__Regatta_Event"
    SRM._Boat_Class_
        SELECT "SRM___Boat_Class_".__raw_name,
               "SRM___Boat_Class_".electric,
               "SRM___Boat_Class_".last_cid,
               "SRM___Boat_Class_".name,
               "SRM___Boat_Class_".pid,
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
        SELECT "SWP__Gallery".__date_finish,
               "SWP__Gallery".__date_start,
               "SWP__Gallery".directory,
               "SWP__Gallery".electric,
               "SWP__Gallery".last_cid,
               "SWP__Gallery".perma_name,
               "SWP__Gallery".pid,
               "SWP__Gallery".short_title,
               "SWP__Gallery".title,
               "SWP__Gallery".type_name,
               "SWP__Gallery".x_locked
        FROM "SWP__Gallery"
    SWP.Page
        SELECT "SWP__Page".__date_finish,
               "SWP__Page".__date_start,
               "SWP__Page".contents,
               "SWP__Page".electric,
               "SWP__Page".format,
               "SWP__Page".head_line,
               "SWP__Page".hidden,
               "SWP__Page".last_cid,
               "SWP__Page".perma_name,
               "SWP__Page".pid,
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

    >>> scope.app_type._T_Extension [0]._sa_table = None
    >>> for T in scope.app_type._T_Extension :
    ...     if T._sa_table is not None :
    ...         print (T.type_name)
    Auth._Account_
    Auth.Account_Anonymous
    Auth.Account
    Auth.Certificate
    Auth.Group
    Auth.Account_in_Group
    Auth.Account_Activation
    Auth.Account_Password_Change_Required
    Auth.Account_EMail_Verification
    Auth.Account_Password_Reset
    EVT.Calendar
    SWP.Page
    SWP.Page_Y
    EVT.Event
    EVT.Event_occurs
    EVT.Recurrence_Spec
    EVT.Recurrence_Rule
    PAP.Address
    PAP.Company
    PAP.Email
    PAP.Phone
    PAP.Person
    PAP.Url
    PAP.Address_Position
    PAP.Person_has_Account
    SRM._Boat_Class_
    SRM.Boat_Class
    SRM.Handicap
    SRM.Boat
    SRM.Club
    SRM.Regatta_Event
    SWP.Clip_O
    SWP.Clip_X
    SWP.Gallery
    SWP.Picture
    SRM.Page
    SRM.Regatta
    SRM.Regatta_C
    SRM.Regatta_H
    SRM.Sailor
    SRM.Boat_in_Regatta
    SRM.Race_Result
    SRM.Team
    SRM.Crew_Member
    SRM.Team_has_Boat_in_Regatta
    PAP.Company_has_Url
    PAP.Person_has_Url
    PAP.Company_has_Phone
    PAP.Person_has_Phone
    PAP.Company_has_Email
    PAP.Person_has_Email
    PAP.Company_has_Address
    PAP.Person_has_Address

    >>> show_tables (scope)
    Auth.Account_in_Group <Table Auth__Account_in_Group>
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Account left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Group right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    Auth.Certificate <Table Auth__Certificate>
        Column __validity_finish         : Datetime             Optional__Nested Date-Time finish
        Column __validity_start          : Datetime             Necessary__Nested Date-Time start
        Column cert_id                   : Integer              Internal__Just_Once Surrogate cert_id primary
        Column desc                      : Varchar(40)          Primary_Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column email                     : Varchar(80)          Primary Email email
        Column last_cid                  : Integer              Internal Int last_cid
        Column pem                       : Blob                 Internal None pem
        Column pid                       : Integer              Internal__Just_Once Surrogate pid
        Column revocation_date           : Datetime             Optional Date-Time revocation_date
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    Auth.Group <Table Auth__Group>
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(32)          Primary String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    Auth._Account_ <Table Auth___Account_>
        Column electric                  : Boolean              Internal Boolean electric
        Column enabled                   : Boolean              Optional Boolean enabled
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(80)          Primary Email name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column superuser                 : Boolean              Optional Boolean superuser
        Column suspended                 : Boolean              Internal Boolean suspended
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    Auth.Account Auth._Account_ <Table Auth__Account>
        Column Auth___Account__pid       : Integer              ---------- primary ForeignKey(u'Auth___Account_.pid')
        Column password                  : Varchar(120)         Internal String password
        Column ph_name                   : Varchar(64)          Internal__Sticky String ph_name
    EVT.Event <Table EVT__Event>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Nested Date start
        Column __time_finish             : Time                 Optional__Nested Time finish
        Column __time_start              : Time                 Necessary__Nested Time start
        Column calendar_pid              : Integer              Primary_Optional__Id_Entity_Reference Entity calendar
        Column detail                    : Varchar(160)         Optional String detail
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Page left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column short_title               : Varchar(64)          Optional__Computed_Set String short_title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    EVT.Event_occurs <Table EVT__Event_occurs>
        Column __time_finish             : Time                 Optional__Nested Time finish
        Column __time_start              : Time                 Necessary__Nested Time start
        Column date                      : Date                 Primary Date date
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Event left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    EVT.Recurrence_Rule <Table EVT__Recurrence_Rule>
        Column count                     : Integer              Optional Int count
        Column desc                      : Varchar(20)          Primary_Optional String desc
        Column easter_offset             : Blob                 Optional__Typed_Collection Int_List easter_offset
        Column electric                  : Boolean              Internal Boolean electric
        Column finish                    : Date                 Optional__Computed_Set Date finish
        Column is_exception              : Boolean              Primary_Optional Boolean is_exception
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Recurrence_Spec left
        Column month                     : Blob                 Optional__Typed_Collection Int_List month
        Column month_day                 : Blob                 Optional__Typed_Collection Int_List month_day
        Column period                    : Integer              Optional Int period
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column restrict_pos              : Blob                 Optional__Typed_Collection Int_List restrict_pos
        Column start                     : Date                 Optional__Computed_Set Date start
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column unit                      : Integer              Optional__Sticky Unit unit
        Column week                      : Blob                 Optional__Typed_Collection Int_List week
        Column week_day                  : Blob                 Optional__Typed_Collection Weekday_RR_List week_day
        Column x_locked                  : Boolean              Internal Boolean x_locked
        Column year_day                  : Blob                 Optional__Typed_Collection Int_List year_day
    EVT.Recurrence_Spec <Table EVT__Recurrence_Spec>
        Column date_exceptions           : Blob                 Optional__Typed_Collection Date_List date_exceptions
        Column dates                     : Blob                 Optional__Typed_Collection Date_List dates
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Event left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    EVT.Calendar <Table EVT__Calendar>
        Column desc                      : Varchar(80)          Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(32)          Primary Name name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Address_Position <Table PAP__Address_Position>
        Column __position___raw_lat      : Varchar(60)          Necessary__Raw_Value__Nested Angle lat
        Column __position___raw_lon      : Varchar(60)          Necessary__Raw_Value__Nested Angle lon
        Column __position_height         : Float                Optional__Nested Float height
        Column __position_lat            : Float                Necessary__Raw_Value__Nested Angle lat
        Column __position_lon            : Float                Necessary__Raw_Value__Nested Angle lon
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Address left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Boat <Table SRM__Boat>
        Column __raw_sail_number         : Varchar(60)          Primary_Optional__Raw_Value Int sail_number
        Column __raw_sail_number_x       : Varchar(60)          Primary_Optional__Raw_Value String sail_number_x
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Boat_Class left
        Column name                      : Varchar(48)          Optional String name
        Column nation                    : Varchar(3)           Primary_Optional Nation nation
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column sail_number               : Integer              Primary_Optional__Raw_Value Int sail_number
        Column sail_number_x             : Varchar(8)           Primary_Optional__Raw_Value String sail_number_x
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Race_Result <Table SRM__Race_Result>
        Column discarded                 : Boolean              Optional__Sticky Boolean discarded
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Boat_in_Regatta left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column points                    : Integer              Necessary Int points
        Column race                      : Smallint             Primary Int race
        Column status                    : Varchar(8)           Optional String status
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Regatta <Table SRM__Regatta>
        Column __result_date             : Datetime             Necessary__Nested Date-Time date
        Column __result_software         : Varchar(64)          Optional__Nested String software
        Column __result_status           : Varchar(64)          Optional__Nested String status
        Column boat_class_pid            : Integer              Primary__Id_Entity_Reference Entity boat_class
        Column discards                  : Integer              Optional Int discards
        Column electric                  : Boolean              Internal Boolean electric
        Column is_cancelled              : Boolean              Optional__Computed_Set Boolean is_cancelled
        Column kind                      : Varchar(32)          Optional String kind
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Regatta_Event left
        Column perma_name                : Varchar(64)          Internal__Auto_Update_Lazy__Computed_Set String perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column races                     : Integer              Optional Int races
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Regatta_C SRM.Regatta <Table SRM__Regatta_C>
        Column SRM__Regatta_pid          : Integer              ---------- primary ForeignKey(u'SRM__Regatta.pid')
        Column is_team_race              : Boolean              Optional Boolean is_team_race
    SRM.Regatta_H SRM.Regatta <Table SRM__Regatta_H>
        Column SRM__Regatta_pid          : Integer              ---------- primary ForeignKey(u'SRM__Regatta.pid')
    SRM.Sailor <Table SRM__Sailor>
        Column __raw_mna_number          : Varchar(60)          Primary_Optional__Raw_Value Int mna_number
        Column club_pid                  : Integer              Primary_Optional__Id_Entity_Reference Entity club
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Person left
        Column mna_number                : Integer              Primary_Optional__Raw_Value Int mna_number
        Column nation                    : Varchar(3)           Primary_Optional Nation nation
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Team <Table SRM__Team>
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column club_pid                  : Integer              Optional__Id_Entity_Reference Entity club
        Column desc                      : Varchar(160)         Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column leader_pid                : Integer              Optional__Id_Entity_Reference Entity leader
        Column left_pid                  : Integer              Link_Role__Init_Only Regatta_C left
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column place                     : Integer              Optional Int place
        Column registration_date         : Date                 Internal Date registration_date
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SWP.Clip_O <Table SWP__Clip_O>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Nested Date start
        Column __date_x_finish           : Date                 Optional__Nested Date finish
        Column __date_x_start            : Date                 Necessary__Nested Date start
        Column abstract                  : Text                 Required Text abstract
        Column contents                  : Text                 Internal__Auto_Update Text contents
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Object_PN left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column prio                      : Integer              Optional__Sticky Int prio
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SWP.Picture <Table SWP__Picture>
        Column __photo_extension         : Varchar(10)          Optional__Init_Only__Nested String extension
        Column __photo_height            : Smallint             Necessary__Nested Y height
        Column __photo_width             : Smallint             Necessary__Nested X width
        Column __thumb_extension         : Varchar(10)          Optional__Init_Only__Nested String extension
        Column __thumb_height            : Smallint             Necessary__Nested Y height
        Column __thumb_width             : Smallint             Necessary__Nested X width
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role__Init_Only Gallery left
        Column name                      : Varchar(100)         Optional__Computed_Set String name
        Column number                    : Integer              Primary Int number
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Person_has_Account <Table PAP__Person_has_Account>
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Account right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Company_has_Address <Table PAP__Company_has_Address>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Address right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Person_has_Address <Table PAP__Person_has_Address>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Address right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Company_has_Email <Table PAP__Company_has_Email>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Email right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Person_has_Email <Table PAP__Person_has_Email>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Email right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Company_has_Phone <Table PAP__Company_has_Phone>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column extension                 : Varchar(5)           Primary_Optional Numeric_String extension
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Phone right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Person_has_Phone <Table PAP__Person_has_Phone>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column extension                 : Varchar(5)           Primary_Optional Numeric_String extension
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Phone right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Company_has_Url <Table PAP__Company_has_Url>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Company left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Url right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Person_has_Url <Table PAP__Person_has_Url>
        Column desc                      : Varchar(20)          Optional__Computed_Set String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Person left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Url right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Boat_in_Regatta <Table SRM__Boat_in_Regatta>
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Boat left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column place                     : Integer              Optional Int place
        Column points                    : Integer              Optional Int points
        Column rank                      : Integer              Internal Int rank
        Column registration_date         : Date                 Internal__Init_Only Date registration_date
        Column right_pid                 : Integer              Link_Role Regatta right
        Column skipper_pid               : Integer              Required__Id_Entity_Reference Entity skipper
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Crew_Member <Table SRM__Crew_Member>
        Column electric                  : Boolean              Internal Boolean electric
        Column key                       : Integer              Optional__Sticky Int key
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Boat_in_Regatta left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Sailor right
        Column role                      : Varchar(32)          Optional String role
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Team_has_Boat_in_Regatta <Table SRM__Team_has_Boat_in_Regatta>
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column left_pid                  : Integer              Link_Role Team left
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column right_pid                 : Integer              Link_Role Boat_in_Regatta right
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Address <Table PAP__Address>
        Column __raw_city                : Varchar(60)          Primary__Raw_Value String city
        Column __raw_country             : Varchar(60)          Primary__Raw_Value String country
        Column __raw_region              : Varchar(60)          Optional__Raw_Value String region
        Column __raw_street              : Varchar(60)          Primary__Raw_Value String street
        Column __raw_zip                 : Varchar(60)          Primary__Raw_Value String zip
        Column city                      : Varchar(30)          Primary__Raw_Value String city
        Column country                   : Varchar(20)          Primary__Raw_Value String country
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column region                    : Varchar(20)          Optional__Raw_Value String region
        Column street                    : Varchar(60)          Primary__Raw_Value String street
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
        Column zip                       : Varchar(6)           Primary__Raw_Value String zip
    PAP.Email <Table PAP__Email>
        Column __raw_address             : Varchar(60)          Primary__Raw_Value Email address
        Column address                   : Varchar(80)          Primary__Raw_Value Email address
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Phone <Table PAP__Phone>
        Column area_code                 : Varchar(5)           Primary Numeric_String area_code
        Column country_code              : Varchar(3)           Primary Numeric_String country_code
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column number                    : Varchar(14)          Primary Numeric_String number
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Url <Table PAP__Url>
        Column desc                      : Varchar(20)          Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column value                     : Varchar(160)         Primary Url value
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Company <Table PAP__Company>
        Column __lifetime_finish         : Date                 Optional__Nested Date finish
        Column __lifetime_start          : Date                 Necessary__Nested Date start
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column __raw_registered_in       : Varchar(60)          Primary_Optional__Raw_Value String registered_in
        Column __raw_short_name          : Varchar(60)          Optional__Raw_Value String short_name
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column registered_in             : Varchar(64)          Primary_Optional__Raw_Value String registered_in
        Column short_name                : Varchar(12)          Optional__Raw_Value String short_name
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    PAP.Person <Table PAP__Person>
        Column __lifetime_finish         : Date                 Optional__Nested Date finish
        Column __lifetime_start          : Date                 Necessary__Nested Date start
        Column __raw_first_name          : Varchar(60)          Primary__Raw_Value String first_name
        Column __raw_last_name           : Varchar(60)          Primary__Raw_Value String last_name
        Column __raw_middle_name         : Varchar(60)          Primary_Optional__Raw_Value String middle_name
        Column __raw_title               : Varchar(60)          Primary_Optional__Raw_Value String title
        Column electric                  : Boolean              Internal Boolean electric
        Column first_name                : Varchar(32)          Primary__Raw_Value String first_name
        Column last_cid                  : Integer              Internal Int last_cid
        Column last_name                 : Varchar(48)          Primary__Raw_Value String last_name
        Column middle_name               : Varchar(32)          Primary_Optional__Raw_Value String middle_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column salutation                : Varchar(80)          Optional String salutation
        Column sex                       : Varchar(1)           Necessary Sex sex
        Column title                     : Varchar(20)          Primary_Optional__Raw_Value String title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Club <Table SRM__Club>
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column long_name                 : Varchar(64)          Optional String long_name
        Column name                      : Varchar(8)           Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Page SWP.Page <Table SRM__Page>
        Column SWP__Page_pid             : Integer              ---------- primary ForeignKey(u'SWP__Page.pid')
        Column desc                      : Varchar(30)          Optional__Computed_Set String desc
        Column event_pid                 : Integer              Primary__Id_Entity_Reference Entity event
    SRM.Regatta_Event <Table SRM__Regatta_Event>
        Column __date_finish             : Date                 Optional__Computed_Set__Nested Date finish
        Column __date_start              : Date                 Necessary__Nested Date start
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column club_pid                  : Integer              Optional__Id_Entity_Reference Entity club
        Column desc                      : Varchar(160)         Optional String desc
        Column electric                  : Boolean              Internal Boolean electric
        Column is_cancelled              : Boolean              Optional Boolean is_cancelled
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(64)          Primary__Raw_Value String name
        Column perma_name                : Varchar(64)          Internal__Auto_Update_Lazy__Computed_Set String perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM._Boat_Class_ <Table SRM___Boat_Class_>
        Column __raw_name                : Varchar(60)          Primary__Raw_Value String name
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column name                      : Varchar(48)          Primary__Raw_Value String name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SRM.Boat_Class SRM._Boat_Class_ <Table SRM__Boat_Class>
        Column SRM___Boat_Class__pid     : Integer              ---------- primary ForeignKey(u'SRM___Boat_Class_.pid')
        Column beam                      : Float                Optional Float beam
        Column loa                       : Float                Optional Float loa
        Column max_crew                  : Smallint             Required Int max_crew
        Column sail_area                 : Float                Optional Float sail_area
    SRM.Handicap SRM._Boat_Class_ <Table SRM__Handicap>
        Column SRM___Boat_Class__pid     : Integer              ---------- primary ForeignKey(u'SRM___Boat_Class_.pid')
    SWP.Gallery <Table SWP__Gallery>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Sticky__Nested Date start
        Column directory                 : Text                 Necessary Directory directory
        Column electric                  : Boolean              Internal Boolean electric
        Column last_cid                  : Integer              Internal Int last_cid
        Column perma_name                : Varchar(80)          Primary Date-Slug perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column short_title               : Varchar(30)          Necessary String short_title
        Column title                     : Varchar(120)         Necessary String title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SWP.Page <Table SWP__Page>
        Column __date_finish             : Date                 Optional__Nested Date finish
        Column __date_start              : Date                 Necessary__Sticky__Nested Date start
        Column contents                  : Text                 Internal__Auto_Update Text contents
        Column electric                  : Boolean              Internal Boolean electric
        Column format                    : Varchar(8)           Optional__Sticky Format format
        Column head_line                 : Varchar(256)         Optional String head_line
        Column hidden                    : Boolean              Optional Boolean hidden
        Column last_cid                  : Integer              Internal Int last_cid
        Column perma_name                : Varchar(80)          Primary Date-Slug perma_name
        Column pid                       : Integer              Internal__Just_Once Surrogate pid primary
        Column prio                      : Integer              Optional__Sticky Int prio
        Column short_title               : Varchar(30)          Necessary String short_title
        Column text                      : Text                 Required Text text
        Column title                     : Varchar(120)         Necessary String title
        Column type_name                 : Varchar(64)          Internal__Type_Name String type_name
        Column x_locked                  : Boolean              Internal Boolean x_locked
    SWP.Clip_X SWP.Page <Table SWP__Clip_X>
        Column SWP__Page_pid             : Integer              ---------- primary ForeignKey(u'SWP__Page.pid')
        Column link_to                   : Varchar(160)         Optional Url link_to
    SWP.Page_Y SWP.Page <Table SWP__Page_Y>
        Column SWP__Page_pid             : Integer              ---------- primary ForeignKey(u'SWP__Page.pid')
        Column year                      : Integer              Primary_Optional Int year

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_filters = _test_filters
        , test_joins   = _test_joins
        , test_select  = _test_select
        , test_tables  = _test_tables
        )
    , ignore = ("HPS", "my", "pg", "sq")
    )

### __END__ GTW.__test__.SAS_SQL

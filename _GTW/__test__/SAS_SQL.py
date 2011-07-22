# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Martin Glueck All rights reserved
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
#    ««revision-date»»···
#--

from   __future__          import unicode_literals

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> print scope.PAP.Person.query (Q.last_name                      == "h")
    SQL: SELECT "GTW__OMP__PAP__Person".pid AS "GTW__OMP__PAP__Person_pid", "GTW__OMP__PAP__Person"."Type_Name" AS "GTW__OMP__PAP__Person_Type_Name", "GTW__OMP__PAP__Person".first_name AS "GTW__OMP__PAP__Person_first_name", "GTW__OMP__PAP__Person".__raw_first_name AS "GTW__OMP__PAP__Person___raw_first_name", "GTW__OMP__PAP__Person".last_name AS "GTW__OMP__PAP__Person_last_name", "GTW__OMP__PAP__Person".__raw_last_name AS "GTW__OMP__PAP__Person___raw_last_name", "GTW__OMP__PAP__Person".middle_name AS "GTW__OMP__PAP__Person_middle_name", "GTW__OMP__PAP__Person".__raw_middle_name AS "GTW__OMP__PAP__Person___raw_middle_name", "GTW__OMP__PAP__Person".electric AS "GTW__OMP__PAP__Person_electric", "GTW__OMP__PAP__Person".title AS "GTW__OMP__PAP__Person_title", "GTW__OMP__PAP__Person".__raw_title AS "GTW__OMP__PAP__Person___raw_title", "GTW__OMP__PAP__Person".sex AS "GTW__OMP__PAP__Person_sex", "GTW__OMP__PAP__Person".last_cid AS "GTW__OMP__PAP__Person_last_cid", "GTW__OMP__PAP__Person".__lifetime_start AS "GTW__OMP__PAP__Person___lifetime_start", "GTW__OMP__PAP__Person".__lifetime_finish AS "GTW__OMP__PAP__Person___lifetime_finish", "GTW__OMP__PAP__Person".salutation AS "GTW__OMP__PAP__Person_salutation", "GTW__OMP__PAP__Person".x_locked AS "GTW__OMP__PAP__Person_x_locked"
         FROM "GTW__OMP__PAP__Person"
         WHERE "GTW__OMP__PAP__Person".last_name = :last_name_1
    >>> print scope.PAP.Person.query (Q.RAW.last_name                  == "H")
    SQL: SELECT "GTW__OMP__PAP__Person".pid AS "GTW__OMP__PAP__Person_pid", "GTW__OMP__PAP__Person"."Type_Name" AS "GTW__OMP__PAP__Person_Type_Name", "GTW__OMP__PAP__Person".first_name AS "GTW__OMP__PAP__Person_first_name", "GTW__OMP__PAP__Person".__raw_first_name AS "GTW__OMP__PAP__Person___raw_first_name", "GTW__OMP__PAP__Person".last_name AS "GTW__OMP__PAP__Person_last_name", "GTW__OMP__PAP__Person".__raw_last_name AS "GTW__OMP__PAP__Person___raw_last_name", "GTW__OMP__PAP__Person".middle_name AS "GTW__OMP__PAP__Person_middle_name", "GTW__OMP__PAP__Person".__raw_middle_name AS "GTW__OMP__PAP__Person___raw_middle_name", "GTW__OMP__PAP__Person".electric AS "GTW__OMP__PAP__Person_electric", "GTW__OMP__PAP__Person".title AS "GTW__OMP__PAP__Person_title", "GTW__OMP__PAP__Person".__raw_title AS "GTW__OMP__PAP__Person___raw_title", "GTW__OMP__PAP__Person".sex AS "GTW__OMP__PAP__Person_sex", "GTW__OMP__PAP__Person".last_cid AS "GTW__OMP__PAP__Person_last_cid", "GTW__OMP__PAP__Person".__lifetime_start AS "GTW__OMP__PAP__Person___lifetime_start", "GTW__OMP__PAP__Person".__lifetime_finish AS "GTW__OMP__PAP__Person___lifetime_finish", "GTW__OMP__PAP__Person".salutation AS "GTW__OMP__PAP__Person_salutation", "GTW__OMP__PAP__Person".x_locked AS "GTW__OMP__PAP__Person_x_locked"
         FROM "GTW__OMP__PAP__Person"
         WHERE "GTW__OMP__PAP__Person".__raw_last_name = :__raw_last_name_1
    >>> print scope.PAP.Person.query (Q.RAW.last_name.LOWER            == "h")
    SQL: SELECT "GTW__OMP__PAP__Person".pid AS "GTW__OMP__PAP__Person_pid", "GTW__OMP__PAP__Person"."Type_Name" AS "GTW__OMP__PAP__Person_Type_Name", "GTW__OMP__PAP__Person".first_name AS "GTW__OMP__PAP__Person_first_name", "GTW__OMP__PAP__Person".__raw_first_name AS "GTW__OMP__PAP__Person___raw_first_name", "GTW__OMP__PAP__Person".last_name AS "GTW__OMP__PAP__Person_last_name", "GTW__OMP__PAP__Person".__raw_last_name AS "GTW__OMP__PAP__Person___raw_last_name", "GTW__OMP__PAP__Person".middle_name AS "GTW__OMP__PAP__Person_middle_name", "GTW__OMP__PAP__Person".__raw_middle_name AS "GTW__OMP__PAP__Person___raw_middle_name", "GTW__OMP__PAP__Person".electric AS "GTW__OMP__PAP__Person_electric", "GTW__OMP__PAP__Person".title AS "GTW__OMP__PAP__Person_title", "GTW__OMP__PAP__Person".__raw_title AS "GTW__OMP__PAP__Person___raw_title", "GTW__OMP__PAP__Person".sex AS "GTW__OMP__PAP__Person_sex", "GTW__OMP__PAP__Person".last_cid AS "GTW__OMP__PAP__Person_last_cid", "GTW__OMP__PAP__Person".__lifetime_start AS "GTW__OMP__PAP__Person___lifetime_start", "GTW__OMP__PAP__Person".__lifetime_finish AS "GTW__OMP__PAP__Person___lifetime_finish", "GTW__OMP__PAP__Person".salutation AS "GTW__OMP__PAP__Person_salutation", "GTW__OMP__PAP__Person".x_locked AS "GTW__OMP__PAP__Person_x_locked"
         FROM "GTW__OMP__PAP__Person"
         WHERE lower("GTW__OMP__PAP__Person".__raw_last_name) = :lower_1
    >>> print scope.PAP.Person.query (Q.RAW.last_name.STARTSWITH       ("H"))
    SQL: SELECT "GTW__OMP__PAP__Person".pid AS "GTW__OMP__PAP__Person_pid", "GTW__OMP__PAP__Person"."Type_Name" AS "GTW__OMP__PAP__Person_Type_Name", "GTW__OMP__PAP__Person".first_name AS "GTW__OMP__PAP__Person_first_name", "GTW__OMP__PAP__Person".__raw_first_name AS "GTW__OMP__PAP__Person___raw_first_name", "GTW__OMP__PAP__Person".last_name AS "GTW__OMP__PAP__Person_last_name", "GTW__OMP__PAP__Person".__raw_last_name AS "GTW__OMP__PAP__Person___raw_last_name", "GTW__OMP__PAP__Person".middle_name AS "GTW__OMP__PAP__Person_middle_name", "GTW__OMP__PAP__Person".__raw_middle_name AS "GTW__OMP__PAP__Person___raw_middle_name", "GTW__OMP__PAP__Person".electric AS "GTW__OMP__PAP__Person_electric", "GTW__OMP__PAP__Person".title AS "GTW__OMP__PAP__Person_title", "GTW__OMP__PAP__Person".__raw_title AS "GTW__OMP__PAP__Person___raw_title", "GTW__OMP__PAP__Person".sex AS "GTW__OMP__PAP__Person_sex", "GTW__OMP__PAP__Person".last_cid AS "GTW__OMP__PAP__Person_last_cid", "GTW__OMP__PAP__Person".__lifetime_start AS "GTW__OMP__PAP__Person___lifetime_start", "GTW__OMP__PAP__Person".__lifetime_finish AS "GTW__OMP__PAP__Person___lifetime_finish", "GTW__OMP__PAP__Person".salutation AS "GTW__OMP__PAP__Person_salutation", "GTW__OMP__PAP__Person".x_locked AS "GTW__OMP__PAP__Person_x_locked"
         FROM "GTW__OMP__PAP__Person"
         WHERE "GTW__OMP__PAP__Person".__raw_last_name LIKE :__raw_last_name_1 || '%%%%'
    >>> print scope.PAP.Person.query (Q.RAW.last_name.LOWER.STARTSWITH ("h"))
    SQL: SELECT "GTW__OMP__PAP__Person".pid AS "GTW__OMP__PAP__Person_pid", "GTW__OMP__PAP__Person"."Type_Name" AS "GTW__OMP__PAP__Person_Type_Name", "GTW__OMP__PAP__Person".first_name AS "GTW__OMP__PAP__Person_first_name", "GTW__OMP__PAP__Person".__raw_first_name AS "GTW__OMP__PAP__Person___raw_first_name", "GTW__OMP__PAP__Person".last_name AS "GTW__OMP__PAP__Person_last_name", "GTW__OMP__PAP__Person".__raw_last_name AS "GTW__OMP__PAP__Person___raw_last_name", "GTW__OMP__PAP__Person".middle_name AS "GTW__OMP__PAP__Person_middle_name", "GTW__OMP__PAP__Person".__raw_middle_name AS "GTW__OMP__PAP__Person___raw_middle_name", "GTW__OMP__PAP__Person".electric AS "GTW__OMP__PAP__Person_electric", "GTW__OMP__PAP__Person".title AS "GTW__OMP__PAP__Person_title", "GTW__OMP__PAP__Person".__raw_title AS "GTW__OMP__PAP__Person___raw_title", "GTW__OMP__PAP__Person".sex AS "GTW__OMP__PAP__Person_sex", "GTW__OMP__PAP__Person".last_cid AS "GTW__OMP__PAP__Person_last_cid", "GTW__OMP__PAP__Person".__lifetime_start AS "GTW__OMP__PAP__Person___lifetime_start", "GTW__OMP__PAP__Person".__lifetime_finish AS "GTW__OMP__PAP__Person___lifetime_finish", "GTW__OMP__PAP__Person".salutation AS "GTW__OMP__PAP__Person_salutation", "GTW__OMP__PAP__Person".x_locked AS "GTW__OMP__PAP__Person_x_locked"
         FROM "GTW__OMP__PAP__Person"
         WHERE lower("GTW__OMP__PAP__Person".__raw_last_name) LIKE :lower_1 || '%%%%'
"""

__test__ = Scaffold.create_test_dict (_test_code, ignore = "HPS")

### __END__ GTW.__test__.SAS_SQL

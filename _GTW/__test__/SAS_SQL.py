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
#    ««revision-date»»···
#--

from   __future__          import unicode_literals

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> print scope.PAP.Person.query (Q.last_name == "h")
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

    >>> print scope.PAP.Person.query (Q.RAW.last_name == "H")
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

    >>> print scope.PAP.Person.query (Q.RAW.last_name.LOWER == "h")
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

    >>> print scope.PAP.Person.query (Q.RAW.last_name.STARTSWITH ("H"))
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

    >>> print scope.PAP.Person.query (Q.RAW.last_name.LOWER.STARTSWITH ("h"))
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

__test__ = Scaffold.create_test_dict (_test_code, ignore = "HPS")

### __END__ GTW.__test__.SAS_SQL

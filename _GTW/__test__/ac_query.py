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
#    GTW.__test__.ac_query
#
# Purpose
#    Testcases for the auto completion interface
#
# Revision Dates
#     8-Jun-2011 (MG) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_attr_ac_query = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> p1 = PAP.Person ("Glueck",          "Martin")
    >>> p2 = PAP.Person ("Tanzer",          "Christian", "", "Mag.")
    >>> p3 = PAP.Person ("Franz-Ferdinand", "Karl")
    >>> for value in "Ma", "martin", "CHRi" :
    ...    q = PAP.Person.first_name.ac_query (value)
    ...    for o in (p1, p2, p3) :
    ...        print value, o.first_name, q (o)
    Ma martin True
    Ma christian False
    Ma karl False
    martin martin True
    martin christian False
    martin karl False
    CHRi martin False
    CHRi christian True
    CHRi karl False

    >>> for value in "Gl", "Glueck", "Ferdinand" :
    ...    q = PAP.Person.last_name.ac_query (value)
    ...    for o in (p1, p2, p3) :
    ...        print value, o.last_name, q (o)
    Gl glueck True
    Gl tanzer False
    Gl franz-ferdinand False
    Glueck glueck True
    Glueck tanzer False
    Glueck franz-ferdinand False
    Ferdinand glueck False
    Ferdinand tanzer False
    Ferdinand franz-ferdinand True

    >>> a1 = PAP.Address ("Langstrasse 4",    "2244", "Spannberg", "Austria")
    >>> a2 = PAP.Address ("Glasauergasse 32", "1130", "Wien",      "Austria")
    >>> for value in "22", "11", "10" :
    ...    q = PAP.Address.zip.ac_query (value)
    ...    for o in (a1, a2) :
    ...        print value, o.zip, q (o)
    22 2244 True
    22 1130 False
    11 2244 False
    11 1130 True
    10 2244 False
    10 1130 False

    >>> SRM   = scope.SRM
    >>> opti  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b1    = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True) ### 1
    >>> b2    = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1208", raw = True) ### 2
    >>> for value in "11", "12" :
    ...    q = SRM.Boat.sail_number.ac_query (value)
    ...    for o in (b1, b2) :
    ...        print value, o.sail_number, q (o)
    11 1107 True
    11 1208 False
    12 1107 False
    12 1208 True
"""
from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict \
    (dict (attr_ac_query = _attr_ac_query))

### __END__ GTW.__test__.ac_query

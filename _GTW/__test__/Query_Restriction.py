# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Query_Restriction
#
# Purpose
#    Test cases for GTW.NAV.E_Type.Query_Restriction
#
# Revision Dates
#    14-Nov-2011 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> qe = QR.from_request_data (PAP.Person.E_Type, dict (qux = "42", qix = "Miles"))
    >>> print qe.limit, qe.offset, qe.filters, sorted (qe.other_req_data.items ())
    None None () [('qix', u'Miles'), ('qux', u'42')]

    >>> rd = dict (
    ...   limit = 24, last_name___GE = "Lee", lifetime__start___EQ = "2008", foo = "bar")
    >>> qr = QR.from_request_data (PAP.Person.E_Type, rd)
    >>> print qr.limit, qr.offset
    24 None
    >>> print qr.filters
    (Record (key = 'last_name___GE', name = u'last_name', op = 'GE', ui_names = (u'Last name',), value = u'Lee'), Record (key = 'lifetime__start___EQ', name = u'lifetime.start', op = 'EQ', ui_names = (u'Lifetime', u'Start'), value = u'2008'))
    >>> print qr.filters_q
    (Q.last_name >= lee, Q.lifetime.start.between (datetime.date(2008, 1, 1), datetime.date(2008, 12, 31)))
    >>> print sorted (qr.other_req_data.items ())
    [('foo', u'bar')]
    >>> print sorted (rd)
    ['foo', 'last_name___GE', 'lifetime__start___EQ', 'limit']

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *
from _GTW._NAV._E_Type.Query_Restriction import Query_Restriction as QR

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Query_Restriction

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.__test.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.__test.Event
#
# Purpose
#    Test SRM.Event creation and querying and recurrence rules
#
# Revision Dates
#    18-Aug-2010 (CT) Creation
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> EVT = scope.EVT
    >>> MOM = scope.MOM
    >>> SWP = scope.SWP

    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> p3 = SWP.Page ("event-3-text", text = "Text for the 3. event")
    >>> p4 = SWP.Page ("event-4-text", text = "Text for the 4. event")

    >>> r1 = MOM.Recurrence_Rule_Set (rules = [MOM.Recurrence_Rule (start = "20100801", count = 7, unit = "Weekly", raw = 1)], date_exceptions = [datetime.datetime(2010, 8, 15)])
    >>> r1 ### 1
    MOM.Recurrence_Rule_Set (date_exceptions = 2010/08/15, rules = ((('count', u'7'), ('start', '2010/08/01'), ('unit', u'Weekly')),))

    >>> e1 = EVT.Event (p1.epk, dict (start = "2010/08/18", finish = "2010/08/31", raw = True), recurrence = r1)
    >>> r1 ### 2
    MOM.Recurrence_Rule_Set (date_exceptions = 2010/08/15, rules = ((('count', u'7'), ('finish', '2010/08/31'), ('start', '2010/08/01'), ('unit', u'Weekly')),))

    >>> list (r1.occurrences)
    [datetime.datetime(2010, 8, 1, 0, 0), datetime.datetime(2010, 8, 8, 0, 0), datetime.datetime(2010, 8, 22, 0, 0), datetime.datetime(2010, 8, 29, 0, 0)]
    >>> e1.dates
    [datetime.datetime(2010, 8, 1, 0, 0), datetime.datetime(2010, 8, 8, 0, 0), datetime.datetime(2010, 8, 22, 0, 0), datetime.datetime(2010, 8, 29, 0, 0)]
"""

from _GTW.__test__.model import *
import datetime

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test.Event
"""
import datetime
EVT = scope.EVT
MOM = scope.MOM
SWP = scope.SWP
SWP.Page._etype.is_partial = False
p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
r1 = MOM.Recurrence_Rule_Set (rules = [MOM.Recurrence_Rule (start = "20100801", count=5, unit = "Weekly", raw = 1)], date_exceptions = [datetime.datetime(2010, 8, 15)])
e1 = EVT.Event (p1.epk, dict (start = "2010/08/18", finish = "2010/08/31", raw = True), rec = r1)

"""

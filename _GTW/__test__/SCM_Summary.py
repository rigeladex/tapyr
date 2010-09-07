# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.__test__.
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
#    GTW.__test__.SCM_Summary
#
# Purpose
#    Test change summaries (MOM.SCM.Summary)
#
# Revision Dates
#     3-Sep-2010 (CT) Creation
#    ««revision-date»»···
#--

from __future__ import unicode_literals

from _GTW.__test__.model import *
import datetime

_test_code = r"""
"""

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.SCM_Summary

"""
scope = Scope ('sqlite://')

import datetime
scope = Scope ()

PAP   = scope.PAP
SRM   = scope.SRM
RR    = SRM.Race_Result
bc    = SRM.Boat_Class (u"Optimist",          max_crew = 1)
x     = SRM.Boat_Class (u"420er",             max_crew = 2)
x     = SRM.Boat_Class (u"Laser",             max_crew = 1)
x     = SRM.Boat_Class (u"Seascape 18",       max_crew = 4)
b     = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True)
c     = b.copy (b.left, b.nation, sail_number = 1134)
p     = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
s     = SRM.Sailor.instance_or_new (p.epk_raw, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
rev   = SRM.Regatta_Event (dict (start = u"20080501", raw = True), u"Himmelfahrt", raw = True)
reg   = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
reh   = SRM.Regatta_H (rev.epk_raw, handicap = u"Yardstick",  raw = True)
bir   = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)
rr1 = SRM.Race_Result (bir, 1, points = 8)
rr2 = SRM.Race_Result (bir, 2, points = 4)
rev.date.set (start = "2010/05/13", finish = "2010/05/13")
bc.set (loa = 2.43)
p.set_raw (title = "Mr.", salutation = "Dear L.")
rr1.set (discarded = True)
x.destroy ()
rev.date.set (finish = "2010/05/14")
rev.date.finish = datetime.date (2010, 05, 13)

cs_1 = MOM.SCM.Summary (scope.uncommitted_changes)
for pid, csp in sorted (cs_1.iteritems ()) :
    print csp

for pid, csp in sorted (cs_1.iteritems ()) :
    print csp.pid, sorted (csp.attribute_changes.iteritems ())

scope.commit ()

TFL.Environment.exec_python_startup ()

"""

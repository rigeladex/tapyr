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
#    Test SRM.Event and recurrence rules
#
# Revision Dates
#    18-Aug-2010 (CT) Creation
#    19-Aug-2010 (CT) Creation continued
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> EVT = scope.EVT
    >>> MOM = scope.MOM
    >>> SWP = scope.SWP
    >>> RR  = MOM.Recurrence_Rule
    >>> RRS = MOM.Recurrence_Rule_Set

    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> p3 = SWP.Page ("event-3-text", text = "Text for the 3. event")
    >>> p4 = SWP.Page ("event-4-text", text = "Text for the 4. event")

    >>> r1 = RR (start = "20100801", count = 7, unit = "Weekly", raw = 1)
    >>> r1.ui_display
    u'20100801, 20100808, 20100815, 20100822, 20100829, 20100905, 20100912'
    >>> rs1 = RRS (rules = [r1], date_exceptions = ["2010/08/15"])
    >>> rs1.ui_display
    u'20100801, 20100808, 20100822, 20100829, 20100905, 20100912'
    >>> e1 = EVT.Event (p1.epk, dict (start = "2010/08/18", finish = "2010/08/31", raw = True), recurrence = rs1)

    Now, `rs1` takes a default value for `until` from `e1.date.finish`
    >>> rs1.ui_display
    u'20100801, 20100808, 20100822, 20100829'
    >>> e1.dates
    [datetime.datetime(2010, 8, 1, 0, 0), datetime.datetime(2010, 8, 8, 0, 0), datetime.datetime(2010, 8, 22, 0, 0), datetime.datetime(2010, 8, 29, 0, 0)]

    >>> r2 = RR (start = "20100801", count = 5, unit = "Daily", week_day = ("TU", "TH"), raw = 1)
    >>> r2.ui_display
    u'20100803, 20100805, 20100810, 20100812, 20100817'

    >>> r3 = RR (start = "20100801", count = 5, unit = "Weekly", week_day = ("TU", "TH"), raw = 1)
    >>> r3.ui_display
    u'20100803, 20100805, 20100810, 20100812, 20100817'

    >>> r4 = RR (start = "20100801", count = 5, unit = "Daily", week_day = ("TU", "TH"), restrict_pos = "1", raw = 1)
    >>> r4.ui_display
    u'20100803, 20100805, 20100810, 20100812, 20100817'

    >>> r5 = RR (start = "20100801", count = 5, unit = "Weekly", week_day = ("TU", "TH"), restrict_pos = "1", raw = 1)
    >>> r5.ui_display
    u'20100803, 20100810, 20100817, 20100824, 20100831'

    >>> r6 = RR (start = "20100801", count = 5, unit = "Monthly", raw = 1)
    >>> r6.ui_display
    u'20100801, 20100901, 20101001, 20101101, 20101201'

    >>> r7 = RR (start = "20100831", count = 5, unit = "Monthly", raw = 1)
    >>> r7.ui_display
    u'20100831, 20101031, 20101231, 20110131, 20110331'

    >>> r8 = RR (start = "20100831", count = 5, unit = "Monthly", month_day = "-1", raw = 1)
    >>> r8.ui_display
    u'20100831, 20100930, 20101031, 20101130, 20101231'

    >>> r9 = RR (start = "20101231", count = 5, unit = "Monthly", month_day = "29, -1", restrict_pos = "1", raw = 1)
    >>> r9.ui_display
    u'20110129, 20110228, 20110329, 20110429, 20110529'

    >>> r10 = RR (start = "20100801", count = 5, period = 2, unit = "Daily", raw = 1)
    >>> r10.ui_display
    u'20100801, 20100803, 20100805, 20100807, 20100809'

    >>> r11 = RR (start = "20100801", count = 5, period = 10, unit = "Daily", raw = 1)
    >>> r11.ui_display
    u'20100801, 20100811, 20100821, 20100831, 20100910'

    >>> r12 = RR (start = "20100101", finish = "20120101", month = "1", week_day = "MO", unit = "Yearly", raw = 1)
    >>> r12.ui_display
    u'20100104, 20100111, 20100118, 20100125, 20110103, 20110110, 20110117, 20110124, 20110131'

    >>> r13 = RR (start = "20100801", count = 5, period = 2, unit = "Weekly", week_day = ("TU", "TH"), raw = 1)
    >>> r13.ui_display
    u'20100810, 20100812, 20100824, 20100826, 20100907'

    >>> r14 = RR (start = "20100801", count = 5, unit = "Monthly", week_day = "MO", raw = 1)
    >>> r14.ui_display
    u'20100802, 20100809, 20100816, 20100823, 20100830'

    Monthly on the 1st Monday
    >>> r15 = RR (start = "20100801", count = 5, unit = "Monthly", week_day = "MO(1)", raw = 1)
    >>> r15.ui_display
    u'20100802, 20100906, 20101004, 20101101, 20101206'

    Every other month on the 1st and last Sunday of the month
    >>> r16 = RR (start = "20100801", count = 5, period = 2, unit = "Monthly", week_day = "SU(1), SU(-1)", raw = 1)
    >>> r16.ui_display
    u'20100801, 20100829, 20101003, 20101031, 20101205'

    Monthly on the fifth to the last day of the month,
    >>> r17 = RR (start = "20101101", count = 5, unit = "Monthly", month_day = "-5", raw = 1)
    >>> r17.ui_display
    u'20101126, 20101227, 20110127, 20110224, 20110327'

    Every 2nd year on the 1st, 100th and 200th day
    >>> r19 = RR (start = "20100101", count = 6, period = 2, unit = "Yearly", year_day = "1,100, 200", raw = 1)
    >>> r19.ui_display
    u'20100101, 20100410, 20100719, 20120101, 20120409, 20120718'

    Every 20th Monday of the year,
    >>> r20 = RR (start = "20100101", count = 6, unit = "Yearly", week_day = "MO(20)", raw = 1)
    >>> r20.ui_display
    u'20100517, 20110516, 20120514, 20130520, 20140519, 20150518'

    Monday of week number 20 (where the default start of the week is Monday),
    >>> r21 = RR (start = "20100101", count = 6, unit = "Yearly", week = "20", week_day = "MO", raw = 1)
    >>> r21.ui_display
    u'20100517, 20110516, 20120514, 20130513, 20140512, 20150511'

    The week number 1 may be in the last year.
    >>> r22 = RR (start = "20100101", count = 6, unit = "Yearly", week = "1", week_day = "MO", raw = 1)
    >>> r22.ui_display
    u'20100104, 20110103, 20120102, 20121231, 20131230, 20141229'

    And the week numbers greater than 51 may be in the next year.
    >>> r23 = RR (start = "20100101", count = 6, unit = "Yearly", week = "52", week_day = "SU", raw = 1)
    >>> r23.ui_display
    u'20120101, 20121230, 20131229, 20141228, 20151227, 20170101'

    Only some years have week number 53:
    >>> r24 = RR (start = "20100101", count = 6, unit = "Yearly", week = "53", week_day = "MO", raw = 1)
    >>> r24.ui_display
    u'20151228, 20201228, 20261228, 20321227, 20371228, 20431228'

    Every Friday the 13th,
    >>> r25 = RR (start = "20100101", count = 6, unit = "Yearly", month_day = "13", week_day = "FR", raw = 1)
    >>> r25.ui_display
    u'20100813, 20110513, 20120113, 20120413, 20120713, 20130913'

    Every four years, the first Tuesday after a Monday in November, (U.S. Presidential Election day):
    >>> r26 = RR (start = "20080101", count = 6, period = 4, unit = "Yearly", month = "11", month_day = "2,3,4,5,6,7,8", week_day = "TU", raw = 1)
    >>> r26.ui_display
    u'20081104, 20121106, 20161108, 20201103, 20241105, 20281107'

    The 3rd instance into the month of one of Tuesday, Wednesday or Thursday,
    >>> r27 = RR (start = "20101101", count = 5, unit = "Monthly", week_day = "TU, WE, TH", restrict_pos = "3", raw = 1)
    >>> r27.ui_display
    u'20101104, 20101207, 20110106, 20110203, 20110303'

    The 2nd to last weekday of the month,
    >>> r28 = RR (start = "20100701", count = 5, unit = "Monthly", week_day = "MO, TU, WE, TH, FR", restrict_pos = "-2", raw = 1)
    >>> r28.ui_display
    u'20100729, 20100830, 20100929, 20101028, 20101129'

    >>> rs2 = RRS (rules = [RR (start = "20100801", unit = "Daily", count = 7, raw = 1)],
    ...  rule_exceptions = [RR (start = "20100801", unit = "Yearly", week_day = "SA,SU", raw = True)])
    >>> rs2.ui_display
    u'20100802, 20100803, 20100804, 20100805, 20100806'

"""

from _GTW.__test__.model import *
import datetime

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test.Event

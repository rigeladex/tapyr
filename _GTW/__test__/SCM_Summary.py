# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#     8-Sep-2010 (CT) Creation continued..
#     9-Sep-2010 (CT) Creation continued...
#    14-Sep-2010 (CT) Creation continued....
#    ««revision-date»»···
#--

from __future__ import unicode_literals

from _GTW.__test__.model import *
import datetime

_basic = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP   = scope.PAP
    >>> SRM   = scope.SRM
    >>> EVT   = scope.EVT
    >>> SWP   = scope.SWP
    >>> RR    = EVT.Recurrence_Rule
    >>> RS    = EVT.Recurrence_Spec
    >>> bc    = SRM.Boat_Class (u"Optimist",          max_crew = 1)
    >>> _     = SRM.Boat_Class (u"420er",             max_crew = 2)
    >>> _     = SRM.Boat_Class (u"Laser",             max_crew = 1)
    >>> x     = SRM.Boat_Class (u"Seascape 18",       max_crew = 4)
    >>> b     = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True)
    >>> c     = b.copy (b.left, b.nation, sail_number = 1134)
    >>> p     = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s     = SRM.Sailor.instance_or_new (p.epk_raw, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
    >>> rev   = SRM.Regatta_Event (dict (start = u"20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg   = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> reh   = SRM.Regatta_H (rev.epk_raw, handicap = u"Yardstick",  raw = True)
    >>> bir   = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)
    >>> r1    = SRM.Race_Result (bir, 1, points = 8)
    >>> r2    = SRM.Race_Result (bir, 2, points = 4)
    >>> p1    = SWP.Page ("event-1-text", text = "Text for the 1. event", date = (("start", "2010/09/08"), ))
    >>> p2    = SWP.Page ("event-2-text", text = "Text for the 2. event", date = (("start", "2010/09/08"), ))
    >>> e1    = EVT.Event (p1.epk, dict (start = "2010/08/18", raw = True))
    >>> rs1   = RS (e1, date_exceptions = ["2010/08/15"])
    >>> rr1   = RR (rs1.epk_raw, start = "20100801", count = 7, unit = "Weekly", raw = True)
    >>>
    >>> _     = rev.date.set (start = "2010/05/13", finish = "2010/05/13")
    >>> _     = bc.set (loa = 2.43)
    >>> _     = p.set_raw (title = "Mr.", salutation = "Dear L.")
    >>> _     = r1.set (discarded = True)
    >>> _     = rev.date.set (finish = "2010/05/14")
    >>> x.destroy ()
    >>> rev.date.finish = datetime.date (2010, 05, 13)
    >>> rs1.dates.append (datetime.datetime (2010, 9, 8, 0, 0))
    >>> rs1.dates.append (datetime.datetime (2010, 10, 8, 0, 0))
    >>>
    >>> ucc  = csm1 = scope.uncommitted_changes
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp
    ...
    <Change Summary for pid 1: newborn, 1 change>
        <Create GTW.OMP.SRM.Boat_Class (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), new-values = {'last_cid' : '1', 'max_crew' : u'1'}>
        <Modify GTW.OMP.SRM.Boat_Class (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), old-values = {'last_cid' : '1', 'loa' : u''}, new-values = {'last_cid' : '22', 'loa' : u'2.43'}>
    <Change Summary for pid 2: newborn>
        <Create GTW.OMP.SRM.Boat_Class (u'420er', 'GTW.OMP.SRM.Boat_Class'), new-values = {'last_cid' : '2', 'max_crew' : u'2'}>
    <Change Summary for pid 3: newborn>
        <Create GTW.OMP.SRM.Boat_Class (u'Laser', 'GTW.OMP.SRM.Boat_Class'), new-values = {'last_cid' : '3', 'max_crew' : u'1'}>
    <Change Summary for pid 4: newborn, just died>
        <Create GTW.OMP.SRM.Boat_Class (u'Seascape 18', 'GTW.OMP.SRM.Boat_Class'), new-values = {'last_cid' : '4', 'max_crew' : u'4'}>
        <Destroy GTW.OMP.SRM.Boat_Class (u'Seascape 18', 'GTW.OMP.SRM.Boat_Class'), old-values = {'last_cid' : '4', 'max_crew' : u'4'}>
    <Change Summary for pid 5: newborn>
        <Create GTW.OMP.SRM.Boat ((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), new-values = {'last_cid' : '5'}>
    <Change Summary for pid 6: newborn, 1 change>
        <Create GTW.OMP.SRM.Boat ((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1134', u'', 'GTW.OMP.SRM.Boat'), new-values = {'last_cid' : '6'}>
        <Copy GTW.OMP.SRM.Boat ((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1134', u'', 'GTW.OMP.SRM.Boat'), new-values = {'last_cid' : '7'}>
          <Create GTW.OMP.SRM.Boat ((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1134', u'', 'GTW.OMP.SRM.Boat'), new-values = {'last_cid' : '6'}>
    <Change Summary for pid 7: newborn, 1 change>
        <Create GTW.OMP.PAP.Person (u'Tanzer', u'Laurens', u'', u'', 'GTW.OMP.PAP.Person'), new-values = {'last_cid' : '8'}>
        <Modify GTW.OMP.PAP.Person (u'Tanzer', u'Laurens', u'', u'Mr.', 'GTW.OMP.PAP.Person'), old-values = {'last_cid' : '8', 'salutation' : u'', 'title' : u''}, new-values = {'last_cid' : '23', 'salutation' : u'Dear L.', 'title' : u'Mr.'}>
    <Change Summary for pid 8: newborn>
        <Create GTW.OMP.SRM.Sailor ((u'Tanzer', u'Laurens', u'', u'', 'GTW.OMP.PAP.Person'), u'AUT', u'29676', u'', 'GTW.OMP.SRM.Sailor'), new-values = {'last_cid' : '9'}>
    <Change Summary for pid 9: newborn, 3 changes>
        <Create GTW.OMP.SRM.Regatta_Event ((('finish', u'2008/05/01'), ('start', u'2008/05/01')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), new-values = {'last_cid' : '10', 'perma_name' : u'himmelfahrt'}>
        <Modify GTW.OMP.SRM.Regatta_Event ((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), old-values = {'date' : (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'last_cid' : '10'}, new-values = {'date' : (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'last_cid' : '21'}>
        <Modify GTW.OMP.SRM.Regatta_Event ((('finish', u'2010/05/14'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), old-values = {'date' : (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'last_cid' : '21'}, new-values = {'date' : (('finish', u'2010/05/14'), ('start', u'2010/05/13')), 'last_cid' : '25'}>
        <Modify/C GTW.OMP.SRM.Regatta_Event.date ((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), old-values = {'finish' : u'2010/05/14', 'last_cid' : '25'}, new-values = {'finish' : u'2010/05/13', 'last_cid' : '27'}>
    <Change Summary for pid 10: newborn>
        <Create GTW.OMP.SRM.Regatta_C (((('finish', u'2008/05/01'), ('start', u'2008/05/01')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), new-values = {'last_cid' : '11', 'perma_name' : u'optimist'}>
    <Change Summary for pid 11: newborn>
        <Create GTW.OMP.SRM.Regatta_H (((('finish', u'2008/05/01'), ('start', u'2008/05/01')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), u'Yardstick', 'GTW.OMP.SRM.Regatta_H'), new-values = {'last_cid' : '12', 'perma_name' : u'yardstick'}>
    <Change Summary for pid 12: newborn>
        <Create GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2008/05/01'), ('start', u'2008/05/01')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), new-values = {'last_cid' : '13', 'skipper' : u'(u"(u\'tanzer\', u\'laurens\', u\'\', u\'\')", u\'AUT\', u\'29676\', u\'\')'}>
    <Change Summary for pid 13: newborn, 1 change>
        <Create GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2008/05/01'), ('start', u'2008/05/01')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'1', 'GTW.OMP.SRM.Race_Result'), new-values = {'last_cid' : '14', 'points' : u'8'}>
        <Modify GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'1', 'GTW.OMP.SRM.Race_Result'), old-values = {'discarded' : u'no', 'last_cid' : '14'}, new-values = {'discarded' : u'yes', 'last_cid' : '24'}>
    <Change Summary for pid 14: newborn>
        <Create GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2008/05/01'), ('start', u'2008/05/01')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'2', 'GTW.OMP.SRM.Race_Result'), new-values = {'last_cid' : '15', 'points' : u'4'}>
    <Change Summary for pid 15: newborn>
        <Create GTW.OMP.SWP.Page (u'event-1-text', 'GTW.OMP.SWP.Page'), new-values = {'contents' : u'<p>Text for the 1. event</p>\n', 'date' : (('start', u'2010/09/08'),), 'last_cid' : '16', 'text' : u'Text for the 1. event'}>
    <Change Summary for pid 16: newborn>
        <Create GTW.OMP.SWP.Page (u'event-2-text', 'GTW.OMP.SWP.Page'), new-values = {'contents' : u'<p>Text for the 2. event</p>\n', 'date' : (('start', u'2010/09/08'),), 'last_cid' : '17', 'text' : u'Text for the 2. event'}>
    <Change Summary for pid 17: newborn>
        <Create GTW.OMP.EVT.Event ((u'event-1-text', 'GTW.OMP.SWP.Page'), (('start', u'2010/08/18'),), u'', 'GTW.OMP.EVT.Event'), new-values = {'last_cid' : '18'}>
    <Change Summary for pid 19: newborn, 2 changes>
        <Create GTW.OMP.EVT.Recurrence_Spec (((u'event-1-text', 'GTW.OMP.SWP.Page'), (('start', u'2010/08/18'),), u'', 'GTW.OMP.EVT.Event'), 'GTW.OMP.EVT.Recurrence_Spec'), new-values = {'date_exceptions' : u'2010/08/15', 'last_cid' : '19'}>
        <Modify GTW.OMP.EVT.Recurrence_Spec (((u'event-1-text', 'GTW.OMP.SWP.Page'), (('start', u'2010/08/18'),), u'', 'GTW.OMP.EVT.Event'), 'GTW.OMP.EVT.Recurrence_Spec'), old-values = {'dates' : u'', 'last_cid' : '19'}, new-values = {'dates' : u'2010/09/08', 'last_cid' : '28'}>
        <Modify GTW.OMP.EVT.Recurrence_Spec (((u'event-1-text', 'GTW.OMP.SWP.Page'), (('start', u'2010/08/18'),), u'', 'GTW.OMP.EVT.Event'), 'GTW.OMP.EVT.Recurrence_Spec'), old-values = {'dates' : u'2010/09/08', 'last_cid' : '28'}, new-values = {'dates' : u'2010/09/08,2010/10/08', 'last_cid' : '29'}>
    <Change Summary for pid 20: newborn>
        <Create GTW.OMP.EVT.Recurrence_Rule ((((u'event-1-text', 'GTW.OMP.SWP.Page'), (('start', u'2010/08/18'),), u'', 'GTW.OMP.EVT.Event'), 'GTW.OMP.EVT.Recurrence_Spec'), u'', u'', 'GTW.OMP.EVT.Recurrence_Rule'), new-values = {'count' : u'7', 'last_cid' : '20', 'start' : u'2010/08/01', 'unit' : u'Weekly'}>

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp.pid, sorted (csp.attribute_changes.iteritems ())
    ...
    1 [('last_cid', (old = None, new = '22')), ('loa', (old = u'', new = u'2.43')), ('max_crew', (old = None, new = u'1'))]
    2 [('last_cid', (old = None, new = '2')), ('max_crew', (old = None, new = u'2'))]
    3 [('last_cid', (old = None, new = '3')), ('max_crew', (old = None, new = u'1'))]
    4 [('last_cid', (old = None, new = None)), ('max_crew', (old = None, new = None))]
    5 [('last_cid', (old = None, new = '5'))]
    6 [('last_cid', (old = None, new = '7'))]
    7 [('last_cid', (old = None, new = '23')), ('salutation', (old = u'', new = u'Dear L.')), ('title', (old = u'', new = u'Mr.'))]
    8 [('last_cid', (old = None, new = '9'))]
    9 [('date', (old = (('finish', u'2008/05/01'), ('start', u'2008/05/01')), new = (('finish', u'2010/05/13'), ('start', u'2010/05/13')))), ('last_cid', (old = None, new = '27')), ('perma_name', (old = None, new = u'himmelfahrt'))]
    10 [('last_cid', (old = None, new = '11')), ('perma_name', (old = None, new = u'optimist'))]
    11 [('last_cid', (old = None, new = '12')), ('perma_name', (old = None, new = u'yardstick'))]
    12 [('last_cid', (old = None, new = '13')), ('skipper', (old = None, new = u'(u"(u\'tanzer\', u\'laurens\', u\'\', u\'\')", u\'AUT\', u\'29676\', u\'\')'))]
    13 [('discarded', (old = u'no', new = u'yes')), ('last_cid', (old = None, new = '24')), ('points', (old = None, new = u'8'))]
    14 [('last_cid', (old = None, new = '15')), ('points', (old = None, new = u'4'))]
    15 [('contents', (old = None, new = u'<p>Text for the 1. event</p>\n')), ('date', (old = None, new = (('start', u'2010/09/08'),))), ('last_cid', (old = None, new = '16')), ('text', (old = None, new = u'Text for the 1. event'))]
    16 [('contents', (old = None, new = u'<p>Text for the 2. event</p>\n')), ('date', (old = None, new = (('start', u'2010/09/08'),))), ('last_cid', (old = None, new = '17')), ('text', (old = None, new = u'Text for the 2. event'))]
    17 [('last_cid', (old = None, new = '18'))]
    19 [('date_exceptions', (old = None, new = u'2010/08/15')), ('dates', (old = u'', new = u'2010/09/08,2010/10/08')), ('last_cid', (old = None, new = '29'))]
    20 [('count', (old = None, new = u'7')), ('last_cid', (old = None, new = '20')), ('start', (old = None, new = u'2010/08/01')), ('unit', (old = None, new = u'Weekly'))]

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)
    1 ['last_cid', 'loa']
    2 ['last_cid']
    3 ['last_cid']
    5 ['last_cid']
    6 ['last_cid']
    7 ['last_cid', 'salutation', 'title']
    8 ['last_cid']
    9 ['date', 'last_cid']
    10 ['last_cid']
    11 ['last_cid']
    12 ['last_cid']
    13 ['discarded', 'last_cid']
    14 ['last_cid']
    15 ['last_cid']
    16 ['last_cid']
    17 ['last_cid']
    19 ['dates', 'last_cid']
    20 ['last_cid']

    >>> scope.commit ()

    >>> print rs1.attr_as_code()
    ((u'event-1-text', ), dict (start = u'2010/08/18'), dict ()), date_exceptions = u"u'2010/08/15'", dates = u"u'2010/09/08',u'2010/10/08'"
    >>> rs1.set (date_exceptions = None)
    1
    >>> rs1.event.date.set (finish = datetime.date (2010, 8, 19), start = datetime.date (2010, 8, 13))
    1
    >>> rs1.dates.pop ()
    datetime.datetime(2010, 10, 8, 0, 0)

    >>> ucc = scope.uncommitted_changes
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp
    ...
    <Change Summary for pid 17: 1 change>
        <Modify GTW.OMP.EVT.Event ((u'event-1-text', 'GTW.OMP.SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', 'GTW.OMP.EVT.Event'), old-values = {'date' : (('start', u'2010/08/18'),), 'last_cid' : '18'}, new-values = {'date' : (('finish', u'2010/08/19'), ('start', u'2010/08/13')), 'last_cid' : '31'}>
    <Change Summary for pid 19: 2 changes>
        <Modify GTW.OMP.EVT.Recurrence_Spec (((u'event-1-text', 'GTW.OMP.SWP.Page'), (('start', u'2010/08/18'),), u'', 'GTW.OMP.EVT.Event'), 'GTW.OMP.EVT.Recurrence_Spec'), old-values = {'date_exceptions' : u'2010/08/15', 'last_cid' : '29'}, new-values = {'date_exceptions' : u'', 'last_cid' : '30'}>
        <Modify GTW.OMP.EVT.Recurrence_Spec (((u'event-1-text', 'GTW.OMP.SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', 'GTW.OMP.EVT.Event'), 'GTW.OMP.EVT.Recurrence_Spec'), old-values = {'dates' : u'2010/09/08,2010/10/08', 'last_cid' : '30'}, new-values = {'dates' : u'2010/09/08', 'last_cid' : '32'}>
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp.pid, sorted (csp.attribute_changes.iteritems ())
    ...
    17 [('date', (old = (('start', u'2010/08/18'),), new = (('finish', u'2010/08/19'), ('start', u'2010/08/13')))), ('last_cid', (old = '18', new = '31'))]
    19 [('date_exceptions', (old = u'2010/08/15', new = u'')), ('dates', (old = u'2010/09/08,2010/10/08', new = u'2010/09/08')), ('last_cid', (old = '29', new = '32'))]

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)
    17 ['date', 'last_cid']
    19 ['date_exceptions', 'dates', 'last_cid']

    >>> scope.commit ()

    >>> SRM.Boat.query (sail_number = 1134).one ().destroy ()
    >>> b.destroy ()

    >>> ucc = scope.uncommitted_changes
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp
    ...
    <Change Summary for pid 5: just died>
        <Destroy GTW.OMP.SRM.Boat ((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), old-values = {'last_cid' : '5'}>
          <Destroy GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), old-values = {'last_cid' : '13', 'skipper' : u'(u"(u\'tanzer\', u\'laurens\', u\'\', u\'mr.\')", u\'AUT\', u\'29676\', u\'\')'}>
            <Destroy GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'1', 'GTW.OMP.SRM.Race_Result'), old-values = {'discarded' : u'yes', 'last_cid' : '24', 'points' : u'8'}>
            <Destroy GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'2', 'GTW.OMP.SRM.Race_Result'), old-values = {'last_cid' : '15', 'points' : u'4'}>
    <Change Summary for pid 6: just died>
        <Destroy GTW.OMP.SRM.Boat ((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1134', u'', 'GTW.OMP.SRM.Boat'), old-values = {'last_cid' : '7'}>
    <Change Summary for pid 12: just died>
        <Destroy GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), old-values = {'last_cid' : '13', 'skipper' : u'(u"(u\'tanzer\', u\'laurens\', u\'\', u\'mr.\')", u\'AUT\', u\'29676\', u\'\')'}>
          <Destroy GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'1', 'GTW.OMP.SRM.Race_Result'), old-values = {'discarded' : u'yes', 'last_cid' : '24', 'points' : u'8'}>
          <Destroy GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'2', 'GTW.OMP.SRM.Race_Result'), old-values = {'last_cid' : '15', 'points' : u'4'}>
    <Change Summary for pid 13: just died>
        <Destroy GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'1', 'GTW.OMP.SRM.Race_Result'), old-values = {'discarded' : u'yes', 'last_cid' : '24', 'points' : u'8'}>
    <Change Summary for pid 14: just died>
        <Destroy GTW.OMP.SRM.Race_Result ((((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', u'', 'GTW.OMP.SRM.Boat'), (((('finish', u'2010/05/13'), ('start', u'2010/05/13')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta'), u'2', 'GTW.OMP.SRM.Race_Result'), old-values = {'last_cid' : '15', 'points' : u'4'}>

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp.pid, sorted (csp.attribute_changes.iteritems ())
    ...
    5 [('last_cid', (old = '5', new = None))]
    6 [('last_cid', (old = '7', new = None))]
    12 [('last_cid', (old = '13', new = None)), ('skipper', (old = u'(u"(u\'tanzer\', u\'laurens\', u\'\', u\'mr.\')", u\'AUT\', u\'29676\', u\'\')', new = None))]
    13 [('discarded', (old = u'yes', new = None)), ('last_cid', (old = '24', new = None)), ('points', (old = u'8', new = None))]
    14 [('last_cid', (old = '15', new = None)), ('points', (old = u'4', new = None))]

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)

    >>> scope.commit ()

    >>> _ = p.lifetime.set (start = "1997/11/16")
    >>> _ = p.lifetime.set (finish = "2077/11/30")

    >>> ucc = scope.uncommitted_changes
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp
    ...
    <Change Summary for pid 7: 2 changes>
        <Modify/C GTW.OMP.PAP.Person.lifetime (u'Tanzer', u'Laurens', u'', u'Mr.', 'GTW.OMP.PAP.Person'), old-values = {'last_cid' : '23', 'start' : u''}, new-values = {'last_cid' : '38', 'start' : u'1997/11/16'}>
        <Modify/C GTW.OMP.PAP.Person.lifetime (u'Tanzer', u'Laurens', u'', u'Mr.', 'GTW.OMP.PAP.Person'), old-values = {'finish' : u'', 'last_cid' : '38'}, new-values = {'finish' : u'2077/11/30', 'last_cid' : '39'}>
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    ...     print csp.pid, sorted (csp.attribute_changes.iteritems ())
    ...
    7 [('last_cid', (old = '23', new = '39')), ('lifetime', (old = (('finish', u''), ('start', u'')), new = (('finish', u'2077/11/30'), ('start', u'1997/11/16'))))]

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)
    7 ['last_cid', 'lifetime']

    >>> len (csm1)
    28
    >>> conflicts, merges = csm1.change_conflicts ({}, scope)
    >>> sorted (conflicts), sorted (merges)
    ([], [])

    >>> scope.destroy ()

"""

_more = dict \
    ( conflicts = """

    >>> scope_1 = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> _ = scope_1.PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> scope_1.commit ()

    >>> scope_2 = Scaffold.scope (%(p1)s, %(n1)s, create = False) # doctest:+ELLIPSIS
    Loading scope MOMT__...

    >>> p1  = scope_1.PAP.Person.instance (u"Tanzer", u"Laurens")
    >>> _   = p1.set (salutation = u"Dear Laurens")
    >>> cs1 = scope_1.uncommitted_changes
    >>> len (cs1) ### 1
    1
    >>> for pid, csp in sorted (cs1.by_pid.iteritems ()) :
    ...     print csp
    <Change Summary for pid 1: 1 change>
        <Modify GTW.OMP.PAP.Person (u'Tanzer', u'Laurens', u'', u'', 'GTW.OMP.PAP.Person'), old-values = {'last_cid' : '1', 'salutation' : u''}, new-values = {'last_cid' : '2', 'salutation' : u'Dear Laurens'}>

    >>> p2 = scope_2.PAP.Person.instance (* p1.epk)
    >>> p2.salutation
    u''
    >>> _ = p2.set (salutation = u"Lieber Laurens")
    >>> cs2 = scope_2.uncommitted_changes
    >>> len (cs2) ### 1
    1
    >>> for pid, csp in sorted (cs2.by_pid.iteritems ()) :
    ...     print csp
    <Change Summary for pid 1: 1 change>
        <Modify GTW.OMP.PAP.Person (u'Tanzer', u'Laurens', u'', u'', 'GTW.OMP.PAP.Person'), old-values = {'last_cid' : '1', 'salutation' : u''}, new-values = {'last_cid' : '3', 'salutation' : u'Lieber Laurens'}>

    >>> scope_1.commit              ()
    >>> scope_1.ems.session.expunge ()
    >>> scope_2.commit              ()
    Traceback (most recent call last):
      ...
    Commit_Conflict

    >>> p2 = scope_2.PAP.Person.instance (* p1.epk)
    >>> p2.salutation
    u'Dear Laurens'

    >>> p1 = scope_1.PAP.Person.instance (* p1.epk)
    >>> p1.salutation
    u'Dear Laurens'

    >>> scope_2.commit ()
    >>> scope_1.commit ()

    >>> scope_1.destroy ()
    >>> scope_2.destroy ()
    """
    )

Scaffold.Backend_Default_Path ["SQL"] = "'test'"
__test__ = dict \
    ( Scaffold.create_test_dict (_more, ignore = ("HPS", "SQL"))
    , ** Scaffold.create_test_dict (_basic)
    )

### __END__ GTW.__test__.SCM_Summary

"""
scope = Scope ('sqlite://')

from   __future__            import unicode_literals
import datetime
scope = Scope ()

PAP   = scope.PAP
SRM   = scope.SRM
EVT   = scope.EVT
SWP   = scope.SWP
RR    = EVT.Recurrence_Rule
RS    = EVT.Recurrence_Spec
bc    = SRM.Boat_Class (u"Optimist",          max_crew = 1)
_     = SRM.Boat_Class (u"420er",             max_crew = 2)
_     = SRM.Boat_Class (u"Laser",             max_crew = 1)
x     = SRM.Boat_Class (u"Seascape 18",       max_crew = 4)
b     = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True)
c     = b.copy (b.left, b.nation, sail_number = 1134)
p     = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
s     = SRM.Sailor.instance_or_new (p.epk_raw, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
rev   = SRM.Regatta_Event (dict (start = u"20080501", raw = True), u"Himmelfahrt", raw = True)
reg   = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
reh   = SRM.Regatta_H (rev.epk_raw, handicap = u"Yardstick",  raw = True)
bir   = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)
r1    = SRM.Race_Result (bir, 1, points = 8)
r2    = SRM.Race_Result (bir, 2, points = 4)
p1    = SWP.Page ("event-1-text", text = "Text for the 1. event")
p2    = SWP.Page ("event-2-text", text = "Text for the 2. event")
e1    = EVT.Event (p1.epk, dict (start = "2010/08/18", raw = True))
rs1   = RS (e1, date_exceptions = ["2010/08/15"])
rr1   = RR (rs1.epk_raw, start = "20100801", count = 7, unit = "Weekly", raw = True)

_     = rev.date.set (start = "2010/05/13", finish = "2010/05/13")
_     = bc.set (loa = 2.43)
_     = p.set_raw (title = "Mr.", salutation = "Dear L.")
_     = r1.set (discarded = True)
_     = rev.date.set (finish = "2010/05/14")
x.destroy ()
rev.date.finish = datetime.date (2010, 05, 13)
rs1.dates.append (datetime.datetime (2010, 9, 8, 0, 0))
rs1.dates.append (datetime.datetime (2010, 10, 8, 0, 0))

ucc = scope.uncommitted_changes
for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    print csp

for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    print csp.pid, sorted (csp.attribute_changes.iteritems ())

scope.commit ()

TFL.Environment.exec_python_startup ()

print rs1.attr_as_code()
rs1.set (date_exceptions = None)
rs1.event.date.set (finish = datetime.date (2010, 8, 19), start = datetime.date (2010, 8, 13))
rs1.dates.pop ()

ucc = scope.uncommitted_changes
for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    print csp

for pid, csp in sorted (ucc.by_pid.iteritems ()) :
    print csp.pid, sorted (csp.attribute_changes.iteritems ())

scope.commit ()

_ = p.lifetime.set (start = "1997/11/16")
_ = p.lifetime.set (finish = "2077/11/30")

"""

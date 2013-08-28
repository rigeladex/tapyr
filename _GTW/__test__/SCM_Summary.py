# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
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
#    19-Mar-2012 (CT) Adapt to reification of `SRM.Handicap`
#    12-Sep-2012 (CT) Adapt to recording of electric changes
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    15-Apr-2013 (CT) Adapt to change of `MOM.Attr.Kind.reset`
#    24-Apr-2013 (CT) Add test `no_net`; adapt to change of `MOM.SCM.Summary`
#    ««revision-date»»···
#--

from __future__ import unicode_literals

from _GTW.__test__.model           import *
from _GTW.__test__.Boat_in_Regatta import clean_change, show_change

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
    >>> ys    = SRM.Handicap ("Yardstick")
    >>> b     = SRM.Boat.instance_or_new (u'Optimist', u"1107", u"AUT", raw = True)
    >>> c     = b.copy (b.left, nation = b.nation, sail_number = "1134")
    >>> p     = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")
    >>> s     = SRM.Sailor.instance_or_new (p, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
    >>> rev   = SRM.Regatta_Event (u"Himmelfahrt", (u"20080501", ), raw = True)
    >>> reg   = SRM.Regatta_C (rev, bc)
    >>> reh   = SRM.Regatta_H (rev, ys)
    >>> bir   = SRM.Boat_in_Regatta (b, reg, skipper = s)
    >>> r1    = SRM.Race_Result (bir, 1, points = 8)
    >>> r2    = SRM.Race_Result (bir, 2, points = 4)
    >>> p1    = SWP.Page ("event-1-text", text = "Text for the 1. event", date = (("start", "2010/09/08"), ))
    >>> p2    = SWP.Page ("event-2-text", text = "Text for the 2. event", date = (("start", "2010/09/08"), ))
    >>> e1    = EVT.Event (p1.epk, ("2010/08/18", ))
    >>> rs1   = RS (e1, date_exceptions = ["2010/08/15"])
    >>> rr1   = RR (rs1, start = "20100801", count = 7, unit = "Weekly", raw = True)
    >>>
    >>> _     = rev.date.set (start = "2010/05/13", finish = "2010/05/13")
    >>> _     = bc.set (loa = 2.43)
    >>> _     = p.set_raw (title = "Mr.", salutation = "Dear L.")
    >>> _     = r1.set (discarded = True)
    >>> _     = rev.date.set (finish = "2010/05/14")

    >>> x
    SRM.Boat_Class (u'seascape 18')
    >>> xtn = x.type_name
    >>> sort_by_cid = TFL.Sorted_By ("-cid")
    >>> int (scope.query_changes (Q.type_name == xtn).order_by (sort_by_cid).first().cid) ### before x.destroy ()
    31
    >>> x.destroy ()
    >>> int (scope.query_changes (Q.type_name == xtn).order_by (sort_by_cid).first().cid) ### after x.destroy ()
    35

    >>> rev.date.finish = datetime.date (2010, 05, 13)
    >>> rs1.dates.append (datetime.datetime (2010, 9, 8, 0, 0))
    >>> rs1.dates.append (datetime.datetime (2010, 10, 8, 0, 0))

    >>> ucc  = csm1 = scope.uncommitted_changes

    >>> for csp in ucc.changes :
    ...     show_change (csp)
    <Create SRM.Boat_Class (u'Optimist', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'1'}>
    <Create SRM.Boat_Class (u'420er', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'2'}>
    <Create SRM.Boat_Class (u'Laser', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'1'}>
    <Create SRM.Boat_Class (u'Seascape 18', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'4'}>
    <Create SRM.Handicap (u'Yardstick', 'SRM.Handicap'), new-values = {'last_cid' : '<n>'}>
    <Create SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
    <Copy SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1134', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
        <Create SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1134', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
    <Create PAP.Person (u'Tanzer', u'Laurens', u'', u'', 'PAP.Person'), new-values = {'last_cid' : '<n>'}>
    <Create SRM.Sailor ((u'Tanzer', u'Laurens', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), new-values = {'last_cid' : '<n>'}>
    <Create SRM.Regatta_Event (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), new-values = {'last_cid' : '<n>', 'perma_name' : u'himmelfahrt'}>
    <Create SRM.Regatta_C ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), new-values = {'is_cancelled' : u'no', 'last_cid' : '<n>', 'perma_name' : u'optimist'}>
    <Create SRM.Regatta_H ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Yardstick', 'SRM.Handicap'), 'SRM.Regatta_H'), new-values = {'is_cancelled' : u'no', 'last_cid' : '<n>', 'perma_name' : u'yardstick'}>
    <Create SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), new-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 9}>
    <Create SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'1', 'SRM.Race_Result'), new-values = {'last_cid' : '<n>', 'points' : u'8'}>
    <Create SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'2', 'SRM.Race_Result'), new-values = {'last_cid' : '<n>', 'points' : u'4'}>
    <Create SWP.Page (u'event-1-text', 'SWP.Page'), new-values = {'contents' : u'<p>Text for the 1. event</p>\n', 'date' : (('start', u'2010/09/08'),), 'last_cid' : '<n>', 'text' : u'Text for the 1. event'}>
    <Create SWP.Page (u'event-2-text', 'SWP.Page'), new-values = {'contents' : u'<p>Text for the 2. event</p>\n', 'date' : (('start', u'2010/09/08'),), 'last_cid' : '<n>', 'text' : u'Text for the 2. event'}>
    <Create EVT.Event ((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/18', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), new-values = {'date_exceptions' : u'2010/08/15', 'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/18', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Create EVT.Recurrence_Rule ((((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), u'', u'', 'EVT.Recurrence_Rule'), new-values = {'count' : u'7', 'last_cid' : '<n>', 'start' : u'2010/08/01', 'unit' : u'Weekly'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Modify SRM.Regatta_Event (u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), old-values = {'date' : (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'last_cid' : '<n>'}, new-values = {'date' : (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'last_cid' : '<n>'}>
    <Modify SRM.Boat_Class (u'Optimist', 'SRM.Boat_Class'), old-values = {'last_cid' : '<n>', 'loa' : u''}, new-values = {'last_cid' : '<n>', 'loa' : u'2.43'}>
    <Modify PAP.Person (u'Tanzer', u'Laurens', u'', u'Mr.', 'PAP.Person'), old-values = {'last_cid' : '<n>', 'salutation' : u'', 'title' : u''}, new-values = {'last_cid' : '<n>', 'salutation' : u'Dear L.', 'title' : u'Mr.'}>
    <Modify SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'1', 'SRM.Race_Result'), old-values = {'discarded' : u'no', 'last_cid' : '<n>'}, new-values = {'discarded' : u'yes', 'last_cid' : '<n>'}>
    <Modify SRM.Regatta_Event (u'Himmelfahrt', (('finish', u'2010/05/14'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), old-values = {'date' : (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'last_cid' : '<n>'}, new-values = {'date' : (('finish', u'2010/05/14'), ('start', u'2010/05/13')), 'last_cid' : '<n>'}>
    <Destroy SRM.Boat_Class (u'Seascape 18', 'SRM.Boat_Class'), old-values = {'last_cid' : '<n>', 'max_crew' : u'4'}>
    <Modify/C SRM.Regatta_Event.date (u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), old-values = {'finish' : u'2010/05/14', 'last_cid' : '<n>'}, new-values = {'finish' : u'2010/05/13', 'last_cid' : '<n>'}>
    <Modify EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), old-values = {'dates' : u'', 'last_cid' : '<n>'}, new-values = {'dates' : u'2010/09/08', 'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Modify EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), old-values = {'dates' : u'2010/09/08', 'last_cid' : '<n>'}, new-values = {'dates' : u'2010/09/08,2010/10/08', 'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/10/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 1
    ...     show_change (csp)
    <Change Summary for pid 1: newborn, 1 change>
        <Create SRM.Boat_Class (u'Optimist', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'1'}>
        <Modify SRM.Boat_Class (u'Optimist', 'SRM.Boat_Class'), old-values = {'last_cid' : '<n>', 'loa' : u''}, new-values = {'last_cid' : '<n>', 'loa' : u'2.43'}>
    <Change Summary for pid 2: newborn>
        <Create SRM.Boat_Class (u'420er', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'2'}>
    <Change Summary for pid 3: newborn>
        <Create SRM.Boat_Class (u'Laser', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'1'}>
    <Change Summary for pid 4: newborn, just died>
        <Create SRM.Boat_Class (u'Seascape 18', 'SRM.Boat_Class'), new-values = {'last_cid' : '<n>', 'max_crew' : u'4'}>
        <Destroy SRM.Boat_Class (u'Seascape 18', 'SRM.Boat_Class'), old-values = {'last_cid' : '<n>', 'max_crew' : u'4'}>
    <Change Summary for pid 5: newborn>
        <Create SRM.Handicap (u'Yardstick', 'SRM.Handicap'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 6: newborn>
        <Create SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 7: newborn, 1 change>
        <Create SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1134', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
        <Copy SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1134', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
          <Create SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1134', u'AUT', u'', 'SRM.Boat'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 8: newborn, 1 change>
        <Create PAP.Person (u'Tanzer', u'Laurens', u'', u'', 'PAP.Person'), new-values = {'last_cid' : '<n>'}>
        <Modify PAP.Person (u'Tanzer', u'Laurens', u'', u'Mr.', 'PAP.Person'), old-values = {'last_cid' : '<n>', 'salutation' : u'', 'title' : u''}, new-values = {'last_cid' : '<n>', 'salutation' : u'Dear L.', 'title' : u'Mr.'}>
    <Change Summary for pid 9: newborn>
        <Create SRM.Sailor ((u'Tanzer', u'Laurens', u'', u'', 'PAP.Person'), u'AUT', u'29676', u'', 'SRM.Sailor'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 10: newborn, 3 changes>
        <Create SRM.Regatta_Event (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), new-values = {'last_cid' : '<n>', 'perma_name' : u'himmelfahrt'}>
        <Modify SRM.Regatta_Event (u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), old-values = {'date' : (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'last_cid' : '<n>'}, new-values = {'date' : (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'last_cid' : '<n>'}>
        <Modify SRM.Regatta_Event (u'Himmelfahrt', (('finish', u'2010/05/14'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), old-values = {'date' : (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'last_cid' : '<n>'}, new-values = {'date' : (('finish', u'2010/05/14'), ('start', u'2010/05/13')), 'last_cid' : '<n>'}>
        <Modify/C SRM.Regatta_Event.date (u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), old-values = {'finish' : u'2010/05/14', 'last_cid' : '<n>'}, new-values = {'finish' : u'2010/05/13', 'last_cid' : '<n>'}>
    <Change Summary for pid 11: newborn>
        <Create SRM.Regatta_C ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), new-values = {'is_cancelled' : u'no', 'last_cid' : '<n>', 'perma_name' : u'optimist'}>
    <Change Summary for pid 12: newborn>
        <Create SRM.Regatta_H ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Yardstick', 'SRM.Handicap'), 'SRM.Regatta_H'), new-values = {'is_cancelled' : u'no', 'last_cid' : '<n>', 'perma_name' : u'yardstick'}>
    <Change Summary for pid 13: newborn>
        <Create SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), new-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 9}>
    <Change Summary for pid 14: newborn, 1 change>
        <Create SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'1', 'SRM.Race_Result'), new-values = {'last_cid' : '<n>', 'points' : u'8'}>
        <Modify SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'1', 'SRM.Race_Result'), old-values = {'discarded' : u'no', 'last_cid' : '<n>'}, new-values = {'discarded' : u'yes', 'last_cid' : '<n>'}>
    <Change Summary for pid 15: newborn>
        <Create SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'2', 'SRM.Race_Result'), new-values = {'last_cid' : '<n>', 'points' : u'4'}>
    <Change Summary for pid 16: newborn>
        <Create SWP.Page (u'event-1-text', 'SWP.Page'), new-values = {'contents' : u'<p>Text for the 1. event</p>\n', 'date' : (('start', u'2010/09/08'),), 'last_cid' : '<n>', 'text' : u'Text for the 1. event'}>
    <Change Summary for pid 17: newborn>
        <Create SWP.Page (u'event-2-text', 'SWP.Page'), new-values = {'contents' : u'<p>Text for the 2. event</p>\n', 'date' : (('start', u'2010/09/08'),), 'last_cid' : '<n>', 'text' : u'Text for the 2. event'}>
    <Change Summary for pid 18: newborn>
        <Create EVT.Event ((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 19: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/18', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/18', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 20: newborn, 2 changes>
        <Create EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), new-values = {'date_exceptions' : u'2010/08/15', 'last_cid' : '<n>'}>
        <Modify EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), old-values = {'dates' : u'', 'last_cid' : '<n>'}, new-values = {'dates' : u'2010/09/08', 'last_cid' : '<n>'}>
        <Modify EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), old-values = {'dates' : u'2010/09/08', 'last_cid' : '<n>'}, new-values = {'dates' : u'2010/09/08,2010/10/08', 'last_cid' : '<n>'}>
    <Change Summary for pid 21: newborn>
        <Create EVT.Recurrence_Rule ((((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), u'', u'', 'EVT.Recurrence_Rule'), new-values = {'count' : u'7', 'last_cid' : '<n>', 'start' : u'2010/08/01', 'unit' : u'Weekly'}>
    <Change Summary for pid 22: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 23: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 24: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 25: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 26: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 27: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 28: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 29: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 30: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 31: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 32: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 33: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 34: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 35: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 36: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 37: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 38: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 39: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 40: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 41: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 42: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/10/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '<n>'}>

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 2
    ...   if csp :
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    1 [('last_cid', (old = None, new = '31')), ('loa', (old = u'', new = u'2.43')), ('max_crew', (old = None, new = u'1'))]
    2 [('last_cid', (old = None, new = '2')), ('max_crew', (old = None, new = u'2'))]
    3 [('last_cid', (old = None, new = '3')), ('max_crew', (old = None, new = u'1'))]
    5 [('last_cid', (old = None, new = '5'))]
    6 [('last_cid', (old = None, new = '6'))]
    7 [('last_cid', (old = None, new = '8'))]
    8 [('last_cid', (old = None, new = '32')), ('salutation', (old = u'', new = u'Dear L.')), ('title', (old = u'', new = u'Mr.'))]
    9 [('last_cid', (old = None, new = '10'))]
    10 [('date', (old = (('finish', u'2008/05/01'), ('start', u'2008/05/01')), new = (('finish', u'2010/05/13'), ('start', u'2010/05/13')))), ('last_cid', (old = None, new = '36')), ('perma_name', (old = None, new = u'himmelfahrt'))]
    11 [('is_cancelled', (old = None, new = u'no')), ('last_cid', (old = None, new = '12')), ('perma_name', (old = None, new = u'optimist'))]
    12 [('is_cancelled', (old = None, new = u'no')), ('last_cid', (old = None, new = '13')), ('perma_name', (old = None, new = u'yardstick'))]
    13 [('last_cid', (old = None, new = '14')), ('registration_date', (old = None, new = u'<today>')), ('skipper', (old = None, new = 9))]
    14 [('discarded', (old = u'no', new = u'yes')), ('last_cid', (old = None, new = '33')), ('points', (old = None, new = u'8'))]
    15 [('last_cid', (old = None, new = '16')), ('points', (old = None, new = u'4'))]
    16 [('contents', (old = None, new = u'<p>Text for the 1. event</p>\n')), ('date', (old = None, new = (('start', u'2010/09/08'),))), ('last_cid', (old = None, new = '17')), ('text', (old = None, new = u'Text for the 1. event'))]
    17 [('contents', (old = None, new = u'<p>Text for the 2. event</p>\n')), ('date', (old = None, new = (('start', u'2010/09/08'),))), ('last_cid', (old = None, new = '18')), ('text', (old = None, new = u'Text for the 2. event'))]
    18 [('last_cid', (old = None, new = '19'))]
    20 [('date_exceptions', (old = None, new = u'2010/08/15')), ('dates', (old = u'', new = u'2010/09/08,2010/10/08')), ('last_cid', (old = None, new = '51'))]
    21 [('count', (old = None, new = u'7')), ('last_cid', (old = None, new = '23')), ('start', (old = None, new = u'2010/08/01')), ('unit', (old = None, new = u'Weekly'))]
    35 [('last_cid', (old = None, new = '59'))]
    36 [('last_cid', (old = None, new = '60'))]
    37 [('last_cid', (old = None, new = '61'))]
    38 [('last_cid', (old = None, new = '62'))]
    39 [('last_cid', (old = None, new = '63'))]
    40 [('last_cid', (old = None, new = '64'))]
    41 [('last_cid', (old = None, new = '65'))]
    42 [('last_cid', (old = None, new = '66'))]

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)
    1 ['last_cid', 'loa']
    2 ['last_cid']
    3 ['last_cid']
    5 ['last_cid']
    6 ['last_cid']
    7 ['last_cid']
    8 ['last_cid', 'salutation', 'title']
    9 ['last_cid']
    10 ['date', 'last_cid']
    11 ['last_cid']
    12 ['last_cid']
    13 ['last_cid']
    14 ['discarded', 'last_cid']
    15 ['last_cid']
    16 ['last_cid']
    17 ['last_cid']
    18 ['last_cid']
    20 ['dates', 'last_cid']
    21 ['last_cid']
    35 ['last_cid']
    36 ['last_cid']
    37 ['last_cid']
    38 ['last_cid']
    39 ['last_cid']
    40 ['last_cid']
    41 ['last_cid']
    42 ['last_cid']

    >>> scope.commit ()

    >>> print rs1.attr_as_code()
    ((u'event-1-text', ), (u'2010/08/18', ), (), u''), dates = u"u'2010/09/08',u'2010/10/08'", date_exceptions = u"u'2010/08/15'"
    >>> rs1.set (date_exceptions = None)
    1
    >>> rs1.event.date.set (finish = datetime.date (2010, 8, 19), start = datetime.date (2010, 8, 13))
    1
    >>> rs1.dates.pop ()
    datetime.datetime(2010, 10, 8, 0, 0)

    >>> ucc = scope.uncommitted_changes
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 3
    ...     print csp
    <Change Summary for pid 18: 1 change>
        <Modify EVT.Event ((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), old-values = {'date' : (('start', u'2010/08/18'),), 'last_cid' : '19'}, new-values = {'date' : (('finish', u'2010/08/19'), ('start', u'2010/08/13')), 'last_cid' : '85'}>
    <Change Summary for pid 20: 2 changes>
        <Modify EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), old-values = {'date_exceptions' : u'2010/08/15', 'last_cid' : '51'}, new-values = {'date_exceptions' : u'', 'last_cid' : '67'}>
        <Modify EVT.Recurrence_Spec (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), 'EVT.Recurrence_Spec'), old-values = {'dates' : u'2010/09/08,2010/10/08', 'last_cid' : '67'}, new-values = {'dates' : u'2010/09/08', 'last_cid' : '100'}>
    <Change Summary for pid 35: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '59'}>
    <Change Summary for pid 36: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '60'}>
    <Change Summary for pid 37: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '61'}>
    <Change Summary for pid 38: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '62'}>
    <Change Summary for pid 39: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '63'}>
    <Change Summary for pid 40: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '64'}>
    <Change Summary for pid 41: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '65'}>
    <Change Summary for pid 42: just died>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/10/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '66'}>
    <Change Summary for pid 43: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '76'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '76'}>
    <Change Summary for pid 44: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '77'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '77'}>
    <Change Summary for pid 45: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/15', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '78'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/15', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '78'}>
    <Change Summary for pid 46: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '79'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/22', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '79'}>
    <Change Summary for pid 47: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '80'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/29', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '80'}>
    <Change Summary for pid 48: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '81'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/09/05', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '81'}>
    <Change Summary for pid 49: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '82'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '82'}>
    <Change Summary for pid 50: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '83'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/09/12', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '83'}>
    <Change Summary for pid 51: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('start', u'2010/08/18'),), u'', u'', 'EVT.Event'), u'2010/10/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '84'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/10/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '84'}>
    <Change Summary for pid 52: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '95'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '95'}>
    <Change Summary for pid 53: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '96'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '96'}>
    <Change Summary for pid 54: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/15', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '97'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/15', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '97'}>
    <Change Summary for pid 55: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '98'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '98'}>
    <Change Summary for pid 56: newborn, just died>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/10/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '99'}>
        <Destroy EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/10/08', u'', 'EVT.Event_occurs'), old-values = {'last_cid' : '99'}>
    <Change Summary for pid 57: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/01', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '106'}>
    <Change Summary for pid 58: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '107'}>
    <Change Summary for pid 59: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/08/15', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '108'}>
    <Change Summary for pid 60: newborn>
        <Create EVT.Event_occurs (((u'event-1-text', 'SWP.Page'), (('finish', u'2010/08/19'), ('start', u'2010/08/13')), u'', u'', 'EVT.Event'), u'2010/09/08', u'', 'EVT.Event_occurs'), new-values = {'last_cid' : '109'}>

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 4
    ...   if csp :
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    18 [('date', (old = (('start', u'2010/08/18'),), new = (('finish', u'2010/08/19'), ('start', u'2010/08/13')))), ('last_cid', (old = '19', new = '85'))]
    20 [('date_exceptions', (old = u'2010/08/15', new = u'')), ('dates', (old = u'2010/09/08,2010/10/08', new = u'2010/09/08')), ('last_cid', (old = '51', new = '100'))]
    35 [('last_cid', (old = '59', new = None))]
    36 [('last_cid', (old = '60', new = None))]
    37 [('last_cid', (old = '61', new = None))]
    38 [('last_cid', (old = '62', new = None))]
    39 [('last_cid', (old = '63', new = None))]
    40 [('last_cid', (old = '64', new = None))]
    41 [('last_cid', (old = '65', new = None))]
    42 [('last_cid', (old = '66', new = None))]
    57 [('last_cid', (old = None, new = '106'))]
    58 [('last_cid', (old = None, new = '107'))]
    59 [('last_cid', (old = None, new = '108'))]
    60 [('last_cid', (old = None, new = '109'))]

    >>> for e, acs in ucc.entity_changes (scope) :
    ...     print e.pid, clean_change (sorted (acs.iteritems ()))
    18 [('date', (old = (('start', u'2010/08/18'),), new = (('finish', u'2010/08/19'), ('start', u'2010/08/13')))), ('last_cid', (old = '19', new = '85'))]
    20 [('date_exceptions', (old = u'2010/08/15', new = u'')), ('dates', (old = u'2010/09/08,2010/10/08', new = u'2010/09/08')), ('last_cid', (old = '51', new = '100'))]
    57 [('last_cid', (old = None, new = '106'))]
    58 [('last_cid', (old = None, new = '107'))]
    59 [('last_cid', (old = None, new = '108'))]
    60 [('last_cid', (old = None, new = '109'))]

    >>> for e, acs in ucc.entity_changes (scope) :
    ...     e
    EVT.Event ((u'event-1-text', ), (u'2010/08/13', u'2010/08/19'), (), u'')
    EVT.Recurrence_Spec (((u'event-1-text', ), (u'2010/08/13', u'2010/08/19'), (), u''))
    EVT.Event_occurs (((u'event-1-text', ), (u'2010/08/13', u'2010/08/19'), (), u''), u'2010/08/01', ())
    EVT.Event_occurs (((u'event-1-text', ), (u'2010/08/13', u'2010/08/19'), (), u''), u'2010/08/08', ())
    EVT.Event_occurs (((u'event-1-text', ), (u'2010/08/13', u'2010/08/19'), (), u''), u'2010/08/15', ())
    EVT.Event_occurs (((u'event-1-text', ), (u'2010/08/13', u'2010/08/19'), (), u''), u'2010/09/08', ())

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)
    18 ['date', 'last_cid']
    20 ['date_exceptions', 'dates', 'last_cid']
    57 ['last_cid']
    58 ['last_cid']
    59 ['last_cid']
    60 ['last_cid']

    >>> scope.commit ()

    >>> SRM.Boat.query (sail_number = 1134).one ().destroy ()
    >>> b.destroy ()

    >>> ucc = scope.uncommitted_changes
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 5
    ...     show_change (csp)
    <Change Summary for pid 6: just died>
        <Destroy SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), old-values = {'last_cid' : '<n>'}>
          <Destroy SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), old-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 9}>
            <Destroy SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'1', 'SRM.Race_Result'), old-values = {'discarded' : u'yes', 'last_cid' : '<n>', 'points' : u'8'}>
            <Destroy SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'2', 'SRM.Race_Result'), old-values = {'last_cid' : '<n>', 'points' : u'4'}>
    <Change Summary for pid 7: just died>
        <Destroy SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'1134', u'AUT', u'', 'SRM.Boat'), old-values = {'last_cid' : '<n>'}>
    <Change Summary for pid 13: just died>
        <Destroy SRM.Boat_in_Regatta (((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), old-values = {'last_cid' : '<n>', 'registration_date' : u'<today>', 'skipper' : 9}>
          <Destroy SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'1', 'SRM.Race_Result'), old-values = {'discarded' : u'yes', 'last_cid' : '<n>', 'points' : u'8'}>
          <Destroy SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'2', 'SRM.Race_Result'), old-values = {'last_cid' : '<n>', 'points' : u'4'}>
    <Change Summary for pid 14: just died>
        <Destroy SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'1', 'SRM.Race_Result'), old-values = {'discarded' : u'yes', 'last_cid' : '<n>', 'points' : u'8'}>
    <Change Summary for pid 15: just died>
        <Destroy SRM.Race_Result ((((u'Optimist', 'SRM.Boat_Class'), u'1107', u'AUT', u'', 'SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2010/05/13'), ('start', u'2010/05/13')), 'SRM.Regatta_Event'), (u'Optimist', 'SRM.Boat_Class'), 'SRM.Regatta_C'), 'SRM.Boat_in_Regatta'), u'2', 'SRM.Race_Result'), old-values = {'last_cid' : '<n>', 'points' : u'4'}>

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 6
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    6 [('last_cid', (old = '6', new = None))]
    7 [('last_cid', (old = '8', new = None))]
    13 [('last_cid', (old = '14', new = None)), ('registration_date', (old = u'<today>', new = None)), ('skipper', (old = 9, new = None))]
    14 [('discarded', (old = u'yes', new = None)), ('last_cid', (old = '33', new = None)), ('points', (old = u'8', new = None))]
    15 [('last_cid', (old = '16', new = None)), ('points', (old = u'4', new = None))]

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)

    >>> scope.commit ()

    >>> _ = p.lifetime.set (start = "1997/11/16")
    >>> _ = p.lifetime.set (finish = "2077/11/30")

    >>> ucc = scope.uncommitted_changes
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 7
    ...     print csp
    <Change Summary for pid 8: 2 changes>
        <Modify/C PAP.Person.lifetime (u'Tanzer', u'Laurens', u'', u'Mr.', 'PAP.Person'), old-values = {'last_cid' : '32', 'start' : u''}, new-values = {'last_cid' : '115', 'start' : u'1997/11/16'}>
        <Modify/C PAP.Person.lifetime (u'Tanzer', u'Laurens', u'', u'Mr.', 'PAP.Person'), old-values = {'finish' : u'', 'last_cid' : '115'}, new-values = {'finish' : u'2077/11/30', 'last_cid' : '116'}>

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 8
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    8 [('last_cid', (old = '32', new = '116')), ('lifetime', (old = (('finish', u''), ('start', u'')), new = (('finish', u'2077/11/30'), ('start', u'1997/11/16'))))]

    >>> for pid, ca in sorted (ucc.changed_attrs.iteritems ()) :
    ...     print pid, sorted (ca)
    8 ['last_cid', 'lifetime']

    >>> len (csm1)
    65
    >>> conflicts, merges = csm1.change_conflicts ({}, scope)
    >>> sorted (conflicts), sorted (merges)
    ([], [])

"""

_no_net = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP   = scope.PAP
    >>> p     = PAP.Person.instance_or_new (u"Tanzer", u"Laurens")

    >>> scope.commit ()

    >>> ucc = scope.uncommitted_changes
    >>> _   = p.set (title = "Mr.")

    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 1
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    1 [('last_cid', (old = '1', new = '2')), ('title', (old = u'', new = u'Mr.'))]

    >>> _ = p.set (title = "")
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 2
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    1 [('last_cid', (old = '1', new = '3'))]

    >>> scope.commit ()

    >>> ucc = scope.uncommitted_changes
    >>> _   = p.set (title = "Mr.")
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 3
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    1 [('last_cid', (old = '3', new = '4')), ('title', (old = u'', new = u'Mr.'))]

    >>> p.destroy ()
    >>> for pid, csp in sorted (ucc.by_pid.iteritems ()) : ### 4
    ...     print csp.pid, clean_change (sorted (csp.attribute_changes.iteritems ()))
    1 [('last_cid', (old = '3', new = None)), ('title', (old = u'', new = None))]

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
        <Modify PAP.Person (u'Tanzer', u'Laurens', u'', u'', 'PAP.Person'), old-values = {'last_cid' : '1', 'salutation' : u''}, new-values = {'last_cid' : '2', 'salutation' : u'Dear Laurens'}>

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
        <Modify PAP.Person (u'Tanzer', u'Laurens', u'', u'', 'PAP.Person'), old-values = {'last_cid' : '1', 'salutation' : u''}, new-values = {'last_cid' : '3', 'salutation' : u'Lieber Laurens'}>

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

    """
    )

Scaffold.Backend_Default_Path ["SQL"] = "'test.sqlite'"

__test__ = dict \
    ( Scaffold.create_test_dict (_more, ignore = ("HPS", "SQL"))
    , ** Scaffold.create_test_dict (_basic)
    )

__test__ = dict \
    ( ** Scaffold.create_test_dict
        ( dict
            ( basic  = _basic
            , no_net = _no_net
            )
        )
    )

### __END__ GTW.__test__.SCM_Summary

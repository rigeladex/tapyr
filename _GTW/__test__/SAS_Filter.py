# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.__test__.SAS_Filter
#
# Purpose
#    Test the SAS function for sorting by attributes of a composite using the
#    SAS backend.
#
# Revision Dates
#    30-Apr-2010 (MG) Creation
#     3-May-2010 (MG) New test for query attributes added
#     5-May-2010 (MG) Additional tests added
#     7-May-2010 (MG) `sail_number` is now a numeric string
#    ««revision-date»»···
#--

_composite = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> p3 = SWP.Page ("event-3-text", text = "Text for the 3. event")
    >>> p4 = SWP.Page ("event-4-text", text = "Text for the 4. event")
    >>> e1 = EVT.Event \
    ...     (p1.epk_raw, dict (start = "1.4.2010", raw = True), raw = True)
    >>> e2 = EVT.Event \
    ...     (p2.epk_raw, dict (start = "1.3.2010", raw = True), raw = True)
    >>> e3 = EVT.Event \
    ...     (p3.epk_raw, dict (start = "1.2.2010", raw = True), raw = True)
    >>> e4 = EVT.Event \
    ...     (p4.epk_raw, dict (start = "1.1.2010", raw = True), raw = True)
    >>> date = datetime.date (2010, 3, 1)
    >>> q = EVT.Event.query ()
    >>> for e in q.all () : print e ### all
    ((u'event-1-text', ), dict (start = u'2010/04/01'), dict ())
    ((u'event-2-text', ), dict (start = u'2010/03/01'), dict ())
    ((u'event-3-text', ), dict (start = u'2010/02/01'), dict ())
    ((u'event-4-text', ), dict (start = u'2010/01/01'), dict ())
    >>> q = EVT.Event.query ().filter (Q.date.start > date)
    >>> for e in q.all () : print e ### filtered 1
    ((u'event-1-text', ), dict (start = u'2010/04/01'), dict ())
    >>> q = EVT.Event.query ().filter (Q.date.start >= date)
    >>> for e in q.all () : print e ### filtered 2
    ((u'event-1-text', ), dict (start = u'2010/04/01'), dict ())
    ((u'event-2-text', ), dict (start = u'2010/03/01'), dict ())
    >>> q = EVT.Event.query ().filter (left = p1)
    >>> for e in q.all () : print e ### filtered 3
    ((u'event-1-text', ), dict (start = u'2010/04/01'), dict ())
"""

_link1_role = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> p3 = SWP.Page ("event-3-text", text = "Text for the 3. event")
    >>> p4 = SWP.Page ("event-4-text", text = "Text for the 4. event")
    >>> e1 = EVT.Event \
    ...     (p1.epk_raw, dict (start = "1.4.2010", raw = True), raw = True)
    >>> e2 = EVT.Event \
    ...     (p2.epk_raw, dict (start = "1.3.2010", raw = True), raw = True)
    >>> e3 = EVT.Event \
    ...     (p3.epk_raw, dict (start = "1.2.2010", raw = True), raw = True)
    >>> e4 = EVT.Event \
    ...     (p4.epk_raw, dict (start = "1.1.2010", raw = True), raw = True)
    >>> date = datetime.date (2010, 3, 1)
    >>> q = EVT.Event_occurs.query ()
    >>> for e in q.all () : print e ### all
    (((u'event-1-text', ), dict (start = u'2010/04/01'), dict ()), u'2010/04/01', dict ())
    (((u'event-2-text', ), dict (start = u'2010/03/01'), dict ()), u'2010/03/01', dict ())
    (((u'event-3-text', ), dict (start = u'2010/02/01'), dict ()), u'2010/02/01', dict ())
    (((u'event-4-text', ), dict (start = u'2010/01/01'), dict ()), u'2010/01/01', dict ())
    >>> q = EVT.Event_occurs.query ().filter (Q.event.date.start > date)
    >>> for e in q.all () : print e ### filter 1
    (((u'event-1-text', ), dict (start = u'2010/04/01'), dict ()), u'2010/04/01', dict ())
    >>> q = EVT.Event_occurs.query ().filter (Q.event.date.start >= date)
    >>> for e in q.all () : print e ### filter 2
    (((u'event-1-text', ), dict (start = u'2010/04/01'), dict ()), u'2010/04/01', dict ())
    (((u'event-2-text', ), dict (start = u'2010/03/01'), dict ()), u'2010/03/01', dict ())
    >>> q = EVT.Event_occurs.query ().filter (event = e1)
    >>> for e in q.all () : print e ### filter 3
    (((u'event-1-text', ), dict (start = u'2010/04/01'), dict ()), u'2010/04/01', dict ())
    >>> q = EVT.Event.query ().filter (Q.date.alive)
    >>> for e in q.all () : print e ### filter 4
    ((u'event-1-text', ), dict (start = u'2010/04/01'), dict ())
    ((u'event-2-text', ), dict (start = u'2010/03/01'), dict ())
    ((u'event-3-text', ), dict (start = u'2010/02/01'), dict ())
    ((u'event-4-text', ), dict (start = u'2010/01/01'), dict ())
"""

_link2_link1 = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', "AUT", "1107", raw = True)
    >>> p   = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> s   = SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (dict (start = "20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (dict (start = "20090521", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (dict (start = "20100513", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> date = datetime.date (2009, 1, 1)
    >>> q = scope.SRM.Boat_in_Regatta.query ()
    >>> for r in q.filter (Q.right.left.date.start > date) : print r
    (((u'Optimist', ), u'AUT', 1107), ((dict (start = u'2009/05/21', finish = u'2009/05/21'), u'Himmelfahrt'), (u'Optimist', )))
    (((u'Optimist', ), u'AUT', 1107), ((dict (start = u'2010/05/13', finish = u'2010/05/13'), u'Himmelfahrt'), (u'Optimist', )))

    >>> q = scope.SRM.Boat_in_Regatta.query ()
    >>> for r in q.filter (Q.right.left.date.start < date) : print r
    (((u'Optimist', ), u'AUT', 1107), ((dict (start = u'2008/05/01', finish = u'2008/05/01'), u'Himmelfahrt'), (u'Optimist', )))
    >>> date2 = datetime.date (2009, 12, 31)
    >>> qf = (Q.right.left.date.start >= date ) \
    ...    & (Q.right.left.date.start <= date2)
    >>> for r in q.filter (qf) : print r
    (((u'Optimist', ), u'AUT', 1107), ((dict (start = u'2009/05/21', finish = u'2009/05/21'), u'Himmelfahrt'), (u'Optimist', )))

    >>> date3 = datetime.date (2010, 05, 13)
    >>> for r in q.filter (Q.right.left.date.start == date3) : print r
    (((u'Optimist', ), u'AUT', 1107), ((dict (start = u'2010/05/13', finish = u'2010/05/13'), u'Himmelfahrt'), (u'Optimist', )))

"""

_query_attr = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> PAP  = scope.PAP
    >>> SRM  = scope.SRM
    >>> bc   = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b    = SRM.Boat.instance_or_new (u'Optimist', "AUT", "1107", raw = True)
    >>> p    = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> s    = SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (dict (start = "20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (dict (start = "20090521", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (dict (start = "20100513", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> q = SRM.Regatta_C.query ()
    >>> for r in q : print r.year, r
    2008 ((dict (start = u'2008/05/01', finish = u'2008/05/01'), u'Himmelfahrt'), (u'Optimist', ))
    2009 ((dict (start = u'2009/05/21', finish = u'2009/05/21'), u'Himmelfahrt'), (u'Optimist', ))
    2010 ((dict (start = u'2010/05/13', finish = u'2010/05/13'), u'Himmelfahrt'), (u'Optimist', ))
    >>> for r in q.filter (Q.event.date.start.D.YEAR (2010)) : print r.year, r
    2010 ((dict (start = u'2010/05/13', finish = u'2010/05/13'), u'Himmelfahrt'), (u'Optimist', ))
    >>> for r in q.filter (Q.event.date.start.D.YEAR (2009)) : print r.year, r
    2009 ((dict (start = u'2009/05/21', finish = u'2009/05/21'), u'Himmelfahrt'), (u'Optimist', ))
"""

if 1 :
    __test__ = dict \
        ( composite   = _composite
        , link1_role  = _link1_role
        , link2_link1 = _link2_link1
        , query_attr  = _query_attr
        )
else :
    __doc__ = _link1_role
    #__doc__ = _query_attr

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q
import  datetime

### __END__ GTW.__test__.SAS_Filter

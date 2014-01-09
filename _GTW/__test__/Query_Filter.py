# -*- coding: utf-8 -*-
# Copyright (C) 2010-2014 Martin Glueck All rights reserved
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
#    GTW.__test__.Query_Filter
#
# Purpose
#    Test the query filters
#
# Revision Dates
#    30-Apr-2010 (MG) Creation
#     3-May-2010 (MG) New test for query attributes added
#     5-May-2010 (MG) Additional tests added
#     7-May-2010 (MG) `sail_number` is now a numeric string
#    19-Jul-2011 (CT) Test for `Q.RAW` added
#    25-Jul-2011 (MG) `_date_queries` added
#    25-Jul-2011 (CT) `_date_queries` corrected (s/query/query_s/)
#    19-Mar-2012 (CT) Adapt to `Boat_Class.name.ignore_case` now being `True`
#    15-Apr-2012 (CT) Use `show` to guarantee deterministic order
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    30-Jul-2013 (CT) Add `show` and `.order_by`, enable HPS
#    23-Sep-2013 (CT) Add test `sub_query_sql`
#    ««revision-date»»···
#--

def show (q) :
    return sorted (str (x) for x in q)

_composite = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> p3 = SWP.Page ("event-3-text", text = "Text for the 3. event")
    >>> p4 = SWP.Page ("event-4-text", text = "Text for the 4. event")
    >>> e1 = EVT.Event (p1.epk_raw, ("1.4.2010", ), raw = True)
    >>> e2 = EVT.Event (p2.epk_raw, ("1.3.2010", ), raw = True)
    >>> e3 = EVT.Event (p3.epk_raw, ("1.2.2010", ), raw = True)
    >>> e4 = EVT.Event (p4.epk_raw, ("1.1.2010", ), raw = True)
    >>> date = datetime.date (2010, 3, 1)
    >>> q = EVT.Event.query ()
    >>> for e in show (q) : print e ### all
    ((u'event-1-text', ), (u'2010/04/01', ), (), u'')
    ((u'event-2-text', ), (u'2010/03/01', ), (), u'')
    ((u'event-3-text', ), (u'2010/02/01', ), (), u'')
    ((u'event-4-text', ), (u'2010/01/01', ), (), u'')
    >>> q = EVT.Event.query ().filter (Q.date.start > date)
    >>> for e in show (q) : print e ### filtered 1
    ((u'event-1-text', ), (u'2010/04/01', ), (), u'')
    >>> q = EVT.Event.query ().filter (Q.date.start >= date)
    >>> for e in show (q) : print e ### filtered 2
    ((u'event-1-text', ), (u'2010/04/01', ), (), u'')
    ((u'event-2-text', ), (u'2010/03/01', ), (), u'')
    >>> q = EVT.Event.query ().filter (left = p1)
    >>> for e in show (q) : print e ### filtered 3
    ((u'event-1-text', ), (u'2010/04/01', ), (), u'')


"""

_link1_role = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> p3 = SWP.Page ("event-3-text", text = "Text for the 3. event")
    >>> p4 = SWP.Page ("event-4-text", text = "Text for the 4. event")
    >>> e1 = EVT.Event (p1.epk_raw, ("1.4.2010", ), raw = True)
    >>> e2 = EVT.Event (p2.epk_raw, ("1.3.2010", ), raw = True)
    >>> e3 = EVT.Event (p3.epk_raw, ("1.2.2010", ), raw = True)
    >>> e4 = EVT.Event (p4.epk_raw, ("1.1.2010", ), raw = True)
    >>> date = datetime.date (2010, 3, 1)
    >>> q = EVT.Event_occurs.query ()
    >>> for e in show (q) : print e ### all
    (((u'event-1-text', ), (u'2010/04/01', ), (), u''), u'2010/04/01', ())
    (((u'event-2-text', ), (u'2010/03/01', ), (), u''), u'2010/03/01', ())
    (((u'event-3-text', ), (u'2010/02/01', ), (), u''), u'2010/02/01', ())
    (((u'event-4-text', ), (u'2010/01/01', ), (), u''), u'2010/01/01', ())
    >>> q = EVT.Event_occurs.query ().filter (Q.event.date.start > date)
    >>> for e in show (q) : print e ### filter 1
    (((u'event-1-text', ), (u'2010/04/01', ), (), u''), u'2010/04/01', ())
    >>> q = EVT.Event_occurs.query ().filter (Q.event.date.start >= date)
    >>> for e in show (q) : print e ### filter 2
    (((u'event-1-text', ), (u'2010/04/01', ), (), u''), u'2010/04/01', ())
    (((u'event-2-text', ), (u'2010/03/01', ), (), u''), u'2010/03/01', ())
    >>> q = EVT.Event_occurs.query ().filter (event = e1)
    >>> for e in show (q) : print e ### filter 3
    (((u'event-1-text', ), (u'2010/04/01', ), (), u''), u'2010/04/01', ())
    >>> q = EVT.Event.query ().filter (Q.date.alive)
    >>> for e in show (q) : print e ### filter 4
    ((u'event-1-text', ), (u'2010/04/01', ), (), u'')
    ((u'event-2-text', ), (u'2010/03/01', ), (), u'')
    ((u'event-3-text', ), (u'2010/02/01', ), (), u'')
    ((u'event-4-text', ), (u'2010/01/01', ), (), u'')


"""

_link2_link1 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', "1107", "AUT", raw = True)
    >>> p   = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> s   = SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", ("20080501", ), raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", ("20090521", ), raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", ("20100513", ), raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> date = datetime.date (2009, 1, 1)
    >>> q = scope.SRM.Boat_in_Regatta.query ().order_by (Q.pid)
    >>> for r in show (q.filter (Q.right.left.date.start > date)) : print r ### SRM.Boat_in_Regatta
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', )))
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', )))

    >>> q = scope.SRM.Boat_in_Regatta.query ()
    >>> for r in q.filter (Q.right.left.date.start < date) : print r
    (((u'optimist', ), 1107, u'AUT',  u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))
    >>> date2 = datetime.date (2009, 12, 31)
    >>> qf = (Q.right.left.date.start >= date ) \
    ...    & (Q.right.left.date.start <= date2)
    >>> for r in q.filter (qf) : print r
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', )))

    >>> date3 = datetime.date (2010, 05, 13)
    >>> for r in q.filter (Q.right.left.date.start == date3) : print r
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', )))

    >>> for r in q.filter (Q.RAW.right.left.date.start == "2010/05/13") : print r
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', )))


"""

_query_attr = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP  = scope.PAP
    >>> SRM  = scope.SRM
    >>> bc   = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b    = SRM.Boat.instance_or_new (u'Optimist', "1107", "AUT", raw = True)
    >>> p    = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> s    = SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", ("20080501", ), raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", ("20090521", ), raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", ("20100513", ), raw = True)
    >>> reg = SRM.Regatta_C     (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)

    >>> q = SRM.Regatta_C.query ().order_by  (Q.pid)
    >>> for r in q : print r.year, r
    2008 ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))
    2009 ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', ))
    2010 ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', ))

    >>> for r in q.filter (Q.event.date.start.D.YEAR (2010)) : print r.year, r
    2010 ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', ))

    >>> for r in q.filter (Q.event.date.start.D.YEAR (2009)) : print r.year, r
    2009 ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', ))

    >>> for r in q.filter (Q.event.date.start.year == 2010) : print r.year, r
    2010 ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', ))

    >>> for r in q.filter (Q.event.date.start >= "2010/01/01", Q.event.date.start <= "2010/12/31") : print r.year, r
    2010 ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', ))

    >>> PAP.Person.query (Q.last_name == "tanzer").all ()
    [PAP.Person (u'tanzer', u'christian', u'', u'')]

    >>> PAP.Person.query (Q.last_name == "Tanzer").all ()
    []

    >>> PAP.Person.query (Q.RAW.last_name == "Tanzer").all ()
    [PAP.Person (u'tanzer', u'christian', u'', u'')]

"""

_date_queries = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> DI  = lambda s : scope.MOM.Date_Interval (s, raw = True)
    >>> p   = scope.PAP.Person  ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> p   = scope.PAP.Person  ("LN 2", "FN 2", lifetime = DI ("2010/01/03"))
    >>> p   = scope.PAP.Person  ("LN 3", "FN 3", lifetime = DI ("2010/02/01"))
    >>> p   = scope.PAP.Person  ("LN 4", "FN 4", lifetime = DI ("2011/01/03"))
    >>> scope.commit ()

    >>> print scope.PAP.Person.query_s (Q.lifetime.start.year == 2010).all ()
    [PAP.Person (u'ln 1', u'fn 1', u'', u''), PAP.Person (u'ln 2', u'fn 2', u'', u''), PAP.Person (u'ln 3', u'fn 3', u'', u'')]
    >>> print scope.PAP.Person.query_s (Q.lifetime.start.year <= 2010).all ()
    [PAP.Person (u'ln 1', u'fn 1', u'', u''), PAP.Person (u'ln 2', u'fn 2', u'', u''), PAP.Person (u'ln 3', u'fn 3', u'', u'')]
    >>> print scope.PAP.Person.query_s (Q.lifetime.start.year >= 2010).all ()
    [PAP.Person (u'ln 1', u'fn 1', u'', u''), PAP.Person (u'ln 2', u'fn 2', u'', u''), PAP.Person (u'ln 3', u'fn 3', u'', u''), PAP.Person (u'ln 4', u'fn 4', u'', u'')]
    >>> print scope.PAP.Person.query_s (Q.lifetime.start.year >  2010).all ()
    [PAP.Person (u'ln 4', u'fn 4', u'', u'')]

"""

_sub_query = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> DI  = lambda s : scope.MOM.Date_Interval (s, raw = True)
    >>> p   = scope.PAP.Person  ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> p   = scope.PAP.Person  ("LN 1", "FN 2", lifetime = DI ("2010/01/03"))
    >>> p   = scope.PAP.Person  ("LN 2", "FN 3", lifetime = DI ("2010/02/01"))
    >>> p   = scope.PAP.Person  ("LN 2", "FN 4", lifetime = DI ("2011/01/03"))
    >>> scope.commit ()

    >>> q1 = scope.PAP.Person.query (last_name = "ln 1").attr ("pid")
    >>> q2 = scope.PAP.Person.query (last_name = "ln 2").attr ("pid")

    >>> print q1.order_by ("pid").all ()
    [1, 2]

    >>> print q2.order_by ("pid").all ()
    [3, 4]

    >>> q  = scope.PAP.Person.query_s (Q.pid.IN (q1))
    >>> print q.all ()
    [PAP.Person (u'ln 1', u'fn 1', u'', u''), PAP.Person (u'ln 1', u'fn 2', u'', u'')]

"""

_sub_query_sql = """
    >>> from _GTW.__test__._SAW_test_functions import show_query
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> DI  = lambda s : scope.MOM.Date_Interval (s, raw = True)
    >>> _   = scope.PAP.Person  ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> _   = scope.PAP.Person  ("LN 1", "FN 2", lifetime = DI ("2010/01/03"))
    >>> _   = scope.PAP.Person  ("LN 2", "FN 3", lifetime = DI ("2010/02/01"))
    >>> _   = scope.PAP.Person  ("LN 2", "FN 4", lifetime = DI ("2011/01/03"))
    >>> scope.commit ()

    >>> q1 = scope.PAP.Person.query (last_name = "ln 1").attr ("pid")
    >>> qe = scope.PAP.Person.query (Q.pid.IN ([]))
    >>> qs = scope.PAP.Person.query (Q.pid.IN (q1))

    >>> show_query (qe)
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE false

    >>> show_query (qs)
    SQL: SELECT
           mom_id_entity.electric AS mom_id_entity_electric,
           mom_id_entity.last_cid AS mom_id_entity_last_cid,
           mom_id_entity.pid AS mom_id_entity_pid,
           mom_id_entity.type_name AS mom_id_entity_type_name,
           mom_id_entity.x_locked AS mom_id_entity_x_locked,
           pap_person.__raw_first_name AS pap_person___raw_first_name,
           pap_person.__raw_last_name AS pap_person___raw_last_name,
           pap_person.__raw_middle_name AS pap_person___raw_middle_name,
           pap_person.__raw_title AS pap_person___raw_title,
           pap_person.first_name AS pap_person_first_name,
           pap_person.last_name AS pap_person_last_name,
           pap_person.lifetime__finish AS pap_person_lifetime__finish,
           pap_person.lifetime__start AS pap_person_lifetime__start,
           pap_person.middle_name AS pap_person_middle_name,
           pap_person.pid AS pap_person_pid,
           pap_person.sex AS pap_person_sex,
           pap_person.title AS pap_person_title
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE mom_id_entity.pid IN (SELECT DISTINCT mom_id_entity.pid AS mom_id_entity_pid
         FROM mom_id_entity
           JOIN pap_person ON mom_id_entity.pid = pap_person.pid
         WHERE pap_person.last_name = :last_name_1)
    Parameters:
         last_name_1          : u'ln 1'

"""

_type_name_query = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> p1 = scope.SWP.Page   (perma_name = "page-1", text = "page-1")
    >>> p2 = scope.SWP.Page   (perma_name = "page-2", text = "page-2")
    >>> y1 = scope.SWP.Page_Y (perma_name = "year-1", text = "year-1", year = 2011)
    >>> y2 = scope.SWP.Page_Y (perma_name = "year-2", text = "year-2", year = 2012)
    >>> c1 = scope.SWP.Clip_O (left = p1, abstract = "abstract-p1.1")
    >>> c2 = scope.SWP.Clip_O (left = p2, abstract = "abstract-p2.1")
    >>> c3 = scope.SWP.Clip_O (left = y1, abstract = "abstract-y1.1")
    >>> c4 = scope.SWP.Clip_O (left = y2, abstract = "abstract-y2.1")
    >>> scope.commit ()

    >>> scope.SWP.Clip_O.query (Q.left.type_name == "SWP.Page").all ()
    [SWP.Clip_O ((u'page-1', ), ()), SWP.Clip_O ((u'page-2', ), ())]

    >>> scope.SWP.Clip_O.query (Q.left.type_name == "SWP.Page_Y").all ()
    [SWP.Clip_O ((u'year-1', 2011), ()), SWP.Clip_O ((u'year-2', 2012), ())]

"""

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q
import  datetime

__test__ = Scaffold.create_test_dict \
    ( dict
        ( composite    = _composite
        , date_queries = _date_queries
        , link1_role   = _link1_role
        , link2_link1  = _link2_link1
        , query_attr   = _query_attr
        , sub_query    = _sub_query
        , type_name    = _type_name_query
        )
    )

__test__.update \
    ( Scaffold.create_test_dict
        ( dict
            ( sub_query_swl = _sub_query_sql
            )
        , ignore = ("HPS", )
        )
    )

### __END__ GTW.__test__.Query_Filter

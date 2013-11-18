# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
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
#    GTW.__test__.Query_Sorted_By
#
# Purpose
#    Test sorting of queries
#
# Revision Dates
#    30-Apr-2010 (MG) Creation
#     7-May-2010 (MG) `sail_number` is now a numeric string
#    10-Aug-2010 (MG) Additional test added
#    10-Aug-2010 (MG) Test changed to allow different backends
#    16-Aug-2010 (MG) Test fixed
#    20-Dec-2010 (CT) Python 2.7 compatibility
#    19-Mar-2012 (CT) Adapt to `Boat_Class.name.ignore_case` now being `True`
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    30-Jul-2013 (CT) Rename to `Query_Sorted_By`, enable `HPS`
#    ««revision-date»»···
#--

_composite = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> e1 = EVT.Event (p1.epk_raw, ("1.2.2010", ), raw = True)
    >>> e2 = EVT.Event (p2.epk_raw, ("1.1.2010", ), raw = True)
    >>> q = EVT.Event.query ().order_by (TFL.Sorted_By (Q.date.start))
    >>> for e in q.all () : print e
    ((u'event-2-text', ), (u'2010/01/01', ), (), u'')
    ((u'event-1-text', ), (u'2010/02/01', ), (), u'')

    >>> for e in EVT.Event.query (sort_key = EVT.Event.sorted_by) :
    ...     print e
    ((u'event-2-text', ), (u'2010/01/01', ), (), u'')
    ((u'event-1-text', ), (u'2010/02/01', ), (), u'')

    >>> for e in EVT.Event.query (sort_key = TFL.Sorted_By ("-date.start")) :
    ...     print e
    ((u'event-1-text', ), (u'2010/02/01', ), (), u'')
    ((u'event-2-text', ), (u'2010/01/01', ), (), u'')

    >>> for e in EVT.Event.query (sort_key = TFL.Sorted_By (Q.left.perma_name)) :
    ...     print e
    ((u'event-1-text', ), (u'2010/02/01', ), (), u'')
    ((u'event-2-text', ), (u'2010/01/01', ), (), u'')


"""

_link1_role = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> e1 = EVT.Event (p1.epk_raw, ("1.2.2010", ), raw = True)
    >>> e2 = EVT.Event (p2.epk_raw, ("1.1.2010", ), raw = True)
    >>> q = EVT.Event_occurs.query_s ()
    >>> for e in q.all () : print e ### default sort order
    (((u'event-2-text', ), (u'2010/01/01', ), (), u''), u'2010/01/01', ())
    (((u'event-1-text', ), (u'2010/02/01', ), (), u''), u'2010/02/01', ())
    >>> q = EVT.Event_occurs.query ().order_by (TFL.Sorted_By ("-event.date.start"))
    >>> for e in q.all () : print e ### sorted by descending date
    (((u'event-1-text', ), (u'2010/02/01', ), (), u''), u'2010/02/01', ())
    (((u'event-2-text', ), (u'2010/01/01', ), (), u''), u'2010/01/01', ())


"""

_link2_link1 = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', u"1107", "AUT", raw = True)
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

    >>> q = scope.SRM.Boat_in_Regatta.query ()
    >>> for r in q.order_by (Q.right.left.date.start) : print r
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', )))
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', )))
    >>> q = scope.SRM.Boat_in_Regatta.query ()
    >>> for r in q.order_by (TFL.Sorted_By ("-right.left.date.start")) : print r
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', )))
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', )))
    (((u'optimist', ), 1107, u'AUT', u''), ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', )))

    Unfortunately, we cannot use `.attrs (* qa)` because
    * `HPS` doesn't currently support expressions for `attrs`
    * PostgreSQL returns floating point numbers for the expression `qd`
    >>> qd = Q.right.left.date.finish.day - Q.right.left.date.start.month
    >>> qa = (Q.right.left, qd, Q.right.left.date.start.year)
    >>> for x in q.order_by (qd) :
    ...     print tuple (q (x) for q in qa)
    (SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), -4, 2008)
    (SRM.Regatta_Event (u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), 8, 2010)
    (SRM.Regatta_Event (u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), 16, 2009)

"""

_query_attr = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP  = scope.PAP
    >>> SRM  = scope.SRM
    >>> bc   = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b    = SRM.Boat.instance_or_new (u'Optimist', u"1107", "AUT", raw = True)
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

    >>> q = SRM.Regatta_C.query ()
    >>> for r in q.order_by (Q.event.date.start) : print r.year, r
    2008 ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))
    2009 ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', ))
    2010 ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', ))
    >>> for r in q.order_by (TFL.Sorted_By ("-event.date.start")) : print r.year, r
    2010 ((u'himmelfahrt', (u'2010/05/13', u'2010/05/13')), (u'optimist', ))
    2009 ((u'himmelfahrt', (u'2009/05/21', u'2009/05/21')), (u'optimist', ))
    2008 ((u'himmelfahrt', (u'2008/05/01', u'2008/05/01')), (u'optimist', ))


"""

if 0 :
    import warnings
    from sqlalchemy import exc as sa_exc
    warnings.filterwarnings \
        (action = "error", category = sa_exc.SAWarning)

from _GTW.__test__.model import *
from _MOM.import_MOM     import Q

__test__ = Scaffold.create_test_dict \
    ( dict
        ( composite       = _composite
        , link1_role      = _link1_role
        , link2_link1     = _link2_link1
        , query_attr      = _query_attr
        )
    )

### __END__ GTW.__test__.Query_Sorted_By

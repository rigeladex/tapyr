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
#    GTW.__test__.Q_Result
#
# Purpose
#    Tests for low level Q_Result functions.
#
# Revision Dates
#     1-Sep-2010 (MG) Creation
#     2-Sep-2010 (CT) Changed to test `HPS` backend, too
#     2-Sep-2010 (CT) Test for `set` of `Q.lifetime.finish` added
#     2-Sep-2010 (MG) More tests added
#    19-Jul-2011 (MG) New tests for `RAW` queries added
#    22-Jul-2011 (MG) Tests for `LOWER` added
#    26-Jul-2011 (CT) Tests (q1, q2, q3) for `attrs` combined with `count`
#                     and `all` added
#    16-Sep-2011 (MG) `attrs_query` test added
#    ««revision-date»»···
#--

from __future__ import unicode_literals

_q_result = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> DI  = lambda s : scope.MOM.Date_Interval (start = s, raw = True)
    >>> _   = PAP.Person  ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> _   = PAP.Person  ("LN 2", "FN 2", title = "Dr.")
    >>> p   = PAP.Person  ("LN 3", "FN 3", lifetime = DI ("2010/03/01"))
    >>> _   = PAP.Person  ("LN 4", "FN 4", title = "DI")
    >>> _   = PAP.Person  ("LN 5", "FN 5", title = "DI")
    >>> a   = PAP.Address ("S", "C", "Z", "C")
    >>> pha = PAP.Person_has_Address (p, a)

    >>> q   = PAP.Person.query ()
    >>> print q.count ()
    5
    >>> len (q.all ())
    5
    >>> print q.attr ("first_name").count ()
    5
    >>> sorted (q.attr ("first_name"))
    [u'fn 1', u'fn 2', u'fn 3', u'fn 4', u'fn 5']
    >>> print q.attrs (Q.first_name).count ()
    5
    >>> sorted (q.attrs (Q.first_name))
    [(u'fn 1',), (u'fn 2',), (u'fn 3',), (u'fn 4',), (u'fn 5',)]

    >>> sorted (q.attr (Q.lifetime.start).distinct (), key = lambda v : (v.__class__.__name__, v))
    [None, datetime.date(2010, 1, 1), datetime.date(2010, 3, 1)]
    >>> sorted (q.attrs (Q.first_name, Q.lifetime.start, "last_name"))
    [(u'fn 1', datetime.date(2010, 1, 1), u'ln 1'), (u'fn 2', None, u'ln 2'), (u'fn 3', datetime.date(2010, 3, 1), u'ln 3'), (u'fn 4', None, u'ln 4'), (u'fn 5', None, u'ln 5')]

    >>> p = PAP.Person.query (pid = 1).one ()
    >>> p.salutation
    u''
    >>> if hasattr (scope.ems.session, "expunge") : scope.ems.session.expunge ()
    >>> q = PAP.Person.query (pid = 1)
    >>> q.set (("salutation", "Mr"), )
    >>> p = PAP.Person.query (pid = 1).one ()
    >>> p.salutation
    u'Mr'
    >>> p.lifetime # 1
    MOM.Date_Interval (start = 2010/01/01)
    >>> q.set (("lifetime.finish", datetime.date(2010, 12, 31)), )
    >>> if hasattr (scope.ems.session, "expunge") : scope.ems.session.expunge ()
    >>> p = PAP.Person.query (pid = 1).one ()
    >>> p.lifetime # 2
    MOM.Date_Interval (finish = 2010/12/31, start = 2010/01/01)
    >>> first (PAP.Person.query (pid = 1).attrs (Q.lifetime.start, Q.lifetime.finish))
    (datetime.date(2010, 1, 1), datetime.date(2010, 12, 31))
    >>> first (PAP.Person.query (pid = 1).attr (Q.lifetime))
    MOM.Date_Interval (finish = 2010/12/31, start = 2010/01/01)
    >>> sorted (PAP.Person.query (pid = 1).attrs ("first_name", Q.lifetime))
    [(u'fn 1', MOM.Date_Interval (finish = 2010/12/31, start = 2010/01/01))]

    >>> sorted (PAP.Person_has_Address.query ().attr ("person"))
    [GTW.OMP.PAP.Person (u'ln 3', u'fn 3', u'', u'')]
    >>> sorted (PAP.Person_has_Address.query ().attrs ("person", "address"))
    [(GTW.OMP.PAP.Person (u'ln 3', u'fn 3', u'', u''), GTW.OMP.PAP.Address (u's', u'c', u'z', u'c'))]

    >>> PAP.Person.query_1 (Q.last_name.STARTSWITH ("ln"))
    (5, None)
    >>> PAP.Person.query_1 (Q.last_name.STARTSWITH ("ln 1"))
    (1, GTW.OMP.PAP.Person (u'ln 1', u'fn 1', u'', u''))
    >>> PAP.Person.query_1 (Q.last_name.STARTSWITH ("ln 42"))
    (0, None)

    >>> q0  = PAP.Person.query (Q.RAW.title.STARTSWITH ("D"))
    >>> q1  = q0.distinct ()
    >>> q1.count ()
    3

    >>> q9  = q0.attrs (Q.RAW.title)
    >>> sorted (q9.all ())
    [(u'DI',), (u'DI',), (u'Dr.',)]
    >>> q9.count ()
    3

    >>> q2  = q1.attrs (Q.RAW.title).order_by (Q.RAW.title)
    >>> q3  = q1.attrs (Q.RAW.title).order_by (Q.RAW.title)
    >>> sorted (q2.all ())
    [(u'DI',), (u'Dr.',)]
    >>> q2.count ()
    2
    >>> q3.count ()
    2
    >>> q2.all ()
    [(u'DI',), (u'Dr.',)]
    >>> q3.all ()
    [(u'DI',), (u'Dr.',)]

    >>> q4  = q2.distinct ()
    >>> q5  = q3.distinct ()
    >>> q4.all ()
    [(u'DI',), (u'Dr.',)]
    >>> q4.count ()
    2
    >>> q5.count ()
    2
    >>> q4.all ()
    [(u'DI',), (u'Dr.',)]
    >>> q5.all ()
    [(u'DI',), (u'Dr.',)]

    >>> q2.first ()
    (u'DI',)
    >>> q3.limit (1).all ()
    [(u'DI',)]

    >>> sorted (q0.all (), key = PAP.Person.sort_key)
    [GTW.OMP.PAP.Person (u'ln 2', u'fn 2', u'', u'dr.'), GTW.OMP.PAP.Person (u'ln 4', u'fn 4', u'', u'di'), GTW.OMP.PAP.Person (u'ln 5', u'fn 5', u'', u'di')]
    >>> print formatted (sorted (q0.attrs (Q.title, Q.SUM (1)).group_by (Q.title)))
    [
      ( 'di'
      , 2
      )
    ,
      ( 'dr.'
      , 1
      )
    ]

    >>> qy = PAP.Person.AQ.lifetime.start.AC ("2010")
    >>> qy
    Q.lifetime.start.between (datetime.date(2010, 1, 1), datetime.date(2010, 12, 31))
    >>> qm = PAP.Person.AQ.lifetime.start.AC ("2010/01")
    >>> qm
    Q.lifetime.start.between (datetime.date(2010, 1, 1), datetime.date(2010, 1, 31))

    >>> PAP.Person.query_s (qy).attrs (Q.last_name, Q.lifetime.start).all ()
    [(u'ln 1', datetime.date(2010, 1, 1)), (u'ln 3', datetime.date(2010, 3, 1))]
    >>> PAP.Person.query_s (qm).attrs (Q.last_name, Q.lifetime.start).all ()
    [(u'ln 1', datetime.date(2010, 1, 1))]

    >>> _   = PAP.Person  ("LN 1", "FN 2", title = "DI")
    >>> _   = PAP.Person  ("LN 4", "FN 1", title = "DI")
    >>> _   = PAP.Person  ("LN 4", "FN 2", title = "DI")
    >>> _   = PAP.Person  ("LN 5", "FN 2", title = "DI")

    >>> q = PAP.Person.query_s ()
    >>> qfn = PAP.Person.AQ.first_name
    >>> qln = PAP.Person.AQ.last_name

    >>> print q.count ()
    9
    >>> sorted (q.attrs ("first_name", "last_name"))
    [(u'fn 1', u'ln 1'), (u'fn 1', u'ln 4'), (u'fn 2', u'ln 1'), (u'fn 2', u'ln 2'), (u'fn 2', u'ln 4'), (u'fn 2', u'ln 5'), (u'fn 3', u'ln 3'), (u'fn 4', u'ln 4'), (u'fn 5', u'ln 5')]

    >>> sorted (q.filter (qfn.IN (["FN 1", "FN 5", "LN 3"])).attrs ("first_name", "last_name"))
    [(u'fn 1', u'ln 1'), (u'fn 1', u'ln 4'), (u'fn 5', u'ln 5')]

    >>> sorted (q.filter (qfn.IN (["FN 1", "FN 2"])).attrs ("first_name", "last_name"))
    [(u'fn 1', u'ln 1'), (u'fn 1', u'ln 4'), (u'fn 2', u'ln 1'), (u'fn 2', u'ln 2'), (u'fn 2', u'ln 4'), (u'fn 2', u'ln 5')]

    >>> sorted (q.filter (qln.IN (["LN 4", "LN 5"])).attrs ("first_name", "last_name"))
    [(u'fn 1', u'ln 4'), (u'fn 2', u'ln 4'), (u'fn 2', u'ln 5'), (u'fn 4', u'ln 4'), (u'fn 5', u'ln 5')]

    >>> scope.destroy ()
"""

_attrs_query = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> DI  = lambda s : scope.MOM.Date_Interval (start = s, raw = True)
    >>> _   = scope.PAP.Person  ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> _   = scope.PAP.Person  ("LN 2", "FN 2", lifetime = DI ("2010/01/10"), title = "Dr.")
    >>> p   = scope.PAP.Person  ("LN 3", "FN 3", lifetime = DI ("2010/01/03"))
    >>> _   = scope.PAP.Person  ("LN 4", "FN 4", lifetime = DI ("2010/01/16"), title = "DI")
    >>> _   = scope.PAP.Person  ("LN 5", "FN 5", lifetime = DI ("2010/02/01"), title = "DI")

    >>> q   = scope.PAP.Person.query ()
    >>> q.attr  ("last_name").order_by (Q.last_name).all ()
    [u'ln 1', u'ln 2', u'ln 3', u'ln 4', u'ln 5']
    >>> q.attr  ("lifetime.start").order_by (Q.lifetime.start).all ()
    [datetime.date(2010, 1, 1), datetime.date(2010, 1, 3), datetime.date(2010, 1, 10), datetime.date(2010, 1, 16), datetime.date(2010, 2, 1)]

    >>> q1  = q.attrs ("last_name", "first_name")
    >>> q1.order_by (Q.last_name).all ()
    [(u'ln 1', u'fn 1'), (u'ln 2', u'fn 2'), (u'ln 3', u'fn 3'), (u'ln 4', u'fn 4'), (u'ln 5', u'fn 5')]

    >>> q2  = q.attrs (Q.last_name, Q.lifetime.start)
    >>> q2.order_by (Q.lifetime.start).all ()
    [(u'ln 1', datetime.date(2010, 1, 1)), (u'ln 3', datetime.date(2010, 1, 3)), (u'ln 2', datetime.date(2010, 1, 10)), (u'ln 4', datetime.date(2010, 1, 16)), (u'ln 5', datetime.date(2010, 2, 1))]

    >>> scope.destroy ()
"""

_raw_query = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> DI  = lambda s : scope.MOM.Date_Interval (start = s, raw = True)
    >>> p   = scope.PAP.Person  ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> p   = scope.PAP.Person  ("LN 2", "FN 2")
    >>> p   = scope.PAP.Person  ("LN 3", "FN 3", lifetime = DI ("2010/01/03"))
    >>> p   = scope.PAP.Person  ("Lname 4", "Fn 3")
    >>> a   = scope.PAP.Address ("S", "C", "Z", "C")
    >>> pha = scope.PAP.Person_has_Address (p, a)


    >>> scope.PAP.Person.query (Q.RAW.last_cid == "1").all ()
    [GTW.OMP.PAP.Person (u'ln 1', u'fn 1', u'', u'')]
    >>> scope.PAP.Person.query (Q.RAW.pid == "1").all ()
    [GTW.OMP.PAP.Person (u'ln 1', u'fn 1', u'', u'')]
    >>> scope.PAP.Person.query (Q.RAW.last_name == "LN 1").all ()
    [GTW.OMP.PAP.Person (u'ln 1', u'fn 1', u'', u'')]
    >>> scope.PAP.Person.query (Q.RAW.lifetime.start == "2010/01/01").all ()
    [GTW.OMP.PAP.Person (u'ln 1', u'fn 1', u'', u'')]

    >>> scope.PAP.Person.query (Q.RAW.last_name.STARTSWITH ("LN")).order_by (Q.last_name).all ()
    [GTW.OMP.PAP.Person (u'ln 1', u'fn 1', u'', u''), GTW.OMP.PAP.Person (u'ln 2', u'fn 2', u'', u''), GTW.OMP.PAP.Person (u'ln 3', u'fn 3', u'', u'')]
    >>> scope.PAP.Person.query (Q.RAW.last_name.STARTSWITH ("Ln")).order_by (Q.last_name).all ()
    [GTW.OMP.PAP.Person (u'lname 4', u'fn 3', u'', u'')]

    >>> scope.destroy ()

"""

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q
from   _TFL.predicate      import first
from   _TFL.Formatter           import Formatter

formatted = Formatter (width = 240)

import datetime

__test__ = Scaffold.create_test_dict \
    ( dict
        ( q_result    = _q_result
        , raw_query   = _raw_query
        , attrs_query = _attrs_query
        )
    )

### __END__ GTW.__test__.Q_Result

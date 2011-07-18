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
#    ��revision-date�����
#--

from __future__ import unicode_literals

_q_result = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> DI  = lambda s : scope.MOM.Date_Interval (start = s, raw = True)
    >>> p   = scope.PAP.Person  ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> p   = scope.PAP.Person  ("LN 2", "FN 2")
    >>> p   = scope.PAP.Person  ("LN 3", "FN 3", lifetime = DI ("2010/01/03"))
    >>> a   = scope.PAP.Address ("S", "C", "Z", "C")
    >>> pha = scope.PAP.Person_has_Address (p, a)

    >>> q   = scope.PAP.Person.query ()
    >>> print q.count ()
    3
    >>> len (q.all ())
    3
    >>> print q.attr ("first_name").count ()
    3
    >>> sorted (q.attr ("first_name"))
    [u'fn 1', u'fn 2', u'fn 3']
    >>> print q.attrs (Q.first_name).count ()
    3
    >>> sorted (q.attrs (Q.first_name))
    [(u'fn 1',), (u'fn 2',), (u'fn 3',)]

    >>> sorted (q.attr (Q.lifetime.start), key = lambda v : (v.__class__.__name__, v))
    [None, datetime.date(2010, 1, 1), datetime.date(2010, 1, 3)]
    >>> sorted (q.attrs (Q.first_name, Q.lifetime.start, "last_name"))
    [(u'fn 1', datetime.date(2010, 1, 1), u'ln 1'), (u'fn 2', None, u'ln 2'), (u'fn 3', datetime.date(2010, 1, 3), u'ln 3')]

    >>> p = scope.PAP.Person.query (pid = 1).one ()
    >>> p.salutation
    u''
    >>> if hasattr (scope.ems.session, "expunge") : scope.ems.session.expunge ()
    >>> q = scope.PAP.Person.query (pid = 1)
    >>> q.set (("salutation", "Mr"), )
    >>> p = scope.PAP.Person.query (pid = 1).one ()
    >>> p.salutation
    u'Mr'
    >>> p.lifetime # 1
    MOM.Date_Interval (start = 2010/01/01)
    >>> q.set (("lifetime.finish", datetime.date(2010, 12, 31)), )
    >>> if hasattr (scope.ems.session, "expunge") : scope.ems.session.expunge ()
    >>> p = scope.PAP.Person.query (pid = 1).one ()
    >>> p.lifetime # 2
    MOM.Date_Interval (finish = 2010/12/31, start = 2010/01/01)
    >>> first (scope.PAP.Person.query (pid = 1).attrs (Q.lifetime.start, Q.lifetime.finish))
    (datetime.date(2010, 1, 1), datetime.date(2010, 12, 31))
    >>> first (scope.PAP.Person.query (pid = 1).attr (Q.lifetime))
    MOM.Date_Interval (finish = 2010/12/31, start = 2010/01/01)
    >>> sorted (scope.PAP.Person.query (pid = 1).attrs ("first_name", Q.lifetime))
    [(u'fn 1', MOM.Date_Interval (finish = 2010/12/31, start = 2010/01/01))]

    >>> sorted (scope.PAP.Person_has_Address.query ().attr ("person"))
    [GTW.OMP.PAP.Person (u'ln 3', u'fn 3', u'', u'')]
    >>> sorted (scope.PAP.Person_has_Address.query ().attrs ("person", "address"))
    [(GTW.OMP.PAP.Person (u'ln 3', u'fn 3', u'', u''), GTW.OMP.PAP.Address (u's', u'c', u'z', u'c'))]

    >>> scope.PAP.Person.query_1 (Q.last_name.STARTSWITH ("ln"))
    (3, None)
    >>> scope.PAP.Person.query_1 (Q.last_name.STARTSWITH ("ln 1"))
    (1, GTW.OMP.PAP.Person (u'ln 1', u'fn 1', u'', u''))
    >>> scope.PAP.Person.query_1 (Q.last_name.STARTSWITH ("ln 4"))
    (0, None)

"""

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q
from   _TFL.predicate      import first
import datetime

__test__ = Scaffold.create_test_dict (_q_result)

### __END__ GTW.__test__.Q_Result



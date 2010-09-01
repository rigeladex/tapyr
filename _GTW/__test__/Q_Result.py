# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
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
#    ««revision-date»»···
#--
from __future__ import unicode_literals

_q_result = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> DI  = lambda s : scope.MOM.Date_Interval (start = s, raw = True)
    >>> p   = scope.PAP.Person ("LN 1", "FN 1", lifetime = DI ("2010/01/01"))
    >>> p   = scope.PAP.Person ("LN 2", "FN 2")
    >>> p   = scope.PAP.Person ("LN 3", "FN 3", lifetime = DI ("2010/01/03"))
    >>> q   = scope.PAP.Person.query ()
    >>> q.count ()
    3
    >>> len (q.all ())
    3
    >>> list (q.attr ("first_name"))
    [u'fn 1', u'fn 2', u'fn 3']
    >>> list (q.attrs (Q.first_name))
    [(u'fn 1',), (u'fn 2',), (u'fn 3',)]

    >>> list (q.attr (Q.lifetime.start))
    [datetime.date(2010, 1, 1), None, datetime.date(2010, 1, 3)]
    >>> list (q.attrs (Q.first_name, Q.lifetime.start, "last_name"))
    [(u'fn 1', datetime.date(2010, 1, 1), u'ln 1'), (u'fn 2', None, u'ln 2'), (u'fn 3', datetime.date(2010, 1, 3), u'ln 3')]

    >>> p = scope.PAP.Person.query (pid = 1).one ()
    >>> p.salutation
    u''
    >>> scope.ems.session.expunge ()
    >>> q = scope.PAP.Person.query (pid = 1)
    >>> q.set (("salutation", "Mr"), )
    >>> p = scope.PAP.Person.query (pid = 1).one ()
    >>> p.salutation
    u'Mr'
"""

from   _GTW.__test__.model import *
from   _MOM.import_MOM     import Q

__test__ = Scaffold.create_test_dict \
    ( _q_result
    , ignore   = "HPS" ### this test cannot work an the HPS backend
    )

### __END__ GTW.__test__.Q_Result



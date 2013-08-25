# -*- coding: iso-8859-15 -*-
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
#    GTW.__test__.Rollback
#
# Purpose
#    Test scope rollback
#
# Revision Dates
#    20-Oct-2010 (MG) Creation
#     2-Jul-2012 (MG) Test fixed due to new handling of exceptions (no
#                     automatic rollback if a Name_Clash occurs)
#    30-Jul-2012 (CT) Replace obsolete comment by tests showing `count`,
#                     `query_s`, and length of `uncommitted_changes`
#    25-Aug-2013 (CT) Add `test_create_m`, fix style
#    ««revision-date»»···
#--

_test_attr = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> per = PAP.Person                   ("ln", "fn")
    >>> per.lifetime.start = "2010/01/01"
    >>> scope.commit                       ()

    >>> per
    PAP.Person (u'ln', u'fn', u'', u'')
    >>> per.lifetime
    MOM.Date_Interval (u'2010/01/01')

    >>> per.lifetime.finish = "2010/02/01"
    >>> per.lifetime
    MOM.Date_Interval (u'2010/01/01', u'2010/02/01')

    >>> scope.rollback ()

    >>> per.lifetime
    MOM.Date_Interval (u'2010/01/01')

"""

_test_create = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> per = PAP.Person ("ln", "fn")
    >>> scope.commit     () ### 1

    >>> p   = PAP.Person ("ln", "fn1")

    >>> PAP.Person.count ### 1
    2
    >>> PAP.Person.query (sort_key = "pid").all () ### 1
    [PAP.Person (u'ln', u'fn', u'', u''), PAP.Person (u'ln', u'fn1', u'', u'')]
    >>> len (scope.uncommitted_changes) ### 1
    1

    >>> per = PAP.Person ("ln", "fn")
    Traceback (most recent call last):
    ...
    Invariants: The attribute values for ('last_name', 'first_name', 'middle_name', 'title') must be unique for each object
      The new definition of Person PAP.Person (u'ln', u'fn', u'', u'') would clash with 1 existing entities
      Already existing:
        PAP.Person (u'ln', u'fn', u'', u'')

    >>> PAP.Person.count ### 2
    2
    >>> PAP.Person.query (sort_key = "pid").all () ### 2
    [PAP.Person (u'ln', u'fn', u'', u''), PAP.Person (u'ln', u'fn1', u'', u'')]
    >>> len (scope.uncommitted_changes) ### 2
    1

    >>> scope.rollback () ### 2

    >>> PAP.Person.count ### 3
    1
    >>> PAP.Person.query (sort_key = "pid").all () ### 3
    [PAP.Person (u'ln', u'fn', u'', u'')]
    >>> len (scope.uncommitted_changes) ### 3
    0

    >>> scope.rollback () ### 4

    >>> PAP.Person.query (first_name = "fn1").all ()
    []

    >>> PAP.Person.count ### 5
    1
    >>> PAP.Person.query (sort_key = "pid").all () ### 5
    [PAP.Person (u'ln', u'fn', u'', u'')]
    >>> len (scope.uncommitted_changes) ### 5
    0


"""

_test_create_m = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> p1 = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> e1 = PAP.Email  ("tanzer@swing.co.at")
    >>> _  = PAP.Person_has_Email (p1, e1)
    >>> scope.commit ()

    >>> scope.MOM.Id_Entity.query (sort_key = Q.pid).all () ### 1
    [PAP.Person (u'tanzer', u'christian', u'', u''), PAP.Email (u'tanzer@swing.co.at'), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> scope.rollback () ### 2

    >>> scope.MOM.Id_Entity.query (sort_key = Q.pid).all () ### 3
    [PAP.Person (u'tanzer', u'christian', u'', u''), PAP.Email (u'tanzer@swing.co.at'), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

    >>> p2 = PAP.Person ("Schlatterbeck", "Ralf", raw = True)
    >>> e2 = PAP.Email  ("rsc@runtux.com")
    >>> _  = PAP.Person_has_Email (p2, e2)

    >>> scope.MOM.Id_Entity.query (sort_key = Q.pid).all () ### 4
    [PAP.Person (u'tanzer', u'christian', u'', u''), PAP.Email (u'tanzer@swing.co.at'), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', )), PAP.Person (u'schlatterbeck', u'ralf', u'', u''), PAP.Email (u'rsc@runtux.com'), PAP.Person_has_Email ((u'schlatterbeck', u'ralf', u'', u''), (u'rsc@runtux.com', ))]

    >>> scope.rollback () ### 5

    >>> scope.MOM.Id_Entity.query (sort_key = Q.pid).all () ### 6
    [PAP.Person (u'tanzer', u'christian', u'', u''), PAP.Email (u'tanzer@swing.co.at'), PAP.Person_has_Email ((u'tanzer', u'christian', u'', u''), (u'tanzer@swing.co.at', ))]

"""

from   _GTW.__test__.model                      import *

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_attr       = _test_attr
        , test_create     = _test_create
        , test_create_m   = _test_create_m
        )
    )

### __END__ GTW.__test__.Rename

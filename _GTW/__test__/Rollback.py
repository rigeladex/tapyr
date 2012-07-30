# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
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
#    ««revision-date»»···
#--

simple = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> per = PAP.Person                   ("ln", "fn")
    >>> per.lifetime.start = datetime.date (2010, 1, 1)
    >>> scope.commit                       ()

    >>> per
    PAP.Person (u'ln', u'fn', u'', u'')
    >>> per.lifetime.finish = datetime.date (2010, 2, 1)
    >>> scope.rollback ()
    >>> scope.destroy  ()
"""

create = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> per = PAP.Person                   ("ln", "fn")
    >>> scope.commit                       ()
    >>> p   = PAP.Person                   ("ln", "fn1")

    >>> PAP.Person.count
    2
    >>> PAP.Person.query_s ().all ()
    [PAP.Person (u'ln', u'fn', u'', u''), PAP.Person (u'ln', u'fn1', u'', u'')]
    >>> len (scope.uncommitted_changes)
    1

    >>> per = PAP.Person                   ("ln", "fn")
    Traceback (most recent call last):
    ...
    Name_Clash: new definition of Person (u'ln', u'fn', u'', u'') clashes with existing Person (u'ln', u'fn', u'', u'')

    >>> PAP.Person.count
    2
    >>> PAP.Person.query_s ().all ()
    [PAP.Person (u'ln', u'fn', u'', u''), PAP.Person (u'ln', u'fn1', u'', u'')]
    >>> len (scope.uncommitted_changes)
    1

    >>> scope.commit                       ()

    >>> PAP.Person.count
    2
    >>> PAP.Person.query_s ().all ()
    [PAP.Person (u'ln', u'fn', u'', u''), PAP.Person (u'ln', u'fn1', u'', u'')]
    >>> len (scope.uncommitted_changes)
    0

    >>> scope.destroy  ()

"""
from   _GTW.__test__.model                      import *
import  datetime

__test__ = Scaffold.create_test_dict \
    ( dict ( simple = simple
           , create = create
           )
    )
if __name__ == "__main__" :
    scope = Scaffold.scope ('postgresql://regtest:regtest@localhost/regtest', None)
    PAP = scope.PAP
    per = PAP.Person                   ("ln", "fn")
    scope.commit                       ()
    p   = PAP.Person                   ("ln", "fn1")
    per = PAP.Person                   ("ln", "fn")
### __END__ GTW.__test__.Rename

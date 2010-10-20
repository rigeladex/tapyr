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
#    GTW.__test__.Rollback
#
# Purpose
#    Test scope rollback
#
# Revision Dates
#    20-Oct-2010 (MG) Creation
#    ««revision-date»»···
#--

test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> PAP = scope.PAP
    >>> per = PAP.Person                   ("ln", "fn")
    >>> per.lifetime.start = datetime.date (2010, 1, 1)
    >>> scope.commit                       ()

    >>> per.lifetime.finish = datetime.date (2010, 2, 1)
    >>> scope.rollback ()
"""

from   _GTW.__test__.model                      import *
import  datetime

__test__ = Scaffold.create_test_dict (test_code)

### __END__ GTW.__test__.Rename

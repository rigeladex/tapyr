# -*- coding: iso-8859-15 -*-
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
#    GTW.__test__.PID_Manager
#
# Purpose
#    Testing of the pid manager
#
# Revision Dates
#    12-May-2010 (MG) Creation
#    ««revision-date»»···
#--

from _GTW.__test__.model import *

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> bc = SRM.Boat_Class ("Optimist", max_crew = 2)
    >>> b1 = SRM.Boat       (bc, "Austria", 1)
    >>> int (bc.pid), int (b1.pid)
    (1, 2)
    >>> scope.ems.pm.reserve (None, 100)
    100
    >>> b2 = SRM.Boat       (bc, "Austria", 2)
    >>> int (b2.pid)
    101
    >>> b3 = SRM.Boat       (bc, "Austria", 2) # doctest:+ELLIPSIS
    Traceback (most recent call last):
        ...
    Duplicate_Link: <class 'GTW.OMP.SRM.Boat' [...]>, ((u'Optimist', ), u'AUT', 2)
    >>> b3 = SRM.Boat       (bc, "Austria", 3)
    >>> int (b3.pid)
    102
"""

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.PID_Manager

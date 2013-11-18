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
#    GTW.__test__.PID_Manager
#
# Purpose
#    Testing of the pid manager
#
# Revision Dates
#    12-May-2010 (MG) Creation
#    19-Mar-2012 (CT) Adapt to `Boat_Class.name.ignore_case` now being `True`
#    ««revision-date»»···
#--

from _GTW.__test__.model import *

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> bc = SRM.Boat_Class ("Optimist", max_crew = 2)
    >>> b1 = SRM.Boat       (bc, 1, "AUT")
    >>> int (bc.pid), int (b1.pid)
    (1, 2)
    >>> scope.ems.pm.reserve (None, 100)
    100
    >>> b2 = SRM.Boat       (bc, 2, "AUT")
    >>> int (b2.pid)
    101
    >>> b3 = SRM.Boat       (bc, 2, "AUT") # doctest:+ELLIPSIS
    Traceback (most recent call last):
        ...
    Invariants: The attribute values for ('left', 'sail_number', 'nation', 'sail_number_x') must be unique for each object
      The new definition of Boat SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'2', u'AUT', u'') would clash with 1 existing entities
      Already existing:
        SRM.Boat ((u'Optimist', 'SRM.Boat_Class'), u'2', u'AUT', u'')
    >>> b3 = SRM.Boat       (bc, 3, "AUT")
    >>> b3.pid > b2.pid
    True

"""

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.PID_Manager

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    GTW.__test__.Boat
#
# Purpose
#    Test SRM.Boat creation and querying
#
# Revision Dates
#    27-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%s, %s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> SRM.Boat_Class ("Optimist", max_crew = 1)
    GTW.OMP.SRM.Boat_Class (u'Optimist')
    >>> print scope.SRM.Boat_Class.count
    1
    >>> scope.SRM.Boat_Class.query (name = u'Optimist').all ()
    [GTW.OMP.SRM.Boat_Class (u'Optimist')]
    >>> scope.SRM.Boat_Class.instance (u'Optimist')
    GTW.OMP.SRM.Boat_Class (u'Optimist')
    >>> SRM.Boat.instance_or_new (u'Optimist', "AUT", "1107", raw = True) ### 1
    GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107)
    >>> print scope.SRM.Boat.count
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107)]
    >>> scope.commit ()

    >>> SRM.Boat.instance_or_new (u'Optimist', "AUT", "1107", raw = True) ### 2
    GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107)
    >>> print scope.SRM.Boat.count
    1
    >>> scope.SRM.Boat.query_s ().all ()
    [GTW.OMP.SRM.Boat ((u'Optimist', ), u'AUT', 1107)]

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Boat

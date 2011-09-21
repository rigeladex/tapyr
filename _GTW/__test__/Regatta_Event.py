# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Regatta_Event
#
# Purpose
#    Test Regatta_Event creation and querying
#
# Revision Dates
#    30-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", dict (start = "20080501", raw = True), raw = True)
    >>> rev.epk_raw
    (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'GTW.OMP.SRM.Regatta_Event')
    >>> SRM.Regatta_Event.instance (* rev.epk_raw, raw = True)
    GTW.OMP.SRM.Regatta_Event (u'Himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01'))
    >>> SRM.Regatta_Event.instance (* rev.epk)
    GTW.OMP.SRM.Regatta_Event (u'Himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01'))

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Regatta_Event

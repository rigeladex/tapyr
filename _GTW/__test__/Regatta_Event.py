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
    >>> scope = Scaffold.scope (%s, %s) # doctest:+ELLIPSIS
    Creating new scope MOMT__... in memory
    >>> SRM = scope.SRM
    >>> rev = SRM.Regatta_Event (dict (start = "20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> rev.epk_raw
    ((('finish', '2008/05/01'), ('start', '2008/05/01')), u'Himmelfahrt', 'GTW.OMP.SRM.Regatta_Event')
    >>> SRM.Regatta_Event.instance (* rev.epk_raw, raw = True)
    GTW.OMP.SRM.Regatta_Event (dict (start = '2008/05/01', finish = '2008/05/01'), u'Himmelfahrt')
    >>> SRM.Regatta_Event.instance (* rev.epk)
    GTW.OMP.SRM.Regatta_Event (dict (start = '2008/05/01', finish = '2008/05/01'), u'Himmelfahrt')

"""

from _GTW.__test__.model import *

__test__ = dict \
    ( HPS = _test_code % (None, None)
    , SQ  = _test_code % ("'sqlite://'", None)
    )

### __END__ GTW.__test__.Regatta_Event

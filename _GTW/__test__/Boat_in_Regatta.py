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
#    GTW.__test__.Boat_in_Regatta
#
# Purpose
#    Test creation and querying of Boat_in_Regatta
#
# Revision Dates
#     3-May-2010 (MG) Creation
#     3-May-2010 (CT) Creation continued
#    ««revision-date»»···
#--

_test_code = r"""
    >>> scope = Scaffold.scope (%s, %s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', "AUT", "1107", raw = True)
    >>> p   = PAP.Person.instance_or_new ("Tanzer", "Christian")
    >>> s   = SRM.Sailor.instance_or_new (p.epk_raw, nation = "AUT", mna_number = "29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (dict (start = "20080501", raw = True), u"Himmelfahrt", raw = True)
    >>> reg = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> reh = SRM.Regatta_H (rev.epk_raw, handicap = "Yardstick",  raw = True)
    >>> list (r.name for r in sorted (rev.regattas))
    [u'Optimist', u'Yardstick']

    >>> reg.set_raw (result = dict (date = "26.5.2009 10:20", software = u"calculated with REGATTA.yellow8.com", status = "final", raw = True))
    1
    >>> reg.FO.result
    u'2009/05/26 10:20:00, calculated with REGATTA.yellow8.com, final'
    >>> scope.commit ()

    >>> SRM.Regatta_C.instance (* reg.epk)
    GTW.OMP.SRM.Regatta_C ((dict (start = '2008/05/01', finish = '2008/05/01'), u'Himmelfahrt'), (u'Optimist', ))
    >>> SRM.Regatta.instance (* reg.epk)
    GTW.OMP.SRM.Regatta_C ((dict (start = '2008/05/01', finish = '2008/05/01'), u'Himmelfahrt'), (u'Optimist', ))
    >>> SRM.Regatta_C.instance (* reg.epk_raw, raw = True)
    GTW.OMP.SRM.Regatta_C ((dict (start = '2008/05/01', finish = '2008/05/01'), u'Himmelfahrt'), (u'Optimist', ))

    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)
"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Boat_in_Regatta

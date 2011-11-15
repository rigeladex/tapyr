# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
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
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP
    >>> SRM = scope.SRM
    >>> bc  = SRM.Boat_Class ("Optimist", max_crew = 1)
    >>> b   = SRM.Boat.instance_or_new (u'Optimist', u"AUT", u"1107", raw = True)
    >>> p   = PAP.Person.instance_or_new (u"Tanzer", u"Christian")
    >>> s   = SRM.Sailor.instance_or_new (p.epk_raw, nation = u"AUT", mna_number = u"29676", raw = True) ### 1
    >>> rev = SRM.Regatta_Event (u"Himmelfahrt", dict (start = u"20080501", raw = True), raw = True)
    >>> reg = SRM.Regatta_C (rev.epk_raw, boat_class = bc.epk_raw, raw = True)
    >>> reh = SRM.Regatta_H (rev.epk_raw, handicap = u"Yardstick",  raw = True)
    >>> list (r.name for r in sorted (rev.regattas))
    [u'Optimist', u'Yardstick']

    >>> reg.set_raw (result = dict (date = "26.5.2009 10:20", software = u"calculated with REGATTA.yellow8.com", status = "final", raw = True))
    1
    >>> unicode (reg.FO.result)
    u'2009/05/26 10:20:00, calculated with REGATTA.yellow8.com, final'
    >>> scope.commit ()

    >>> rev.epk_raw
    (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'GTW.OMP.SRM.Regatta_Event')
    >>> reg.epk_raw
    ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C')
    >>> SRM.Regatta_C.instance (* reg.epk)
    GTW.OMP.SRM.Regatta_C ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', ))
    >>> SRM.Regatta.instance (* reg.epk)
    GTW.OMP.SRM.Regatta_C ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', ))
    >>> SRM.Regatta_C.instance (* reg.epk_raw, raw = True)
    GTW.OMP.SRM.Regatta_C ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', ))

    >>> bir = SRM.Boat_in_Regatta (b.epk_raw, reg.epk_raw, skipper = s.epk_raw, raw = True)
    >>> bir.epk_raw
    (((u'Optimist', 'GTW.OMP.SRM.Boat_Class'), u'AUT', u'1107', 'GTW.OMP.SRM.Boat'), ((u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'GTW.OMP.SRM.Regatta_Event'), (u'Optimist', 'GTW.OMP.SRM.Boat_Class'), 'GTW.OMP.SRM.Regatta_C'), 'GTW.OMP.SRM.Boat_in_Regatta')
    >>> SRM.Boat_in_Regatta.instance (* bir.epk_raw, raw = True)
    GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', ), u'AUT', u'1107'), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', )))

    >>> BiR = SRM.Boat_in_Regatta
    >>> sort_key = TFL.Sorted_By ("-regatta.event.date.start", "skipper.person.last_name", "skipper.person.first_name")

    >>> print sort_key
    <Sorted_By: Descending-Getter function for `.regatta.event.date.start`, Getter function for `.skipper.person.last_name`, Getter function for `.skipper.person.first_name`>
    >>> print BiR.E_Type.sort_key_pm (sort_key)
    <Sorted_By: Getter function for `.relevant_root.type_name`, <Sorted_By: Descending-Getter function for `.regatta.event.date.start`, Getter function for `.skipper.person.last_name`, Getter function for `.skipper.person.first_name`>>

    >>> list (BiR.query (sort_key = sort_key))
    [GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', ), u'AUT', u'1107'), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', )))]
    >>> list (BiR.query_s (sort_key = sort_key))
    [GTW.OMP.SRM.Boat_in_Regatta (((u'Optimist', ), u'AUT', u'1107'), ((u'himmelfahrt', dict (start = u'2008/05/01', finish = u'2008/05/01')), (u'Optimist', )))]

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Boat_in_Regatta

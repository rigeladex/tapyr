# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
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
#    14-Nov-2011 (CT) Add tests for `query` and `query_s` with `sort_key`
#    12-Oct-2012 (CT) Adapt to repr change of `An_Entity`
#    29-Jul-2013 (CT) Add tests for `set` of `name`
#    ««revision-date»»···
#--

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SRM = scope.SRM
    >>> RE  = SRM.Regatta_Event
    >>> rev = RE (u"Himmelfahrt", ("20080501", ), raw = True)
    >>> rev.epk_raw
    (u'Himmelfahrt', (('finish', u'2008/05/01'), ('start', u'2008/05/01')), 'SRM.Regatta_Event')
    >>> RE.instance (* rev.epk_raw, raw = True)
    SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))
    >>> RE.instance (* rev.epk)
    SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))

    >>> sort_key = TFL.Sorted_By ("-date.start", "name")

    >>> print sort_key
    <Sorted_By: Descending-Getter function for `.date.start`, Getter function for `.name`>
    >>> print RE.E_Type.sort_key_pm (sort_key)
    <Sorted_By: Getter function for `.relevant_root.type_name`, <Sorted_By: Descending-Getter function for `.date.start`, Getter function for `.name`>>

    >>> list (RE.query (sort_key = sort_key))
    [SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))]
    >>> list (RE.query_s (sort_key = sort_key))
    [SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))]

    >>> scope.commit ()

    >>> rev.set (name = "himmelfahrt")
    0

    >>> rev.set_raw (name = "Himmelfahrt")
    0

    >>> rev.set (name = "Himmelfahrt")
    1

    >>> RE.query ().all ()
    [SRM.Regatta_Event (u'himmelfahrt', (u'2008/05/01', u'2008/05/01'))]

    >>> for x in RE.query () :
    ...     print x.ui_display
    Himmelfahrt 2008/05/01

    >>> rev.set_raw (name = "Himmelfahrtskommando")
    1

    >>> RE.query ().all ()
    [SRM.Regatta_Event (u'himmelfahrtskommando', (u'2008/05/01', u'2008/05/01'))]

"""

from _GTW.__test__.model import *

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Regatta_Event

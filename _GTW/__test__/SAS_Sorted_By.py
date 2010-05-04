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
#    GTW.__test__.SAS_Sorted_By
#
# Purpose
#    Test the SAS function for sorting by attributes of a composite using the
#    SAS backend.
#
# Revision Dates
#    30-Apr-2010 (MG) Creation
#    ««revision-date»»···
#--

_composite = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> e1 = EVT.Event \
    ...     (p1.epk_raw, dict (start = "1.2.2010", raw = True), raw = True)
    >>> e2 = EVT.Event \
    ...     (p2.epk_raw, dict (start = "1.1.2010", raw = True), raw = True)
    >>> for e in EVT.Event.query ().all () : print e
    ((u'event-1-text', ), dict (start = '2010/02/01'), dict ())
    ((u'event-2-text', ), dict (start = '2010/01/01'), dict ())
    >>> q = EVT.Event.query ().order_by (TFL.Sorted_By (Q.date.start))
    >>> for e in q.all () : print e
    ((u'event-2-text', ), dict (start = '2010/01/01'), dict ())
    ((u'event-1-text', ), dict (start = '2010/02/01'), dict ())
"""

_link1_role = r"""
    >>> scope = Scaffold.scope ("sqlite://")
    Creating new scope MOMT__SAS__SAS in memory
    >>> EVT = scope.EVT
    >>> SWP = scope.SWP
    >>> p1 = SWP.Page ("event-1-text", text = "Text for the 1. event")
    >>> p2 = SWP.Page ("event-2-text", text = "Text for the 2. event")
    >>> e1 = EVT.Event \
    ...     (p1.epk_raw, dict (start = "1.2.2010", raw = True), raw = True)
    >>> e2 = EVT.Event \
    ...     (p2.epk_raw, dict (start = "1.1.2010", raw = True), raw = True)
    >>> q = EVT.Event_occurs.query ()
    >>> for e in q.all () : print e ### default sort order
    (((u'event-1-text', ), dict (start = '2010/02/01'), dict ()), '2010/02/01', dict ())
    (((u'event-2-text', ), dict (start = '2010/01/01'), dict ()), '2010/01/01', dict ())
    >>> q = EVT.Event_occurs.query ().order_by (TFL.Sorted_By (Q.event.date.start))
    >>> for e in q.all () : print e ### sorted
    (((u'event-2-text', ), dict (start = '2010/01/01'), dict ()), '2010/01/01', dict ())
    (((u'event-1-text', ), dict (start = '2010/02/01'), dict ()), '2010/02/01', dict ())
"""

if 1 :
    __test__ = dict \
        ( composite  = _composite
        , link1_role = _link1_role
        )
else :
    #__doc__ = _composite
    __doc__ = _link1_role

from _GTW.__test__.model import *
from _MOM.import_MOM     import Q
### __END__ GTW.__test__.SAS_Sorted_By



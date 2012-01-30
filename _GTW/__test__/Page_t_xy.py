# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.__test__.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.__test__.Page_t_xy
#
# Purpose
#    Test Page subtypes.
#
# Revision Dates
#    30-Jan-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

_test_code = r"""
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> SWP = scope.SWP
    >>> TST = scope.TST

    >>> TST.Page_X ("foo", text = "X")
    TST.Page_X (u'foo')
    >>> TST.Page_X.query_s (perma_name = "foo").all ()
    [TST.Page_X (u'foo')]
    >>> TST.Page_Y.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [TST.Page_X (u'foo')]

    >>> TST.Page_Y ("foo", text = "Y")
    Traceback (most recent call last):
      ...
    Name_Clash: new definition of TST.Page_Y (u'foo') clashes with existing TST.Page_X (u'foo')
    >>> TST.Page_X.query_s (perma_name = "foo").all ()
    [TST.Page_X (u'foo')]
    >>> TST.Page_Y.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [TST.Page_X (u'foo')]

    >>> TST.Page_Y ("bar", text = "Y")
    TST.Page_Y (u'bar')
    >>> TST.Page_X.query_s ().all ()
    [TST.Page_X (u'foo')]
    >>> TST.Page_Y.query_s ().all ()
    [TST.Page_Y (u'bar')]
    >>> SWP.Page.query_s ().all ()
    [TST.Page_Y (u'bar'), TST.Page_X (u'foo')]

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *
from   _TFL.Package_Namespace   import Package_Namespace

TST = Package_Namespace ("_TST")

_Ancestor_Essence = GTW.OMP.SWP.Page

class _TST_Entity_ (MOM.Entity) :

    _real_name = "Entity"
    PNS        = TST
    is_partial = True

Entity = _TST_Entity_ # end class

class _TST_Object_ (Entity, MOM.Object) :

    _real_name  = "Object"
    is_partial  = True

Object = _TST_Object_ # end class

class _TST_Page_ (Object, _Ancestor_Essence) :

    _real_name = "Page"

Page = _TST_Page_ # end class

_Ancestor_Essence = Page

class Page_X (_Ancestor_Essence) :
    """Page of type X"""

    ui_name = "Page X"

# end class Page_X

class Page_Y (_Ancestor_Essence) :
    """Page of type Y"""

    ui_name = "Page Y"

# end class Page_Y

__test__ = Scaffold.create_test_dict \
    ( dict
        ( normal  = _test_code
        )
    )

### __END__ GTW.__test__.Page_t_xy

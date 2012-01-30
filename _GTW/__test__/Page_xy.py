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
#    GTW.__test__.Page_xy
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

    >>> SWP.Page_X ("foo", text = "X")
    GTW.OMP.SWP.Page_X (u'foo')
    >>> SWP.Page_X.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_X (u'foo')]
    >>> SWP.Page_Y.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_X (u'foo')]

    >>> SWP.Page_Y ("foo", text = "Y")
    Traceback (most recent call last):
      ...
    Name_Clash: new definition of GTW.OMP.SWP.Page_Y (u'foo') clashes with existing GTW.OMP.SWP.Page_X (u'foo')
    >>> SWP.Page_X.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_X (u'foo')]
    >>> SWP.Page_Y.query_s (perma_name = "foo").all ()
    []
    >>> SWP.Page.query_s (perma_name = "foo").all ()
    [GTW.OMP.SWP.Page_X (u'foo')]

    >>> SWP.Page_Y ("bar", text = "Y")
    GTW.OMP.SWP.Page_Y (u'bar')
    >>> SWP.Page_X.query_s ().all ()
    [GTW.OMP.SWP.Page_X (u'foo')]
    >>> SWP.Page_Y.query_s ().all ()
    [GTW.OMP.SWP.Page_Y (u'bar')]
    >>> SWP.Page.query_s ().all ()
    [GTW.OMP.SWP.Page_Y (u'bar'), GTW.OMP.SWP.Page_X (u'foo')]

    >>> scope.destroy ()

"""

from _GTW.__test__.model import *

_Ancestor_Essence = GTW.OMP.SWP.Page

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

### __END__ GTW.__test__.Page_xy

# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.__test__.Attr_polisher
#
# Purpose
#    Test attribute polishers
#
# Revision Dates
#    25-Sep-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW.__test__.model      import *
from   _MOM.import_MOM          import Q

_test_person = """

    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> p0 = PAP.Person ("tanzer", "christian", raw = True)
    >>> print (p0.ui_display)
    Tanzer Christian

    >>> p0.destroy ()

    >>> p1 = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> print (p1.ui_display)
    Tanzer Christian

    >>> p1.destroy ()

    >>> p2 = PAP.Person ("TANZER", "CHRISTIAN", raw = True)
    >>> print (p2.ui_display)
    Tanzer Christian

    >>> p2.destroy ()

    >>> p3 = PAP.Person ("tanZer", "ChRiStIaN", raw = True)
    >>> print (p3.ui_display)
    tanZer ChRiStIaN

    >>> p3.destroy ()

"""

_test_phone = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> PAP = scope.PAP

    >>> p0  = PAP.Phone (number = "+43 123 4567890", raw = True)
    >>> print (p0.ui_display)
    43/123/4567890

    >>> p1  = PAP.Phone ("43", "1", "234567", raw = True)

    >>> print (p1.ui_display)
    43/1/234567

    >>> _   = p1.set_raw (number = "+44 9 234568")

    >>> print (p1.ui_display)
    44/9/234568

"""

__test__ = Scaffold.create_test_dict \
    ( dict
        ( test_person         = _test_person
        , test_phone          = _test_phone
        )
    )

### __END__ GTW.__test__.Attr_polisher

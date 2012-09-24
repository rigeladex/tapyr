# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
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
#    GTW.__test__.Attr_DNS
#
# Purpose
#    Test GTW.OMP.DNS subclasses and links
#
# Revision Dates
#    06-Sep-2012 (RS) Creation
#    23-Sep-2012 (RS) Add `raw = True` to records
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...
    >>> DNS = scope.GTW.OMP.DNS
    >>> print (DNS.Zone.count_strict, DNS.Record.count)
    0 0

    >>> z = DNS.Zone (name = 'example.com')
    >>> dnsa1 = DNS.A_Record \\
    ...     ( left    = z
    ...     , name    = "test.example.com"
    ...     , address = dict (address = "1.2.3.4")
    ...     , raw     = True
    ...     )
    >>> dnsa1b = DNS.A_Record \\
    ...     ( left    = z
    ...     , name    = "test.example.com"
    ...     , address = dict (address = "1.2.3.5")
    ...     , raw     = True
    ...     )
    >>> dnsa2 = DNS.A_Record \\
    ...     ( left    = z
    ...     , name    = "test2.example.com"
    ...     , address = dict (address = "2.3.4.5")
    ...     , raw     = True
    ...     )
    >>> cn1 = DNS.CNAME_Record \\
    ...     ( left    = z
    ...     , name    = "test3.example.com"
    ...     , target  = "test2.example.com"
    ...     , raw     = True
    ...     )
"""

from   _GTW.__test__.model       import *
from   _MOM.import_MOM           import Q
import _GTW._OMP._DNS.import_DNS
import _GTW._OMP._DNS.Nav

__test__ = Scaffold.create_test_dict (_test_code)

### __END__ GTW.__test__.Subjects

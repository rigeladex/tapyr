# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.DNS.
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
#    GTW.OMP.DNS.Entity
#
# Purpose
#    Common base class for essential classes of DNS
#
# Revision Dates
#     6-Sep-2012 (RS) Creation
#    12-Sep-2012 (RS) Use `derive_pns_bases`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                   import GTW
from   _MOM.import_MOM        import *

import _MOM.derive_pns_bases

import _GTW._OMP._DNS

MOM.derive_pns_bases (GTW.OMP.DNS, MOM)

if __name__ != "__main__" :
    GTW.OMP.DNS._Export ("*")
### __END__ GTW.OMP.DNS.Entity

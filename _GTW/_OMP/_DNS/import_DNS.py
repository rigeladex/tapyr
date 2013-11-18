# -*- coding: utf-8 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
# ****************************************************************************
# This module is part of the package GTW.OMP.DNS.
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
#    GTW.OMP.DNS.import_DNS
#
# Purpose
#    Import DNS object model
#
# Revision Dates
#    06-Sep-2012 (RS) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._DNS         import DNS

import _GTW._OMP._DNS.AAAA_Record
import _GTW._OMP._DNS.A_Record
import _GTW._OMP._DNS.CNAME_Record
import _GTW._OMP._DNS.MX_Record
import _GTW._OMP._DNS.NS_Record
import _GTW._OMP._DNS.Secondary_IP4
import _GTW._OMP._DNS.Secondary_IP6
import _GTW._OMP._DNS.SRV_Record
import _GTW._OMP._DNS.TXT_Record
import _GTW._OMP._DNS.Zone

### __END__ GTW.OMP.DNS.import_DNS

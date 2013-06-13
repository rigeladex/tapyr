# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Entity
#
# Purpose
#    Common base classes for essential classes of GTW.OMP.SRM
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    13-Jun-2013 (CT) Pass `pns_alias` to `MOM.derive_pns_bases`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
import _MOM.derive_pns_bases

import _GTW._OMP._PAP.Person
import _GTW._OMP._SRM

MOM.derive_pns_bases (GTW.OMP.SRM, MOM, pns_alias = "SRM")

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Entity

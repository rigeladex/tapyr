# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.Entity
#
# Purpose
#    Common base class for essential classes of GTW.OMP.PAP
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#     3-Feb-2010 (MG) `is_partial` added
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

import _GTW._OMP._PAP

class _PAP_Entity_ (MOM.Entity) :
    """Common base class for essential classes of GTW.OMP.PAP"""

    _real_name = "Entity"
    is_partial = True
    PNS        = GTW.OMP.PAP

Entity = _PAP_Entity_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Entity

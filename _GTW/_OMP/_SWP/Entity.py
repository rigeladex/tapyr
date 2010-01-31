# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SWP.
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
#    GTW.OMP.SWP.Entity
#
# Purpose
#    Common base class for essential classes of GTW.OMP.SWP
#
# Revision Dates
#    31-Jan-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

import _GTW._OMP._SWP

class _SWP_Entity_ (MOM.Entity) :
    """Common base class for essential classes of GTW.OMP.SWP"""

    _real_name = "Entity"

    PNS        = GTW.OMP.SWP

Entity = _SWP_Entity_ # end class

class _SWP_Object_ (Entity, MOM.Object) :
    """Common base class for essential objects of GTW.OMP.SWP"""

    _real_name  = "Object"

# end class _SWP_Object_

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Entity

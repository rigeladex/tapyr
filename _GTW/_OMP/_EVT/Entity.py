# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.EVT.
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
#    GTW.OMP.EVT.Entity
#
# Purpose
#    Common base class for essential classes of GTW.OMP.EVT
#
# Revision Dates
#    10-Mar-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

import _GTW._OMP._EVT

class _EVT_Entity_ (MOM.Entity) :
    """Common base class for essential classes of GTW.OMP.EVT"""

    _real_name = "Entity"

    PNS        = GTW.OMP.EVT
    is_partial = True

Entity = _EVT_Entity_ # end class

class _EVT_Object_ (Entity, MOM.Object) :
    """Common base class for essential objects of GTW.OMP.EVT"""

    _real_name  = "Object"

    is_partial  = True

Object = _EVT_Object_ # end class

class _EVT_Link1_ (Entity, MOM.Link1) :
    """Common base class for essential unary links of GTW.OMP.EVT"""

    _real_name  = "Link1"

    is_partial  = True

Link1 = _EVT_Link1_ # end class

class _EVT_Link2_ (Entity, MOM.Link2) :
    """Common base class for essential binary links of GTW.OMP.EVT"""

    _real_name  = "Link2"

    is_partial  = True

Link2 = _EVT_Link2_ # end class

if __name__ != "__main__" :
    GTW.OMP.EVT._Export ("*")
### __END__ GTW.OMP.EVT.Entity

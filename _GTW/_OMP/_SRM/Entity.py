# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._PAP.Person
import _GTW._OMP._SRM

class _SRM_Entity_ (MOM.Entity) :
    """Common base class for essential classes of GTW.OMP.SRM"""

    _real_name = "Entity"

    PNS        = GTW.OMP.SRM
    is_partial = True

Entity = _SRM_Entity_ # end class

class _SRM_Link1_ (Entity, MOM.Link1) :
    """Common base class for essential unary links of GTW.OMP.SRM"""

    _real_name  = "Link1"

    is_partial  = True

Link1 = _SRM_Link1_ # end class

class _SRM_Link2_ (Entity, MOM.Link2) :
    """Common base class for essential binary links of GTW.OMP.SRM"""

    _real_name  = "Link2"

    is_partial  = True

Link2 = _SRM_Link2_ # end class

class _SRM_Object_ (Entity, MOM.Object) :
    """Common base class for essential objects of GTW.OMP.SRM"""

    _real_name  = "Object"

    is_partial  = True

Object = _SRM_Object_ # end class

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Entity

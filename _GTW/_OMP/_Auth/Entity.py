# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.Auth.Entity
#
# Purpose
#    Common base class for essential classes of GTW.OMP.Auth
#
# Revision Dates
#    13-Jan-2010 (MG) Creation
#    16-Jan-2010 (CT) `Object` added
#     3-Feb-2010 (MG) `is_partial` added
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

import _GTW._OMP._Auth

class _Auth_Entity_ (MOM.Entity) :
    """Common base class for essential classes of GTW.OMP.Auth"""

    _real_name = "Entity"

    is_partial = True
    PNS        = GTW.OMP.Auth

Entity = _Auth_Entity_ # end class

class _Auth_Object_ (Entity, MOM.Named_Object) :
    """Common base class for essential objects of GTW.OMP.Auth"""

    is_partial = True
    _real_name = "Object"

    class _Attributes (MOM.Named_Object._Attributes) :
        pass
    # end class _Attributes

Object = _Auth_Object_ # end class

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Entity

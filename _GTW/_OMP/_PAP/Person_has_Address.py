# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Person_has_Address
#
# Purpose
#    Model the link between a person and an address
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#     3-Feb-2010 (CT) `_Person_has_Property_` factored
#    19-Feb-2010 (MG) `left.auto_cache` added
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Entity
from   _GTW._OMP._PAP._Person_has_Property_  import _Person_has_Property_
from   _GTW._OMP._PAP.Address                import Address

_Ancestor_Essence = _Person_has_Property_

class Person_has_Address (_Ancestor_Essence) :
    """Model the link between a person and an address"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :

            auto_cache    = True

        # end class left

        class right (_Ancestor.right) :

            role_type     = Address
            auto_cache    = True

        # end class right

    # end class _Attributes

# end class Person_has_Address

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Person_has_Address

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This module is part of the package DNS.
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
#    DNS.Entity
#
# Purpose
#    Common base class for essential classes of DNS
#
# Revision Dates
#     6-Sep-2012 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _GTW._OMP._DNS         import DNS

_Ancestor_Essence = MOM.Entity

class _DNS_Entity_ (_Ancestor_Essence) :
    """Common base class for essential classes of DNS"""

    _real_name = "Entity"
    is_partial = True
    PNS        = DNS

Entity = _DNS_Entity_ # end class

_Ancestor_Essence = MOM.An_Entity

class _DNS_An_Entity_ (Entity, _Ancestor_Essence) :
    """Common base class for essential classes of DNS"""

    _real_name = "An_Entity"
    is_partial = True

An_Entity = _DNS_An_Entity_ # end class

_Ancestor_Essence = MOM.Id_Entity

class _DNS_Id_Entity_ (Entity, _Ancestor_Essence) :
    """Common base class for essential classes of DNS"""

    _real_name = "Id_Entity"
    is_partial = True

Id_Entity = _DNS_Id_Entity_ # end class

_Ancestor_Essence = MOM.Object

class _DNS_Object_ (Entity, _Ancestor_Essence) :
    """Common base class for essential object classes of DNS."""

    _real_name = "Object"
    is_partial = True

Object = _DNS_Object_ # end class

_Ancestor_Essence = MOM.Link1

class _DNS_Link1_ (Entity, _Ancestor_Essence) :
    """Common base class for essential unary link classes of DNS."""

    _real_name = "Link1"
    is_partial = True

Link1 = _DNS_Link1_ # end class

_Ancestor_Essence = MOM.Link2

class _DNS_Link2_ (Entity, _Ancestor_Essence) :
    """Common base class for essential binary link classes of DNS."""

    _real_name = "Link2"
    is_partial = True

Link2 = _DNS_Link2_ # end class

if __name__ != "__main__" :
    DNS._Export ("*")
### __END__ DNS.Entity

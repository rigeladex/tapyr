# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Person_owns_Boat
#
# Purpose
#    Owner of boat
#
# Revision Dates
#     6-Feb-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._PAP.Person
import _GTW._OMP._SRM.Boat

_Ancestor_Essence = GTW.OMP.SRM.Link2

class Person_owns_Boat (_Ancestor_Essence) :
    """Owner of boat."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Owner of a boat"""

            role_type          = GTW.OMP.PAP.Person
            role_name          = "owner"
            auto_rev_ref       = True

        # end class left

        class right (_Ancestor.right) :
            """Boat owned by a person"""

            role_type          = GTW.OMP.SRM.Boat
            role_name          = "boat"
            auto_rev_ref       = True
            max_links          = 1

        # end class right

        ### Non-primary attributes

    # end class _Attributes

# end class Person_owns_Boat

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Person_owns_Boat

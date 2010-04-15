# -*- coding: iso-8859-1 -*-
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
#    GTW.OMP.SRM.Sailor
#
# Purpose
#    Model a sailor
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._PAP.Person

import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Sailor (_Ancestor_Essence) :
    """A person that is member of a sailing club."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :

            role_type          = GTW.OMP.PAP.Person
            max_links          = 1

        # end class left

        class nation (A_Nation) :
            """Nation for which the sailor sails."""

            kind               = Attr.Primary_Optional

        # end class nation

        class mna_number (A_String) :
            """Membership number in Member National Authorities (MNA)."""

            kind               = Attr.Primary_Optional

        # end class mna_number

    # end class _Attributes

# end class Sailor

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Sailor

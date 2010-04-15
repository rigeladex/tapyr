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
#    GTW.OMP.SRM.Boat_Class
#
# Purpose
#    Model a class of sailboats
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Object

class Boat_Class (_Ancestor_Essence) :
    """Modela class of sailboats"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class name (A_String) :
            """Name of class of sailboats."""

            kind               = Attr.Primary
            max_length         = 48

        # end class name

        ### Non-primary attributes

        class beam (A_Float) :
            """Maximum beam of boat (in meters)."""

            kind               = Attr.Optional
            max_value          = 5.0
            min_value          = 0.5

        # end class beam

        class loa (A_Float) :
            """Length over all (in meters)."""

            kind               = Attr.Optional
            max_value          = 10.0
            min_value          = 2.0

        # end class loa

        class max_crew (A_Int) :
            """Maximum number of crew for this class of sailboats."""

            kind               = Attr.Mandatory
            max_value          = 4
            min_value          = 1

        # end class max_crew

        class sail_area (A_Float) :
            """Seal area upwind (in square meters)."""

            kind               = Attr.Optional
            min_value          = 3.5

        # end class sail_area

    # end class _Attributes

# end class Boat_Class

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Boat_Class



# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.SRM.Team
#
# Purpose
#    Model a team of sailors participating in a regatta
#
# Revision Dates
#    31-Aug-2010 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._PAP.Person

import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Team (_Ancestor_Essence) :
    """A team of sailors participating in a regatta."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Regatta in which this team sails."""

            role_type          = GTW.OMP.SRM.Regatta_C
            role_name          = "regatta"
            auto_cache         = True

        # end class left

        class name (A_String) :
            """Name of the sailing team."""

            kind               = Attr.Primary
            max_length         = 64

        # end class name

        ### Non-primary attributes

        class club (A_String) :
            """Club the team sails for."""

            kind               = Attr.Optional
            max_length         = 8

        # end class club

        class desc (A_String) :
            """Short description of the team."""

            kind               = Attr.Optional
            max_length         = 160

        # end class desc

        class leader (A_Entity) :
            """Leader of team."""

            Class              = GTW.OMP.PAP.Person
            kind               = Attr.Optional

        # end class leader

        class place (A_Int) :
            """Place of team in this regatta."""

            kind               = Attr.Optional
            min_value          = 1

        # end class place

        class registration_date (A_Date) :
            """Date of registration."""

            kind               = Attr.Internal

            def computed_default (self) :
                return self.now ()
            # end def computed_default

        # end class registration_date

    # end class _Attributes

# end class Team

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Team

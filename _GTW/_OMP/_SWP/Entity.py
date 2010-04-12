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
#     6-Feb-2010 (MG) Missing `is_partial` added
#    10-Feb-2010 (CT) Bug fix (`Object = _SWP_Object_` added)
#    22-Mar-2010 (CT) `Object_PN` added (factored from `SWP.Page`)
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _MOM._Attr.Date_Interval import *
from   _GTW                     import GTW

import _GTW._OMP._PAP.Person
import _GTW._OMP._SWP

class _SWP_Entity_ (MOM.Entity) :
    """Common base class for essential classes of GTW.OMP.SWP"""

    _real_name = "Entity"

    PNS        = GTW.OMP.SWP
    is_partial = True

Entity = _SWP_Entity_ # end class

class _SWP_Link1_ (Entity, MOM.Link1) :
    """Common base class for essential unary links of GTW.OMP.SWP"""

    _real_name  = "Link1"

    is_partial  = True

Link1 = _SWP_Link1_ # end class

class _SWP_Link2_ (Entity, MOM.Link2) :
    """Common base class for essential binary links of GTW.OMP.SWP"""

    _real_name  = "Link2"

    is_partial  = True

Link2 = _SWP_Link2_ # end class

class _SWP_Object_ (Entity, MOM.Object) :
    """Common base class for essential objects of GTW.OMP.SWP"""

    _real_name  = "Object"

    is_partial  = True

Object = _SWP_Object_ # end class

_Ancestor_Essence = Object

class Object_PN (_Ancestor_Essence) :
    """Object with a perma_name."""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class perma_name (A_Date_Slug) :
            """Name used for perma-link."""

            kind               = Attr.Primary
            ui_name            = "Name"

            check              = ("""" " not in value""", )

        # end class perma_name

        ### Non-primary attributes

        class creator (A_Object) :
            """Creator of the contents."""

            kind               = Attr.Optional
            Class              = GTW.OMP.PAP.Person

        # end class creator

        class date (A_Date_Interval_N) :
            """Publication (`start`) and expiration date (`finish`)"""

            kind               = Attr.Optional

            explanation        = """
              The page won't be visible before the start date.

              After the finish date, the page won't be displayed (except
              possibly in an archive).
              """

        # end class date

        class short_title (A_String) :
            """Short title (used in navigation)."""

            kind               = Attr.Required
            max_length         = 30

        # end class title

        class title (A_String) :
            """Title of the web page"""

            kind               = Attr.Required
            max_length         = 120

        # end class title

    # end class _Attributes

# end class Object_PN

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Entity

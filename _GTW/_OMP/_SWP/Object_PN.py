# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.SWP.
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
#    GTW.OMP.SWP.Object_PN
#
# Purpose
#    Model an object with a perma_name.
#
# Revision Dates
#    17-Jun-2013 (CT) Creation (recovered from late `_SWP.Entity` module)
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM.import_MOM          import *
from   _MOM._Attr.Date_Interval import *

from   _GTW                     import GTW

import _GTW._OMP._SWP

_Ancestor_Essence = GTW.OMP.SWP.Object

class Object_PN (_Ancestor_Essence) :
    """Object with a perma_name."""

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class perma_name (A_Date_Slug) :
            """Name used for perma-link."""

            kind               = Attr.Primary
            max_length         = 80
            ui_name            = "Name"

            check              = ("""' ' not in value""", )

        # end class perma_name

        ### Non-primary attributes

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

            kind               = Attr.Necessary
            max_length         = 30

        # end class title

        class title (A_String) :
            """Title of the web page"""

            kind               = Attr.Necessary
            max_length         = 120

        # end class title

    # end class _Attributes

# end class Object_PN

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Object_PN

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
#    GTW.OMP.SWP.Gallery
#
# Purpose
#    Model a gallery of pictures
#
# Revision Dates
#    22-Mar-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _GTW                     import GTW

import _GTW._OMP._SWP.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SWP.Object_PN

class Gallery (_Ancestor_Essence) :
    """Model a gallery of pictures"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class directory (A_Dirname) :
            """Directory where pictures of gallery are stored."""

            kind               = Attr.Required

        # end class directory

    # end class _Attributes

# end class Gallery

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Gallery

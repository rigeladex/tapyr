# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.Attr.
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
#    MOM.Attr.Position
#
# Purpose
#    Composite attribute type for geographical position
#
# Revision Dates
#     4-Feb-2010 (CT) Creation
#    13-Oct-2010 (CT) `example` added
#     5-Apr-2011 (MG) `distance` abd friends added
#     6-Apr-2011 (MG) `distance` calculation moved into TFL.Sphere
#    19-May-2011 (CT) Description for `lat` and `lon` improved
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    19-Jul-2012 (RS) Use `A_Angle` instead of `A_Float` for `lat`, `lon`
#     5-Jun-2013 (CT) Use `is_attr_type`, not home-grown code
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                  import TFL
from   _MOM                  import MOM

from   _MOM._Attr            import Attr
import _MOM._Attr.Kind
from   _MOM._Attr.Type       import *

import _MOM.Entity

from   _TFL.I18N             import _, _T, _Tn
import _TFL.Sphere

_Ancestor_Essence = MOM.An_Entity

class Position (_Ancestor_Essence) :
    """Model a geographical position."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class lat (A_Angle) :
            """Geographical latitude"""

            kind               = Attr.Necessary
            example            = u"42"
            min_value          = -90.0
            max_value          = +90.0
            ui_name            = "Latitude"

        # end class lat

        class lon (A_Angle) :
            """Geographical longitude"""

            kind               = Attr.Necessary
            example            = u"137"
            min_value          = -180.0
            max_value          = +180.0
            ui_name            = "Longitude"

        # end class lon

        class height (A_Float) :
            """Height above mean sea level"""

            kind               = Attr.Optional
            example            = u"1764"

        # end class height

    # end class _Attributes

    def distance (self, other) :
        return TFL.Earth.distance (self, other)
    # end def distance

# end class Position

class A_Position (_A_Composite_) :
    """Models an attribute holding a geographical position."""

    P_Type         = Position
    typ            = "Position"

# end class A_Position

__all__ = tuple (k for (k, v) in globals ().iteritems () if is_attr_type (v))

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Position

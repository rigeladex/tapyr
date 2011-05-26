# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    MOM.Attr.A_2D
#
# Purpose
#    Composite attribute type for 2D values (positions, sizes, ...)
#
# Revision Dates
#    22-Mar-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _TFL.I18N             import _, _T, _Tn

_Ancestor_Essence = MOM.An_Entity

class _D2_Value_ (_Ancestor_Essence) :
    """Base class for two-dimensional values (e.g., position or size)."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class x (A_Attr_Type) :
            """Value in x (horizontal) direction."""

            kind               = Attr.Necessary
            rank               = 1

        # end class x

        class y (A_Attr_Type) :
            """Value in y (vertical) direction."""

            kind               = Attr.Necessary
            rank               = 2

        # end class y

    # end class _Attributes

# end class _D2_Value_

_Ancestor_Essence = _D2_Value_

class D2_Value_Int (_Ancestor_Essence) :
    """Model a two-dimensional integer-based value."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class x (_Ancestor.x, A_Int) :
            pass
        # end class x


        class y (_Ancestor.y, A_Int) :
            pass
        # end class y

    # end class _Attributes

# end class D2_Value_Int

_Ancestor_Essence = _D2_Value_

class D2_Value_Float (_Ancestor_Essence) :
    """Model a two-dimensional float-based value."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class x (_Ancestor.x, A_Float) :
            pass
        # end class x


        class y (_Ancestor.y, A_Float) :
            pass
        # end class y

    # end class _Attributes

# end class D2_Value_Float

class A_2D_Int (_A_Composite_) :
    """Models an attribute holding a two-dimensional integer-based value."""

    C_Type           = D2_Value_Int
    typ              = "D2_Value_Int"

# end class A_2D_Int

class A_2D_Float (_A_Composite_) :
    """Models an attribute holding a two-dimensional float-based value."""

    C_Type           = D2_Value_Float
    typ              = "D2_Value_Float"

# end class A_2D_Float

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (*  __all__)
### __END__ MOM.Attr.A_2D

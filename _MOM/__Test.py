# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    MOM.__Test
#
# Purpose
#    Test for MOM meta object model
#
# Revision Dates
#    18-Oct-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM       import *

class Rodent (MOM.Named_Object) :
    """Model a rodent of the Better Mouse Trap application."""

    class _Attributes (MOM.Named_Object._Attributes) :

        class color (A_String) :
            """Color of the rodent"""

            kind     = Attr.Optional

        # end class color

        class weight (A_Float) :
            """Weight of the rodent"""

            kind     = Attr.Required
            check    = ("value > 0", )

        # end class weight

    # end class _Attributes

# end class Rodent

class Mouse (Rodent) :
    """Model a mouse of the Better Mouse Trap application."""

    is_partial = False

# end class Mouse

class Rat (Rodent) :
    """Model a rat of the Better Mouse Trap application."""

    is_partial = False

# end class Rat

class Trap (MOM.Object) :
    """Model a trap of the Better Mouse Trap application."""

    is_partial = False

    class _Attributes (MOM.Object._Attributes) :

        class cat (A_String) :
            """Category of the trap"""

            kind     = Attr.Primary

        # end class cat

        class serial_no (A_Int) :
            """Serial number of the trap"""

            kind     = Attr.Primary

        # end class serial_no

        class max_weight (A_Float) :
            """Maximum weight of rodent the trap can hold"""

            kind     = Attr.Optional
            check    = ("value > 0", )

        # end class max_weight

    # end class _Attributes

# end class Trap

### __END__ MOM.__Test

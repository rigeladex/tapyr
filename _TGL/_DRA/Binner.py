# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TGL.DRA.Binner
#
# Purpose
#    Support for binning of measurement values
#
# Revision Dates
#    15-Nov-2006 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TGL import TGL

import _TFL._Meta.Object
import _TGL._DRA

class Binner (TFL.Meta.Object) :
    """Distribute measurement values into bins.

       The range of possible values is split into bins zhat are numbered from
       1 to `n` (0 is reserved for invalid values). Each measured value is
       mapped to the bin containing it.
    """

    def __init__ (self, offset, width) :
        self.offset = float (offset)
        self.width  = float (width)
    # end def __init__

    def binned (self, r) :
        """Returns bin index for value `r`."""
        return int ((r - self.offset) // self.width) + 1
    # end def binned

    def dennib (self, i) :
        """Returns value corresponding to bin `i`."""
        return (i - 1) * self.width + self.offset + self.width / 2
    # end def dennib

# end class Binner

if __name__ != "__main__" :
    TGL._Export ("*")
### __END__ TGL.DRA.Binner

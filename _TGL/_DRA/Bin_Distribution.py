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
#    TGL.DRA.Bin_Distribution
#
# Purpose
#    Compute distribution of binned measurement data
#
# Revision Dates
#    17-Nov-2006 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TGL import TGL

import _TFL.defaultdict
import _TFL._Meta.Object
import _TGL._DRA

class Bin_Distribution (TFL.Meta.Object) :
    """Compute distribution of binned measurement data"""

    def __init__ (self, abscissa, * indices) :
        self.abscissa       = abscissa
        self.distribution   = TFL.defaultdict (int)
        self.measurements   = 0
        self.invalid_values = 0
        self.add (* indices)
    # end def __init__

    def add (self, * indices) :
        d = self.distribution
        for i in indices :
            if i > 0 :
                d [i] += 1
                self.measurements   += 1
            else :
                self.invalid_values += 1
    # end def add

    def probabilities (self) :
        result = TFL.defaultdict (int)
        n      = float (self.measurements)
        for i, f in self.distribution.iteritems () :
            result [i] = f / n
        return result
    # end def probabilities

# end class Bin_Distribution

if __name__ != "__main__" :
    TGL._Export ("*")
### __END__ TGL.DRA.Bin_Distribution


# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2010 Mag. Christian Tanzer. All rights reserved
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
#    TGL.DRA.Interpolator
#
# Purpose
#    Interpolate for equidistantly spaced data
#
# Revision Dates
#    11-Nov-2007 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TGL import TGL

import _TFL._Meta.Object
import _TGL._DRA

import _TFL.Accessor

class Interpolator_3 (TFL.Meta.Object) :
    """Interpolate from three data values.

       >>> calcer = Interpolator_3 ((7, 0.884226), (8, 0.877366), (9, 0.870531))
       >>> print calcer (8.18125)
       0.87612530127
    """

    ### see J. Meeus, ISBN 0-943396-61-1, pp. 23-24
    ### XXX generalize to any (odd) number of data points

    x_getter = TFL.Getter [0]
    y_getter = TFL.Getter [1]

    def __init__ (self, p1, p2, p3, x_getter = None, y_getter = None) :
        if x_getter is not None :
            self.x_getter = x_getter
        if y_getter is not None :
            self.y_getter = y_getter
        Y = self.y_getter
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.a  = a = Y (p2) - Y (p1)
        self.b  = b = Y (p3) - Y (p2)
        self.c  = b - a
    # end def __init__

    def __call__ (self, x) :
        """Interpolated value at `x`."""
        X = self.x_getter
        Y = self.y_getter
        n = x - X (self.p2)
        return Y (self.p2) + (n / 2.0) * (self.a + self.b + n * self.c)
    # end def __call__

# end class Interpolator_3

if __name__ != "__main__" :
    TGL.DRA._Export ("*")
### __END__ Interpolator



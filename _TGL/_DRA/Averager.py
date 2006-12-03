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
#    TGL.DRA.Averager
#
# Purpose
#    Compute average and standard deviation of data series
#
# Revision Dates
#    22-Nov-2006 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TGL import TGL

import _TFL._Meta.Object
import _TGL._DRA

import math

class Averager (TFL.Meta.Object) :
    """Compute average and standard deviation of data series.

       >>> runner = Averager ()
       >>> runner.add (x*x for x in range (3))
       >>> "%8.2f +- %5.3f" % (runner.average, runner.standard_deviation)
       '    1.67 +- 2.082'
       >>> runner.add (2**x for x in range (3,10))
       >>> "%8.2f +- %5.3f" % (runner.average, runner.standard_deviation)
       '  102.10 +- 165.085'
    """

    average            = property (lambda s : s.sum_x / s.n)
    standard_deviation = property \
        ( lambda s : (s.n > 1) and math.sqrt
            ((s.sum_xx * s.n - s.sum_x ** 2) / (s.n * (s.n - 1))) or 0
        )

    def __init__ (self, s = []) :
        self.n      = 0
        self.sum_x  = 0.0
        self.sum_xx = 0.0
        if s :
            self.add (s)
    # end def __init__

    def add (self, s) :
        """Add elements of iterable `s`."""
        for x in s :
            self.n      += 1
            self.sum_x  += x
            self.sum_xx += x * x
    # end def add

# end class Averager

if __name__ != "__main__" :
    TGL.DRA._Export ("*")
### __END__ Averager

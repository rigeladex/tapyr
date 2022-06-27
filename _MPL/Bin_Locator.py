# -*- coding: utf-8 -*-
# Copyright (C) 2006-2016 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    MPL.Bin_Locator
#
# Purpose
#    Locator for binned values
#
# Revision Dates
#    11-Dec-2006 (CT) Creation (factored from `Bin_Distribution_Plot`)
#    13-Dec-2006 (CT) `pad` added
#    30-Jun-2008 (CT) Adapted to (undocumented [Arrrg]) changes in
#                     matplotlib 0.98
#     9-Oct-2016 (CT) Move out from ..._DRA to toplevel package
#    ««revision-date»»···
#--

from   _MPL      import MPL

from   matplotlib.mlab       import frange
from   matplotlib.ticker     import Locator

class Bin_Locator (Locator) :

    dataInterval = property (lambda s : s.axis.get_data_interval ())
    viewInterval = property (lambda s : s.axis.get_view_interval ())

    def __init__ (self, binner, delta = 1.0, phase = None, pad = 0) :
        self.binner = binner
        self.delta  = delta
        self.phase  = phase
        self.pad    = pad
    # end def __init__

    def __call__ (self) :
        binner     = self.binner
        delta      = self.delta
        phase      = self.phase
        vmin, vmax = self.viewInterval
        wmin       = binner.value (vmin, False)
        wmax       = binner.value (vmax, False)
        if phase is not None :
            wmin -= (wmin % delta - phase)
        return \
            [ i for i in
                (   binner.index_f (v)
                for v in frange (wmin, wmax + 0.001 * delta, delta)
                )
            if vmin <= i <= vmax
            ]
    # end def __call__

    def autoscale (self) :
        binner = self.binner
        bounds = self.dataInterval
        pad    = self.pad
        v_min  = binner.index (binner.value (min (bounds), False) - pad)
        v_max  = binner.index (binner.value (max (bounds), False) + pad)
        return v_min, v_max
    # end def autoscale

# end class Bin_Locator

if __name__ != "__main__" :
    MPL._Export ("*")
### __END__ MPL.Bin_Locator

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
#    TGL.DRA.MPL
#
# Purpose
#    Matplotlib support for DRA package
#
# Revision Dates
#    24-Nov-2006 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TGL import TGL
import _TGL._DRA.Binner
import _TFL._Meta.Object

import pylab
import matplotlib.numerix.ma as     ma
from   matplotlib.mlab       import frange
from   matplotlib.ticker     import Locator, FuncFormatter

class Bin_Locator (Locator) :

    def __init__ (self, binner, delta = 1.0, phase = None) :
        self.binner = binner
        self.delta  = delta
        self.phase  = phase
    # end def __init__

    def __call__ (self) :
        self.verify_intervals ()
        binner     = self.binner
        delta      = self.delta
        phase      = self.phase
        vmin, vmax = self.viewInterval.get_bounds ()
        wmin       = binner.value (vmin, False)
        wmax       = binner.value (vmax, False)
        if phase is not None :
            wmin -= (wmin % delta - phase)
        return \
            [ i for i in
                (   binner.index (v)
                for v in frange (wmin, wmax + 0.001 * delta, delta)
                )
            if vmin <= i <= vmax
            ]
    # end def __call__

    def autoscale (self) :
        d_min, d_max = self.dataInterval.get_bounds ()
        binner       = self.binner
        v_min        = binner.index (binner.value (d_min - 1, False))
        v_max        = binner.index (binner.value (d_max + 1, False))
        print v_min, d_min, d_max, v_max
        return v_min, v_max
    # end def autoscale

# end class Bin_Locator

class Bin_Distribution_Plot (TFL.Meta.Object) :
    """Matplotlib plot for Bin_Distribution"""

    cmap              = pylab.cm.YlOrRd
    grid              = True
    shading           = "flat"
    x_tick_delta      = None
    x_tick_offset     = 0
    x_tick_format     = "%s"
    x_width           = 1.0
    y_tick_delta      = None
    y_tick_offset     = 0
    y_tick_format     = "%s"
    y_width           = 1.0

    def __init__ (self, xs, ys, fs, ** kw) :
        self.xs = xs
        self.ys = ys
        self.fs = fs
        self.__dict__.update (kw)
        self.x_binner = xb = TGL.DRA.Binner (int (min (xs)), self.x_width)
        self.y_binner = yb = TGL.DRA.Binner (int (min (ys)), self.y_width)
        self.xi       = xi = [xb.index (i) for i in xs]
        self.yi       = yi = [yb.index (i) for i in ys]
        self._setup_frequency_map (xi, yi, fs)
    # end def __init__

    def _setup_frequency_map (self, ls, ks, fs) :
        ### No idea why args need to specify `ls, ks` here (instead of `ks,ls`)
        fm = pylab.zeros ((max (ks) + 1, max (ls) + 1), dtype = pylab.double)
        for k, l, f in zip (ks, ls, fs) :
            fm [k, l] = f
        self.fm = ma.masked_where (fm == 0, fm)
    # end def _setup_frequency_map

    def plot (self, ax) :
        """Put the Bin_Distribution plot into `axes`"""
        xb, xf = self.x_binner, self.x_tick_format
        yb, yf = self.y_binner, self.y_tick_format
        xd     = self.x_tick_delta or xb.width
        yd     = self.y_tick_delta or yb.width
        BL, FF = Bin_Locator,   FuncFormatter
        ax.xaxis.set_major_locator   (BL (xb, xd, self.x_tick_offset))
        ax.yaxis.set_major_locator   (BL (yb, yd, self.y_tick_offset))
        ax.xaxis.set_major_formatter \
            (FF (lambda v, i : xf % (xb.value (v, False), )))
        ax.yaxis.set_major_formatter \
            (FF (lambda v, i : yf % (yb.value (v, False), )))
        pylab.pcolor \
            ( self.fm
            , cmap    = self.cmap
            , vmin    = 0.0
            , vmax    = 100.0
            , shading = self.shading
            )
        pylab.colorbar ()
        pylab.grid     (self.grid)
    # end def plot

# end class Bin_Distribution_Plot

if __name__ != "__main__" :
    TGL.DRA._Export ("*")
### __END__ TGL.DRA.MPL

"""

from pylab         import *
from _TGL._DRA.MPL import *
D   = load ("/tmp/w.dat")
bdp = Bin_Distribution_Plot \
    ( D [:,0], D [:,1], D [:,2]
    , x_tick_delta = 2, x_tick_format = "%d"
    , y_tick_delta = 1, y_tick_offset = 1, y_width = 0.5
    )
ax  = subplot (111)
bdp.plot (ax)
xlabel   ("Week")
ylabel   ("kg")
title    ("Weight before breakfast")
show     ()

"""

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
#    TGL.DRA.MPL.Bin_Distribution_Plot
#
# Purpose
#    Plot for Bin_Distribution
#
# Revision Dates
#    24-Nov-2006 (CT) Creation
#    26-Nov-2006 (CT) `errorbar` and `plot` added
#    11-Dec-2006 (CT) Moved into package TGL.DRA.MPL and renamed from `MPL`
#                     to `Bin_Distribution_Plot`
#    11-Dec-2006 (CT) `Bin_Locator` factored into separate module
#    13-Dec-2006 (CT) `x_pad` and `y_pad` added
#    ««revision-date»»···
#--

from   _TFL import TFL
from   _TGL import TGL

import _TGL._DRA.Binner
import _TGL._DRA._MPL.Bin_Locator
import _TFL._Meta.Object

import pylab
import matplotlib.numerix.ma as     ma
from   matplotlib.ticker     import FuncFormatter

class Bin_Distribution_Plot (TFL.Meta.Object) :
    """Matplotlib plot for Bin_Distribution"""

    cmap              = pylab.cm.YlOrRd
    grid              = dict \
        ( color       = "#E5D3C9"
        , linestyle   = "-"
        , linewidth   = 0.1
        )
    shading           = "flat"
    x_formatter       = None
    x_locator         = TGL.DRA.MPL.Bin_Locator
    x_pad             = 0
    x_tick_delta      = None
    x_tick_offset     = 0
    x_tick_format     = "%s"
    x_width           = 1.0
    y_formatter       = None
    y_locator         = TGL.DRA.MPL.Bin_Locator
    y_pad             = 0
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
        fm = pylab.zeros ((max (ks) + 1, max (ls) + 1), typecode = "d")
        #fm = pylab.zeros ((max (ks) + 1, max (ls) + 1), dtype = pylab.double)
        for k, l, f in zip (ks, ls, fs) :
            fm [k, l] = f
        self.fm = ma.masked_where (fm == 0, fm)
    # end def _setup_frequency_map

    def display (self, ax) :
        """Put the Bin_Distribution plot into `axes`"""
        xb          = self.x_binner
        yb          = self.y_binner
        xd          = self.x_tick_delta or xb.width
        yd          = self.y_tick_delta or yb.width
        FF          = FuncFormatter
        x_formatter = self.x_formatter
        if x_formatter is None :
            x_formatter = FF \
                (lambda v, i : self.x_tick_format % (xb.value (v, False), ))
        y_formatter = self.y_formatter
        if y_formatter is None :
            y_formatter = FF \
                (lambda v, i : self.y_tick_format % (yb.value (v, False), ))
        ax.xaxis.set_major_locator   \
            (self.x_locator (xb, xd, self.x_tick_offset, self.x_pad))
        ax.yaxis.set_major_locator   \
            (self.y_locator (yb, yd, self.y_tick_offset, self.y_pad))
        ax.xaxis.set_major_formatter (x_formatter)
        ax.yaxis.set_major_formatter (y_formatter)
        pylab.pcolor \
            ( self.fm
            , cmap    = self.cmap
            , vmin    = 0.0
            , vmax    = 100.0
            , shading = self.shading
            )
        pylab.colorbar ()
        pylab.grid     (** self.grid)
    # end def display

    def errorbar (self, xs, ys, yerr, marker_fmt, error_fmt, linewidth = 0.5, ** kw):
        """Display error bars"""
        xb = self.x_binner
        yb = self.y_binner
        xi = [xb.index_f (i) for i in xs]
        yi = [yb.index_f (i) for i in ys]
        if 1 :
            pylab.vlines \
            ( xi
            , [yb.index_f (y - d) for (y, d) in zip (ys, yerr)]
            , [yb.index_f (y + d) for (y, d) in zip (ys, yerr)]
            , error_fmt
            , linewidth = linewidth
            )
        if 0 : ### don't like the look of `pylab.errorbar`
            pylab.errorbar \
            ( xi
            , [yb.index_f (y) for y in ys]
            , [   (yb.index_f (y + d) - yb.index_f (y - d)) / 2
              for (y, d) in zip (ys, yerr)
              ]
            , fmt       = None
            , linewidth = linewidth
            , ** kw
            )
        pylab.plot (xi, yi, marker_fmt, ** kw)
    # end def errorbar

    def plot (self, xs, ys, * args, ** kw) :
        """Put `plot` of `xs` versus `ys` (`args` and `kw` are passed on to
           `pylab.plot`).
        """
        xb = self.x_binner
        yb = self.y_binner
        xi = [xb.index_f (x) for x in xs]
        yi = [yb.index_f (y) for y in ys]
        pylab.plot (xi, yi, * args, ** kw)
    # end def plot

# end class Bin_Distribution_Plot

if __name__ != "__main__" :
    TGL.DRA.MPL._Export ("*")
### __END__ TGL.DRA.MPL.Bin_Distribution_Plot

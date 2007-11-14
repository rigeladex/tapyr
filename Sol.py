# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    Sol
#
# Purpose
#    Display 24-hour clock showing sunrise, transit, and sunset
#
# Revision Dates
#    13-Nov-2007 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _TGL                  import TGL
from   _CAL                  import CAL

from   _TFL._TKT._Tk.CTK     import *
from   _TGL.Angle            import Angle_D, Angle_R

import _CAL.Date
import _CAL.Time
import _CAL._Sky.Sun

import _TFL._Meta.Object

class Display (TFL.Meta.Object) :
    """Solar clock."""

    background   = "grey85"
    civil_color  = "dodger blue"
    day_color    = "light sky blue"
    grid_color   = "grey75"
    hand_color   = "red"
    nautic_color = "royal blue"
    night_color  = "blue"
    border       = 5
    pad_x        = 0
    pad_y        = 0
    period       = 1000 * 300 ### specified in milliseconds --> 5 minutes

    def __init__ (self, master, rts, size = 64) :
        self.canvas = canvas = CTK.Canvas \
            ( master
            , background         = self.background
            , highlightthickness = 0
            , name               = "clock"
            )
        b         = self.border
        self.rect = rect = b, b, size - b, size -b
        CTK.Oval \
            ( canvas, rect
            , fill               = self.night_color
            , outline            = ""
            , width              = 0
            , tags               = "night"
            )
        rise  = 270 - rts.rise.time.as_degrees
        sett  = 270 - rts.set.time.as_degrees
        twl_m = 270 - rts.nautic_twilight_start.time.as_degrees
        twl_e = 270 - rts.nautic_twilight_finis.time.as_degrees
        self._canvas_arc  (rise,  sett - rise,  self.day_color,   "day")
        self._canvas_arc  (twl_m, rise - twl_m, self.civil_color, "twilight")
        self._canvas_arc  (twl_e, sett - twl_e, self.civil_color, "twilight")
        for i in (0, 45, 90, 135, 180, 225, 270, 315) :
            self._canvas_arc  (i - 1, +2, self.grid_color, "grid")
        canvas.configure  (height = size, width = size)
        canvas.after_idle (self.update)
    # end def __init__

    def pack (self) :
        self.canvas.pack (padx = self.pad_x, pady = self.pad_y)
    # end def pack

    def update (self, event = None) :
        time   = 270 - CAL.Time ().as_degrees
        canvas = self.canvas
        canvas.delete    ("hand")
        self._canvas_arc (time - 3, +7, self.hand_color, "hand")
        canvas.after     (self.period, self.update)
    # end def update

    def _canvas_arc (self, start, extent, fill, tags) :
        CTK.Arc \
            ( self.canvas, self.rect
            , start              = start
            , extent             = extent
            , fill               = fill
            , outline            = ""
            , width              = 0
            , tags               = tags
            )
    # end def _canvas_arc

# end class Display

class Toplevel (TFL.Meta.Object) :
    """Toplevel for solor clock."""

    background   = "grey70"
    relief       = CTK.RAISED

    class _TL_ (CTK.C_Toplevel) :
        widget_class = "Sol_Display"

    def __init__ (self, rts, size) :
        self.toplevel = toplevel = self._TL_ \
            ( bg                 = self.background
            , destroy_cmd        = self.destroy
            , relief             = self.relief
            , title              = "Sol-Clock"
            )
        self.display  = display  = Display (toplevel, rts, size)
        display.pack ()
    # end def __init__

    def destroy (self, event = None) :
        self.toplevel.destroy ()
        try :
            CTK.root.destroy  ()
        except StandardError, exc :
            pass
    # end def destroy

    def mainloop (self) :
        try :
            self.toplevel.mainloop ()
        except KeyboardInterrupt :
            pass
    # end def mainloop

# end class Toplevel

def command_spec (arg_array = None) :
    from   _TFL.Command_Line import Command_Line
    return Command_Line \
        ( option_spec =
            ( "pos:S?Position of display in geometry-format"
            , "size:I=64?Size of clock (square)"
            )
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    s = CAL.Sky.Sun (CAL.Date ())
    rts = CAL.Sky.RTS_Sun \
        ((s - 1, s, s + 1), Angle_D (48, 14), Angle_D (-16, -20))
    a = Toplevel (rts, cmd.size)
    if cmd.pos :
        a.toplevel.geometry (cmd.pos)
    CTK.root.withdraw ()
    a.mainloop ()
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ Sol

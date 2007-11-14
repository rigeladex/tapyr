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
#    14-Nov-2007 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _TGL                  import TGL
from   _CAL                  import CAL

from   _TFL._TKT._Tk.CTK     import *
from   _TFL.predicate        import pairwise
from   _TGL.Angle            import Angle_D, Angle_R

import _CAL.Date
import _CAL.Time
import _CAL._Sky.Location
import _CAL._Sky.Sun

import _TFL._Meta.Object

class Display (TFL.Meta.Object) :
    """Solar clock."""

    tag_colors   = dict \
        ( astro  = "#086FFF"
        , civil  = "#9CD8FC"
        , day    = "#D3F0FE"
        , grid   = "grey65"
        , hand   = "red"
        , nautic = "#5BC2FE"
        , night  = "#0005B1"
        )
    background   = "#BEBEBE"
    border       = 5
    pad_x        = 0
    pad_y        = 0
    period       = 1000 * 60 ### specified in milliseconds --> 1 minute

    def __init__ (self, master, date, location, size = 64) :
        self.date     = date
        self.location = location
        self.balloon  = balloon = CTK.Balloon (master, arrow = False)
        self.canvas   = canvas  = CTK.Canvas \
            ( master
            , background         = self.background
            , highlightthickness = 0
            , name               = "clock"
            )
        b             = self.border
        bi            = size // 4
        self.rect     = rect = b,  b,  size - b,  size -b
        self.rect2           = bi, bi, size - bi, size - bi
        CTK.Oval \
            ( canvas, rect
            , fill    = self.tag_colors ["night"]
            , outline = ""
            , width   = 0
            , tags    = "night"
            )
        self._display_rts (date, location, canvas, rect)
        balloon.body.configure (font = ("Arial", 8))
        canvas.configure  (height = size, width = size)
        canvas.bind       ("<Enter>",   self._balloon_show)
        master.bind       ("<Leave>",   self._balloon_hide)
        canvas.after      (self.period, self.update)
    # end def __init__

    def pack (self) :
        self.canvas.pack (padx = self.pad_x, pady = self.pad_y)
    # end def pack

    def update (self, event = None) :
        canvas = self.canvas
        date   = CAL.Date ()
        if date != self.date :
            self.date = date
            self._display_rts (date, self.location, canvas, self.rect)
        canvas.delete ("hand")
        self._hand    (canvas)
        canvas.after  (self.period, self.update)
    # end def update

    def _arc (self, start, extent, tag, rect = None) :
        CTK.Arc \
            ( self.canvas, rect or self.rect
            , start              = start
            , extent             = extent
            , fill               = self.tag_colors [tag]
            , outline            = ""
            , width              = 0
            , tags               = (tag, ) + ("sol", )
            )
    # end def _arc

    def _balloon_show (self, event = None) :
        if event :
            widget  = event.widget
            r       = self.rts
            message = "\n".join \
                ( ( ", ".join
                      ( ( "Sunrise : %02d:%02d" % r.rise.time.hh_mm
                        , "transit : %02d:%02d" % r.transit.time.hh_mm
                        , "sunset : %02d:%02d"  % r.set.time.hh_mm
                        )
                      )
                  , "Civil  twilight starts %02d:%02d, ends %02d:%02d"
                    % (r.civil_twilight_start.time.hh_mm
                    + r.civil_twilight_finis.time.hh_mm)
                  , "Nautic twilight starts %02d:%02d, ends %02d:%02d"
                    % (r.nautic_twilight_start.time.hh_mm
                    + r.nautic_twilight_finis.time.hh_mm)
                  , "Astro  twilight starts %02d:%02d, ends %02d:%02d"
                    % (r.astro_twilight_start.time.hh_mm
                    + r.astro_twilight_finis.time.hh_mm)
                  )
                )
            x    = event.x_root - event.x
            y    = event.y_root - event.y
            offx = 0
            offy = 5
            if event.x_root > 200 :
                offx = -200
            if event.y_root > 100 :
                offy = -25
            self.balloon.activate \
                (widget, message, x = x, y = y, offx = offx, offy = offy)
    # end def _balloon_show

    def _balloon_hide (self, event = None) :
        self.balloon.deactivate ()
    # end def _balloon_hide

    def _display_rts (self, date, location, canvas, rect) :
        self.rts = rts = CAL.Sky.RTS_Sun.On_Day (date, location)
        canvas.delete ("sol")
        events = \
            [ rts.astro_twilight_start
            , rts.nautic_twilight_start
            , rts.civil_twilight_start
            , rts.rise
            , rts.set
            , rts.civil_twilight_finis
            , rts.nautic_twilight_finis
            , rts.astro_twilight_finis
            ]
        for (a, b), tag in zip \
            ( pairwise (events)
            , ("astro", "nautic", "civil", "day", "civil", "nautic", "astro")
            ) :
            x = 270 - a.time.as_degrees
            y = 270 - b.time.as_degrees
            self._arc (x, y - x, tag)
        for i in range (0, 360, 45) :
            self._arc (i - 1, +2, "grid")
        self._hand (canvas)
    # end def _display_rts

    def _hand (self, canvas) :
        time = 270 - CAL.Time ().as_degrees
        self._arc (time - 7, +15, "hand", self.rect2)
        self._arc (time - 2,  +5, "hand", self.rect)
    # end def _hand

# end class Display

class Toplevel (TFL.Meta.Object) :
    """Toplevel for solor clock."""

    background   = "grey70"
    relief       = CTK.RAISED

    class _TL_ (CTK.C_Toplevel) :
        widget_class = "Sol_Display"

    def __init__ (self, date, location, size) :
        self.toplevel = toplevel = self._TL_ \
            ( bg                 = self.background
            , destroy_cmd        = self.destroy
            , relief             = self.relief
            , title              = "Sol-Clock"
            )
        self.display  = display  = Display (toplevel, date, location, size)
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
        ( arg_spec    =
            ( "date:S=%s" % CAL.Date ()
            ,
            )
        , option_spec =
            ( "latitude:F?Latitude (north is positive)"
            , "location:S=Vienna?Location of observer"
            , "longitude:F?Longitude (negative is east of Greenwich)"
            , "pos:S?Position of display in geometry-format"
            , "size:I=64?Size of clock (square)"
            )
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    date = CAL.Date.from_string (cmd.date)
    if cmd.latitude and cmd.longitude :
        location = CAL.Sky.Location (cmd.latitude, cmd.longitude)
    else :
        location = CAL.Sky.Location.Table [cmd.location]
    a = Toplevel (date, location, cmd.size)
    if cmd.pos :
        a.toplevel.geometry (cmd.pos)
    CTK.root.withdraw ()
    a.mainloop ()
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ Sol

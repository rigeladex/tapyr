# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    PSD
#
# Purpose
#    Pythonic Status Display
#
# Revision Dates
#     3-Jun-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL              import TFL
from   CTK               import *
from   Record            import Record
from   _TFL.predicate    import *
from   _TFL.Regexp       import *
from   _TFL._D2          import D2
import _TFL._D2.Point
import _TFL._D2.Rect
import _TFL._Meta.Object

import sos, sys, time

class ACPI_Updater (TFL.Meta.Object) :
    """Update ACPI-related status"""

    alarm_color   = "orange"
    low_color     = "yellow"
    normal_color  = "light green"
    online_color  = "Deep Sky blue"

    _acpi_pattern = Regexp \
        ( r"^ \s* Battery \s+ \#\d \s+ : \s+ "
              r"(?P<bat_status> [^,]+),  \s+ "
              r"(?P<percent> [0-9.]+)%"
              r"(?: , \s+"
                  r"(?P<hours>   [0-9]{2}):"
                  r"(?P<minutes> [0-9]{2}):"
                  r"(?P<seconds> [0-9]{2})"
              r")?"
              r"\s* "
          r"AC \s+ adapter   \s+ : \s+ (?P<ac_status> on|off)-line \s*"
          r"(?: Thermal \s+ info \s+ : \s + "
              r"(?P<therm_stat> [^,]+), \s+ "
              r"(?P<temperature> [0-9]+) \s+ C"
          r")?"
        , re.VERBOSE | re.IGNORECASE | re.MULTILINE
        )

    def __init__ (self) :
        self.last_status_change = time.time ()
        self.last_ac_status     = None
        self.last_bat_status    = None
    # end def __init__

    def __call__ (self, status) :
        status.acpi = None
        pipe = sos.popen ("acpitool")
        l = pipe.read    ()
        pipe.close       ()
        p = self._acpi_pattern
        if p.search (l) :
            if p.hours is not None :
                minutes = int (p.hours) * 60 + int (p.minutes)
            else :
                minutes = None
            ac_status   = p.ac_status
            bat_status  = p.bat_status
            now         = time.time ()
            percent     = int (round (float (p.percent)))
            speed       = self._get_speed ()
            temperature = int (p.temperature)
            if self.last_ac_status != ac_status :
                self.last_ac_status     = ac_status
                self.last_status_change = now
            if self.last_bat_status != bat_status :
                if (  bat_status           == "charging"
                   or self.last_bat_status == "charging"
                   ) :
                    self.last_bat_status    = bat_status
                    self.last_status_change = now
            color = self.normal_color
            if ac_status == "on" :
                color = self.online_color
            else :
                if percent < 40 :
                    color = self.low_color
                if percent <= 5 :
                    color = self.alarm_color
            same_status_duration = (now - self.last_status_change) // 60
            status.acpi = Record \
                ( ac_status            = ac_status
                , bat_minutes          = minutes
                , bat_percent          = percent
                , bat_status           = bat_status
                , color                = color
                , same_status_duration = same_status_duration
                , speed                = speed
                , temperature          = temperature
                , time                 = now
                )
    # end def __call__

    def _get_speed (self) :
        try :
            f = open \
                ("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq")
        except IOError :
            pass
        else :
            try :
                v = f.read ().strip ()
            finally :
                f.close ()
            try :
                return int (v) // 1000
            except (ValueError, TypeError) :
                pass
    # end def _get_speed

# end class ACPI_Updater

class Entry (TFL.Meta.Object) :
    """One entry of a status display"""

    background   = "black"
    spacer       = 1
    updater      = None

    def __init__ (self, canvas, pos, width) :
        self.canvas = canvas
        self.pos    = D2.Point (pos.x, pos.y + self.spacer)
        self.size   = size = D2.Point (width, self.height)
        self.rect   = rect = D2.Rect  (pos,  size)
        self.widget = CTK.Rectangle \
            ( canvas, rect.top_left.list (), rect.bottom_right.list ()
            , fill    = self.background
            , outline = ""
            , width   = 0
            , tags    = self.rect_tag
            )
    # end def __init__

    def update (self, status) :
        """Update the entry with the current status"""
    # end def update

    def _formatted_minutes (self, minutes, head = "", tail = "") :
        if minutes is not None :
            return "%s%d:%02d%s" % ((head, ) + divmod (minutes, 60) + (tail, ))
        return ""
    # end def

# end class Entry

class _Text_Entry_ (Entry) :

    background   = "gray20"
    height       = 14
    text_color   = "white"
    text_font    = "6x13"

    def _new_text (self, canvas, pos, offset, anchor, tag) :
        p = pos + offset
        return CTK.CanvasText \
            ( canvas, p.list ()
            , anchor   = anchor
            , fill     = self.text_color
            , font     = self.text_font
            , tags     = tag
            , text     = ""
            )
    # end def _new_text

# end class _Text_Entry_

class Text_C_Entry (_Text_Entry_) :
    """One entry of a status display with text at center"""

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        x = self.size.x // 2
        self.l_text = self._new_text \
            (canvas, self.pos, D2.Point (x, 0), CTK.N, self.c_tag)
    # end def __init__

# end class Text_C_Entry

class Text_L_Entry (_Text_Entry_) :
    """One entry of a status display with text at left"""

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        rect = self.rect
        self.l_text = self._new_text \
            (canvas, rect.top_left, D2.Point (1, +1), CTK.NW, self.l_tag)
    # end def __init__

# end class Text_L_Entry

class Text_R_Entry (_Text_Entry_) :
    """One entry of a status display with text at right"""

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        rect = self.rect
        self.r_text = self._new_text \
            (canvas, rect.top_right, D2.Point (-1, +1), CTK.NE, self.r_tag)
    # end def __init__

# end class Text_R_Entry

class Text_LR_Entry (Text_L_Entry, Text_R_Entry) :
    """One entry of a status display with texts at left and right"""

# end class Text_LR_Entry

_acpi_updater = ACPI_Updater ()

class ACPI_Entry (Text_LR_Entry) :
    """Entry displaying ACPI information"""

    text_color   = "black"

    l_tag        = "acpistatus"
    r_tag        = "acpivalue"
    rect_tag     = "acpientry"

    updater      = _acpi_updater

    def update (self, status) :
        s = status.acpi
        if s :
            canvas     = self.canvas
            remaining  = self._formatted_minutes (s.bat_minutes, head = " ")
            bat_status = s.bat_status
            color      = s.color
            if s.ac_status == "on" :
                s_format = "%s%s%s"
                if bat_status == "charging" :
                    status = ""
                else :
                    status = "->"
                remaining = ""
            else :
                status   = ""
                s_format = "%s%s%2.2s"
                if bat_status == "discharging" :
                    bat_status = ""
            status = \
                ( s_format
                % (status, s.same_status_duration, bat_status.capitalize ())
                )
            value  = "%s%%%s" % (s.bat_percent, remaining)
            tcolor = self.text_color
            self.widget.config (fill = color)
            self.l_text.config (fill = tcolor, text = status)
            self.r_text.config (fill = tcolor, text = value)
            return status, value
    # end def update

# end class ACPI_Entry

class ACPI_Gauge (Entry) :
    """Entry displaying ACPI as gauge"""

    background   = "black"
    gauge_tag    = "acpigauge"
    height       = 5
    rect_tag     = "acpirect"
    spacer       = 0

    updater      = _acpi_updater

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        rect = self.rect
        self.gauge = CTK.Rectangle \
            ( canvas, rect.top_left.list (), rect.bottom_right.list ()
            , fill    = self.background
            , outline = ""
            , width   = 0
            , tags    = self.gauge_tag
            )
    # end def __init__

    def update (self, status) :
        s = status.acpi
        if s :
            percent = s.bat_percent
            size    = self.size
            rect    = D2.Rect \
                ( self.pos, D2.Point (0.01 * percent * size.x, size.y))
            self.canvas.coords \
                ( self.gauge_tag
                , * (rect.top_left.list () + rect.bottom_right.list ())
                )
            self.widget.config (fill = s.color)
    # end def update

# end class ACPI_Gauge

class CPU_Entry (Text_LR_Entry) :
    """Entry displaying CPU information"""

    l_tag        = "cputemp"
    r_tag        = "cpuspeed"
    rect_tag     = "cpuentry"

    updater      = _acpi_updater

    def update (self, status) :
        s = status.acpi
        if s :
            canvas     = self.canvas
            if s.temperature :
                self.l_text.config (text = "%s C"   % s.temperature)
            if s.speed :
                self.r_text.config (text = "%s MHz" % s.speed)

    # end def update

# end class CPU_Entry

class Date_Entry (Text_C_Entry) :
    """Entry displaying the date"""

    c_tag    = "date"
    rect_tag = "datebody"

    def update (self, status) :
        d = time.strftime ("%a %d-%b-%Y", time.localtime ())
        self.canvas.itemconfigure (self.c_tag, text = d)
    # end def update

# end class Date_Entry

class Time_Entry (Text_C_Entry) :
    """Entry displaying the time"""

    c_tag    = "time"
    rect_tag = "timebody"

    def update (self, status) :
        t = time.strftime ("%H:%M", time.localtime ())
        self.canvas.itemconfigure (self.c_tag, text = t)
    # end def update

# end class Time_Entry

class Display (TFL.Meta.Object) :
    """Main widget of status display"""

    background   = "grey30"
    foreground   = "grey77"
    pad_x        = 3
    pad_y        = 3
    period       = 1000
    relief       = CTK.RAISED
    widget_class = "PSD_Display"

    class _TL_ (CTK.C_Toplevel) :
        widget_class = "APM_Display"

    def __init__ (self, kind, width, * entry_t) :
        updaters      = {}
        self.entries  = entries  = []
        self.status   = Record ()
        self.toplevel = toplevel = self._TL_ \
            ( bg                 = self.background
            , class_             = self.widget_class
            , relief             = self.relief
            , title              = "%s Status" % (kind, )
            )
        self.canvas   = canvas   = CTK.Canvas \
            ( toplevel
            , background         = "black"
            , name               = "canvas"
            , highlightthickness = 0
            )
        canvas.pack (padx = self.pad_x, pady = self.pad_y)
        pos = D2.Point (0, 0)
        w   = width - 2 * self.pad_x
        for e in entry_t :
            pos.y += 2 * e.spacer
            o = e (canvas, pos = pos, width = width)
            entries.append (o)
            if o.updater is not None and o.updater not in updaters :
                updaters [o.updater] = len (updaters)
            pos.y += o.size.y
        self.size = D2.Point (width, pos.y * self.pad_y)
        self.updaters = \
            [u [0] for u in dusort (updaters.iteritems (), lambda (k, v) : v)]
        canvas.configure (height = pos.y, width = width)
        toplevel.after_idle (self.update)
    # end def __init__

    def destroy (self, event = None) :
        self.toplevel.destroy ()
    # end def destroy

    def mainloop (self) :
        self.toplevel.mainloop ()
    # end def mainloop

    def update (self, event = None) :
        status = self.status
        for u in self.updaters :
            u (status)
        for e in self.entries :
            e.update (status)
        self.toplevel.after (self.period, self.update)
    # end def update

# end class Display

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    return Command_Line ( option_spec =
                            ( "pos:S?Position of display in geometry-format"
                            , "width:I=100?Width of display"
                            )
                        , arg_array   = arg_array
                        )
# end def command_spec

def main (cmd) :
    a = Display \
        ( "ACPI", cmd.width
        , Date_Entry, Time_Entry, ACPI_Entry, ACPI_Gauge, CPU_Entry
        )
    if cmd.pos :
        a.geometry (cmd.pos)
    CTK.root.withdraw ()
    try :
        try :
            a.mainloop ()
        finally :
            CTK.root.destroy ()
    except KeyboardInterrupt :
        raise SystemExit
    except StandardError :
        pass
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ PSD

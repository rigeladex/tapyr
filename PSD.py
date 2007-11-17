# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2007 Mag. Christian Tanzer. All rights reserved
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
#     4-Jun-2005 (CT) Creation continued
#     7-Jun-2005 (CT) `_get_temperatures` added to remember
#                     `/proc/acpi/ibm/thermal`
#    28-Nov-2006 (CT) `_acpi_pattern` adapted to change in `acpitool`s output
#     9-Sep-2007 (CT) Display ` Full` instead of `Charged`
#    17-Nov-2007 (CT) `Time_Entry` removed from call to `Toplevel`
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   CTK                   import *
from   _TFL.Record           import Record
from   _TFL.Numeric_Interval import Numeric_Interval as Ival
from   _TFL.predicate        import *
from   _TFL.Regexp           import *
from   _TFL._D2              import D2
import _TFL._D2.Point
import _TFL._D2.Rect
import _TFL._Meta.Object

from   _TFL                  import sos

import sys, time

class R_Map (TFL.Meta.Object) :
    """Map one range into another"""

    def __init__ (self, source, target) :
        self.source = source
        self.target = target
        self.s_len  = source.upper - source.lower
        self.t_len  = target.upper - target.lower
    # end def __init__

    def __call__ (self, value) :
        s_percentage = float (value - self.source.lower) / self.s_len
        return s_percentage * self.t_len + self.target.lower
    # end def __call__

# end class R_Map

class _Bar_ (TFL.Meta.Object) :

    def __init__ (self, canvas, rect, background, tag, source_ival) :
        self.canvas     = canvas
        self.background = background
        self.rect       = rect
        self.tag        = tag
        self.widget     = CTK.Rectangle \
            ( canvas, rect.top_left.list (), rect.bottom_right.list ()
            , fill    = background
            , outline = ""
            , width   = 0
            , tags    = tag
            )
    # end def __init__

    def update (self, value) :
        rect = self._scaled_rect (self.rect, value)
        self.canvas.coords \
            ( self.tag
            , * (rect.top_left.list () + rect.bottom_right.list ())
            )
    # end def update

# end class _Bar_

class H_Bar (_Bar_) :
    """Horizontal bar"""

    def __init__ (self, canvas, rect, background, tag, source_ival) :
        self.r_map = R_Map (source_ival, Ival (0, rect.size.x))
        self.__super.__init__ (canvas, rect, background, tag, source_ival)
    # end def __init__

    def _scaled_rect (self, rect, value) :
        v = self.r_map (value)
        return D2.Rect (rect.top_left, D2.Point (v, rect.size.y))
    # end def _scaled_rect

# end class H_Bar

class V_Bar (_Bar_) :
    """Vertical bar"""

    def __init__ (self, canvas, rect, background, tag, source_ival) :
        self.r_map = R_Map (source_ival, Ival (0, rect.size.y))
        self.__super.__init__ (canvas, rect, background, tag, source_ival)
    # end def __init__

    def _scaled_rect (self, rect, value) :
        v = self.r_map (value)
        return D2.Rect \
            (rect.bottom_left - D2.Point (0, v), D2.Point (rect.size.x, v))
    # end def _scaled_pos

# end class V_Bar

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
          r"(?: Thermal \s+ (?: info|zone \s+ \d+) \s+ : \s + "
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

    def _get_temperatures (self) :
        pass
        ### XXX /proc/acpi/ibm/thermal
        ### (/usr/share/doc/ibm-acpi-0.11-r1/README.gz)
        ### Alas: the sensors seem to be wired differently in different
        ### models (e.g., for my X40 hddtemp shows a totally different
        ### temperature than field 3 of /proc/acpi/ibm/thermal)
        ### Googling didn't turn up any more information about it
    # end def _get_temperatures

# end class ACPI_Updater

class Entry (TFL.Meta.Object) :
    """One entry of a status display"""

    background   = "black"
    spacer       = 1
    updater      = None

    def __init__ (self, canvas, pos, width) :
        self.canvas = canvas
        self.pos    = D2.Point (pos.x, pos.y + self.spacer)
        self.size   = size = D2.Point (width,    self.height)
        self.rect   = rect = D2.Rect  (self.pos, size)
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

    background   = "gray"
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

    l_offset = D2.Point (1, 0)

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        rect = self.rect
        self.l_text = self._new_text \
            (canvas, rect.top_left, self.l_offset, CTK.NW, self.l_tag)
    # end def __init__

# end class Text_L_Entry

class Text_R_Entry (_Text_Entry_) :
    """One entry of a status display with text at right"""

    r_offset = D2.Point (-1, 0)

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        rect = self.rect
        self.r_text = self._new_text \
            (canvas, rect.top_right, self.r_offset, CTK.NE, self.r_tag)
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
            duration   = self._formatted_minutes \
                (s.same_status_duration, tail = " ")
            bat_status = s.bat_status.capitalize ()
            color      = s.color
            if s.ac_status == "on" :
                s_format = "%s%s%s"
                if bat_status == "Charging" :
                    status = ""
                else :
                    status = "->"
                    if s.bat_percent == 100 or bat_status == "Charged" :
                        bat_status = " Full"
                remaining = ""
            else :
                status   = ""
                s_format = "%s%s%2.2s"
                if bat_status == "Discharging" :
                    bat_status = ""
            status = s_format % (status, duration, bat_status)
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
        self.gauge = H_Bar \
            (canvas, self.rect, self.background, self.gauge_tag, Ival (0, 100))
    # end def __init__

    def update (self, status) :
        s = status.acpi
        if s :
            self.gauge.update  (s.bat_percent)
            self.widget.config (fill = s.color)
    # end def update

# end class ACPI_Gauge

class CPU_Entry (Text_LR_Entry) :
    """Entry displaying CPU information"""

    r_offset         = D2.Point (-10, +1)

    l_tag            = "cputemp"
    r_tag            = "cpuspeed"
    rect_tag         = "cpuentry"

    text_color       = "black"
    speed_background = "gray77"
    speed_color      = "gray50"
    speed_width      = 5

    t_colors         = \
        ( "gray"                  ### <  30
        , "CornflowerBlue"        ### <  40
        , "LightSkyBlue"          ### <  50
        , "aquamarine"            ### <  60
        , "LightGoldenrod"        ### <  70
        , "DarkSalmon"            ### <  80
        , "light coral"           ### <  90
        , "DeepPink"              ### < 100
        )

    updater      = _acpi_updater

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        rect          = self.rect
        self.sg_size  = gs = D2.Point (self.speed_width  + 2, self.height)
        self.sg_rect  = gr = D2.Rect  (rect.bottom_right - gs, gs)
        self.s_gauge  = CTK.Rectangle \
            ( canvas, gr.top_left.list (), gr.bottom_right.list ()
            , fill    = self.speed_background
            , outline = ""
            , width   = 0
            , tags    = "speedgauge"
            )
        min_speed     = self._get_speed ("min")
        max_speed     = self._get_speed ("max")
        if min_speed is not None and max_speed is not None :
            bs = D2.Point (self.speed_width, self.height - 2)
            br = D2.Rect  (rect.bottom_right - bs - D2.Point (1, 1), bs)
            self.s_bar = V_Bar \
                (canvas, br, self.speed_color, "speedbar", Ival (0, max_speed))
        else :
            self.s_bar = None
    # end def __init__

    def update (self, status) :
        s = status.acpi
        if s :
            canvas = self.canvas
            t      = s.temperature
            if t :
                t_colors = self.t_colors
                self.l_text.config (text = "%s C"   % t)
                i = min (max ((t - 20) // 10, 0), len (t_colors) - 1)
                self.widget.config  (fill = t_colors [i])
            if s.speed :
                self.r_text.config  (text = "%s MHz" % s.speed)
                if self.s_bar :
                    self.s_bar.update (s.speed)
    # end def update

    def _get_speed (self, name) :
        for nf in ("cpuinfo_%s_freq", "scaling_%s_freq") :
            n = nf % name
            try :
                f = open ("/sys/devices/system/cpu/cpu0/cpufreq/%s" % n)
                try :
                    v = f.read ().strip ()
                finally :
                    f.close ()
                return int (v) // 1000
            except (IOError, ValueError, TypeError) :
                pass
    # end def _get_speed

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
    """Status display comprising various entries"""

    background   = "grey30"
    foreground   = "grey77"
    pad_x        = 3
    pad_y        = 3
    period       = 1000
    widget_class = "PSD_Display"

    def __init__ (self, master, width, * entry_t) :
        updaters      = {}
        self.entries  = entries  = []
        self.status   = Record ()
        self.canvas   = canvas   = CTK.Canvas \
            ( master
            , background         = "black"
            , name               = "canvas"
            , highlightthickness = 0
            )
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
        canvas.configure  (height = pos.y, width = width)
        canvas.after_idle (self.update)
    # end def __init__

    def pack (self) :
        self.canvas.pack (padx = self.pad_x, pady = self.pad_y)
    # end def pack

    def update (self, event = None) :
        status = self.status
        for u in self.updaters :
            u (status)
        for e in self.entries :
            e.update (status)
        self.canvas.after (self.period, self.update)
    # end def update

# end class Display

class Toplevel (TFL.Meta.Object) :
    """Toplevel for status display"""

    background   = "#BEBEBE"
    relief       = CTK.RAISED

    class _TL_ (CTK.C_Toplevel) :
        widget_class = "PSD_Display"

    def __init__ (self, kind, width, * entries) :
        self.toplevel = toplevel = self._TL_ \
            ( bg                 = self.background
            , destroy_cmd        = self.destroy
            , relief             = self.relief
            , title              = "%s Status" % (kind, )
            )
        self.display  = display  = Display (toplevel, width, * entries)
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
        self.toplevel.mainloop ()
    # end def mainloop

# end class Toplevel

def command_spec (arg_array = None) :
    from   _TFL.Command_Line import Command_Line
    return Command_Line \
        ( option_spec =
            ( "pos:S?Position of display in geometry-format"
            , "width:I=100?Width of display"
            )
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    a = Toplevel \
        ("ACPI", cmd.width, Date_Entry, ACPI_Entry, ACPI_Gauge, CPU_Entry)
    if cmd.pos :
        a.toplevel.geometry (cmd.pos)
    CTK.root.withdraw ()
    a.mainloop ()
# end def main

if __name__ == "__main__":
    main (command_spec ())
### __END__ PSD

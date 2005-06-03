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
        pipe = os.popen ("acpitool")
        l = pipe.read   ()
        pipe.close      ()
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
            same_status_duration = (now - self.last_status_change) // 60
            status.acpi = Record \
                ( ac_status            = ac_status
                , bat_minutes          = minutes
                , bat_percent          = percent
                , bat_status           = bat_status
                , same_status_duration = same_status_duration
                , speed                = speed
                , temperature          = temperature
                , time                 = now
                )
        status.acpi = None
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

    background   = "gray77"
    updater      = None

    def __init__ (self, canvas, pos, width) :
        self.canvas = canvas
        self.pos    = pos
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

    height       = 14
    text_font    = "6x13"

    def _new_text (self, canvas, pos, offset, anchor, tag) :
        return CTK.CanvasText \
            ( canvas, (pos + offset).list ()
            , anchor   = anchor
            , text     = ""
            , tags     = tag
            , font     = self.text_font
            )
    # end def _new_text

# end class _Text_Entry_

class Text_C_Entry (_Text_Entry_) :
    """One entry of a status display with text at center"""

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        x = self.size.x // 2
        self.l_text = self._new_text \
            (canvas, self.pos, D2.Point (x, -1), CTK.N, self.c_tag)
    # end def __init__

# end class Text_C_Entry

class Text_L_Entry (_Text_Entry_) :
    """One entry of a status display with text at left"""

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        self.l_text = self._new_text \
            (canvas, self.pos, D2.Point (1, -1), CTK.NE, self.l_tag)
    # end def __init__

# end class Text_L_Entry

class Text_R_Entry (_Text_Entry_) :
    """One entry of a status display with text at right"""

    def __init__ (self, canvas, ** kw) :
        self.__super.__init__ (canvas, ** kw)
        self.r_text = self._new_text \
            (canvas, self.pos, D2.Point (-1, -1), CTK.NE, self.r_tag)
    # end def __init__

# end class Text_R_Entry

class Text_LR_Entry (Text_L_Entry, Text_R_Entry) :
    """One entry of a status display with texts at left and right"""

# end class Text_LR_Entry

class _ACPI_Entry_ (Entry) :

    updater      = ACPI_Updater ()

# end class _ACPI_Entry_

class ACPI_Entry (_ACPI_Entry_, Text_LR_Entry) :
    """Entry displaying ACPI information"""

    alarm_color  = "orange"
    low_color    = "yellow"
    normal_color = "light green"
    online_color = "deep sky blue"

    l_tag        = "acpistatus"
    r_tag        = "acpivalue"
    rect_tag     = "acpientry"

    def update (self, status) :
        s = status.acpi
        if s :
            canvas     = self.canvas
            remaining  = self._formatted_minutes (s.bat_minutes, head = " ")
            bat_status = s.bat_status
            if s.ac_status == "on" :
                color    = self.online_color
                s_format = "%s%s%s"
                if bat_status == "charging" :
                    status = ""
                else :
                    status = "->"
                remaining = ""
            else :
                color    = self.normal_color
                status   = ""
                s_format = "%s%s%2.2s"
                if s.bat_percent < 40 :
                    color = self.low_color
                if s.bat_percent <= 5 :
                    color = self.alarm_color
                if bat_status == "discharging" :
                    bat_status = ""
            status = \
                ( s_format
                % (status, s.same_status_duration, bat_status.capitalize ())
                )
            value  = "%s%%%s" % (s.bat_percent, remaining)
            canvas.itemconfigure (self.l_tag,    text = status)
            canvas.itemconfigure (self.r_tag,    text = value)
            canvas.itemconfigure (self.rect_tag, bg   = color)
    # end def update

# end class ACPI_Entry

class ACPI_Gauge (_ACPI_Entry_) :
    """Entry displaying ACPI as gauge"""

    height   = 5
    rect_tag = "acpibar"

    def update (self, status) :
        if status.acpi :
            percent = status.acpi.bat_percent
            self.canvas.coords \
                ( self.rect_tag
                , 0,                            0
                , 0.01 * percent * self.size.x, self.size.y
                )
    # end def update

# end class ACPI_Gauge

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
    spacer       = 1
    widget_class = "PSD_Display"

    def __init__ (self, kind, width, * entry_t) :
        updaters      = {}
        self.entries  = entries  = []
        self.status   = Record ()
        self.toplevel = toplevel = CTK.C_Toplevel.__init__ \
            ( self
            , bg                 = self.background
            , class_             = self.widget_class
            , relief             = self.relief
            , title              = "%s Status" % (kind, )
            )
        self.canvas   = canvas   = CTK.Canvas \
            ( toplevel
            , name               = "canvas"
            , highlightthickness = 0
            , width              = width
            , bg                 = self.foreground
            )
        canvas.pack (padx = self.pad_x, pady = self.pad_y)
        pos = D2.Point (self.spacer, 0)
        w   = width - 2 * self.pad_x
        for e in entry_t :
            o = entry_t    (canvas, pos, width)
            entries.append (o)
            if o.updater is not None and o.updater not in updaters :
                updaters [o.updater] = len (updaters)
            pos.y += o.size.y + self.spacer
        self.size = D2.Point (width, pos.y + self.spacer + 2 * self.pad_y)
        self.updaters = \
            [u [0] for u in dusort (updaters.iteritems (), lambda (k, v) : v)]
        self.after_idle (self.update)
    # end def __init__

    def update (self, event = None) :
        status = self.status
        for u in self.updaters :
            u (status)
        for e in self.entries :
            e.updater (status)
        self.after (self.period, self.update_apm)
    # end def update

# end class Display

### __END__ PSD

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. lucky@spannberg.com
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
#    CAL.GTK.Week
#
# Purpose
#    Handle the display of one week of a calendar
#
# Revision Dates
#    03-Oct-2004 (MGL) Creation
#    ««revision-date»»···
#--
import  pygtk
pygtk.require ("2.0")
import  gtk

from   _TFL                    import TFL
from    Regexp                 import Regexp
import _TFL._Meta.Object
import _CAL._GTK.Color
import _CAL._GTK.Event
import _CAL._GTK.Text_Property

class Event_Display (object) :
    """Handles the height requests for a certain event for all the possible
       states.
    """

    slice_pat = Regexp ("\[(.*):(.*)\]")
    span_pat  = Regexp ("(style|weight|variant)=([^, ]+)")

    def __init__ (self, event, width, detail = 0) :
        self._event       = event
        self._detail      = detail - 1
        self._height_dict = {}
        self.next_detail    (width)
    # end def __init__

    def next_detail (self, width) :
        self._detail  = (self._detail + 1) % self._event.gtk_levels
        self.height, self._display = self._height (self._detail, width)
    # end def next_detail

    def _height (self, detail, width) :
        if detail not in self._height_dict :
            format = []
            h      = 0
            for line_formats in self._event.gtk_display  [self._detail] :
                line_format = []
                lx          = 0
                lh          = 0
                for f in line_formats :
                    text = f (self._event)
                    if f.width is None :
                        width = width
                    else :
                        width = f.width
                    lx, lh = CAL.GTK.Text_Handling.instance.set_layout \
                        (text, x = lx, y = 0, lh = lh, width = width)
                    line_format.append ((text, f.x, f.width))
                h += lh
                format.append (line_format)
            self._height_dict [detail] = (h, format)
        return self._height_dict [detail]
    # end def _height

    def draw (self, window, gc, color, x, y, width) :
        txp = CAL.GTK.Text_Handling.instance
        for line_format in self._display :
            lw = x
            lh = 0
            for text, xadd, ww in line_format :
                lw += xadd
                if ww is None :
                    ww = width
                lw, lh = txp.set_layout \
                    (text, window, gc, lw, y, lh, draw = True, width = ww)
            y += lh
    # end def draw

# end class Event_Display

class Day_Display (object) :
    """Handles the height control of all event display of one day."""

    def __init__ (self, day, width, details = None) :
        details          = details or [0] * len (day.appointments)
        self.day         = day
        self.min_height  = CAL.GTK.Text_Handling.week_day_h
        self.width       = width
        self._events     = \
            [ Event_Display (e, self.width, details [i])
                  for i, e in enumerate (day.appointments)
            ]
        self.height      = max \
            ( reduce (lambda l, r : l + r.height, self._events, 0)
            + len (self._events) - 1
            , self.min_height
            )
    # end def __init__

    def button_down (self, x, y) :
        end = 0
        for e in self._events :
            end += e.height
            if y <= end :
                break
        else :
            ### event not in this day
            return None, None
        e.next_detail (self.width)
        self.height = max \
            ( reduce (lambda l, r : l + r.height, self._events, 0)
            + len (self._events) - 1
            , self.min_height
            )
        return self.day, e
    # end def button_down

    def draw_events (self, window, gc, color, x, y, width) :
        old_fg        = gc.foreground
        first         = True
        for e in self._events :
            if not first :
                gc.foreground = color.white
                window.draw_line (gc, x + 2, y, x + width - 4, y)
                y            += 1
                gc.foreground = old_fg
            e.draw (window, gc, color, x, y, width)
            y     += e.height
            first  = False
        if not first :
            txp = CAL.GTK.Text_Handling.instance
            txp.layout.set_width (-1)
            txp.wrap_width = -1
    # end def draw_events

# end class Day_Display

class Week (TFL.Meta.Object, gtk.DrawingArea) :
    """Display a week in all the different state`s
       - simple, all days in one row
       - expanded, one day in one row
         * events in the different states
    """

    day_detail = None

    def __init__ (self, week, day_display = None, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.week        = week
        self.day_display = day_display
        self.color       = CAL.GTK.Color         (self)
        txp              = CAL.GTK.Text_Handling (self)
        self.connect    ("expose-event",       self._expose)
        self.connect    ("button-press-event", self._button_down)
        self.set_events (gtk.gdk.EXPOSURE_MASK | gtk.gdk.BUTTON_PRESS_MASK)
        self.month    = TFL.Time_Tuple.months [week.sun.month].capitalize ()
        self.week_no  = "%02d" % (self.week.number, )
        self.bgcolor  = self.color.color_of_day (self.week.mon, today = False)
        self.overview = True
        self.set_size_request (-1, txp.week_no_h)
        self.show             ()
    # end def __init__

    def _button_down (self, widget, event) :
        txp = CAL.GTK.Text_Handling.instance
        if event.button == 1 and event.type == gtk.gdk.BUTTON_PRESS :
            if not self.overview :
                week_no = txp.week_no_w
                day     = None
                if event.x <= week_no :
                    self.overview = True
                    self.set_size_request (-1, txp.week_no_h)
                    return
                if event.x >= (week_no * 2) :
                    x, y      = event.x, event.y
                    day_start = 1
                    for dd in self.day_detail :
                        day_end = day_start + dd.height
                        if day_start <= y < day_end :
                            day, app = dd.button_down (x, y - day_start)
                            break
                        day_start  = day_end
                    else :
                        return
                if day :
                    self.set_size_request \
                        ( -1
                         , txp.week_no_h
                         + reduce ( lambda l, r : l + r.height
                                  , self.day_detail
                                  , 0
                                  )
                        )
            else :
                self.overview = False
                if not self.day_detail :
                    width = self.get_allocation ().width
                    self.day_detail = \
                        [Day_Display (d, width, None) for d in self.week.days]
                self.set_size_request \
                    ( -1
                    , txp.week_no_h
                    + reduce (lambda l, r : l + r.height, self.day_detail, 0)
                    )
    # end def _button_down

    def _expose (self, widget, event) :
        alloc         = self.get_allocation ()
        width, height = alloc.width, alloc.height
        gc            = widget.get_style ().fg_gc [gtk.STATE_NORMAL]
        x             = y = 0
        old_fg        = gc.foreground
        gc.foreground = self.bgcolor
        widget.window.draw_rectangle (gc, True, x, y, width, height)
        gc.foreground = old_fg
        if self.overview :
            self._draw_overview (widget.window, gc, x, y, width, height)
        else :
            self._draw_detail   (widget.window, gc, x, y, width, height)
    # end def _expose

    def _draw_overview (self, window, gc, x, y, width, height) :
        txp           = CAL.GTK.Text_Handling.instance
        old_fg        = gc.foreground
        gc.foreground = self.color.week_number
        window.draw_rectangle (gc, True, x, y, width, height)
        gc.foreground = self.color.white
        txp.draw_text (self.week_no, window, gc, x, y)
        x     += txp.week_no_w
        width -= txp.month_w - 1
        txp.draw_text (self.month, window, gc, width + 1, y)
        day_width = (width -x) / 7.0
        for day in self.week.days :
            next_day = int (x + day_width)
            if day.date.weekday () == 6 :
                dw   = width - x
            else :
                dw   = next_day - x
            gc.foreground = self.color.color_of_day (day.date)
            window.draw_rectangle (gc, True, x, y, dw, height)
            gc.foreground = old_fg
            txp.draw_text \
                ( "%02d" % day.number, window, gc
                , x + (dw - txp.week_no_w) // 2, y
                )
            x        = next_day
    # end def _draw_overview

    def _draw_detail (self, window, gc, x, y, width, height) :
        txp = CAL.GTK.Text_Handling.instance
        old_fg        = gc.foreground
        dw            = width - x
        y            += self._draw_week_description (window, gc, x, y, height)
        for dd in self.day_detail :
            gc.foreground = self.color.white
            window.draw_line (gc, x, y, x + dw, y)
            x  = txp.week_no_w + 2
            dw = width - x
            y += 1
            dh = dd.height
            gc.foreground = self.color.color_of_day (dd.day.date)
            window.draw_rectangle (gc, True, x, y, dw, dh)
            gc.foreground = old_fg
            txp.draw_text \
                ( "%s\n%02d"
                % (self.week._day_names [dd.day.weekday ()], dd.day.number)
                , window, gc
                , x, y
                )
            dd.draw_events (window, gc, self.color, 2 * x, y, dw - x)
            y += dh
    # end def _draw_detail

    def _draw_week_description (self, window, gc, x, y, height) :
        w    = self.week
        txp  = CAL.GTK.Text_Handling.instance
        text = ( '<span weight="bold">KW%02d   </span>'
                 '<span style="italic">%02d.%s %d .. %02d.%s %d</span>'
               % ( w.number
                 , w.mon.day
                 , TFL.Time_Tuple.months [w.mon.month].capitalize ()
                 , w.mon.year
                 , w.sun.day, self.month, w.sun.year
                 )
               )
        txp.draw_text (text, window, gc, x, y + 1)
        return txp.week_no_h
    # end def _draw_week_description

# end class Week

if __name__ != "__main__" :
    CAL.GTK._Export ("*")
else :
    import _CAL.Year
    import _CAL.Event
    cal   = CAL.Calendar ("Lucky's Calendar", directory = (r"f:\tmp", ))
    y     = cal.add_year     (2004)
    w = gtk.Window         ()
    w.connect              ("delete-event", gtk.mainquit)
    w.show                 ()
    #w.set_size_request     (240, 320)
    c = gtk.VBox           ()
    c.show                 ()
    w.add                  (c)
    for w in y.weeks [:5] :
        week = Week        (w)
        c.add              (week)
    gtk.mainloop           ()
### __END__ CAL.GTK.Week

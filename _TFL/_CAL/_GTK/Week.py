# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    TFL.CAL.GTK.Week
#
# Purpose
#    Displays the weeknumber and the month/days of one week (depending on the
#    display detail level of the week).
#
# Revision Dates
#    11-Feb-2004 (MG) Creation
#    ««revision-date»»···
#--
import  pygtk
pygtk.require ("2.0")
import  gtk
from   _TFL                         import TFL
from    Date_Time                   import Time_Tuple
import _TFL._CAL._GTK.Drawing_Area

class Week_Number (TFL.CAL.GTK.Drawing_Area) :
    """Displays the week number"""

    event_binding     = TFL.d_dict \
        ( expose      = "_expose"
        , button_down = "_button_down"
        )

    height_small = None
    height_large = None
    width_number = None

    def __init__ (self, week) :
        self.week   = week
        self.number = None
        self.__super.__init__ ("02", wrap = False, border = True)
        self.border_width = self.border_width * self.border
        if not self.width_number :
            width, height = self.layout.get_pixel_extents () [1] [2:]
            self.__class__.width_number = width  + 2 * self.border_width
            self.__class__.height_small = height + 2 * self.border_width
        self.set_size_request (self.width_number, self.height_small)
    # end def __init__

    def _expose (self, widget, event) :
        if not self.number :
            w           = self.week
            self.number = w.thu.week
            self.month  = w.mon.month
            self.short  = "%02d" % (self.number, )
            self.long   = "\n".join \
                ( "%s%04d" % ( Time_Tuple.months [self.month].capitalize ()
                              , w.mon.year #% 100
                              )
                )
            if self.month != w.sun.month :
                m         = w.sun.month
                y         = w.sun.year
                self.last = "\n".join \
                    ( "%s%04d" % ( Time_Tuple.months [m].capitalize ()
                                  , y #% 100
                                  )
                    )
            else :
                self.last = None
            self.bgcolor  = self._colors.colors.get \
                (("even_month", "odd_month") [self.month % 2])
        self.__super._expose (widget, event)
    # end def _expose

    def _draw_content (self, x, y, width, height) :
        x += 1
        y += 1
        self.gc.foreground = self._colors.day_text
        self.layout.set_markup (self.short)
        self.draw_layout       (x, y)
        if not self.border_state :
            y += self.height_small
            if not self.last :
                y += (height - y - self.month_height) // 2
            else :
                y += self.height_small // 2
            x += self.width_number // 4
            self.layout.set_markup (self.long)
            self.draw_layout       (x, y)
            if self.last :
                y = height - self.month_height - self.height_small // 2
                self.layout.set_markup (self.last)
                self.draw_layout       (x, y)
    # end def _draw_content

    def _button_down (self, widget, event) :
        if event.button == 1:
            self.border_state = not self.border_state
            if not (self.border_state or self.height_large) :
                self.layout.set_markup (self.long)
                self.__class__.month_height = \
                    self.layout.get_pixel_extents () [1] [3]
                self.__class__.height_large = \
                    (self.height_small * 3 + self.month_height * 2)
                self.__class__.height_large += 2 * self.border_width
            self.set_size_request \
                ( self.width_number
                , (self.height_large, self.height_small) [self.border_state]
                )
    # end def _button_down

# end class Week_Number

class _Month_Day_ (TFL.CAL.GTK.Drawing_Area) :
    """Root class for the Month/Day display widget.
       They have a common ancestor because they should have the same width!
       """

    fixed_width = None

    def __init__ (self, text, day, border = False, wrap = False, * args, ** kw) :
        kw ["bgcolor"] = ("even_month", "odd_month") [day.month % 2]
        self.__super.__init__ (border = border, wrap = wrap, * args, ** kw)
        if not self.fixed_width :
            self.layout.set_markup ("Th\n29")
            ( width_0
            , self.__class__.day_height
            ) = self.layout.get_pixel_extents () [1] [2:]
            self.layout.set_markup ("""<span size="x-small">Mar</span>""")
            ( width_1
            , self.__class__.month_height
            ) = self.layout.get_pixel_extents () [1] [2:]
            self.__class__.fixed_width = max (width_0, width_1)
        self.layout.set_markup (text)
    # end def __init__

# end class _Month_Day_

class Month (_Month_Day_) :
    """Displays the name of the month."""

    def __init__ (self, week) :
        m = ( """<span size="small">%s</span>"""
            % Time_Tuple.months [week.mon.month].capitalize ()
            )
        self.__super.__init__ (m, week.mon)
        self.set_size_request  (self.fixed_width, self.month_height)
    # end def __init__

    def _draw_content (self, x, y, width, height) :
        y = (height - self.month_height) // 2
        self.__super._draw_content (x, y, width, height)
    # end def _draw_content

# end class Month

class Day_Name (_Month_Day_) :
    """Display the name and day number of a day"""

    def __init__ (self, day) :
        text = "%s\n%02d" % (TFL.CAL.Week._day_names [day.weekday], day.day)
        self.__super.__init__  (text, day, x = 1, y = 1)
        self.set_size_request  (self.fixed_width, self.day_height)
    # end def __init__

# end class Day_Name

class Week (TFL.Meta.Object) :
    """Handels the displaying of one week"""

    def __init__ (self, week, table, row) :
        self.table         = table
        self.row           = row
        self.week_number   = Week_Number (week)
        self.days          = []
        self.month         = None
        self.display_level = 0
        table.attach \
            ( self.week_number, 0, 1, row, row + 7
            , yoptions = gtk.FILL
            , xoptions = gtk.FILL
            )
        self.week_number.register_callback ("button_down", self._expand_week)
        self.week_number.register_callback ("expose", self._expose_week_no)
    # end def __init__

    def _expose_week_no (self, widget, event) :
        if not self.month :
            self.month = Month (self.week_number.week)
            self.table.attach \
                ( self.month, 1, 2, self.row, self.row + 7
                , yoptions = gtk.FILL
                , xoptions = gtk.FILL
                )
    # end def _expose_week_no

    def _expand_week (self, widget, event) :
        row = self.row
        self.display_level = not self.display_level
        if self.display_level :
            self.table.remove (self.month)
            if not self.days :
                self._create_days ()
            for day_name, day_events in self.days :
                self.table.attach \
                    ( day_name, 1, 2, row, row + 1
                    , yoptions = gtk.FILL
                    , xoptions = gtk.FILL
                    )
                ### self.table.remove (day_events)
                row += 1
        else :
            for day_name, day_events in self.days :
                self.table.remove (day_name)
                ### self.table.remove (day_events)
            self.table.attach \
                ( self.month, 1, 2, row, row + 7
                , yoptions = gtk.FILL
                , xoptions = gtk.FILL
                )
    # end def _expand_week

    def _create_days (self) :
        for day in self.week_number.week.days :
            day_name   = Day_Name (day)
            day_events = None ### XXX
            self.days.append ((day_name, day_events))
    # end def _create_days

# end class Week

if __name__ == "__main__" :
    import _TFL._CAL.Year
    y = TFL.CAL.Year       (2004)
    w = gtk.Window         ()
    w.connect              ("delete-event", gtk.mainquit)
    w.show                 ()
    w.set_size_request     (240, 100)
    t = gtk.Table          (len (y.weeks) * 7, 3, False)
    t.show                 ()
    s = gtk.ScrolledWindow ()
    s.show                 ()
    w.add                  (s)
    s.add_with_viewport    (t)
    row = 0
    for w in y.weeks :#[:10] :
        week = Week (w, t, row)
        row += 7
    gtk.mainloop           ()
### __END__ TFL.CAL.GTK.Week



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
#    TFL.CAL.GTK.Drawing_Area
#
# Purpose
#    A text widget which can receive button events and can be dragged.
#
# Revision Dates
#    10-Feb-2004 (MG) Creation
#    ««revision-date»»···
#--
import  pygtk
pygtk.require ("2.0")
import  gtk
from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL.d_dict
import _TFL._CAL._GTK.Color

class Drawing_Area (TFL.Meta.Object, gtk.DrawingArea) :
    """A text widget which can receive button events and can be dragged."""

    border_width      = 1
    event_mask        = TFL.d_dict \
        ( expose      = ("expose-event",       gtk.gdk.EXPOSURE_MASK)
        , button_down = ("button-press-event", gtk.gdk.BUTTON_PRESS_MASK)
        )
    event_binding     = TFL.d_dict \
        ( expose      = "_expose"
        )

    def __init__ (self, text = "", wrap = True, border = False, x = 0, y = 0, bgcolor = None) :
        self.__super.__init__ ()
        self.wrap         = wrap
        self.text         = text
        self.border       = border
        self.x            = x
        self.y            = y
        self.width        = -1
        self.layout       = self.create_pango_layout (self.text)
        self._colors      = TFL.CAL.GTK.Color        (self)
        self.bgcolor      = bgcolor and self._colors.colors.get (bgcolor)
        mask              = 0
        self.border_state = True
        for name, fct_name in self.event_binding.iteritems () :
            fct = fct_name and getattr (self, fct_name, None)
            if fct :
                signal, event  = self.event_mask [name]
                mask          |= event
                cb_list        = "%s_callbacks" % (name, )
                setattr      (self, cb_list, [])
                self.connect (signal, self._call, fct, cb_list)
        self.set_events      (mask)
        self.show            ()
    # end def __init__

    def register_callback (self, name, fct) :
        if name in self.event_binding :
            getattr (self, "%s_callbacks" % (name, )).append (fct)
    # end def register_callback

    def _call (self, widget, event, fct, callback) :
        fct (widget, event)
        [cb (widget, event) for cb in getattr (self, callback)]
    # end def _call

    def _expose (self, widget, event) :
        self.gc       = widget.get_style ().fg_gc [gtk.STATE_NORMAL]
        alloc         = self.get_allocation ()
        width, height = alloc.width, alloc.height
        x,     y      = self.x, self.y
        if self.wrap and self.width != width :
            self.layout.set_width (width * 1000)
            self.requested_height = \
                ( self.layout.get_pixel_extents () [1] [3]
                + 2 * self.border_width * self.border
                )
            self.set_size_request (-1, self.requested_height)
        if self.bgcolor :
            self.gc.foreground = self.bgcolor
            self.draw_rectangle (True, 0, 0, width - 1, height - 1)
        if self.border :
            self._draw_border (self.border_state, x, y, width - 1 , height - 1)
            x += 1
            y += 1
        self._draw_content (x, y, width, height)
        self.width, self.height = width, height
    # end def _expose

    def _draw_content (self, x, y, width, height) :
        self.gc.foreground = self._colors.day_text
        self.draw_layout (x, y)
    # end def _draw_content

    def _draw_border (self, state, x, y, width, height) :
        if state :
            color_1, color_2 = self._colors.white, self._colors.black
        else :
            color_2, color_1 = self._colors.white, self._colors.black
        for off in range (self.border_width) :
            for color, line in \
                ( ( color_1
                   , [ (x,         y + height)
                     , (x,         y)
                     , (x + width, y)
                     ]
                  )
                , ( color_2
                  , [ (x + width, y)
                    , (x + width, y + height)
                    , (x,         y + height)
                    ]
                  )
                ) :
                self.gc.foreground = color
                self.window.draw_lines (self.gc, line)
            x      += 1
            y      += 1
            height -= 2
            width  -= 2
    # end def _draw_border

    def draw_layout (self, x, y) :
        self.window.draw_layout (self.gc, x, y, self.layout)
    # end def draw_layout

    def draw_rectangle (self, * args, ** kw) :
        self.window.draw_rectangle (self.gc,* args, ** kw)
    # end def draw_rectangle

# end class Drawing_Area

class Text_Display (Drawing_Area) :
    """A widget whoch has two states and displays different text in these
       states.
    """

    event_binding     = TFL.d_dict \
        ( expose      = "_expose"
        , button_down = "_button_down"
        )

    def __init__ (self, normal, expanded = None, rotated=  True, wrap = False, ** kw) :
        self.__super.__init__ (normal, wrap = wrap, ** kw)
        expanded        = expanded or normal
        if rotated :
            expanded    = "\n".join (expanded)
        self.text       = (normal, expanded)
    # end def __init__

    def _button_down (self, widget, event) :
        if event.button == 1:
            self.border_state = not self.border_state
            self.layout.set_markup (self.text [not self.border_state])
            width, height = self.layout.get_pixel_extents () [1] [2:]
            if self.border :
                width  += 2 * self.border_width
                height += 2 * self.border_width
            self.set_size_request (width, height)
    # end def _button_down

# end class Text_Display

if __name__ != "__main__" :
    TFL.CAL.GTK._Export ("*")
else :
    w = gtk.Window      ()
    w.connect           ("delete-event", gtk.mainquit)
    w.show              ()
    b = gtk.VBox        ()
    b.show              ()
    w.add               (b)
    border = True
    colors = ("entry_even", "entry_odd")
    i      = 0
    for t in ( "Test me and keep the rest up to date whats going on here"
             , "Siingle Liner *g*"
             , "One More"
             ) :
        t1 = Text_Display (t, border = border, bgcolor = colors [i % 2])
        #b.pack_start      (t1, fill = True, expand = False)
        b.add (t1)
        i += 1
    gtk.mainloop        ()
### __END__ TFL.CAL.GTK.Drawing_Area

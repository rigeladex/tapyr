# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
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
#    CAL.TKT.GTK.Day_Cell_Renderer
#
# Purpose
#    «text»···
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _CAL                   import CAL
from   Record                 import Record
import _CAL._TKT
import _CAL._TKT._GTK
import _TGL._TKT._GTK.Generic_Cell_Renderer
import _CAL.Date

class Day_Cell_Renderer (CAL.TKT.GTK.Generic_Cell_Renderer) :
    """A cell renderer for a tree view displaing a day of a calenadar."""

    gtk         = CAL.TKT.GTK.gtk
    layout      = None
    Class_Name  = "Day_Cell_Renderer"
    GTK_Class   = CAL.TKT.GTK.CustomCellRenderer
    Properties  = dict \
        ( day = CAL.TKT.GTK.Object_Property
            (nick = "day", description = "A day object")
        )

    def size_request (self, tree_view, cell_area = None) :
        if not self.layout :
            self.mode           = self.gtk.CELL_RENDERER_MODE_ACTIVATABLE
            self.current_date   = CAL.Date ()
            self.layout         = tree_view.create_pango_layout ("")
            self.colormap       = cm = tree_view.get_colormap        ()
            self.colors         = Record \
                ( month_colors  =
                    (cm.alloc_color ("gray55"), cm.alloc_color ("gray77"))
                , today         = cm.alloc_color ("red")
                , day           = cm.alloc_color ("black")
                , current_month = cm.alloc_color ("lightyellow")
                , current_week  = cm.alloc_color ("yellow")
                , weekend       = cm.alloc_color ("blue")
                )
        self.layout.set_text ("Mo")
        w, h = self.layout.get_pixel_extents () [0] [2:]
        return (0, 0, w + 15, h)
    # end def size_request

    def render ( self
               , window
               , tree_view
               , bg_area
               , cell_area
               , expose_area
               , flags
               ) :
        self.layout.set_text ("%2d" % (self.day.day, ))
        memory  = tree_view.get_data ("ktw_object").AC.memory
        style   = tree_view.get_style ()
        bg_gc   = style.bg_gc  [self.gtk.STATE_NORMAL]
        fg_gc   = style.fg_gc  [self.gtk.STATE_NORMAL]
        bg_fg   = bg_gc.foreground
        fg_fg   = fg_gc.foreground
        day     = self.day
        month   = day.month
        colors  = self.colors
        if day.week == memory.current_day.week :
            bg_gc.foreground = colors.current_week
        elif month == self.current_date.month  :
            bg_gc.foreground = colors.current_month
        else :
            bg_gc.foreground = colors.month_colors [month % 2]
        window.draw_rectangle (bg_gc, True, * list (bg_area))
        if self.day.date == memory.current_day :
            style.paint_focus \
                ( window, self.gtk.STATE_NORMAL, bg_area, tree_view
                , "day focus", * list (cell_area)
                )
        if day == self.current_date :
            fg_col = colors.today
        elif not day.is_weekday :
            fg_col = colors.weekend
        else :
            fg_col = colors.day
        fg_gc.foreground = fg_col
        window.draw_layout (fg_gc, cell_area.x + 2, cell_area.y - 2, self.layout)
        bg_gc.foreground = bg_fg
        fg_gc.foreground = fg_fg
    # end def render

    def activate (self, event, widget, path, bg_area, cell_area, flags) :
        memory             = widget.get_data ("ktw_object").AC.memory
        memory.current_day = self.day.date
    # end def activate

# end class Day_Cell_Renderer

if __name__ != "__main__" :
    CAL.TKT.GTK._Export ("Day_Cell_Renderer")
### __END__ CAL.TKT.GTK.Day_Cell_Renderer

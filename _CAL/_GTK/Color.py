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
#    CAL.GTK.Color
#
# Purpose
#    Color handling and definition of the calendar
#
# Revision Dates
#    10-Feb-2004 (MG)  Creation
#    03-Oct-2004 (MGL) Use new `TFL.Date_Time` module
#    ««revision-date»»···
#--
import  pygtk
pygtk.require ("2.0")
import gtk

from   _TFL               import TFL
import _TFL.Date_Time
import _TFL._Meta.Object

class Color (TFL.Meta.Object) :
    """Simplified color handling of GTK."""

    colors     = {}
    instance   = None
    color_list = dict \
        ( white           = (65535, ) * 3
        , black           = (    0, ) * 3
        , week_number     = (51400, 51400, 51400)
        , odd_month       = (56283, 55769, 54227)
        , even_month      = (51400, 50115, 48573)
        , today           = (51657, 57825, 65535)
#        , today           = (50000, 50000,     0)
        , load_null       = (20000, 65535, 20000)
        , load_full       = (65535,     0,     0)
        , day_text        = (    0,     0,     0)
        , entry_even      = (    0, 32896, 65535)
        , entry_odd       = (    0, 12593, 25186)
        )

    def __new__ (cls, widget) :
        if cls.instance :
            return cls.instance
        self = cls.instance = TFL.Meta.Object.__new__ (cls)
        cm   = widget.get_colormap ()
        for name, color in self.color_list.iteritems () :
            self.colors [name] = cm.alloc_color (* color)
        return self
    # end def __new__

    def color_of_day (self, date, today = True) :
        if today and date == TFL.Date.today () :
            return self.colors ["today"]
        else :
            return ( self.colors ["even_month"], self.colors ["odd_month"]
                   ) [date.month % 2]
    # end def color_of_day

    def __getattr__ (self, name) :
        if name in self.color_list :
            return self.colors [name]
        raise AttributeError, name
    # end def __getattr__

# end class Color

if __name__ != "__main__" :
    import _CAL._GTK
    CAL.GTK._Export ("Color")
### __END__ CAL.GTK.Color

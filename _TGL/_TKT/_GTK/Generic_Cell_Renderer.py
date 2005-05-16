# -*- coding: iso-8859-1 -*-
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
#    TGL.TKT.GTK.Generic_Cell_Renderer
#
# Purpose
#    Wrapper for the GTK widget GenericCellRenderer
#
# Revision Dates
#    15-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Cell_Renderer
import  gobject

class CustomCellRenderer (GTK.gtk.GenericCellRenderer) :
    """GTK class with allows easy ceration of a custom cell renderer"""

    def on_get_size (gtk_obj, * args) :
        self = gtk_obj.get_data ("ktw_object")
        return self.size_request (* args)
    # end def on_get_size

    def on_render (gtk_obj, * args) :
        self = gtk_obj.get_data ("ktw_object")
        return self.render (* args)
    # end def on_render

    def on_activate (gtk_obj, * args) :
        self = gtk_obj.get_data ("ktw_object")
        if hasattr (self, "activate") :
            return self.activate (* args)
    # end def on_activate

    def on_start_editing (gtk_obj, * args) :
        self = gtk_obj.get_data ("ktw_object")
        if hasattr (self, "start_editing") :
            return self.start_editing (* args)
    # end def on_start_editing

# end class CustomCellRenderer

gobject.type_register (CustomCellRenderer)

class Generic_Cell_Renderer (GTK.Cell_Renderer) :
    """Wrapper for the GTK widget GenericCellRenderer"""

    GTK_Class        = CustomCellRenderer

    __gtk_properties = \
        (
        )

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
    # end def __init__

# end class Generic_Cell_Renderer

if __name__ != "__main__" :
    GTK._Export ("Generic_Cell_Renderer", "CustomCellRenderer")
### __END__ TGL.TKT.GTK.Generic_Cell_Renderer

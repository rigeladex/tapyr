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
#    TGL.TKT.GTK.Window
#
# Purpose
#    Wrapper for the GTK widget Window
#
# Revision Dates
#    22-Mar-2005 (MG) Automated creation
#    22-Mar-2005 (MG) Creation continued
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin

class Window (GTK.Bin) :
    """Wrapper for the GTK widget Window"""

    GTK_Class        = GTK.gtk.Window
    __gtk_properties = \
        ( GTK.SG_Property  ("accept_focus")
        , GTK.Property     ("allow_grow")
        , GTK.Property     ("allow_shrink")
        , GTK.SG_Property  ("decorated")
        , GTK.Property     ("default_height")
        , GTK.Property     ("default_width")
        , GTK.SG_Property  ("destroy_with_parent")
        , GTK.SG_Property  ("focus_on_map")
        , GTK.SG_Property  ("gravity")
        , GTK.Property     ("has_toplevel_focus", set = None)
        , GTK.SG_Property  ("icon")
        , GTK.SG_Property  ("icon_name")
        , GTK.Property     ("is_active", set = None)
        , GTK.SG_Property  ("modal")
        , GTK.SG_Property  ("resizable")
        , GTK.SG_Property  ("role")
        , GTK.SG_Property  ("screen")
        , GTK.SG_Property  ("skip_pager_hint")
        , GTK.SG_Property  ("skip_taskbar_hint")
        , GTK.SG_Property  ("title")
        , GTK.Property     ("type")
        , GTK.SG_Property  ("type_hint")
        , GTK.Property     ("window_position")
        )

    def __init__ (self, title = None, ** kw) :
        self.__super.__init__ (** kw)
        if title :
            self.title = title
    # end def __init__

# end class Window

if __name__ != "__main__" :
    GTK._Export ("Window")
### __END__ TGL.TKT.GTK.Window

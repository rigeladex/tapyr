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
#    TGL.TKT.GTK.Tree_View
#
# Purpose
#    Wrapper for the GTK widget TreeView
#
# Revision Dates
#    22-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container

class Tree_View (GTK.Container) :
    """Wrapper for the GTK widget TreeView"""

    GTK_Class        = GTK.gtk.TreeView
    __gtk_properties = \
        ( GTK.SG_Property  ("enable_search")
        , GTK.SG_Property  ("expander_column")
        , GTK.SG_Property  ("fixed_height_mode")
        , GTK.SG_Property  ("hadjustment")
        , GTK.Property     ("headers_clickable")
        , GTK.SG_Property  ("headers_visible")
        , GTK.SG_Property  ("hover_expand")
        , GTK.SG_Property  ("hover_selection")
        , GTK.SG_Property  ("model")
        , GTK.SG_Property  ("reorderable")
        , GTK.SG_Property  ("rules_hint")
        , GTK.SG_Property  ("search_column")
        , GTK.SG_Property  ("vadjustment")
        )

# end class Tree_View

if __name__ != "__main__" :
    GTK._Export ("Tree_View")
### __END__ TGL.TKT.GTK.Tree_View

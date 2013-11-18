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
#    TGL.TKT.GTK.Cell_Renderer_Text
#
# Purpose
#    Wrapper for the GTK widget CellRendererText
#
# Revision Dates
#    27-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Cell_Renderer

class Cell_Renderer_Text (GTK.Cell_Renderer) :
    """Wrapper for the GTK widget CellRendererText"""

    GTK_Class        = GTK.gtk.CellRendererText
    __gtk_properties = \
        ( GTK.Property            ("attributes")
        , GTK.Property            ("background", get = None)
        , GTK.Property            ("background_gdk")
        , GTK.Property            ("background_set")
        , GTK.Property            ("editable")
        , GTK.Property            ("editable_set")
        , GTK.Property            ("ellipsize")
        , GTK.Property            ("ellipsize_set")
        , GTK.Property            ("family")
        , GTK.Property            ("family_set")
        , GTK.Property            ("font")
        , GTK.Property            ("font_desc")
        , GTK.Property            ("foreground", get = None)
        , GTK.Property            ("foreground_gdk")
        , GTK.Property            ("foreground_set")
        , GTK.Property            ("language")
        , GTK.Property            ("language_set")
        , GTK.Property            ("markup", get = None)
        , GTK.Property            ("rise")
        , GTK.Property            ("rise_set")
        , GTK.Property            ("scale")
        , GTK.Property            ("scale_set")
        , GTK.Property            ("single_paragraph_mode")
        , GTK.Property            ("size")
        , GTK.Property            ("size_points")
        , GTK.Property            ("size_set")
        , GTK.Property            ("stretch")
        , GTK.Property            ("stretch_set")
        , GTK.Property            ("strikethrough")
        , GTK.Property            ("strikethrough_set")
        , GTK.Property            ("style")
        , GTK.Property            ("style_set")
        , GTK.Property            ("text")
        , GTK.Property            ("underline")
        , GTK.Property            ("underline_set")
        , GTK.Property            ("variant")
        , GTK.Property            ("variant_set")
        , GTK.Property            ("weight")
        , GTK.Property            ("weight_set")
        , GTK.Property            ("width_chars")
        )

# end class Cell_Renderer_Text

if __name__ != "__main__" :
    GTK._Export ("Cell_Renderer_Text")
### __END__ TGL.TKT.GTK.Cell_Renderer_Text

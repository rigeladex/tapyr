# -*- coding: utf-8 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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

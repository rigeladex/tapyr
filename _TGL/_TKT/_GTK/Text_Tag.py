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
#    TGL.TKT.GTK.Text_Tag
#
# Purpose
#    Wrapper for the GTK widget TextTag
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.G_Object

class Text_Tag (GTK.G_Object) :
    """Wrapper for the GTK widget TextTag"""

    GTK_Class        = GTK.gtk.TextTag
    __gtk_properties = \
        ( GTK.Property            ("background", get = None)
        , GTK.Property            ("background_full_height")
        , GTK.Property            ("background_full_height_set")
        , GTK.Property            ("background_gdk")
        , GTK.Property            ("background_set")
        , GTK.Property            ("background_stipple")
        , GTK.Property            ("background_stipple_set")
        , GTK.Property            ("direction")
        , GTK.Property            ("editable")
        , GTK.Property            ("editable_set")
        , GTK.Property            ("family")
        , GTK.Property            ("family_set")
        , GTK.Property            ("font")
        , GTK.Property            ("font_desc")
        , GTK.Property            ("foreground", get = None)
        , GTK.Property            ("foreground_gdk")
        , GTK.Property            ("foreground_set")
        , GTK.Property            ("foreground_stipple")
        , GTK.Property            ("foreground_stipple_set")
        , GTK.Property            ("indent")
        , GTK.Property            ("indent_set")
        , GTK.Property            ("invisible")
        , GTK.Property            ("invisible_set")
        , GTK.Property            ("justification")
        , GTK.Property            ("justification_set")
        , GTK.Property            ("language")
        , GTK.Property            ("language_set")
        , GTK.Property            ("left_margin")
        , GTK.Property            ("left_margin_set")
        , GTK.Property            ("name")
        , GTK.Property            ("pixels_above_lines")
        , GTK.Property            ("pixels_above_lines_set")
        , GTK.Property            ("pixels_below_lines")
        , GTK.Property            ("pixels_below_lines_set")
        , GTK.Property            ("pixels_inside_wrap")
        , GTK.Property            ("pixels_inside_wrap_set")
        , GTK.Property            ("right_margin")
        , GTK.Property            ("right_margin_set")
        , GTK.Property            ("rise")
        , GTK.Property            ("rise_set")
        , GTK.Property            ("scale")
        , GTK.Property            ("scale_set")
        , GTK.Property            ("size")
        , GTK.Property            ("size_points")
        , GTK.Property            ("size_set")
        , GTK.Property            ("stretch")
        , GTK.Property            ("stretch_set")
        , GTK.Property            ("strikethrough")
        , GTK.Property            ("strikethrough_set")
        , GTK.Property            ("style")
        , GTK.Property            ("style_set")
        , GTK.Property            ("tabs")
        , GTK.Property            ("tabs_set")
        , GTK.Property            ("underline")
        , GTK.Property            ("underline_set")
        , GTK.Property            ("variant")
        , GTK.Property            ("variant_set")
        , GTK.Property            ("weight")
        , GTK.Property            ("weight_set")
        , GTK.Property            ("wrap_mode")
        , GTK.Property            ("wrap_mode_set")
        )

# end class Text_Tag

if __name__ != "__main__" :
    GTK._Export ("Text_Tag")
### __END__ TGL.TKT.GTK.Text_Tag

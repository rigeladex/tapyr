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
#    TGL.TKT.GTK.Cell_Renderer
#
# Purpose
#    Wrapper for the GTK widget CellRenderer
#
# Revision Dates
#    27-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object

class Cell_Renderer (GTK.Object) :
    """Wrapper for the GTK widget CellRenderer"""

    GTK_Class        = GTK.gtk.CellRenderer
    __gtk_properties = \
        ( GTK.Property     ("cell_background", get = None)
        , GTK.Property     ("cell_background_gdk")
        , GTK.Property     ("cell_background_set")
        , GTK.Property     ("height")
        , GTK.Property     ("is_expanded")
        , GTK.Property     ("is_expander")
        , GTK.Property     ("mode")
        , GTK.Property     ("sensitive")
        , GTK.Property     ("visible")
        , GTK.Property     ("width")
        , GTK.Property     ("xalign")
        , GTK.Property     ("xpad")
        , GTK.Property     ("yalign")
        , GTK.Property     ("ypad")
        )

# end class Cell_Renderer

if __name__ != "__main__" :
    GTK._Export ("Cell_Renderer")
### __END__ TGL.TKT.GTK.Cell_Renderer

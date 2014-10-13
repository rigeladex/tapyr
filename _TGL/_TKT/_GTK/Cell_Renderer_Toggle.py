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
#    TGL.TKT.GTK.Cell_Renderer_Toggle
#
# Purpose
#    Wrapper for the GTK widget CellRendererToggle
#
# Revision Dates
#    27-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Cell_Renderer

class Cell_Renderer_Toggle (GTK.Cell_Renderer) :
    """Wrapper for the GTK widget CellRendererToggle"""

    GTK_Class        = GTK.gtk.CellRendererToggle
    __gtk_properties = \
        ( GTK.Property            ("activatable")
        , GTK.SG_Property         ("active")
        , GTK.Property            ("inconsistent")
        , GTK.SG_Property         ("radio")
        )

# end class Cell_Renderer_Toggle

if __name__ != "__main__" :
    GTK._Export ("*")
### __END__ TGL.TKT.GTK.Cell_Renderer_Toggle

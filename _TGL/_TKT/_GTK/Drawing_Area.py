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
#    TGL.TKT.GTK.Drawing_Area
#
# Purpose
#    Wrapper for the GTK widget DrawingArea
#
# Revision Dates
#    08-Sep-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Widget

class Drawing_Area (GTK.Widget) :
    """Wrapper for the GTK widget DrawingArea"""

    GTK_Class        = GTK.gtk.DrawingArea
    __gtk_properties = \
        (
        )

# end class Drawing_Area

if __name__ != "__main__" :
    GTK._Export ("Drawing_Area")
### __END__ TGL.TKT.GTK.Drawing_Area

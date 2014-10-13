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
#    TGL.TKT.GTK.Button
#
# Purpose
#    Wrapper for the GTK widget Button
#
# Revision Dates
#    31-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin

class Button (GTK.Bin) :
    """Wrapper for the GTK widget Button"""

    GTK_Class        = GTK.gtk.Button
    __gtk_properties = \
        ( GTK.SG_Property         ("focus_on_click")
        , GTK.SG_Object_Property  ("image")
        , GTK.SG_Property         ("label")
        , GTK.SG_Property         ("relief")
        , GTK.SG_Property         ("use_stock")
        , GTK.SG_Property         ("use_underline")
        , GTK.Property            ("xalign")
        , GTK.Property            ("yalign")
        )

# end class Button

if __name__ != "__main__" :
    GTK._Export ("Button")
### __END__ TGL.TKT.GTK.Button

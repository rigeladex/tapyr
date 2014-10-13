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
#    TGL.TKT.GTK.Scrolled_Window
#
# Purpose
#    Wrapper for the GTK widget ScrolledWindow
#
# Revision Dates
#    03-Apr-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin

class Scrolled_Window (GTK.Bin) :
    """Wrapper for the GTK widget ScrolledWindow"""

    GTK_Class        = GTK.gtk.ScrolledWindow
    __gtk_properties = \
        ( GTK.SG_Object_Property  ("hadjustment")
        , GTK.Property            ("hscrollbar_policy")
        , GTK.SG_Property         ("shadow_type")
        , GTK.SG_Object_Property  ("vadjustment")
        , GTK.Property            ("vscrollbar_policy")
        , GTK.Property            ("window_placement")
        )

# end class Scrolled_Window

if __name__ != "__main__" :
    GTK._Export ("Scrolled_Window")
### __END__ TGL.TKT.GTK.Scrolled_Window

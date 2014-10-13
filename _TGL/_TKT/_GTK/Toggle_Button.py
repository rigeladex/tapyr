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
#    TGL.TKT.GTK.Toggle_Button
#
# Purpose
#    Wrapper for the GTK widget ToggleButton
#
# Revision Dates
#    09-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Button

class Toggle_Button (GTK.Button) :
    """Wrapper for the GTK widget ToggleButton"""

    GTK_Class        = GTK.gtk.ToggleButton
    __gtk_properties = \
        ( GTK.SG_Property         ("active")
        , GTK.Property            ("draw_indicator")
        , GTK.SG_Property         ("inconsistent")
        )

# end class Toggle_Button

if __name__ != "__main__" :
    GTK._Export ("Toggle_Button")
### __END__ TGL.TKT.GTK.Toggle_Button

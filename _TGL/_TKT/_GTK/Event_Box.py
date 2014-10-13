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
#    TGL.TKT.GTK.Event_Box
#
# Purpose
#    Wrapper for the GTK widget EventBox
#
# Revision Dates
#    28-Mar-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin

class Event_Box (GTK.Bin) :
    """Wrapper for the GTK widget EventBox"""

    GTK_Class        = GTK.gtk.EventBox
    __gtk_properties = \
        ( GTK.SG_Property         ("above_child")
        , GTK.SG_Property         ("visible_window")
        )

# end class Event_Box

if __name__ != "__main__" :
    GTK._Export ("Event_Box")
### __END__ TGL.TKT.GTK.Event_Box

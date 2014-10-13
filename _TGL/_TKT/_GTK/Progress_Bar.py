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
#    TGL.TKT.GTK.Progress_Bar
#
# Purpose
#    Wrapper for the GTK widget ProgressBar
#
# Revision Dates
#    20-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Progress

class Progress_Bar (GTK.Progress) :
    """Wrapper for the GTK widget ProgressBar"""

    GTK_Class        = GTK.gtk.ProgressBar
    __gtk_properties = \
        ( GTK.Property            ("activity_blocks")
        , GTK.Property            ("activity_step")
        , GTK.SG_Object_Property  ("adjustment")
        , GTK.Property            ("bar_style")
        , GTK.Property            ("discrete_blocks")
        , GTK.SG_Property         ("ellipsize")
        , GTK.SG_Property         ("fraction")
        , GTK.SG_Property         ("orientation")
        , GTK.SG_Property         ("pulse_step")
        , GTK.SG_Property         ("text")
        )

# end class Progress_Bar

if __name__ != "__main__" :
    GTK._Export ("Progress_Bar")
### __END__ TGL.TKT.GTK.Progress_Bar

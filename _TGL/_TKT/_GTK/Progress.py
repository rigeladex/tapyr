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
#    TGL.TKT.GTK.Progress
#
# Purpose
#    Wrapper for the GTK widget Progress
#
# Revision Dates
#    20-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Widget

class Progress (GTK.Widget) :
    """Wrapper for the GTK widget Progress"""

    GTK_Class        = GTK.gtk.Progress
    __gtk_properties = \
        ( GTK.Property            ("activity_mode")
        , GTK.Property            ("show_text")
        , GTK.Property            ("text_xalign")
        , GTK.Property            ("text_yalign")
        )

# end class Progress

if __name__ != "__main__" :
    GTK._Export ("Progress")
### __END__ TGL.TKT.GTK.Progress

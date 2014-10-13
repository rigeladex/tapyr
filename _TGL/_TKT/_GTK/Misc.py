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
#    TGL.TKT.GTK.Misc
#
# Purpose
#    Wrapper for the GTK widget Misc
#
# Revision Dates
#    2005-Mar-22 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Widget

class Misc (GTK.Widget) :
    """Wrapper for the GTK widget Misc"""

    GTK_Class        = GTK.gtk.Misc
    __gtk_properties = \
        ( GTK.Property     ("xalign")
        , GTK.Property     ("xpad")
        , GTK.Property     ("yalign")
        , GTK.Property     ("ypad")
        )

# end class Misc

if __name__ != "__main__" :
    GTK._Export ("Misc")
### __END__ TGL.TKT.GTK.Misc

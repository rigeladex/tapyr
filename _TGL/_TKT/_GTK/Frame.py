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
#    TGL.TKT.GTK.Frame
#
# Purpose
#    Wrapper for the GTK widget Frame
#
# Revision Dates
#    09-May-2005 (MG) Automated creation
#     9-May-2005 (MG) Deprecated property `shadow` removed
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin

class Frame (GTK.Bin) :
    """Wrapper for the GTK widget Frame"""

    GTK_Class        = GTK.gtk.Frame
    __gtk_properties = \
        ( GTK.SG_Property         ("label")
        , GTK.SG_Object_Property  ("label_widget")
        , GTK.Property            ("label_xalign")
        , GTK.Property            ("label_yalign")
        , GTK.SG_Property         ("shadow_type")
        )

# end class Frame

if __name__ != "__main__" :
    GTK._Export ("Frame")
### __END__ TGL.TKT.GTK.Frame

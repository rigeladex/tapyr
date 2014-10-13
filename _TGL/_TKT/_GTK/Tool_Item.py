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
#    TGL.TKT.GTK.Tool_Item
#
# Purpose
#    Wrapper for the GTK widget ToolItem
#
# Revision Dates
#    09-Apr-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin

class Tool_Item (GTK.Bin) :
    """Wrapper for the GTK widget ToolItem"""

    GTK_Class        = GTK.gtk.ToolItem
    __gtk_properties = \
        ( GTK.SG_Property         ("is_important")
        , GTK.SG_Property         ("visible_horizontal")
        , GTK.SG_Property         ("visible_vertical")
        )

# end class Tool_Item

if __name__ != "__main__" :
    GTK._Export ("Tool_Item")
### __END__ TGL.TKT.GTK.Tool_Item

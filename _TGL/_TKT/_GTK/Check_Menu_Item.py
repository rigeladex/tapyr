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
#    TGL.TKT.GTK.Check_Menu_Item
#
# Purpose
#    Wrapper for the GTK widget CheckMenuItem
#
# Revision Dates
#    09-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Menu_Item

class Check_Menu_Item (GTK.Menu_Item) :
    """Wrapper for the GTK widget CheckMenuItem"""

    GTK_Class        = GTK.gtk.CheckMenuItem
    __gtk_properties = \
        ( GTK.SG_Property         ("active")
        , GTK.SG_Property         ("draw_as_radio")
        , GTK.SG_Property         ("inconsistent")
        )

# end class Check_Menu_Item

if __name__ != "__main__" :
    GTK._Export ("Check_Menu_Item")
### __END__ TGL.TKT.GTK.Check_Menu_Item

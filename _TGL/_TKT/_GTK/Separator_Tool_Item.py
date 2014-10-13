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
#    TGL.TKT.GTK.Separator_Tool_Item
#
# Purpose
#    Wrapper for the GTK widget SeparatorToolItem
#
# Revision Dates
#    09-Apr-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Tool_Item

class Separator_Tool_Item (GTK.Tool_Item) :
    """Wrapper for the GTK widget SeparatorToolItem"""

    GTK_Class        = GTK.gtk.SeparatorToolItem
    __gtk_properties = \
        ( GTK.SG_Property         ("draw")
        ,
        )

# end class Separator_Tool_Item

if __name__ != "__main__" :
    GTK._Export ("Separator_Tool_Item")
### __END__ TGL.TKT.GTK.Separator_Tool_Item

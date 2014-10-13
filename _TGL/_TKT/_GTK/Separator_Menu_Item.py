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
#    TGL.TKT.GTK.Separator_Menu_Item
#
# Purpose
#    Wrapper for the GTK widget SeparatorMenuItem
#
# Revision Dates
#    08-Apr-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Menu_Item

class Separator_Menu_Item (GTK.Menu_Item) :
    """Wrapper for the GTK widget SeparatorMenuItem"""

    GTK_Class        = GTK.gtk.SeparatorMenuItem
    __gtk_properties = \
        ( 
        )

# end class Separator_Menu_Item

if __name__ != "__main__" :
    GTK._Export ("Separator_Menu_Item")
### __END__ TGL.TKT.GTK.Separator_Menu_Item

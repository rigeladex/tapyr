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
#    TGL.TKT.GTK.Item
#
# Purpose
#    Wrapper for the GTK widget Item
#
# Revision Dates
#    07-Apr-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Bin

class Item (GTK.Bin) :
    """Wrapper for the GTK widget Item"""

    GTK_Class        = GTK.gtk.Item
    __gtk_properties = \
        ( 
        )

# end class Item

if __name__ != "__main__" :
    GTK._Export ("Item")
### __END__ TGL.TKT.GTK.Item

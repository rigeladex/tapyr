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
#    TGL.TKT.GTK.V_Box
#
# Purpose
#    Wrapper for the GTK widget VBox
#
# Revision Dates
#    2005-Mar-22 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Box

class V_Box (GTK.Box) :
    """Wrapper for the GTK widget VBox"""

    GTK_Class        = GTK.gtk.VBox
    __gtk_properties = \
        ( 
        )

# end class V_Box

if __name__ != "__main__" :
    GTK._Export ("V_Box")
### __END__ TGL.TKT.GTK.V_Box

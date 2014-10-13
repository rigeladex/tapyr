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
#    TGL.TKT.GTK.H_Button_Box
#
# Purpose
#    Wrapper for the GTK widget HButtonBox
#
# Revision Dates
#    09-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Button_Box

class H_Button_Box (GTK.Button_Box) :
    """Wrapper for the GTK widget HButtonBox"""

    GTK_Class        = GTK.gtk.HButtonBox
    __gtk_properties = \
        ( 
        )

# end class H_Button_Box

if __name__ != "__main__" :
    GTK._Export ("H_Button_Box")
### __END__ TGL.TKT.GTK.H_Button_Box

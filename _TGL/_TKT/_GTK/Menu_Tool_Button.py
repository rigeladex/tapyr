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
#    TGL.TKT.GTK.Menu_Tool_Button
#
# Purpose
#    Wrapper for the GTK widget MenuToolButton
#
# Revision Dates
#    09-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Tool_Button

class Menu_Tool_Button (GTK.Tool_Button) :
    """Wrapper for the GTK widget MenuToolButton"""

    GTK_Class        = GTK.gtk.MenuToolButton
    __gtk_properties = \
        ( GTK.SG_Object_Property  ("menu")
        ,
        )

# end class Menu_Tool_Button

if __name__ != "__main__" :
    GTK._Export ("Menu_Tool_Button")
### __END__ TGL.TKT.GTK.Menu_Tool_Button

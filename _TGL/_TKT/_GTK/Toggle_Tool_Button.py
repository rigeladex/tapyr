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
#    TGL.TKT.GTK.Toggle_Tool_Button
#
# Purpose
#    Wrapper for the GTK widget ToggleToolButton
#
# Revision Dates
#    09-May-2005 (MG) Automated creation
#     9-May-2005 (MG) Property `active` added
#     9-May-2005 (MG) `_init_attrs` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Tool_Button

class Toggle_Tool_Button (GTK.Tool_Button) :
    """Wrapper for the GTK widget ToggleToolButton"""

    GTK_Class        = GTK.gtk.ToggleToolButton
    __gtk_properties = \
        ( GTK.SG_Property         ("active")
        ,
        )

    def _init_attrs (self, label, ** kw) :
        return dict (kw, stock_id = label)
    # end def _init_attrs

# end class Toggle_Tool_Button

if __name__ != "__main__" :
    GTK._Export ("Toggle_Tool_Button")
### __END__ TGL.TKT.GTK.Toggle_Tool_Button

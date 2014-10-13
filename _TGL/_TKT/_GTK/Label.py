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
#    TGL.TKT.GTK.Label
#
# Purpose
#    Wrapper for the GTK widget Label
#
# Revision Dates
#    22-Mar-2005 (MG) Automated creation
#    15-May-2005 (MG) `mnemonic_widget` corrected
#    14-Aug-2005 (MG) Property `text` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Misc

class Label (GTK.Misc) :
    """Wrapper for the GTK widget Label"""

    GTK_Class        = GTK.gtk.Label
    __gtk_properties = \
        ( GTK.SG_Property         ("angle")
        , GTK.SG_Property         ("attributes")
        , GTK.Property            ("cursor_position", set = None)
        , GTK.SG_Property         ("ellipsize")
        , GTK.SG_Property         ("justify")
        , GTK.SG_Property         ("label")
        , GTK.SG_Property         ("max_width_chars")
        , GTK.SG_Property         ("mnemonic_keyval", set = None)
        , GTK.SG_Object_Property  ("mnemonic_widget")
        , GTK.SG_Property         ("pattern", get = None)
        , GTK.SG_Property         ("selectable")
        , GTK.Property            ("selection_bound", set = None)
        , GTK.SG_Property         ("single_line_mode")
        , GTK.SG_Property         ("text")
        , GTK.SG_Property         ("use_markup")
        , GTK.SG_Property         ("use_underline")
        , GTK.SG_Property         ("width_chars")
        , GTK.Property            ("wrap")
        )

# end class Label

if __name__ != "__main__" :
    GTK._Export ("Label")
else :
    from _TGL._TKT._GTK import GTK
    import _TGL._TKT._GTK.V_Box
    import _TGL._TKT._GTK.Test_Window

    b        = GTK.V_Box ()
    l1       = Label     ("Foo Bar")
    l2       = Label     ()
    l1.wrap  = l2.wrap = True
    l2.label = "Foo Bar" * 40
    b.pack         (l1, expand = False, fill = True)
    b.pack         (l2, expand = False, fill = True)
    w = GTK.Test_Window (title = "Test Label", child = b)
    w.show_all     ()
    GTK.main       ()
### __END__ TGL.TKT.GTK.Label

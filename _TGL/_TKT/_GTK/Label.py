# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
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
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Misc

class Label (GTK.Misc) :
    """Wrapper for the GTK widget Label"""

    GTK_Class        = GTK.gtk.Label
    __gtk_properties = \
        ( GTK.SG_Property  ("angle")
        , GTK.SG_Property  ("attributes")
        , GTK.Property     ("cursor_position", set = None)
        , GTK.SG_Property  ("ellipsize")
        , GTK.SG_Property  ("justify")
        , GTK.SG_Property  ("label")
        , GTK.SG_Property  ("max_width_chars")
        , GTK.SG_Property  ("mnemonic_keyval", set = None)
        , GTK.SG_Property  ("mnemonic_widget")
        , GTK.SG_Property  ("pattern", get = None)
        , GTK.SG_Property  ("selectable")
        , GTK.Property     ("selection_bound", set = None)
        , GTK.SG_Property  ("single_line_mode")
        , GTK.SG_Property  ("use_markup")
        , GTK.SG_Property  ("use_underline")
        , GTK.SG_Property  ("width_chars")
        , GTK.Property     ("wrap")
        )

# end class Label

if __name__ != "__main__" :
    GTK._Export ("Label")
else :
    from _TGL._TKT._GTK import GTK
    import _TGL._TKT._GTK.V_Box
    import _TGL._TKT._GTK.Window
    import _TGL._TKT._GTK.Signal

    b        = GTK.V_Box ()
    l1       = Label     ("Foo Bar")
    l2       = Label     ()
    l1.wrap  = l2.wrap = True
    l2.label = "Foo Bar" * 40
    b.pack         (l1, expand = False, fill = True)
    b.pack         (l2, expand = False, fill = True)
    w = GTK.Window (title = "Test Label", child = b)
    w.show_all     ()
    w.bind_add     (GTK.Signal.Destroy, GTK.quit)
    GTK.main       ()

### __END__ TGL.TKT.GTK.Label

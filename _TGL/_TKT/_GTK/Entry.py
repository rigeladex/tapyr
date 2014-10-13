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
#    TGL.TKT.GTK.Entry
#
# Purpose
#    Wrapper for the GTK widget Entry
#
# Revision Dates
#    21-May-2005 (MG) Automated creation
#     3-Jun-2005 (MG) `get` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Widget

class Entry (GTK.Widget) :
    """Wrapper for the GTK widget Entry"""

    GTK_Class        = GTK.gtk.Entry
    __gtk_properties = \
        ( GTK.SG_Property         ("activates_default")
        , GTK.Property            ("cursor_position", set = None)
        , GTK.SG_Property         ("editable")
        , GTK.SG_Property         ("has_frame")
        , GTK.SG_Property         ("invisible_char")
        , GTK.SG_Property         ("max_length")
        , GTK.Property            ("scroll_offset", set = None)
        , GTK.Property            ("selection_bound", set = None)
        , GTK.SG_Property         ("text")
        , GTK.SG_Property         ("visibility")
        , GTK.SG_Property         ("width_chars")
        , GTK.Property            ("xalign")
        )

    def get (self) :
        return self.text
    # end def get

# end class Entry

if __name__ != "__main__" :
    GTK._Export ("Entry")
### __END__ TGL.TKT.GTK.Entry

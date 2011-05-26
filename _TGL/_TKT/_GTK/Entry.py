# -*- coding: iso-8859-15 -*-
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

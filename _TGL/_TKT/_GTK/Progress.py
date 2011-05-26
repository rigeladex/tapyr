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
#    TGL.TKT.GTK.Progress
#
# Purpose
#    Wrapper for the GTK widget Progress
#
# Revision Dates
#    20-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Widget

class Progress (GTK.Widget) :
    """Wrapper for the GTK widget Progress"""

    GTK_Class        = GTK.gtk.Progress
    __gtk_properties = \
        ( GTK.Property            ("activity_mode")
        , GTK.Property            ("show_text")
        , GTK.Property            ("text_xalign")
        , GTK.Property            ("text_yalign")
        )

# end class Progress

if __name__ != "__main__" :
    GTK._Export ("Progress")
### __END__ TGL.TKT.GTK.Progress

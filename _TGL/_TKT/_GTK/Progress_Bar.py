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
#    TGL.TKT.GTK.Progress_Bar
#
# Purpose
#    Wrapper for the GTK widget ProgressBar
#
# Revision Dates
#    20-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Progress

class Progress_Bar (GTK.Progress) :
    """Wrapper for the GTK widget ProgressBar"""

    GTK_Class        = GTK.gtk.ProgressBar
    __gtk_properties = \
        ( GTK.Property            ("activity_blocks")
        , GTK.Property            ("activity_step")
        , GTK.SG_Object_Property  ("adjustment")
        , GTK.Property            ("bar_style")
        , GTK.Property            ("discrete_blocks")
        , GTK.SG_Property         ("ellipsize")
        , GTK.SG_Property         ("fraction")
        , GTK.SG_Property         ("orientation")
        , GTK.SG_Property         ("pulse_step")
        , GTK.SG_Property         ("text")
        )

# end class Progress_Bar

if __name__ != "__main__" :
    GTK._Export ("Progress_Bar")
### __END__ TGL.TKT.GTK.Progress_Bar

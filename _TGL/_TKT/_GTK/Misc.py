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
#    TGL.TKT.GTK.Misc
#
# Purpose
#    Wrapper for the GTK widget Misc
#
# Revision Dates
#    2005-Mar-22 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Widget

class Misc (GTK.Widget) :
    """Wrapper for the GTK widget Misc"""

    GTK_Class        = GTK.gtk.Misc
    __gtk_properties = \
        ( GTK.Property     ("xalign")
        , GTK.Property     ("xpad")
        , GTK.Property     ("yalign")
        , GTK.Property     ("ypad")
        )

# end class Misc

if __name__ != "__main__" :
    GTK._Export ("Misc")
### __END__ TGL.TKT.GTK.Misc

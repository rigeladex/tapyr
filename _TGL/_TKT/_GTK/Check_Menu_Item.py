# -*- coding: utf-8 -*-
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
#    TGL.TKT.GTK.Check_Menu_Item
#
# Purpose
#    Wrapper for the GTK widget CheckMenuItem
#
# Revision Dates
#    09-May-2005 (MG) Automated creation
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Menu_Item

class Check_Menu_Item (GTK.Menu_Item) :
    """Wrapper for the GTK widget CheckMenuItem"""

    GTK_Class        = GTK.gtk.CheckMenuItem
    __gtk_properties = \
        ( GTK.SG_Property         ("active")
        , GTK.SG_Property         ("draw_as_radio")
        , GTK.SG_Property         ("inconsistent")
        )

# end class Check_Menu_Item

if __name__ != "__main__" :
    GTK._Export ("Check_Menu_Item")
### __END__ TGL.TKT.GTK.Check_Menu_Item

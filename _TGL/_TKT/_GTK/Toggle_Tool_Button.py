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

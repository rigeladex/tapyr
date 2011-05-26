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
#    TGL.TKT.GTK.Tool_Button
#
# Purpose
#    Wrapper for the GTK widget ToolButton
#
# Revision Dates
#    09-Apr-2005 (MG) Automated creation
#     9-Apr-2005 (MG) Support for icons added
#     9-May-2005 (MG) `_init_attrs` factored from `__init__`
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Tool_Item

class Tool_Button (GTK.Tool_Item) :
    """Wrapper for the GTK widget ToolButton"""

    GTK_Class        = GTK.gtk.ToolButton
    __gtk_properties = \
        ( GTK.SG_Object_Property  ("icon_widget")
        , GTK.SG_Property         ("label")
        , GTK.SG_Object_Property  ("label_widget")
        , GTK.SG_Property         ("stock_id")
        , GTK.SG_Property         ("use_underline")
        )

    def __init__ (self, label = None, icon = None, stock = None, ** kw) :
        if not stock :
            self.__super.__init__ (** self._init_attrs (label, ** kw))
            self.icon_widget = icon
        else :
            self.__super.__init__ (stock = stock_id, ** kw)
    # end def __init__

    def _init_attrs (self, label, ** kw) :
        return dict (kw, label = label, icon_widget = None)
    # end def _init_attrs

# end class Tool_Button

if __name__ != "__main__" :
    GTK._Export ("Tool_Button")
### __END__ TGL.TKT.GTK.Tool_Button

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
#    TGL.TKT.GTK.Tree_View_Column
#
# Purpose
#    Wrapper for the GTK widget TreeViewColumn
#
# Revision Dates
#    27-Mar-2005 (MG) Automated creation
#    27-Mar-2005 (MG) Creation continued
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object
import _TGL._TKT._GTK.Pack_Mixin

class Renderer_Wrapper (GTK.FP_Object_Extract) :
    """Converts the first parameter from an int to a Cell_Renderer object"""

    def __call__ (self, renderer, ** kw) :
        if isinstance (renderer, int) :
            renderer = self.owner.renderers [renderer]
        return self.__super.__call__ (renderer, ** kw)
    # end def __call__
# end class Renderer_Wrapper

class Tree_View_Column (GTK.Object, GTK.Pack_Mixin) :
    """Wrapper for the GTK widget TreeViewColumn"""

    GTK_Class        = GTK.gtk.TreeViewColumn
    __gtk_properties = \
        ( GTK.SG_Property  ("alignment")
        , GTK.SG_Property  ("clickable")
        , GTK.SG_Property  ("expand")
        , GTK.SG_Property  ("fixed_width")
        , GTK.SG_Property  ("max_width")
        , GTK.SG_Property  ("min_width")
        , GTK.SG_Property  ("reorderable")
        , GTK.SG_Property  ("resizable")
        , GTK.SG_Property  ("sizing")
        , GTK.SG_Property  ("sort_indicator")
        , GTK.SG_Property  ("sort_order")
        , GTK.SG_Property  ("spacing")
        , GTK.SG_Property  ("title")
        , GTK.SG_Property  ("visible")
        , GTK.SG_Property  ("widget")
        , GTK.SG_Property  ("width", set = None)
        , GTK.SG_Object_List_Property
            ( "renderers", set = None, get_fct_name = "get_cell_renderers")
        )

    _wtk_delegation = dict \
        ( set_attributes = Renderer_Wrapper
        , add_attribute  = Renderer_Wrapper
        , clear          = "clear"
        )

    def __init__ (self, title = None, renderer = None, * args, ** kw) :
        if renderer :
            renderer = renderer.wtk_object
        self.__super.__init__ (title, renderer, * args, ** kw)
    # end def __init__

# end class Tree_View_Column

if __name__ != "__main__" :
    GTK._Export ("Tree_View_Column")
### __END__ TGL.TKT.GTK.Tree_View_Column

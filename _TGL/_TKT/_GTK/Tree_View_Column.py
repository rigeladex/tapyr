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
#    TGL.TKT.GTK.Tree_View_Column
#
# Purpose
#    Wrapper for the GTK widget TreeViewColumn
#
# Revision Dates
#    27-Mar-2005 (MG) Automated creation
#    27-Mar-2005 (MG) Creation continued
#     1-Apr-2005 (MG) `_wtk_delegation` changed
#    16-May-2005 (MG) `sort_column_id` added
#    18-May-2005 (MG) Don't used `Pack_Mixin` (pack does not support the
#                     `fill` property)
#    17-Jun-2005 (MG) `set_cell_function` and `set_renderer_attributes` added
#    28-Dec-2005 (MG) `widget` property fixed
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object
import _TGL._TKT._GTK.Pack_Mixin

class Delegator_R (GTK.Delegator_O) :
    """Converts the first parameter from an int to a Cell_Renderer object"""

    def __call__ (self, this, renderer, ** kw) :
        if isinstance (renderer, int) :
            renderer = this.renderers [renderer]
        return self.__super.__call__ (this, renderer, ** kw)
    # end def __call__

# end class Delegator_R

class Tree_View_Column (GTK.Object) :
    """Wrapper for the GTK widget TreeViewColumn"""

    GTK_Class        = GTK.gtk.TreeViewColumn
    __gtk_properties = \
        ( GTK.SG_Property        ("alignment")
        , GTK.SG_Property        ("clickable")
        , GTK.SG_Property        ("expand")
        , GTK.SG_Property        ("fixed_width")
        , GTK.SG_Property        ("max_width")
        , GTK.SG_Property        ("min_width")
        , GTK.SG_Property        ("reorderable")
        , GTK.SG_Property        ("resizable")
        , GTK.SG_Property        ("sizing")
        , GTK.SG_Property        ("sort_column_id")
        , GTK.SG_Property        ("sort_indicator")
        , GTK.SG_Property        ("sort_order")
        , GTK.SG_Property        ("spacing")
        , GTK.SG_Property        ("title")
        , GTK.SG_Property        ("visible")
        , GTK.SG_Object_Property ("widget")
        , GTK.SG_Property        ("width", set = None)
        , GTK.SG_Object_List_Property
            ("renderers", set = None, get_fct_name = "get_cell_renderers")
        )

    _wtk_delegation = GTK.Delegation \
                          ( Delegator_R   ("set_attributes")
        , Delegator_R     ("add_attribute")
        , GTK.Delegator   ("clear")
        , GTK.Delegator_O ("set_cell_function", "set_cell_data_func")
        )

    def __init__ (self, title = None, renderer = None, * args, ** kw) :
        if renderer :
            renderer = renderer.wtk_object
        self.__super.__init__ (title, renderer, * args, ** kw)
    # end def __init__

    def pack (self, child, start = True, expand = True) :
        if start :
            fct = self.wtk_object.pack_start
        else :
            fct = self.wtk_object.pack_end
        return fct (child.wtk_object, expand = expand)
    # end def pack

    def set_renderer_attributes ( self
                                , tree_view_column
                                , cell_renderer
                                , model
                                , iter
                                , cell
                                ) :
        model = model.get_data ("ktw_object")
        ui = model.ui_object (iter)
        cell._lazy_populate (ui, cell_renderer.get_data ("ktw_object"))
    # end def set_renderer_attributes

# end class Tree_View_Column

if __name__ != "__main__" :
    GTK._Export ("Tree_View_Column")
### __END__ TGL.TKT.GTK.Tree_View_Column

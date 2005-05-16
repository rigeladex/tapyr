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
#    TGL.TKT.GTK.Tree_View
#
# Purpose
#    Wrapper for the GTK widget TreeView
#
# Revision Dates
#    27-Mar-2005 (MG) Automated creation
#    27-Mar-2005 (MG) `__init__` and test added
#     1-Apr-2005 (MG) `_wtk_delegation` changed
#    16-May-2005 (MG) Test case for generic cell renderer added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container

class Tree_View (GTK.Container) :
    """Wrapper for the GTK widget TreeView"""

    GTK_Class        = GTK.gtk.TreeView
    __gtk_properties = \
        ( GTK.SG_Property        ("enable_search")
        , GTK.SG_Object_Property ("expander_column")
        , GTK.SG_Property        ("fixed_height_mode")
        , GTK.SG_Object_Property ("hadjustment")
        , GTK.Property           ("headers_clickable")
        , GTK.SG_Property        ("headers_visible")
        , GTK.SG_Property        ("hover_expand")
        , GTK.SG_Property        ("hover_selection")
        , GTK.SG_Object_Property ("model")
        , GTK.SG_Property        ("reorderable")
        , GTK.SG_Property        ("rules_hint")
        , GTK.SG_Property        ("search_column")
        , GTK.SG_Object_Property ("vadjustment")
        )

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator_O ("append_column")
        )

    def __init__ (self, model = None, * args, ** kw) :
        if model :
            model = model.wtk_object
        self.__super.__init__ (model, * args, ** kw)
    # end def __init__

# end class Tree_View

if __name__ != "__main__" :
    GTK._Export ("Tree_View")
else :
    import _TGL._TKT._GTK.Test_Window
    import _TGL._TKT._GTK.Model
    import _TGL._TKT._GTK.Cell_Renderer_Text
    import _TGL._TKT._GTK.Generic_Cell_Renderer
    import _TGL._TKT._GTK.Tree_View_Column
    from   _TGL._UI.App_Context   import App_Context
    from   _TGL                   import TGL
    AC  = App_Context (TGL)
    gtk = GTK.gtk
    import gobject

    class Cell_Renderer (GTK.Generic_Cell_Renderer) :

        layout      = None
        Class_Name  = "Day_Renderer"
        GTK_Class   = GTK.CustomCellRenderer
        Properties  = dict \
            (day = GTK.Number_Property (gobject.TYPE_UINT, default = 0))

        __gtk_properties = {}
        def size_request (self, tree_view, cell_area = None) :
            if not self.layout :
                self.__class__.layout = tree_view.create_pango_layout ("")
            self.layout.set_text ("99")
            w, h = self.layout.get_pixel_extents () [0] [2:]
            return (w, 6, w, h)
        # end def size_request

        def render ( self
                   , window
                   , tree_view
                   , bg_area
                   , cell_area
                   , expose_area
                   , flags
                   ) :
            self.layout.set_text ("%02d - %d" % (flags, self.day))
            gc = tree_view.get_style ().fg_gc  [flags]
            window.draw_layout \
                ( gc
                , cell_area.x, cell_area.y
                , self.layout
                )
        # end def render

    # end class Cell_Renderer

    t  = GTK.Tree_Model          (str, float, gobject.TYPE_UINT)
    for i in range (10) :
        t.add (("Row_%2d" % (i, ), i / 10.0, i))
    v  = Tree_View               (t)
    r1 = GTK.Cell_Renderer_Text  ()
    c1 = GTK.Tree_View_Column    ("Text-Column", r1)
    c1.set_attributes            (r1, text = 0)

    r2 = GTK.Cell_Renderer_Text  ()
    c2 = GTK.Tree_View_Column    ("Text-Column", r2)
    c2.set_attributes            (0, text = 1)

    r3 = Cell_Renderer           ()
    c3 = GTK.Tree_View_Column    ("Custom-Column", r3)
    c3.set_attributes            (0, day  = 2)


    v.append_column              (c1)
    v.append_column              (c2)
    v.append_column              (c3)
    w  = GTK.Test_Window         ("Tree-View Test", AC = AC)
    w.add                        (v)
    w.show_all                   ()
    GTK.main                     ()
### __END__ TGL.TKT.GTK.Tree_View

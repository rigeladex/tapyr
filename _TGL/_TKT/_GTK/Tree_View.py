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
#    16-May-2005 (MG) `children` redefined, `selected_iters` added
#    10-Jun-2005 (MG) `selection` and `clear_selection` added
#    26-Jul-2005 (MG) Selction handling changed by introducing `Tree_Selection`
#    26-Jul-2005 (MG) New signal `Select` added
#    28-Jul-2005 (MG) `Tree_Selection.next` added
#    30-Jul-2005 (MG) `select_all` added
#     3-Aug-2005 (MG) `__len__`: performance improoved (use GTK internal
#                     function)
#     6-Aug-2005 (MG) `Selection.extend` factored
#     6-Aug-2005 (MG) Basic DND handling added
#     7-Aug-2005 (MG) Debug print removed, `s/_select/extend/g`
#    09-Jan-2006 (MG) `next` and `prev`: `current` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Container
import  gobject

class Tree_Selection (GTK.Object_Wrapper) :
    """Wrapper for the tree selection object."""

    def __init__ (self, wtk_model, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.wtk_model = wtk_model
    # end def __init__

    def set (self, selection) :
        self.wtk_object.unselect_all ()
        self.extend                  (selection)
    # end def set

    def extend (self, selection) :
        model = self.wtk_model
        if not isinstance (selection, (tuple, list)) :
            selection = (selection, )
        for element in filter (None, selection) :
            self.wtk_object.select_iter (model.iter (element))
    # end def extend

    def _tree_iters (self) :
        model, pathes = self.wtk_object.get_selected_rows ()
        if pathes :
            for p in pathes :
                yield model.get_iter (p)
    # end def _tree_iters

    def __iter__ (self) :
        return (self.wtk_model.ui_object (i) for i in self._tree_iters ())
    # end def __iter__

    def __getitem__ (self, index) :
        return tuple (self) [index]
    # end def __getitem__

    def __len__ (self) :
        return self.wtk_object.count_selected_rows ()
    # end def __len__

    def _delta_ (self, current, delta) :
        if current is None :
            selection = tuple (self._tree_iters ())
            if selection :
                current = selection [-1]
        else :
            current = self.wtk_model.iter (current)
        if current :
            iter = self.wtk_model.iter_delta (current, delta)
            if iter :
                return self.wtk_model.ui_object (iter)
    # end def _delta_

    def next (self, delta = 1, current = None) :
        ### returns the object after `current` or None if
        ### the selection oject is the last
        ### if `current` is None, the current selection is used
        return self._delta_ (current, delta)
    # end def next

    def prev (self, delta = 1, current = None) :
        ### returns the object before `current` or None if
        ### the selection oject is the last
        ### if `current` is None, the current selection is used
        return self._delta_ (current, -delta)
    # end def prev

    def all (self) :
        return self.wtk_object.select_all ()
    # end def all

# end class Tree_Selection

class Tree_View (GTK.Container) :
    """Wrapper for the GTK widget TreeView"""

    GTK_Class        = GTK.gtk.TreeView
    Class_Name       = "Tree_View"

    __gtk_properties = \
        ( GTK.SG_Object_List_Property
            ("children", set = None, get_fct_name = "get_columns")
        , GTK.SG_Property             ("enable_search")
        , GTK.SG_Object_Property      ("expander_column")
        , GTK.SG_Property             ("fixed_height_mode")
        , GTK.SG_Object_Property      ("hadjustment")
        , GTK.Property                ("headers_clickable")
        , GTK.SG_Property             ("headers_visible")
        , GTK.SG_Property             ("hover_expand")
        , GTK.SG_Property             ("hover_selection")
        , GTK.SG_Object_Property      ("model")
        , GTK.SG_Property             ("reorderable")
        , GTK.SG_Property             ("rules_hint")
        , GTK.SG_Property             ("search_column")
        , GTK.SG_Object_Property      ("vadjustment")
        , GTK.SG_Property
            ( "selection_mode"
            , get = lambda s    : s._selection.wtk_object.get_mode ()
            , set = lambda s, v : s._selection.wtk_object.set_mode (v)
            )
        )

    _wtk_delegation = GTK.Delegation \
        ( GTK.Delegator_O ("append_column")
        )

    Signals = dict \
        ( select       = (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
        , dnd_motion   =
            (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (object, ))
        )

    def __init__ (self, model = None, * args, ** kw) :
        gtk_model = model and model.wtk_object
        self.__super.__init__ (gtk_model, * args, ** kw)
        self._selection = Tree_Selection \
            (model, self.wtk_object.get_selection ())
        self._selection.bind_add \
            ( self.TNS.Signal.Changed
            , lambda * a : self.emit (self.TNS.Signal.Select)
            )
    # end def __init__

    selection = property \
        ( lambda s    : s._selection
        , lambda s, v : s._selection.set (v)
        )

    def _bind_ (self, signal, * args, ** kw) :
        result = self.__super._bind_ (signal, * args, ** kw)
        if signal is self.TNS.Signal.DND_Motion :
            self._dnd_cid = self.bind_add \
                (self.TNS.Signal.Drag_Motion, self._dnd_motion)
        return result
    # end def _bind_

    def _dnd_motion (self, event) :
        drop_info = self.wtk_object.get_dest_row_at_pos (event.x, event.y)
        if drop_info :
            model = self.model.wtk_object
            iter  = model.get_iter (drop_info [0])
            if iter :
                self.emit (self.TNS.Signal.DND_Motion, self.model.ui_object (iter))
    # end def _dnd_motion

    def unbind (self, signal, * args, ** kw) :
        result     = self.__super.unbind (signal, * args, ** kw)
        dnd_motion = self.TNS.Signal.DND_Motion
        if signal is dnd_motion and not self._handlers [signal] :
            self.unbind (dnd_motion, self._dnd_cid)
        return result
    # end def unbind

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

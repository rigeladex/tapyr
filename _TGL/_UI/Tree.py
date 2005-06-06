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
#    TGL.UI.Tree
#
# Purpose
#    Abstract user interface for Tree
#
# Revision Dates
#     3-Jun-2005 (MG) Creation
#     5-Jun-2005 (MG) Lazy population added
#     5-Jun-2005 (MG) Basic sort implemented
#     5-Jun-2005 (MG) Filter support added
#     6-Jun-2005 (CT) `_Tree_` and `Rooted_Tree` factored
#     6-Jun-2005 (MG) Changed to new structure of `Tree_Adapter`
#     6-Jun-2005 (MG) Sort bug fixed
#    ««revision-date»»···
#--

from   _TGL                import TGL
from   _TFL                import TFL
import _TGL._UI
import _TGL._UI.Mixin
import _TFL._Meta.Object

### todo
### - implement special sort function

class Dummy_Entry (object) :

    def __init__ (self, element) :
        self.element = element
    # end def __init__

# end class Dummy_Entry

class _Tree_ (TGL.UI.Mixin) :

    Adapter = None ### redefine in descendents

    def __init__ ( self
                 , ui_model
                 , lazy     = True
                 , sort     = None
                 , filter   = None
                 , AC       = None
                 ) :
        self.__super.__init__ (AC = AC)
        TNS             = self.TNS
        Adapter         = self.Adapter
        self.ui_model   = ui_model
        self.tkt_model  = self.t_model = Adapter.create_model (TNS, AC)
        if filter :
            self.tkt_f_model = Adapter.create_filter_model \
                (TNS, AC, self.t_model, filter)
            self.t_model     = self.tkt_f_model
        if sort is not None :
            self.tkt_s_model = Adapter.create_sort_model \
                (TNS, AC, self.t_model)
            self.t_model     = self.tkt_s_model
        self.tkt             = self._create_tkt_tree     (lazy, sort)
        self._lazy_bind      = None
        self._model_populate (lazy)
    # end def __init__

    def _model_populate (self, lazy, parent = None) :
        self._pending_populates = {}
        for element in self.Adapter.root_children (self.ui_model) :
            self._add_element (element, parent, lazy)
    # end def _model_populate

    def _add_element (self, element, parent, lazy) :
        Adapter = self.Adapter
        model   = self.tkt_model
        model.add (Adapter.row_data (element), parent = parent)
        if Adapter.has_children (element) :
            if lazy :
                self._pending_populates [element] = model.add_empty \
                    (Dummy_Entry (element), parent = element)
                if not self._lazy_bind :
                    self._lazy_bind = self.tkt.bind_add \
                        (self.TNS.Signal.Row_Expanded, self._populate_row)
            else :
                for child in Adapter.children (element) :
                    self._add_element (child, element, lazy)
    # end def _add_element

    def _create_tkt_tree (self, lazy, sort) :
        tkt = self.TNS.Tree      (self.t_model, AC = self.AC)
        self.Adapter.create_view (tkt)
        if sort :
            if sort is True :
                sort = xrange (len (tkt.children))
            for col in sort :
                tkt.children [col].sort_column_id = col
        return tkt
    # end def _create_tkt_tree

    def _populate_row (self, event) :
        reference   = self.t_model.ui_object (event.tree_iter)
        if isinstance (reference, Dummy_Entry) :
            element = reference.element
        else :
            element = reference
        if element in self._pending_populates :
            for child in self.Adapter.children (element) :
                self._add_element (child, element, True)
            self.tkt_model.remove (self._pending_populates [element])
            del self._pending_populates [element]
            if not self._pending_populates :
                self.tkt.unbind (self.TNS.Signal.Row_Expanded, self._lazy_bind)
    # end def _populate_row

# end class _Tree_

class Rooted_Tree (_Tree_) :
    """Base class for trees displaying the root"""

    def _model_populate (self, lazy) :
        parent = self.ui_model
        self.tkt_model.add (self.Adapter.row_data (parent), parent = None)
        super (Rooted_Tree, self)._model_populate (lazy, parent)
        # XXX why does this `__super` call not work -> calls
        # `_model_populate` form this class instead of the super class ???
        #self.__super._model_populate (lazy, parent)
    # end def _model_populate

# end class Rooted_Tree

class Tree (_Tree_) :
    """Base class for trees and lists (not displaying the root)"""

# end class Tree

if __name__ != "__main__" :
    TGL.UI._Export ("*")
else :
    from   _TGL._UI.App_Context   import App_Context
    import _TGL._UI.Tree_Adapter
    from    Record                import Record
    import _TGL._TKT._GTK.Model
    import _TGL._TKT._GTK.Cell_Renderer_Text
    import _TGL._TKT._GTK.Tree_View_Column
    import _TGL._TKT._GTK.Tree
    import _TGL._TKT._GTK.Test_Window
    import _TGL._TKT._GTK.Interpreter_Window
    GTK   = TGL.TKT.GTK

    AC    = App_Context     (TGL)

    class Test_Adapter (TGL.UI.Tree_Adapter) :

        schema = \
            ( TGL.UI.Column ( "Age"
                            , TGL.UI.Text_Cell        (("age", int))
                            )
            , TGL.UI.Column ( "Name"
                            , TGL.UI.Text_Cell_Styled ("first_name")
                            , TGL.UI.Text_Cell_Styled ("last_name")
                            )
            , TGL.UI.Column ( "Male"
                            , TGL.UI.Text_Cell        (("gender", bool))
                            )
            )

        @classmethod
        def has_children (cls, element) :
            return element.children
        # end def has_children

        @classmethod
        def children (cls, element) :
            return element.children
        # end def children

    # end class Test_Adapter

    class Person (object) :

        def __init__ (self, first_name, last_name, age, gender = 0) :
            self.first_name = first_name
            self.last_name  = last_name
            self.age        = age
            self.gender     = gender
            self.style      = Record \
                (background = None, foreground = "red")
            self.children   = []
        # end def __init__

    # end class Person

    root = Person ("Adam", "", 2000)
    root.children = \
        ( Person ("Herbert",  "Glueck",    56)
        , Person ("Eduard",   "Wiesinger", 52)
        , Person ("Hans",     "Herbert",    2)
        , Person ("Kurt",     "Herbert",    2)
        , Person ("Franz",    "Herbert",    5)
        , Person ("Jimy",     "Herbert",   10)
        , Person ("Karin",    "Herbert",   19, 1)
        , Person ("Julia",    "Herbert",   56, 1)
        , Person ("Helen",    "Herbert",    8, 1)
        , Person ("Stefanie", "Herbert",    2, 1)
        )
    root.children [0].children = \
        ( Person ("Martin",  "Glueck",    29)
        , Person ("Ines",    "Glueck",    31, 1)
        )
    root.children [0].children [1].children = \
        ( Person ("Celina",  "Glueck", 4, 1)
        ,
        )
    root.children [1].children = \
        ( Person ("Mathias", "Wiesinger", 23)
        ,
        )
    win     = GTK.Test_Window (title = "Tree Adapter Test", AC = AC)

    def gender_filter (ui) :
        ### a row filter example:
        ### return not ui [7]
        if isinstance (ui, Dummy_Entry) :
            return True
        return not ui.gender
    # end def gender_filter

    My_Tree = Rooted_Tree.New (Adapter = Test_Adapter)
    tree    = My_Tree \
        ( root
        , lazy    = True
        , filter  = gender_filter
        , sort    = (0, 1, 2)
        , AC      = AC
        )
    tree.tkt.show   ()
    #tree.tkt.hover_expand    = True
    #tree.tkt.hover_selection = True
    win.add         (tree.tkt)
    win.default_height = 150
    win.default_width  = 250
    win.show                   ()
    #w = GTK.Interpreter_Window (win, global_dict = globals (), AC = AC)
    #w.show                     ()
    GTK.main                   ()
### __END__ TGL.UI.Tree

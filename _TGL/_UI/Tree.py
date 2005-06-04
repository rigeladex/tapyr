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
#    «text»···
#
# Revision Dates
#     3-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                import TGL
from   _TFL                import TFL
import _TGL._UI
import _TGL._UI.Mixin
import _TFL._Meta.Object

class Tree (TGL.UI.Mixin) :
    """Base class for trees and lists"""

    def __init__ ( self
                 , ui_model
                 , adapter
                 , lazy     = True
                 , sort     = None
                 , filter   = None
                 , root     = False
                 , AC       = None
                 ) :
        self.__super.__init__ (AC = AC)
        self.ui_model        = ui_model
        self.adapter         = adapter
        self.sort            = sort
        self.tkt_model       = self.t_model = adapter.create_model ()
        self._model_populate (root, lazy)
        if sort :
            self.tkt_s_model = adapter.create_sort_model (self.t_model, sort)
            self.t_model     = self.tkt_s_model
        if filter :
            self.tkt_f_model = adapter.create_filter_model \
                (self.t_model, filter)
            self.t_model     = self.tkt_f_model
        self.tkt             = self._create_tkt_tree ()
    # end def __init__

    def _model_populate (self, root, lazy) :
        adapter   = self.adapter
        tkt_model = self.tkt_model
        if root :
            parent = self.ui_model
            tkt_model.add (adapter.row_data (parent), parent = None)
        else :
            parent = None
        for element in adapter.children (self.ui_model) :
            self._add_element (element, parent, lazy)
    # end def _model_populate

    def _add_element (self, element, parent, lazy) :
        adapter = self.adapter
        self.tkt_model.add (adapter.row_data (element), parent = parent)
        if adapter.has_children (element) :
            if lazy :
                print "Add `populate` element..."
            else :
                for child in adapter.children (element) :
                    self._add_element (child, element, lazy)
    # end def _add_element

    def _create_tkt_tree (self) :
        tkt = self.TNS.Tree      (self.t_model, AC = self.AC)
        self.adapter.create_view (tkt)
        return tkt
    # end def _create_tkt_tree

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
    GTK   = TGL.TKT.GTK

    AC    = App_Context     (TGL)

    class Test_Adapter (TGL.UI.Tree_Adapter) :

        schema = \
            ( TGL.UI.Column ( "Name"
                            , TGL.UI.Text_Cell_Styled ("first_name")
                            , TGL.UI.Text_Cell_Styled ("last_name")
                            )
            , TGL.UI.Column ( "Age"
                            , TGL.UI.Text_Cell        (("age", int))
                            )
            , TGL.UI.Column ( "Male"
                            , TGL.UI.Text_Cell        (("gender", bool))
                            )
            )

        def has_children (self, element) :
            return element.children
        # end def has_children

        def children (self, element) :
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
                (background = "white", foreground = "red")
            self.children   = []
        # end def __init__

    # end class Person

    root = Person ("Adam", "", 2000)
    root.children = \
        ( Person ("Herbert", "Glueck",    56)
        , Person ("Eduard",  "Wiesinger", 52)
        , Person ("Hans",    "Herbert",    2)
        )
    root.children [0].children = \
        ( Person ("Martin",  "Glueck",    29)
        , Person ("Ines",    "Glueck",    31, 1)
        )
    root.children [0].children [1].children = \
        ( Person ("Celina",  "Glueck", 4)
        ,
        )
    root.children [1].children = \
        ( Person ("Mathias", "Wiesinger", 23)
        ,
        )
    win     = GTK.Test_Window (title = "Tree Adapter Test", AC = AC)
    tree    = Tree  \
        (root, Test_Adapter (AC = AC), lazy = False, root = True, AC = AC)
    tree.tkt.show   ()
    win.add         (tree.tkt)
    win.default_height = 150
    win.default_width  = 250
    win.show                  ()
    GTK.main                  ()
### __END__ TGL.UI.Tree

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
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
#    TGL.UI._test_Tree_DND
#
# Purpose
#    A test for the TGL.UI.Tree DND operations
#
# Revision Dates
#     7-Jun-2005 (MG) Creation (factored from TGL.UI.Tree)
#    17-Jun-2005 (MG) `Lazy_Cell` added
#    ««revision-date»»···
#--
#
from   _TGL                   import TGL
import _TGL._UI
from   _TGL._UI.App_Context   import App_Context
import _TGL._UI.Tree_Adapter
import _TGL._UI.Tree
from    Record                import Record
import _TGL._TKT._GTK.Model
import _TGL._TKT._GTK.Cell_Renderer_Text
import _TGL._TKT._GTK.Tree_View_Column
import _TGL._TKT._GTK.Tree
import _TGL._TKT._GTK.Test_Window
import _TGL._TKT._GTK.Interpreter_Window
import  os
pys = os.environ.get ("PYTHONSTARTUP")
if pys :
    execfile (pys)
GTK   = TGL.TKT.GTK

AC    = App_Context     (TGL)

class Test_Adapter (TGL.UI.Tree_Adapter) :

    Model_Type = "List_Model"

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

    def has_children (cls, element) :
        return False
    # end def has_children

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

win     = GTK.Test_Window (title = "Tree Adapter Test", AC = AC)

My_Tree = TGL.UI.Tree.New (Adapter = Test_Adapter)
tree    = My_Tree \
    ( root
    , lazy           = False
    , multiselection = True
    , AC             = AC
    )
### DND specific
def test (event) :
    w = event.widget
    x = len (w.selection)
    if event.object :
        event.widget.selection.extend (event.object)
        tree.see                      (event.object, valign = 0.5)
# end def test
if 0 :
    import gtk

    src_type = (( "text/plain", 0, 80), )
    tree.tkt.wtk_object.drag_source_set \
       (gtk.gdk.BUTTON1_MASK, src_type, gtk.gdk.ACTION_COPY)
    tree.tkt.wtk_object.connect ("drag-motion", test)
    tree.tkt.wtk_object.drag_dest_set(0, [], 0)
else :
    tree.add_dnd_source (1, "copy", "PMA-Message/select", "PMA-Message/move")
    tree.add_dnd_target ("copy", "PMA-Message/select")
    tree.tkt.bind_add   (tree.TNS.Signal.DND_Motion, test)
tree.tkt.show   ()
win.add         (tree.tkt)
win.default_height = 150
win.default_width  = 250
win.show                   ()
#w = GTK.Interpreter_Window (win, global_dict = globals (), AC = AC)
#w.show                     ()
GTK.main                   ()

### __END__ TGL.UI._test_Tree_DND

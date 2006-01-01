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
#    TGL.UI._test_Tree
#
# Purpose
#    A test for the TGL.UI.Tree and firends
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

class Lazy_Cell (TGL.UI.Cell) :

    renderer_class      = "Cell_Renderer_Text"
    auto_attributes     = dict \
        ( lazy = ("text", str, "_get_text")
        )
    lazy                = True
    c                   = 0

    def _get_text (self, obj, attr_name) :
        self.c += 1
        return "Lazy %d" % (self.c, )
    # end def _get_text

# end class Lazy_Cell

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
        , TGL.UI.Column ( "Lazy", Lazy_Cell ())
        )

    def has_children (cls, element) :
        return element.children
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
b       = GTK.V_Box       (AC = AC)
b.show                    ()
win.add                   (b)

def gender_filter (ui, gender = True) :
    ### a row filter example:
    return ui.gender == gender
# end def gender_filter

My_Tree = TGL.UI.Rooted_Tree.New (Adapter = Test_Adapter)
tree    = My_Tree \
    ( root
    , lazy    = True
    #, filter  = gender_filter
    , sort    = (0, 1, 2)
    , AC      = AC
    )
m_tree = tree.clone (filter = lambda ui : gender_filter (ui, True ))
f_tree = tree.clone (filter = lambda ui : gender_filter (ui, False))
#tree.tkt.hover_expand    = True
#tree.tkt.hover_selection = True
for t in tree, m_tree, f_tree :
    t.tkt.show ()
    b.add      (t.tkt)
win.default_height = 150
win.default_width  = 250
win.show                   ()
#w = GTK.Interpreter_Window (win, global_dict = globals (), AC = AC)
#w.show                     ()
GTK.main                   ()

### __END__ TGL.UI._test_Tree

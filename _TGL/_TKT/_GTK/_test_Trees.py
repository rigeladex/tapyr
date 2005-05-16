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
#    TGL.TKT.GTK._test_Trees
#
# Purpose
#    Test the various tree posibilities (filer/sort/...)
#
# Revision Dates
#    16-May-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                   import TGL
from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Test_Window
import _TGL._TKT._GTK.H_Box
import _TGL._TKT._GTK.V_Box
import _TGL._TKT._GTK.Model
import _TGL._TKT._GTK.Cell_Renderer_Text
import _TGL._TKT._GTK.Tree_View_Column
import _TGL._TKT._GTK.Tree_View
from   _TGL._UI.App_Context   import App_Context

AC    = App_Context     (TGL)
win   = GTK.Test_Window (title = "Tree Test", AC = AC)
bv    = GTK.V_Box       (AC    = AC)
bh1   = GTK.H_Box       (AC    = AC)
bh2   = GTK.H_Box       (AC    = AC)
win.add                 (bv)
bv.add                  (bh1)
bv.add                  (bh2)

bh1.show                ()
bh2.show                ()
bv.show                 ()

model = GTK.Tree_Model  (object, str, int, int, AC = AC, ui_column = 0)
class Dummy :
    def __init__ (self, index) :
        self.index = index
    # end def __init__

    def __str__ (self) :
        return "Dummy (%s)" % (self.index, )
    # end def __str__

# end class Dummy

for i in range (15) :
    x = Dummy (i)
    model.add ((x, "Row_%2d" % (i, ), i, 30 - i))

def change_sort (event) :
    column = event.widget
    if column.sort_indicator :
        column.sort_order = not column.sort_order
    else :
        column.sort_indicator = True
# end def change_sort

def cursor_moved (event, model = model) :
    widget = event.widget
    for iter in widget.selected_iters () :
        print iter, widget.model.iter_to_object (iter)
# end def cursor_moved

views   = []
columns = []
models  = []
for i in range (4) :
    if i % 2 :
        sort_col = 1 + i // 2
        nmodel   = GTK.Sort_Model   (model, column = sort_col)
        fct      = None
    else :
        ### Filter_Model
        nmodel   = GTK.Sort_Model (model)
        sort_col = None
        fct      = None
    view = GTK.Tree_View          (nmodel)
    models.append (nmodel)
    r1   = GTK.Cell_Renderer_Text ()
    c1   = GTK.Tree_View_Column   ("C1", r1, text = 1)
    r2   = GTK.Cell_Renderer_Text ()
    c2   = GTK.Tree_View_Column   ("C2", r2, text = 2)
    r3   = GTK.Cell_Renderer_Text ()
    c3   = GTK.Tree_View_Column   ("C3", r3, text = 3)
    columns.append ((c1, c2, c3))
    c1.resizable = c2.resizable = c3.resizable = True
    if sort_col is not None :
        print sort_col
        #(c1, c2, c3) [sort_col].sort_indicator = True
        (c1, c2, c3) [sort_col].sort_column_id = 2
    if fct :
        for c in c1, c2, c3 :
            c.bind_add (GTK.Signal.Clicked, fct)
    view.append_column            (c1)
    view.append_column            (c2)
    view.append_column            (c3)
    view.show                     ()
    view.headers_clickable = True
    view.bind_add (GTK.Signal.Cursor_Changed, cursor_moved)
    views.append                  (view)

bh1.add                 (views [0])
bh1.add                 (views [1])
bh2.add                 (views [2])
bh2.add                 (views [3])
win.show                ()
GTK.main                ()
### __END__ TGL.TKT.GTK._test_Trees



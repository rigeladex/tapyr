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
#    TGL.TKT.Tree_Adapter
#
# Purpose
#    Base class used for the creation of an TKT.Tree out of any tree/list
#    like objects which provide are iterable.
#
# Revision Dates
#    17-May-2005 (MG) Creation
#    18-May-2005 (MG) `_setup_model` use `self.children` for the loop
#    ««revision-date»»···
#--

from   _TGL                import TGL
from   _TFL                import TFL
import _TGL._TKT
import _TGL._TKT.Mixin
import _TFL._Meta.Object

class Cell (TFL.Meta.Object) :
    """A cell with gets render specific attributes out of an `UI` element.
    """

    renderer_attributes = ()

    def __init__ (self, * attributes, ** options) :
        self.__super.__init__ ()
        if len (attributes) > len (self.renderer_attributes) :
            raise TypeError, "Too many renderer attributes specified"
        self.attr_map = {}
        for ui, rend in zip (attributes, self.renderer_attributes) :
            if not isinstance (ui, (list, tuple)) :
                mt = str
            else :
                ui, mt = ui
            self.attr_map [ui] = rend, mt
        self.attr_map.update (options)
    # end def __init__

    def setup_column_types (self, column_types) :
        self.start_index = index = len (column_types)
        self.renderer_attr_dict  = {}
        self.attr_order          = []
        for ui, (rend, mt) in self.attr_map.iteritems () :
            column_types.append    (mt)
            self.attr_order.append ((ui, getattr))
            self.renderer_attr_dict [rend] = index
            index += 1
    # end def setup_column_types

    def add_data (self, ui) :
        return [f (ui, n) for (n, f) in self.attr_order]
    # end def add_data

# end class Cell

class _Style_Mixin_ (TFL.Meta.Object) :
    """Extends a normal cell to use some of the attributes out of style object
    """

    style_map           = dict \
        ( background    = ("background", str)
        , foreground    = ("foreground", str)
        )

    def __init__ (self, * attributes, ** options) :
        self.__super.__init__ (* attributes, ** options)
    # end def __init__

    def setup_column_types (self, column_types) :
        self.__super.setup_column_types (column_types)
        index                   = len (column_types)
        style_get_attr          = lambda o, n : getattr (o.style, n)
        for ui, (rend, mt) in self.style_map.iteritems () :
            column_types.append    (mt)
            self.renderer_attr_dict [rend] = index
            self.attr_order.append ((ui, style_get_attr))
            index += 1
    # end def setup_column_types

# end class _Style_Mixin_

class Text_Cell (Cell) :
    """A cell with uses a normal text renderer"""

    renderer_attributes = ("text", )
    renderer_class      = ("Cell_Renderer_Text")

# end class Text_Cell

class Text_Cell_Styled (_Style_Mixin_, Text_Cell) : pass

class Column (TFL.Meta.Object) :
    """Specifies the properties of on column displayed by the TNS.Tree"""

    default_attributes = dict \
        ( visible       = True
        , clickable     = True
        , resizable     = True
        , reorderable   = True
        , alignment     = 0.6
        , header_widget = None
        , sort_function = None
        )

    def __init__ (self, title, * cells, ** kw) :
        self.__super.__init__ ()
        self.title = title
        for name, default in self.default_attributes.iteritems () :
            setattr (self, name, kw.get (name, default))
            if name in kw :
                del kw [name]
        if kw :
            raise TypeError, "Illegal paramaters `%s`" % (kw.keys (), )
        self.cells      = cells
    # end def __init__

    def setup_column_types (self, column_types) :
        for cell in self.cells :
            cell.setup_column_types (column_types)
    # end def setup_column_types

    def add_column (self, tree) :
        self.column = column = tree.TNS.Tree_View_Column (self.title)
        for name in ( "alignment"
                    , "clickable"
                    , "visible"
                    , "resizable"
                    , "reorderable"
                    ) :
            setattr (column, name, getattr (self, name))
        tree.append_column (column)
        for cell in self.cells :
            renderer = getattr    (tree.TNS, cell.renderer_class) ()
            column.pack           (renderer)
            column.set_attributes (renderer, ** cell.renderer_attr_dict)
    # end def add_column

    def add_row_data (self, ui, row) :
        for cell in self.cells :
            row.extend (cell.add_data (ui))
    # end def add_row_data

    def __str__ (self) :
        return '%s ("%s", %s)' % \
            ( self.__class__.__name__, self.title
            , ", ".join ([str (c) for c in self.cells])
            )
    # end def __str__

# end class Column

class Tree_Adapter (TGL.TKT.Mixin) :
    """Base class for the TKT.<TNS>.Tree creation."""

    schema = () ### to be defined by descendents

    def __init__ (self, ui_model, model = None, lazy = True, AC = None) :
        self.__super.__init__    (AC = AC)
        self.ui_model = ui_model
        if not model :
            model  = self._setup_model  (ui_model, lazy)
        self.model = model
        self.tkt   = self.TNS.Tree (self.model, AC = AC)
        for col in self.schema :
            col.add_column (self.tkt)
    # end def __init__

    def has_children (self, element) :
        ### must return wether the `element` has childrens or not
        raise NotImplementedError
    # end def has_children

    def children (self, element) :
        ### returns all child elements of `element`
        raise NotImplementedError
    # end def children

    def _setup_model (self, ui_model, lazy) :
        column_types = []
        for col in self.schema :
            col.setup_column_types (column_types)
        ui_column = len            (column_types)
        column_types.append        (object)
        model = self.TNS.Tree_Model \
            (AC = self.AC, ui_column = ui_column, * column_types)
        for ui in self.children (ui_model) :
            self._add_row (model, ui, None, lazy)
        return model
    # end def _setup_model

    def _add_row (self, model, ui, parent, lazy) :
        row = []
        for column in self.schema :
            column.add_row_data (ui, row)
        row.append              (ui)
        node = model.add        (row, parent = parent)
        if self.has_children (ui) :
            if not lazy :
                for cui in self.children (ui) :
                    self._add_row (model, cui, node, lazy)
            else :
                print "Add sub element", ui
    # end def _add_row

# end class Tree_Adapter

if __name__ != "__main__" :
    TGL.TKT._Export ("*")
else :
    from   _TGL._UI.App_Context   import App_Context
    from    Record                import Record
    import _TGL._TKT._GTK.Model
    import _TGL._TKT._GTK.Cell_Renderer_Text
    import _TGL._TKT._GTK.Tree_View_Column
    import _TGL._TKT._GTK.Tree
    import _TGL._TKT._GTK.Test_Window
    GTK = TGL.TKT.GTK

    AC    = App_Context     (TGL)
    class Test_Adapter (Tree_Adapter) :

        schema = \
            ( Column ( "Name"
                     , Text_Cell_Styled ("first_name")
                     , Text_Cell_Styled ("last_name")
                     )
            , Column ( "Age"
                     , Text_Cell        (("age", int))
                     )
            , Column ( "Male"
                     , Text_Cell        (("gender", bool))
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

    ui_model = \
        ( Person ("Herbert", "Glueck",    56)
        , Person ("Eduard",  "Wiesinger", 52)
        , Person ("Hans",    "Herbert",    2)
        )
    ui_model [0].children = \
        ( Person ("Martin",  "Glueck",    29)
        , Person ("Ines",    "Glueck",    31, 1)
        )
    ui_model [0].children [1].children = \
        ( Person ("Celina",  "Glueck", 4)
        ,
        )
    ui_model [1].children = \
        ( Person ("Mathias", "Wiesinger", 23)
        ,
        )
    win     = GTK.Test_Window (title = "Tree Adapter Test", AC = AC)
    adapter = Test_Adapter    (ui_model, lazy = False, AC = AC)
    adapter.tkt.show          ()
    win.add                   (adapter.tkt)
    win.default_height = 150
    win.default_width  = 250
    win.show                  ()
    GTK.main                  ()
### __END__ TGL.TKT.Tree_Adapter

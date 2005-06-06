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
#    TGL.UI.Tree_Adapter
#
# Purpose
#    Base class used for the creation of an TKT.Tree out of any tree/list
#    like objects which provide are iterable.
#
# Revision Dates
#    17-May-2005 (MG) Creation
#    18-May-2005 (MG) `_setup_model` use `self.children` for the loop
#     3-Jun-2005 (MG) Move from `TKT` package into the `UI` package
#     3-Jun-2005 (MG) `TGL.UI.Tree` factored
#     5-Jun-2005 (MG) Parameter `sort` removed from `create_sort_model`
#     6-Jun-2005 (CT) `root_children` added
#    ««revision-date»»···
#--

from   _TGL                import TGL
from   _TFL                import TFL
import _TGL._UI
import _TGL._UI.Mixin
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
        , alignment     = 0.5
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

class Tree_Adapter (TGL.UI.Mixin) :
    """Base class for the TKT.<TNS>.Tree creation."""

    schema = () ### to be defined by descendents

    def has_children (self, element) :
        ### must return wether the `element` has childrens or not
        raise NotImplementedError
    # end def has_children

    def children (self, element) :
        ### returns all child elements of `element`
        raise NotImplementedError
    # end def children

    def create_model (self) :
        column_types = []
        for col in self.schema :
            col.setup_column_types (column_types)
        ui_column = len            (column_types)
        column_types.append        (object)
        return self.TNS.Tree_Model \
            (AC = self.AC, ui_column = ui_column, * column_types)
    # end def create_model

    def create_filter_model (self, model, filter) :
        return self.TNS.Filter_Model (model, filter)
    # end def create_filter_model

    def create_sort_model (self, model) :
        return self.TNS.Sort_Model (model)
    # end def create_sort_model

    def create_view (self, tkt) :
        for col in self.schema :
            col.add_column (tkt)
    # end def create_view

    def root_children (self, root) :
        ### returns all child elements of `root`
        return self.children (root)
    # end def root_children

    def row_data (self, element, row = None) :
        if row is None :
            row = []
            for column in self.schema :
                column.add_row_data (element, row)
        row.append                  (element)
        return row
    # end def row_data

# end class Tree_Adapter

if __name__ != "__main__" :
    TGL.UI._Export ("*")
### __END__ TGL.UI.Tree_Adapter

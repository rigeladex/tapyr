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
#     6-Jun-2005 (MG) Convert all methods of `Tree_Adapter` into static- or
#                     classmethods
#     7-Jun-2005 (MG) Changed to use `__autowrap`
#    17-Jun-2005 (MG) `auto_attributes` added and used, `_Style_Mixin_`
#                     changed to use new `auto_attributes` feature
#    17-Jun-2005 (MG) Support for `lazy` cells added
#    17-Jun-2005 (MG) Class variables `Model_Type` and `rules_hint` added
#    30-Jul-2005 (MG) Allow `kw` for `row_data`
#    30-Jul-2005 (MG) Support fixed value attributes for renderer attributes
#    13-Aug-2005 (MG) `Toggle_Cell` added
#    13-Aug-2005 (MG) Add `AC` to the creation of the renderer instance
#    13-Aug-2005 (MG) Set the `renderer` attribute for the cell
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
    auto_attributes     = dict () ### can be defined by descendents
    lazy                = False

    def __init__ (self, * attributes, ** options) :
        self.__super.__init__ ()
        self.__dict__.update  (options)
        if "lazy" in options :
            self.lazy = options ["lazy"]
            del options ["lazy"]
        if len (attributes) > len (self.renderer_attributes) :
            raise TypeError, "Too many renderer attributes specified"
        self.attr_map = {}
        aa            = self.auto_attributes
        for ui_attr, (rend_attr, tkt_type, get_fct) in aa.iteritems () :
            if not callable (get_fct) and isinstance (get_fct, (str, unicode)):
                get_fct             = getattr (self, get_fct, get_fct)
            self.attr_map [ui_attr] = rend_attr, tkt_type, get_fct
        for ui_attr, rend_attr in zip (attributes, self.renderer_attributes) :
            tkt_type = str
            if isinstance (rend_attr, (list, tuple)) :
                rend_attr, tkt_type = rend_attr
            if not isinstance (ui_attr, (list, tuple)) :
                get_fct                        = getattr
            else :
                if len (ui_attr) > 2 :
                    ui_attr, tkt_type, get_fct = ui_attr
                else :
                    ui_attr, tkt_type          = ui_attr
                    get_fct                    = getattr
            if not callable (get_fct) :
                get_fct                        = getattr (self, get_fct)
            self.attr_map [ui_attr]            = rend_attr, tkt_type, get_fct
    # end def __init__

    def setup_column_types (self, column_types) :
        self.start_index = index = len (column_types)
        self.renderer_attr_dict  = {}
        self.attr_order          = []
        if not self.lazy :
            am = self.attr_map
            for ui_attr, (rend_attr, tkt_type, get_fct) in am.iteritems () :
                column_types.append    (tkt_type)
                self.attr_order.append ((ui_attr, get_fct))
                self.renderer_attr_dict [rend_attr] = index
                index += 1
    # end def setup_column_types

    def add_data (self, ui, kw) :
        row = []
        for (n, f) in self.attr_order :
            if callable (f) :
                row.append (f (ui, n, ** kw))
            else :
                row.append (f)
        return row
    # end def add_data

    def _lazy_populate (self, ui, renderer) :
        attr_map = self.attr_map
        for ui_attr, (rend_attr, tkt_type, get_fct) in attr_map.iteritems () :
            if callable (get_fct) :
                value = get_fct (ui, ui_attr)
            else :
                value = get_fct
            setattr (renderer, rend_attr, value)
    # end def _lazy_populate

# end class Cell

class _Style_Mixin_ (TFL.Meta.Object) :
    """Extends a normal cell to use some of the attributes out of style object
    """

    def _style_get (self, obj, attr_name, ** kw) :
        return getattr (obj.style, attr_name)
    # end def _style_get

    auto_attributes     = dict \
        ( background    = ("background", str, "_style_get")
        , foreground    = ("foreground", str, "_style_get")
        )

# end class _Style_Mixin_

class Text_Cell (Cell) :
    """A cell with uses a normal text renderer"""

    renderer_attributes = ("text", )
    renderer_class      = "Cell_Renderer_Text"

# end class Text_Cell

class Text_Cell_Styled (_Style_Mixin_, Text_Cell) : pass

class Toggle_Cell (Cell) :
    """A cell with uses a normal text renderer"""

    renderer_attributes = (("active", bool), )
    renderer_class      = "Cell_Renderer_Toggle"

# end class Toggle_Cell

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
            renderer = getattr (tree.TNS, cell.renderer_class) (AC = tree.AC)
            column.pack        (renderer)
            if cell.lazy :
                column.set_cell_function \
                    ( renderer
                    , column.set_renderer_attributes
                    , cell
                    )
            else :
                column.set_attributes (renderer, ** cell.renderer_attr_dict)
            cell.renderer = renderer
    # end def add_column

    def add_row_data (self, ui, row, kw) :
        for cell in self.cells :
            row.extend (cell.add_data (ui, kw))
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

    Model_Type = "Tree_Model"

    schema     = () ### to be defined by descendents
    __autowrap = dict \
        ( root_children = classmethod
        , children      = classmethod
        , has_children  = classmethod
        )
    rules_hint          = True

    def has_children (cls, element) :
        ### must return wether the `element` has childrens or not
        raise NotImplementedError
    # end def has_children

    def children (cls, element) :
        ### returns all child elements of `element`
        raise NotImplementedError
    # end def children

    @classmethod
    def create_model (cls, TNS, AC) :
        column_types = []
        for col in cls.schema :
            col.setup_column_types (column_types)
        ui_column = len            (column_types)
        column_types.append        (object)
        return getattr (TNS, cls.Model_Type) \
            (AC = AC, ui_column = ui_column, * column_types)
    # end def create_model

    @staticmethod
    def create_filter_model (TNS, AC, model, filter) :
        return TNS.Filter_Model (model, filter, AC = AC)
    # end def create_filter_model

    @staticmethod
    def create_sort_model (TNS, AC, model) :
        return TNS.Sort_Model (model, AC = AC)
    # end def create_sort_model

    @classmethod
    def create_view (cls, tkt) :
        for col in cls.schema :
            col.add_column (tkt)
    # end def create_view

    def root_children (cls, root) :
        ### returns all child elements of `root`
        return cls.children (root)
    # end def root_children

    @classmethod
    def row_data (cls, element, kw = {}, row = None) :
        if row is None :
            row = []
            for column in cls.schema :
                column.add_row_data (element, row, kw)
        row.append                  (element)
        return row
    # end def row_data

# end class Tree_Adapter

if __name__ != "__main__" :
    TGL.UI._Export ("*")
### __END__ TGL.UI.Tree_Adapter

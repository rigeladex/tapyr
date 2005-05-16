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
#    TGL.TKT.GTK.Model
#
# Purpose
#    Tree/List data models required by the Tree_View widget
#
# Revision Dates
#    27-Mar-2005 (MG) Creation
#    16-May-2005 (MG) `Sort_Model` added
#    16-May-2005 (MG) `iter_to_object` added
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Object
import _TGL._TKT._GTK.Constants

class Dict_Mapper (dict) :
    """Maps an TGL.UI element to a GTK-TreeIter objects"""

    def __init__ (self, model) :
        pass ### no need for the model parameter
    # end def __init__

# end class Dict_Mapper

class Model_Proxy_Mapper (object) :
    """Maps a TGL.UI elements to GTK-TreeIter objects"""

    def __init__ (self, model) :
        self.model = model
    # end def __init__

    def __getitem__ (self, key) :
        return self.model.iter [key]
    # end def __getitem__

    def __setitem__ (self, key, value) :
        raise RuntimeError, "Set opertion ot allowed for a Procy"
    # end def __setitem__

    def get (self, key, default = None) :
        return self.model.iter, get (key, default)
    # end def get

# end class Model_Proxy_Mapper

class _Model_ (GTK.Object) :
    """Root class for all `Model` (Tree/List Model, FilterModel, SortModel)"""

    Iter_Mapper      = Dict_Mapper
    GTK_Class        = None

    __gtk_properties = \
       ( GTK.SG_Property
             ("columns", get_fct_name = "get_n_columns", set = None)
       ,
       )

    def __init__ (self, * column_types, ** kw) :
        self.ui_column = kw.get ("ui_column", None)
        if "ui_column" in kw :
            del kw ["ui_column"]
        self.__super.__init__        (* column_types, ** kw)
        self.iter      = {}
    # end def __init__

    def add (self, row, after = None, ** kw) :
        after_iter     = self.iter.get (after, after)
        iter           = self._add (row, after_iter = after_iter, ** kw)
        if self.ui_column is not None :
            self.iter [row [self.ui_column]] = iter
        return iter
    # end def add

    def remove (self, node) :
        iter  = self.iter.get (node, node)
        child = self.wtk_object.iter_children (iter)
        while child :
            if self.ui_column is not None :
                self.remove (self.wtk_object.get (child, self.ui_column))
            else :
                self.remove (child)
            child = self.wtk_object.iter_next (child)
        if node in self.iter :
            del self.iter    [name]
        self.wtk_object.remove (iter)
    # end def remove

    def __getitem__ (self, key) :
        return self.wtk_object [key]
    # end def __getitem__

    def __setitem__ (self, key, value) :
        self.wtk_object [key] = value
    # end def __setitem__

    def __delitem__ (self, key) :
        self.remove (self.wtk_object [key].iter)
    # end def __delitem__

    def pprint (self, sep = ":") :
        for row in self.wtk_object :
            print "\n".join (self._format_row (row, sep))
    # end def pprint

    def _format_row (self, row, sep = ":", intend = 0) :
        result = ["%s%s" % (" " * intend, sep.join (str (c) for c in row))]
        for r in row.iterchildren () :
            result.extend (self._format_row (r, sep, intend + 2))
        return result
    # end def _format_row

    def iter_to_object (self, iter) :
        if self.ui_column is not None :
            return self.wtk_object [iter] [self.ui_column]
    # end def iter_to_object

# end class _Model_

class List_Model (_Model_) :
    """Wrapper for the gtk.ListStore class
       >>> l = List_Model (str,int)
       >>> r0 = l.add (("Row_1", 0))
       >>> r1 = l.add (("Row_2", 1))
       >>> l.pprint ()
       Row_1:0
       Row_2:1
       >>> r1_5 = l.add (("Row_1_5", 15), after = r0)
       >>> l.pprint ()
       Row_1:0
       Row_1_5:15
       Row_2:1
       >>> del l [1]
       >>> l.pprint ()
       Row_1:0
       Row_2:1
    """

    GTK_Class    = GTK.gtk.ListStore

    def _add (self, row, after_iter) :
        if after_iter :
            return self.wtk_object.insert_after (after_iter, row)
        else :
            return self.wtk_object.append       (row)
    # end def _add

    def has_children (self, * args, ** kw) :
        return False
    # end def has_children

# end class List_Model

class Tree_Model (_Model_) :
    """Wrapper for the gtk.TreeStore class

       >>> from _TGL._TKT._GTK.Model import *
       >>> t = Tree_Model (str,int)
       >>> p = t.add (("Test_1",     1))
       >>> c = t.add (("Test_1_1",   2), parent = p)
       >>> d = t.add (("Test_1_1_1", 3), parent = c)
       >>> t [0] [0]
       'Test_1'
       >>> t [0] [1]
       1
       >>> t [0] [1] = 2
       >>> t [0] [1]
       2
       >>> t.pprint ()
       Test_1:2
         Test_1_1:2
           Test_1_1_1:3
    """

    GTK_Class    = GTK.gtk.TreeStore

    def _add (self, row, after_iter, parent = None) :
        par_iter = self.iter.get  (parent, parent)
        if after_iter :
            return self.wtk_object.insert_after (par_iter, after_iter, row)
        else :
            return self.wtk_object.append       (par_iter, row)
    # end def _add

    def has_children (self, node) :
        iter = self.iter.get (node, node)
        return self.wtk_object.iter_has_child (iter)
    # end def has_children

# end class Tree_Model

class Sort_Model (GTK.Object) :
    """Sorts a child model"""

    GTK_Class = GTK.gtk.TreeModelSort

    sort_order    = property \
        (lambda s    : s._order,  lambda s, v : s._set_order  (v))
    sort_column   = property \
        (lambda s    : s._column, lambda s, v : s._set_column (v))

    def __init__ (self, child_model, order = GTK.SORT_ASCENDING, column = 0) :
        self.__super.__init__ (child_model.wtk_object)
        self.model      = child_model
        self._order     = order
        self._column    = column
        self._functions = {}
    # end def __init__

    def _set_sort_column (self, column) :
        self._column = column
        self.wtk_object.set_sort_column_id (self._column, self._order)
    # end def _set_sort_column

    def _set_sort_order (self, order) :
        self._order = order
        self.wtk_object.set_sort_column_id (self._column, self._order)
    # end def _set_sort_order

    def set_sort_funcion (self, id, fct, data = None, destroy = None) :
        """The sort function must accept the following parameter:
             treemodel, iter1, iter2, user_data
        """
        if fct is None :
            if id in self._functions :
                del self._functions [id]
        else :
            self._functions [id] = (fct, data, destroy)
        self.wtk_object.set_sort_func (id, fct, data, destroy)
    # end def set_sort_funcion

    def sort_function (self, id) :
        return self._functions [id]
    # end def sort_function

    def iter_to_object (self, iter) :
        return self.model.iter_to_object \
            (self.wtk_object.convert_iter_to_child_iter (None, iter))
    # end def iter_to_object

# end class Sort_Model

if __name__ != "__main__" :
    GTK._Export ("List_Model", "Tree_Model", "Sort_Model")
### __END__ TGL.TKT.GTK.Model

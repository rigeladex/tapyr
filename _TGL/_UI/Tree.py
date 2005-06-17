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
#     7-Jun-2005 (MG) `show_header` added
#     7-Jun-2005 (MG) Test code moved into a new file `_test_Tree`
#     7-Jun-2005 (MG) `update_model` added
#    10-Jun-2005 (MG) `update_model`: clearing of old model added
#    11-Jun-2005 (MG) `clear_selection`, `selection` and `update` added
#    17-Jun-2005 (MG) Use `Adapter.rules_hint`
#    17-Jun-2005 (MG) `see` added
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
                 , ui_model    = None
                 , lazy        = True
                 , sort        = None
                 , filter      = None
                 , show_header = True
                 , AC          = None
                 ) :
        self.__super.__init__ (AC = AC)
        TNS             = self.TNS
        Adapter         = self.Adapter
        self.ui_model   = None
        self.tkt_model  = self.t_model = Adapter.create_model (TNS, AC)
        if filter :
            self.tkt_f_model = Adapter.create_filter_model \
                (TNS, AC, self.t_model, filter)
            self.t_model     = self.tkt_f_model
        if sort is not None :
            self.tkt_s_model = Adapter.create_sort_model \
                (TNS, AC, self.t_model)
            self.t_model     = self.tkt_s_model
        self.tkt             = self._create_tkt_tree (lazy, sort, show_header)
        self._lazy_bind      = None
        self.lazy            = lazy
        if ui_model :
            self.update_model (ui_model)
    # end def __init__

    def update (self, element) :
        return self.tkt_model.update \
            (element, (self.Adapter.row_data (element)))
    # end def update

    def update_model (self, ui_model) :
        if self.ui_model :
            self.tkt_model.clear ()
        self.ui_model = ui_model
        self._model_populate (self.lazy)
    # end def update_model

    def selection (self) :
        return self.tkt.selection ()
    # end def selection

    def clear_selection (self) :
        return self.tkt.clear_selection ()
    # end def clear_selection

    def see (self, element) :
        element = self.tkt_model.iter [element]
        self.tkt.see (self.tkt_model, element)
    # end def see

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

    def _create_tkt_tree (self, lazy, sort, show_header) :
        tkt = self.TNS.Tree      (self.t_model, AC = self.AC)
        tkt.headers_visible = show_header
        tkt.rules_hint      = self.Adapter.rules_hint
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
### __END__ TGL.UI.Tree

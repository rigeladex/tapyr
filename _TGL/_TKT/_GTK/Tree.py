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
#    TGL.TKT.GTK.Tree
#
# Purpose
#    Tree_View widget contained in a scrolled window.
#
# Revision Dates
#    18-May-2005 (MG) Creation
#    10-Jun-2005 (MG) `scroll_policies` added
#    29-Jul-2005 (MG) `see` changed to expand the row which shall be seen
#    29-Jul-2005 (MG) `add` and `remove` added
#    29-Jul-2005 (MG) `next` and `prev` added
#     1-Aug-2005 (MG) `see`: add `set_cursor'
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Cell_Renderer_Text
import _TGL._TKT._GTK.Tree_View
import _TGL._TKT._GTK.Tree_View_Column
import _TGL._TKT._GTK.Scrolled_Window

class Tree (GTK.Tree_View) :
    """A scrollable tree view widget"""

    exposed_widget = None ### required to override the property

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.exposed_widget = self.TNS.Scrolled_Window ()
        ### cannot use the default add here !!! (will add itself or None)
        self.exposed_widget.wtk_object.add             (self.wtk_object)
        self.exposed_widget.show                       ()
    # end def __init__

    def add (self, element, parent = None) :
        self.model.add (element, parent = None)
    # end def add

    def next (self) :
        return self._selection.next ()
    # end def next

    def prev (self) :
        return self._selection.prev ()
    # end def prev
    
    def remove (self, element) :
        self.model.remove (element)
    # end def remove

    def scroll_policies (self, b = None, h = None, v = None) :
        if b is not None :
            v = h = b
        if h is not None :
            self.exposed_widget.hscrollbar_policy = h
        if v is not None :
            self.exposed_widget.vscrollbar_policy = v
    # end def scroll_policies

    def see (self, model, iter, column = None) :
        if column is not None :
            column = self.children [column].wtk_object
        pathes     = []
        get_path   = model.wtk_object.get_path
        while iter :
            pathes.append                       (get_path (iter))
            iter = model.wtk_object.iter_parent (iter)
        if pathes :
            for p in reversed (pathes) :
                self.wtk_object.expand_row (p, False)
            self.wtk_object.scroll_to_cell (p, column)
            self.wtk_object.set_cursor     (p, column, False)
    # end def see

# end class Tree

if __name__ != "__main__" :
    GTK._Export ("Tree")
### __END__ TGL.TKT.GTK.Tree

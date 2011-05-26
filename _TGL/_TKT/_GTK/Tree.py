# -*- coding: iso-8859-15 -*-
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
#     6-Aug-2005 (MG) Basic DND handling added
#     6-Aug-2005 (MG) Alignment of `see` added
#     3-Sep-2005 (MG) Call `show` in `__init__`
#    09-Jan-2006 (MG) `next` and `prev` pass arguments to the selection
#                     functions
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._Meta.Object
from   _TGL._TKT._GTK         import GTK
import _TGL._TKT._GTK.Cell_Renderer_Text
import _TGL._TKT._GTK.Tree_View
import _TGL._TKT._GTK.Tree_View_Column
import _TGL._TKT._GTK.Scrolled_Window

import  gobject

class DND_Type (TFL.Meta.Object) :
    """Object which defines a type used for drag and drop"""

    id    = 80
    Table = {}

    def __new__ (cls, mime_type, scope = 0, info = None) :
        if mime_type in cls.Table :
            self = cls.Table [mime_type]
            if (self.scope != scope) or (info and (self.info != info)) :
                raise TypeError, "Redefinition of `%s`" % (mime_type, )
            return self
        self = cls.Table [mime_type] = super (DND_Type, cls).__new__ (cls)
        self.mime_type               = mime_type
        self.scope                   = scope
        if info is None :
            info    = cls.id
            cls.id += 1
        self.info   = info
        return self
    # end def __new__

# end class DND_Type

class Tree (GTK.Tree_View) :
    """A scrollable tree view widget"""

    exposed_widget     = None ### required to override the property

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.exposed_widget = self.TNS.Scrolled_Window ()
        ### cannot use the default add here !!! (will add itself or None)
        self.exposed_widget.wtk_object.add             (self.wtk_object)
        self.exposed_widget.show                       ()
        self.show                                      ()
    # end def __init__

    def add (self, element, parent = None) :
        self.model.add (element, parent = None)
    # end def add

    def clear_dnd_sources (self) :
        self.wtk_object.drag_source_unset ()
    # end def clear_dnd_sources

    def next (self, * args, ** kw) :
        return self._selection.next (* args, ** kw)
    # end def next

    def prev (self, * args, ** kw) :
        return self._selection.prev (* args, ** kw)
    # end def prev

    def remove (self, element) :
        self.model.remove (element)
    # end def remove

    def set_dnd_targets (self, flags, targets, actions) :
        if not isinstance (flags, int) :
            raise NotImplementedError
        if not isinstance (actions, (tuple, list)) :
            actions = (actions, )
        actions     = sum \
            ( int (getattr (self.TNS, "DND_ACTION_%s" % (a.upper (), )))
                for a in actions
            )
        targets = [(s.mime_type, s.scope, s.info) for s in targets]
        self.wtk_object.drag_dest_set (flags, targets, actions)
    # end def set_dnd_sources

    def set_dnd_sources (self, button, action, sources) :
        button  = getattr (self.TNS, "BUTTON%d_MASK" % (button, ))
        action  = getattr (self.TNS, "DND_ACTION_%s" % (action.upper (), ))
        sources = [(s.mime_type, s.scope, s.info) for s in sources]
        self.wtk_object.drag_source_set (button, sources, action)
    # end def set_dnd_sources

    def scroll_policies (self, b = None, h = None, v = None) :
        if b is not None :
            v = h = b
        if h is not None :
            self.exposed_widget.hscrollbar_policy = h
        if v is not None :
            self.exposed_widget.vscrollbar_policy = v
    # end def scroll_policies

    def see (self, model, iter, column = None, halign = None, valign = None) :
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
            use_align = False
            if not (halign is valign is None) :
                use_align = True
            halign    = halign or 0.0
            valign    = valign or 0.0
            self.wtk_object.scroll_to_cell \
                (p, column, use_align, valign, halign)
            # self.wtk_object.set_cursor     (p, column, False)
    # end def see

# end class Tree

if __name__ != "__main__" :
    GTK._Export ("*")
### __END__ TGL.TKT.GTK.Tree

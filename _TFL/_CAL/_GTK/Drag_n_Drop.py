# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Martin Glück. All rights reserved
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
#    TFL.CAL.GTK.Drag_n_Drop
#
# Purpose
#    Some classes which makes drag and drop with GTK a bit easier to use
#
# Revision Dates
#    11-Feb-2004 (MG) Creation
#    ««revision-date»»···
#--
import  pygtk
pygtk.require ("2.0")
import  gtk
from   _TFL               import TFL
import _TFL._Meta.Object

class Drag_n_Drop_Kind (TFL.Meta.Object) :
    """Models a drag & drop kin, e.g.:
        - text/plain
    """
    __id = [-1]

    def __init__ ( self
                 , kind  = "text/plain"
                 , flags = gtk.TARGET_SAME_APP
                 , id    = None
                 ) :
        self.kind  = kind
        self.flags = flags
        if id is None :
            id = max (self.__id) + 1
        self.id = id
        self.__id.append (id)
    # end def __init__

    def __call__ (self) :
        return (self.kind, self.flags, self.id)
    # end def __call__

# end class Drag_n_Drop_Kind

class Drap_n_Drop (TFL.Meta.Object) :
    """A kind fo container which should hold all source and traget widgets
       for one drag and drop action.
    """

    def __init__ (self, name = None) :
        self.name              = name
        self.sources           = []
        self.destinations      = []
        self.source_kinds      = []
        self.destination_kinds = []
        self.drag_source       = None
        self.drap_target       = None
        self.drap_position     = (None, None)
    # end def __init__

    def _kind (self, kind, * args) :
        if not isinstance (kind, Drag_n_Drop_Kind) :
            kind = Drag_n_Drop_Kind (kind, * args)
        return kind
    # end def _kind

    def add_source_kind (self, * args) :
        self.source_kinds.append (self._kind (* args))
    # end def add_source_kind

    def add_destination_kind (self, * args) :
        self.destination_kinds.append (self._kind (* args))
    # end def add_destination_kind

    def add_source_widget ( self
                          , widget
                          , mask           = gtk.gdk.BUTTON1_MASK
                          , action         = gtk.gdk.ACTION_MOVE
                          , begin_callback = None
                          ) :
        widget.drag_source_set \
            (mask, [kind () for kind in self.source_kinds], action)
        self.sources.append (widget)
        if begin_callback :
            widget.connect ("drag-begin", begin_callback)
    # end def add_source_widget

    def add_destination_widget ( self
                               , widget
                               , mask          = gtk.gdk.BUTTON1_MASK
                               , action        = gtk.gdk.ACTION_MOVE
                               , drop_callback = None
                               ) :
        widget.drag_dest_set \
            ( gtk.DEST_DEFAULT_ALL
            , [kind () for kind in self.destination_kinds]
            , action
            )
        self.destinations.append (widget)
        if drop_callback :
            widget.connect("drag-drop",  drop_callback)
    # end def add_destination_widget

# end class Drap_n_Drop

if __name__ != "__main__" :
    import _TFL._CAL._GTK
    TFL.CAL.GTK._Export ("*")
### __END__ TFL.CAL.GTK.Drag_n_Drop

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
#    TGL.TKT.GTK.Signal
#
# Purpose
#    Warpper for the signal handling of GTK
#
# Revision Dates
#    26-Mar-2005 (MG) Creation
#    31-Mar-2005 (MG) `Key_Binding` added
#    31-Mar-2005 (MG) `GDK_Signal`: `signal_name` corrected
#    31-Mar-2005 (MG) Button signals added (*_Click_[123])
#    ««revision-date»»···
#--

from   _TGL._TKT._GTK         import GTK
from   _TFL                import TFL
import _TFL._Meta.Object

class _Event_ (object) :
    """Opaque event object mapping all `parameters` of the signal into the
       `event` parameter
    ."""

    def __init__ (self, widget, event = None, kw = {}) :
        self.__dict__.update (kw)
        self.widget = widget.get_data ("ktw_object") or widget
        self._event = event
    # end def __init__

    def __getattr__ (self, name) :
        result = getattr (self._event, name)
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class _Event_

class Signal (TFL.Meta.Object) :
    """Base class for all signal types."""

    def __new__ (cls, name, * args, ** kw) :
        if not hasattr (cls, name) :
            self = TFL.Meta.Object.__new__ (cls, * args, ** kw)
            setattr (Signal, name, self)
            return self
        raise NameError, "A signal with the name `%s already exists`" \
              % (name, )
    # end def __new__

    def __init__ (self, name, * args, ** kw) :
        self.name         = name
        self._signal_args = args
        self._doc         = kw.get ("description", "")
        self._bindings    = {}
    # end def __init__

# end class Signal

class GTK_Signal (Signal) :
    """A real GTK signal."""

    def __init__ (self, name, * args, ** kw) :
        self.__super.__init__ (name, * args, ** kw)
        signal_name       = kw.get ("signal_name")
        self._signal_name = signal_name or name.lower ()
        self._callbacks_i = len (args)
    # end def __init__

    def _call (self, widget, event, args) :
        uargs, ukw = args [self._callbacks_i + 1 :]
        kw         = {}
        for name, value in zip (self._signal_args, args) :
            kw [name] = value
        cb   = args [self._callbacks_i]
        return cb (_Event_ (widget, event, kw), * uargs, ** ukw)
    # end def _call

    def __call__ (self, widget, * args) :
        return self._call (widget, None, args)
    # end def __call__

    def connect (self, gtk_widget, callback, args, kw) :
        return gtk_widget.connect \
            (self._signal_name, self, callback, args, kw)
    # end def connect

    def connect_after (self, gtk_widget, callback, args, kw) :
        return gtk_widget.connect_after \
            (self._signal_name, self, callback, args, kw)
    # end def connect_after

    def disconnect (self, gtk_widget, cid) :
        return gtk_widget.disconnect (cid)
    # end def disconnect

    def emit (self, gtk_widget, * args) :
        return gtk_widget.emit (self._signal_name, * args)
    # end def emit

# end clasws GTK_Signal

class GDK_Signal (GTK_Signal) :
    """A signel emitted from the GDK library. These signal have a special
       `event` parameter for the callback which contains some detailed
       information about the event.
    """

    def __init__ (self, name, * args, ** kw) :
        signal_name       = kw.get ("signal_name")
        if not signal_name :
            kw ["signal_name"] = \
                "%s_event" % (name.lower (), )
        self.__super.__init__ (name, * args, ** kw)
    # end def __init__

    def __call__ (self, widget, event, * args) :
        return self._call (widget, event, args)
    # end def __call__

# end class GDK_Signal

GTK_Signal ( "Activate")
GTK_Signal ( "Changed")
GTK_Signal ( "Clicked")
GTK_Signal ( "Cursor_Changed")
GTK_Signal ( "Destroy")
GTK_Signal ( "Drag_Begin",    "drag_context")
GTK_Signal ( "Drag_Data_Get", "drag_context", "selection", "info", "timestamp")
GTK_Signal ( "Drag_Data_Received"
           , "drag_context"
           , "x", "y"
           , "selection"
           , "info"
           , "timestamp"
           )
GTK_Signal ( "Edit")
GTK_Signal ( "Edited", "path_string", "new_text")
GTK_Signal ( "Enter")
GTK_Signal ( "Handle_Moved", "gparamspec", signal_name = "notify::position")
GTK_Signal ( "Key_Binding", "accel_id")
GTK_Signal ( "Leave")
GTK_Signal ( "Map")
GTK_Signal ( "Orientation_Changed", "orientation")
GTK_Signal ( "Realize")
GTK_Signal ( "Pressed")
GTK_Signal ( "Pushed")
GTK_Signal ( "Popped")
GTK_Signal ( "Released")
GTK_Signal ( "Toggled")
GTK_Signal ( "Value_Changed")
GTK_Signal ( "Rows_Reordered")
GTK_Signal ( "Size_Allocate", "allocation")
GTK_Signal ( "Size_Request",  "requisition")
GTK_Signal ( "Show")

GDK_Signal ( "Button_Press")
GDK_Signal ( "Button_Release")
GDK_Signal ( "Configure")
GDK_Signal ( "Delete")
GDK_Signal ( "Double_Click_1")
GDK_Signal ( "Double_Click_2")
GDK_Signal ( "Double_Click_3")
GDK_Signal ( "Enter_Notify")
GDK_Signal ( "Expose")
GDK_Signal ( "Focus_In")
GDK_Signal ( "Focus_Out")
GDK_Signal ( "Key_Press")
GDK_Signal ( "Leave_Notify")
GDK_Signal ( "Motion_Notify")
GDK_Signal ( "Single_Click_1")
GDK_Signal ( "Single_Click_2")
GDK_Signal ( "Single_Click_3")
GDK_Signal ( "Triple_Click_1")
GDK_Signal ( "Triple_Click_2")
GDK_Signal ( "Triple_Click_3")
### special signals for TGW.Notebook
GTK_Signal ( "Switch_Page", "page", "page_nr")

### special signals for Tree's
GTK_Signal ( "Row_Changed",          "tree_path", "tree_iter")
GTK_Signal ( "Row_Expanded",         "tree_iter", "tree_path")
GTK_Signal ( "Row_Collapsed",        "tree_iter", "tree_path")
GTK_Signal ( "Tree_Entry_Expanded",  "ui_entry")
GTK_Signal ( "Tree_Entry_Collapsed", "ui_entry")
GTK_Signal ( "Cell_Renamed",         "new_name")
GTK_Signal ( "Text_Drop",            "ui_target", "ui_source", "text")
GTK_Signal ( "Tree_Cursor_Position_Changed")

if __name__ != "__main__" :
    GTK._Export ("Signal")
### __END__ TGL.TKT.GTK.Signal

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
#    TGL.TKT.GTK.Eventname
#
# Purpose
#    Provide symbolic names for GTK events (keys, mouse clicks, ...)
#
# Revision Dates
#    31-Mar-2005 (MG) Creation
#     1-Apr-2005 (CT) Beefed up
#     2-Apr-2005 (MG) Key names corrected ("<Fx>" -> "Fx", "<Insert>" ->
#                     "Insert", ...)
#     3-Apr-2005 (MG) `Combined_Binder._call` typo fixed
#     7-Apr-2005 (MG) `s/Button_Signal_Binder/Mouse_Button_Binder/g`
#    30-Jul-2005 (MG) Debug output added
#    ««revision-date»»···
#--

"""
Consistency check:

>>> from   _TGL                       import TGL
>>> import _TGL._TKT
>>> import _TGL._TKT.Eventname
>>> import _TGL._TKT._Batch.Eventname
>>> import _TGL._TKT._Tk.Eventname
>>> import _TGL._TKT._GTK.Eventname
>>> TGL.TKT._Eventname.check_names (TGL.TKT.GTK.Eventname, TGL.TKT.Tk.Eventname)
_TGL._TKT._Tk.Eventname defines all names that _TGL._TKT._GTK.Eventname defines
_TGL._TKT._GTK.Eventname defines all names that _TGL._TKT._Tk.Eventname defines
>>> TGL.TKT._Eventname.check_names (TGL.TKT.GTK.Eventname, TGL.TKT.Batch.Eventname)
_TGL._TKT._Batch.Eventname defines all names that _TGL._TKT._GTK.Eventname defines
_TGL._TKT._GTK.Eventname defines all names that _TGL._TKT._Batch.Eventname defines

"""

from   _TGL._TKT._GTK         import GTK
from   _TGL                   import TGL
from   _TFL                   import TFL
import _TFL._Meta.Object
import _TGL._TKT
import _TGL._TKT.Eventname
import _TGL._TKT._GTK.Signal

import  pygtk
pygtk.require ("2.0")
import gtk

class Key_Binder (TFL.Meta.Object) :
    """Binder used to connect a keyboard `shortcut` to a callback."""

    __id = 0

    def __init__ (self, key_name) :
        self.name           = key_name
        try :
            self.key_spec   = kv, km = gtk.accelerator_parse (key_name)
        except :
            print key_name
            raise
        self._connects      = {}
        self._id            = self.__id
        self.__class__.__id = self._id + 1
        assert kv, "%s %s %s" % (key_name, kv, km)
        gtk.binding_entry_add_signal \
            (gtk.Widget, kv, km, "key-binding", int, self._id)
    # end def __init__

    def connect (self, widget, callback, args, kw) :
        wtk = widget.get_data ("ktw_object")
        if not wtk._key_bindings :
            wtk.bind_add (GTK.Signal.Key_Binding, self)
        cid = object ()
        wtk._key_bindings.setdefault (self._id, []).append \
            ((callback, cid, args, kw))
        return cid
    # end def connect

    def connect_after (self, * args, ** kw) :
        return self.connect (* args, ** kw)
    # end def connect_after

    def disconnect (self, widget, cid) :
        wtk = widget.get_data ("ktw_object")
        cbs = wtk._key_bindings.get (self._id, ())
        for i, (cb, id, args, kw) in enumerate (cbs) :
            if cid is id :
                del cbs [i]
        if not cbs :
            del wtk._key_bindings [self._id]
    # end def disconnect

    def __call__ (self, event) :
        widget   = event.widget
        accel_id = event.accel_id
        for cb, cid, args, kw in widget._key_bindings.get (accel_id, ()) :
            if cb (event, * args, ** kw) :
                return True
    # end def __call__

# end class Key_Binder

class Signal_Binder (TFL.Meta.Object) :
    """Binder used to connect signals to callback functions"""

    def __init__ (self, name) :
        self.name   = name
        self.signal = getattr (GTK.Signal, name)
    # end def __init__

    def connect (self, widget, callback, args, kw) :
        return self.signal.connect (widget, callback, args, kw)
    # end def connect

    def connect_after (self, widget, callback, args, kw) :
        return self.signal.connect_after (widget, callback, args, kw)
    # end def connect_after

    def disconnect (self, widget, cid) :
        return self.signal.disconnect (widget, cid)
    # end def disconnect

    def __str__ (self) :
        return self.name
    # end def __str__

# end class Signal_Binder

class Mouse_Button_Binder (Signal_Binder) :
    """A binder which mapps the button-press-event of GTK to new created
       signal for the seperate buttons and event type (single, double, ...)
    """

    delegation_map = \
        { (1, gtk.gdk.  BUTTON_PRESS) : GTK.Signal.Single_Click_1
        , (2, gtk.gdk.  BUTTON_PRESS) : GTK.Signal.Single_Click_2
        , (3, gtk.gdk.  BUTTON_PRESS) : GTK.Signal.Single_Click_3
        , (1, gtk.gdk._2BUTTON_PRESS) : GTK.Signal.Double_Click_1
        , (2, gtk.gdk._2BUTTON_PRESS) : GTK.Signal.Double_Click_2
        , (3, gtk.gdk._2BUTTON_PRESS) : GTK.Signal.Double_Click_3
        , (1, gtk.gdk._3BUTTON_PRESS) : GTK.Signal.Triple_Click_1
        , (2, gtk.gdk._3BUTTON_PRESS) : GTK.Signal.Triple_Click_2
        , (3, gtk.gdk._3BUTTON_PRESS) : GTK.Signal.Triple_Click_3
        }

    def __init__ (self, name, real_signal) :
        self.__super.__init__ (name)
        self.real_signal = getattr (GTK.Signal, real_signal)
    # end def __init__

    def __call__ (self, event) :
        button     = event.button
        event_type = event.type
        event.widget.emit \
            (self.delegation_map [button, event_type], event._event)
    # end def __call__

    def connect (self, widget, callback, args, kw) :
        wtk  = widget.get_data ("ktw_object")
        bbd  = wtk._button_bindings
        real = self.real_signal
        if real not in bbd :
             bbd [real] = (wtk.bind_add (real, self), {})
        cid = self.signal.connect (widget, callback, args, kw)
        bbd [real] [1] [cid] = True
        return cid
    # end def connect

    def connect_after (self, * args, ** kw) :
        return self.connect (* args, ** kw)
    # end def connect_after

    def disconnect (self, widget, cid) :
        wtk  = widget.get_data ("ktw_object")
        bbd  = wtk._button_bindings
        real = self.real_signal
        del bbd [real] [1] [cid]
        if not bbd [real] [1] :
            wtk.unbind (real, bbd [real] [0])
            del bbd [real]
        return self.signal.disconnect (widget, cid)
    # end def disconnect

# end class Mouse_Button_Binder

class Combined_Binder (TFL.Meta.Object) :
    """Allows to create events that combine several signals into one"""

    def __init__ (self, name, * binders) :
        self.name    = name
        self.binders = binders
    # end def __init__

    def _call (self, method, widget, callback, args, kw) :
        return \
            [ getattr (binder, method) (widget, callback, args, kw)
                for binder in self.binders
            ]
    # end def _call

    def connect (self, widget, callback, args, kw) :
        return self._call ("connect", widget, callback, args, kw)
    # end def connect

    def connect_after (self, widget, callback, args, kw) :
        return self._call ("connect_after", widget, callback, args, kw)
    # end def connect_after

    def disconnect (self, widget, cids) :
        return \
            [ binder.disconnect (widget, cid)
                for (binder, cid) in zip (self.binders, cids)
            ]
    # end def disconnect

    def __str__ (self) :
        return "%s (%s)" % \
            (self.name, ", ".join ([str (b) for b in self.binders]))
    # end def __str__

# end class Combined_Binder

MBB = Mouse_Button_Binder

Eventname = TGL.TKT._Eventname \
    ( any_enter         = Combined_Binder
          ( "Any_Enter"
          , Signal_Binder ("Enter_Notify")
          , Signal_Binder ("Focus_In")
          )
    , any_leave         = Combined_Binder
          ( "Any_Leave"
          , Signal_Binder ("Focus_Out")
          , Signal_Binder ("Leave_Notify")
          )
    , click_1           = MBB           ("Single_Click_1", "Button_Press")
    , click_2           = MBB           ("Single_Click_2", "Button_Press")
    , click_3           = MBB           ("Single_Click_3", "Button_Press")
    , close_node        = Key_Binder    ("Delete")
    , close_node_1      = Key_Binder    ("<Shift>Delete")
    , close_node_all    = Key_Binder    ("<Ctrl>Delete")
    , close_window      = Key_Binder    ("<Ctrl>w")
    , commit            = Key_Binder    ("<Ctrl>Return")
    , complete          = Key_Binder    ("<Alt>i")
    , continue_scan     = None ### XXX ??? Signal_Binder ("<Mouse><Move>2")
    , copy              = Key_Binder    ("<Ctrl>c")
    , cursor_down       = Key_Binder    ("Down")
    , cursor_end        = Key_Binder    ("End")
    , cursor_home       = Key_Binder    ("Home")
    , cursor_left       = Key_Binder    ("Left")
    , cursor_right      = Key_Binder    ("Right")
    , cursor_up         = Key_Binder    ("Up")
    , cut               = Key_Binder    ("<Ctrl>x")
    , double_click_1    = MBB           ("Double_Click_1", "Button_Press")
    , double_click_2    = MBB           ("Double_Click_2", "Button_Press")
    , double_click_3    = MBB           ("Double_Click_3", "Button_Press")
    , exit              = Key_Binder    ("<Ctrl>q")
    , focus_enter       = Signal_Binder ("Focus_In")
    , focus_leave       = Signal_Binder ("Focus_Out")
    , help              = Key_Binder    ("F1")
    , history_complete  = Key_Binder    ("<Alt>q")
    , history_next      = Key_Binder    ("<Alt>Down")
    , history_previous  = Key_Binder    ("<Alt>Up")
    , mouse_enter       = Signal_Binder ("Enter_Notify")
    , mouse_leave       = Signal_Binder ("Leave_Notify")
    , mouse_motion      = Signal_Binder ("Motion_Notify")
    , new               = Key_Binder    ("<Ctrl>n")
    , node_down         = Key_Binder    ("<Alt>n")
    , node_end          = Key_Binder    ("<Alt>e")
    , node_home         = Key_Binder    ("<Alt>a")
    , node_left         = Key_Binder    ("<Alt>b")
    , node_right        = Key_Binder    ("<Alt>f")
    , node_up           = Key_Binder    ("<Alt>p")
    , open              = Key_Binder    ("<Ctrl>o")
    , open_node         = Key_Binder    ("Insert")
    , open_node_1       = Key_Binder    ("<Shift>Insert")
    , open_node_all     = Key_Binder    ("<Ctrl>Insert")
    , paste             = Key_Binder    ("<Ctrl>v")
    , Print             = Key_Binder    ("<Ctrl>p")
    , Print_all         = None
    , redo              = Key_Binder    ("<Ctrl>y")
    , rename            = Key_Binder    ("F2")
    , save              = Key_Binder    ("<Ctrl>s")
    , save_and_exit     = Key_Binder    ("<Ctrl>e")
    , save_as           = Key_Binder    ("<Ctrl><Shift>s")
    , search            = Key_Binder    ("<Ctrl>f")
    , search_next       = Key_Binder    ("F3")
    , search_prev       = Key_Binder    ("<Shift>F3")
    , select_all        = Key_Binder    ("<Ctrl>a")
    , start_scan        = None ### XXX ??? Signal_Binder ("<Mouse><Press>2")
    , triple_click_1    = MBB           ("Triple_Click_1", "Button_Press")
    , triple_click_2    = MBB           ("Triple_Click_2", "Button_Press")
    , triple_click_3    = MBB           ("Triple_Click_3", "Button_Press")
    , undo              = Key_Binder    ("<Ctrl>z")
    )

if __name__ != "__main__" :
    GTK._Export ("*")
### __END__ TGL.TKT.GTK.Eventname

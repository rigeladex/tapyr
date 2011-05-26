# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL.TKT.Tk.Command_Interfacer
#
# Purpose
#    Model command interface for Tkinter based GUI
#
# Revision Dates
#    22-Dec-2004 (CT) Creation
#    10-Jan-2005 (CT) `CI_Menu.add_group` completed
#    10-Jan-2005 (CT) `CI_Menu.add_separator` added
#    10-Jan-2005 (CT) `remove_command`, `remove_group`, and
#                     `remove_separator` of `CI_Menu` added
#    10-Jan-2005 (CT) `enable_entry` and `disable_entry` of `CI_Menu` added
#    11-Jan-2005 (CT) `as_check_button` added to `add_command`
#    11-Jan-2005 (CT) `bind_to_activation` and `bind_to_sync` implemented
#    11-Jan-2005 (CT) `bind_to_widget` added
#    11-Jan-2005 (CT) `CI_Menubar` added
#    11-Jan-2005 (CT) `CI_Toolbar` and `CI_Toolbar_Category` added
#    12-Jan-2005 (CT) Factored to `TFL`
#    12-Jan-2005 (CT) `_CI_Widget_` and `_CI_` used as ancestors
#    12-Jan-2005 (CT) s/CI_Toolbar_Category/_CI_Toolbar_Group_/g
#    12-Jan-2005 (CT) `CI_Event_Binder` and `_CI_Event_Binding_` added
#    13-Jan-2005 (CT) Small fixes
#    18-Jan-2005 (CT) Small fixes
#    18-Jan-2005 (CT) Derive from `TFL.TKT.Mixin` instead of `TFL.Meta.Object`
#    26-Jan-2005 (CT) s/as_check_button/state_var/
#    26-Jan-2005 (CT) `Boolean_Variable` exported
#    26-Jan-2005 (CT) `CI_Menu.add_group` changed to return a `CI_Menu`
#                     instead of a `CTK.C_Menu`
#    28-Jan-2005 (CT) `index` added
#    31-Jan-2005 (CT) `_index_offset` factored and used consistently in
#                     `CI_Menu`
#     1-Feb-2005 (CT) Use `CTK.canonical_key_name`
#     1-Feb-2005 (CT) `CI_Menu.index` changed again
#     1-Feb-2005 (CT) `set_auto_short_cuts` added
#     2-Feb-2005 (CT) `CI_Menu.index` changed again
#    14-Feb-2005 (MG) Smaller bugs fixed
#    16-Feb-2005 (MG) `bind_to_widget`: parameter `event_name` added
#    17-Feb-2005 (CT) s/widget/wtk_widget/g
#    21-Feb-2005 (CT) `CI_Menu._index_offset` changed from `1` to `0` (and
#                     `CI_Menubar._index_offset` redefined to `1`)
#    23-Feb-2005 (CT) `exposed_widget` added
#    24-Feb-2005 (CT) `CI_Button_Box` added
#     8-Apr-2005 (CT) `_CI_Toolbar_Group_.add_command` changed to pass
#                     `before = index + delta` to toolbar widget
#    26-Apr-2005 (CT) `CI_Menu.bind_to_widget` fixed (translate `event_name`
#                     via `Eventname`)
#    16-Aug-2005 (CT)  `_CI_Toolbar_Group_` changed to allow nested groups
#                      (without displaying them visually)
#    16-Sep-2005 (MZO) [17208] added manual bind of menu-accelerators.
#    19-Jul-2006 (MZO) [18758] `add_group` implemented
#    26-Jul-2006 (MZO) [18758] label of buttons defined
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL                 import TFL
import _TFL._TKT._Tk
import _TFL._TKT.Command_Interfacer

from   CTK                  import *
from   Regexp               import *
from   predicate            import dict_from_list

import CTK_Toolbar
import traceback
import weakref

class _CI_ (TFL.TKT.Command_Interfacer) :

    name_clean = Regexp ("[^a-zA-Z_0-9]+")

# end class _CI_

class _CI_Widget_ (_CI_) :

    widget = None

    def __init__ (self, AC, parent, ** kw) :
        self.__super.__init__ (AC = AC, parent = parent, ** kw)
        self.wtk_widget = self.exposed_widget \
                        = self.Widget_Type (parent, ** kw)
    # end def __init__

    def clear (self) :
        raise NotImplementedError, "%s.clear" % (self.__class__.__name__ [3:])
    # end def clear

    def destroy (self) :
        if self.wtk_widget is not None :
            self.wtk_widget.destroy ()
            self.wtk_widget = self.exposed_widget = None
    # end def destroy

# end class _CI_Widget_

class CI_Button_Box (_CI_Widget_) :
    """Implement a button box command interfacer for Tkinter"""

    Widget_Type         = CTK.Buttongrid

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.b_name = {}
    # end def __init__

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        b_name  = self.b_name [name] = self.name_clean.sub ("_", name.lower ())
        im_name = icon or b_name
        return self.wtk_widget.add \
            ( button_name = b_name
            , command     = callback
            , image       = CTK.image_mgr.get (im_name)
            , cmd_name    = name
            , text        = name
            )
    # end def add_command

    def remove_command (self, index) :
        raise NotImplementedError, "Buttonbox.remove_command"
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        return self
    # end def add_group

    def remove_group (self, index) :
        raise NotImplementedError, "Buttonbox.remove_group"
    # end def remove_group

    ### event specific methods
    def enable_entry (self, name) :
        self.wtk_widget.enable_entry (self.b_name [name])
    # end def enable

    def disable_entry (self, name) :
        self.wtk_widget.disable_entry (self.b_name [name])
    # end def disable_entry

    def bind_to_sync (self, callback) :
        self.wtk_widget.bind ("<Any-Enter>", callback)
    # end def bind_to_sync

# end class CI_Button_Box

class _CI_Event_Binding_ (_CI_) :
    """Encapsulate a single event binding"""

    def __init__ (self, AC, ev_binder, name, callback, ev_name) :
        self.__super.__init__ (AC = AC)
        self.ev_binder  = weakref.proxy (ev_binder)
        self.name       = name
        self.callback   = callback
        self.ev_name    = ev_name
        self.bindings   = {}
    # end def __init__

    def enable_entry (self, index) :
        bindings = self.bindings
        ev_name  = self.ev_name
        callback = self.callback
        for w in self.ev_binder.widgets :
            bindings [w] = w.bind (ev_name, callback)
    # end def enable

    def disable_entry (self, index) :
        ev_name  = self.ev_name
        for w, binding in self.bindings.iteritems () :
            w.unbind (ev_name, binding)
    # end def disable_entry

# end class _CI_Event_Binding_

class CI_Event_Binder (_CI_) :
    """Implement an event-bound interfacer for Tkinter (i.e., commands
       triggered by key-presses, mouse-clicks and other such events)
    """

    def __init__ (self, AC, * widgets) :
        self.__super.__init__          (AC = AC)
        self.widgets  = dict_from_list (widgets)
        self.bindings = {}
    # end def __init__

    def add_widget (self, * widgets) :
        for w in widgets :
            self.widgets [w] = None
    # end def add_widget

    def remove_widget (self, * widgets) :
        for w in widgets :
            try :
                del self.widgets [w]
            except KeyError :
                pass
    # end def remove_widget

    def destroy (self) :
        for b in self.bindings.itervalues () :
            b.disable_entry (b)
        self.widgets  = None
        self.bindings = None
    # end def destroy

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        ev_name = getattr (self.TNS.Eventname, (info or name).lower ())
        result  = _CI_Event_Binding_ (self.AC, self, name, callback, ev_name)
        self.bindings [name] = result
        return result
    # end def add_command

    def remove_command (self, index) :
        binding = self.bindings [index]
        bindings.disable_entry  (index)
        del self.bindings       [index]
    # end def remove_command

    ### event specific methods
    def enable_entry (self, index) :
        self.bindings [index].enable_entry (index)
    # end def enable

    def disable_entry (self, index) :
        self.bindings [index].disable_entry (index)
    # end def disable_entry

# end class CI_Event_Binder

class CI_Menu (_CI_Widget_) :
    """Implement a menu command interfacer for Tkinter"""

    Widget_Type        = CTK.C_Menu
    max_cmds_per_group = 20

    _index_offset      = 0

    def clear (self) :
        self.wtk_widget.clear ()
    # end def clear

    def index (self, name) :
        if name == -1 :
            result = self.wtk_widget.index (END)
            if result is not None :
                result += self._index_offset
        else :
            result = self.wtk_widget.index (name) - self._index_offset
        return result
    # end def index

    def set_auto_short_cuts (self) :
        try :
            self.wtk_widget.set_auto_short_cuts ()
        except CTK.TclError :
            pass
    # end def set_auto_short_cuts

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        if state_var is not None :
            fct = self.wtk_widget.insert_checkbutton
            kw  = dict (variable = state_var, ** kw)
        else :
            fct = self.wtk_widget.insert_command
        self._bind_accelerator_to_toplevel (accelerator, callback)
        return fct \
            ( index       = index + delta + self._index_offset
            , label       = name
            , command     = callback
            , underline   = underline
            , accelerator = CTK.canonical_key_name (accelerator)
            , ** kw
            )
    # end def add_command

    def remove_command (self, index) :
        self._remove (index + self._index_offset)
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        result = CI_Menu \
            ( self.AC, self.wtk_widget
            , name       = self.name_clean.sub ("_", name.lower ())
            , balloon    = self.wtk_widget.balloon
            , help       = self.wtk_widget.help_widget
            , tearoff    = 0
            )
        self.wtk_widget.insert_cascade \
            ( index + delta + self._index_offset
            , label      = name
            , menu       = result.wtk_widget
            , underline  = kw.get ("underline")
            )
        return result
    # end def add_group

    def remove_group (self, index) :
        self._remove (index + self._index_offset)
    # end def remove_group

    ### separator specific methods
    def add_separator (self, name = None, index = None, delta = 0) :
        self.wtk_widget.insert_separator (index + delta + self._index_offset)
    # end def add_separator

    def remove_separator (self, index) :
        self._remove (index + self._index_offset)
    # end def remove_separator

    ### event specific methods
    def bind_to_activation (self, callback) :
        self.wtk_widget.configure (postcommand = callback)
    # end def bind_to_activation

    def bind_to_sync (self, callback) :
        self.wtk_widget.configure (postcommand = callback)
    # end def bind_to_sync

    def bind_to_widget (self, widget, event_name) :
        ev_name = getattr (self.TNS.Eventname, (event_name).lower ())
        widget.bind (ev_name, self.wtk_widget.popup)
    # end def bind_to_widget

    def enable_entry (self, name) :
        try :
            self.wtk_widget.enable_entry (name)
        except CTK.TclError :
            if 0 and __debug__ :
                traceback.print_exc ()
                print "Enable_entry", self.wtk_widget, name
    # end def enable

    def disable_entry (self, name) :
        try :
            self.wtk_widget.disable_entry (name)
        except CTK.TclError :
            if 0 and __debug__ :
                traceback.print_exc ()
                print "Disable_entry", self.wtk_widget, name
    # end def disable_entry

    ### internals
    def _bind_accelerator_to_toplevel (self, accelerator, callback) :
        ### tk does not bind accel (display only textlabel).
        if accelerator :
            toplevel = self._find_toplevel ()
            if toplevel is not None :
                toplevel.bind (accelerator, callback)
    # end def _bind_accelerator_to_toplevel

    def _find_toplevel (self) :
        ### return toplevel window (widget) or None
        toplevel = getattr (self, "_menu_toplevel", -1)
        if toplevel == -1 :
            self._menu_toplevel = None
            menubar = self.wtk_widget.winfo_toplevel ()
            if menubar is not None :
                top = menubar.master.winfo_toplevel ()
                if toplevel is not None :
                    self._menu_toplevel = top
            toplevel = self._menu_toplevel
        return toplevel
    # end def _find_toplevel

    def _remove (self, index) :
        self.wtk_widget.delete (index)
    # end def _remove

# end class CI_Menu

class CI_Menubar (CI_Menu) :
    """Implement a menubar command interfacer for Tkinter"""

    ### for some reason, `_index_offset` must be 1 for menus used as a
    ### menubar (otherwise, the left most entry isn't displayed)
    _index_offset       = 1

    def __init__ (self, AC, parent, ** kw) :
        self.__super.__init__ (AC = AC, parent = parent, ** kw)
        parent.toplevel.configure (menu = self.wtk_widget)
        ### the following hacks around a bug in Tkinter 1.63 which doesn't
        ### correctly handle menus configured as menubar
        hacked_name = str (self.wtk_widget).replace (".", "#")
        parent.toplevel.children [hacked_name] = self.wtk_widget
    # end def __init__

# end class CI_Menubar

class CI_Toolbar (_CI_Widget_) :
    """Implement a toolbar command interfacer for Tkinter"""

    Widget_Type = CTK_Toolbar.Toolbar

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        raise NotImplementedError, "Toolbar.add_command"
    # end def add_command

    def remove_command (self, index) :
        raise NotImplementedError, "Toolbar.remove_command"
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        cat    = self.wtk_widget.add_category (name, index, delta)
        result = _CI_Toolbar_Group_ (self.AC, cat, self.wtk_widget)
        return result
    # end def add_group

    def remove_group (self, index) :
        raise NotImplementedError, "Toolbar.remove_group"
    # end def remove_group

    ### event specific methods
    def bind_to_sync (self, callback) :
        self.wtk_widget.bind ("<Any-Enter>", callback)
    # end def bind_to_sync

# end class CI_Toolbar

class _CI_Toolbar_Group_ (_CI_) :

    def __init__ (self, AC, category, widget, b_name = None, index_offset = 0) :
        self.__super.__init__ (AC = AC)
        if b_name is None :
            b_name        = {}
        self.category     = category
        self.wtk_widget   = self.exposed_widget = widget
        self.b_name       = b_name
        self.index_offset = index_offset
    # end def __init__

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        if state_var is not None :
            raise NotImplementedError, "as_check_button"
        b_name  = self.b_name [name] = self.name_clean.sub ("_", name.lower ())
        im_name = icon or b_name
        return self.wtk_widget.add_button \
            ( category    = self.category
            , name        = b_name
            , command     = callback
            , image       = CTK.image_mgr.get (im_name)
            , cmd_name    = cmd_name
            , before      = index + delta + self.index_offset
            )
    # end def add_command

    def remove_command (self, index) :
        raise NotImplementedError, "Toolbar.remove_command"
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        return self.__class__ \
            ( self.AC, self.category, self.wtk_widget
            , b_name        = self.b_name
            , index_offset  = len (self.b_name)
            )
    # end def add_group

    def remove_group (self, index) :
        raise NotImplementedError, "Toolbar.remove_group"
    # end def remove_group

    ### event specific methods
    def enable_entry (self, name) :
        self.wtk_widget [self.category].enable_entry (self.b_name [name])
    # end def enable

    def disable_entry (self, name) :
        self.wtk_widget [self.category].disable_entry (self.b_name [name])
    # end def disable_entry

# end class _CI_Toolbar_Group_

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("*")
    TFL.TKT.Tk.Boolean_Variable = CTK.Boolean_Variable
### __END__ TFL.TKT.Tk.Command_Interfacer

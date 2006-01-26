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
#    TGL.TKT.GTK.Command_Interfacer
#
# Purpose
#    Model command interface for GTK based GUI
#
# Revision Dates
#     8-Apr-2005 (MG) Creation
#     9-May-2005 (MG) Check items (toolbar, menu) added
#     9-May-2005 (MG) `CI_Button_Box` added
#    12-May-2005 (MG) Icon support for menus added
#    12-May-2005 (MG) Group support added to `_CI_Toolbar_Group_`
#    15-May-2005 (MG) `accelerator` support added
#    15-May-2005 (MG) `underline` support added
#    20-May-2005 (MG) `_menu_item`: added support for `Key_Binder` objects as
#                     accelerator
#    20-May-2005 (MG) `_push_help` and `_pop_help` impelented
#    21-May-2005 (MG) `_CI_Menu_Mixin_._new_group`: right align hack for
#                     `Help` added
#    10-Jun-2005 (MG) Test for automatic menu item activation
#    10-Jun-2005 (MG) Allow signal's for `Event_Binder`
#    10-Jun-2005 (MG) `Event_Binder` corrected
#    27-Jul-2005 (MG) `CI_Event_Binder.add_widget` type corrected
#    12-Aug-2005 (MG) `CI_Event_Binder.__init__`: allow ** kw
#    ««revision-date»»···
#--
from   _TFL.predicate       import dict_from_list
from   _TGL                 import TGL
from   _TFL.Regexp          import *
import _TFL.NO_List
import _TGL._TKT._GTK
import _TGL._TKT.Command_Interfacer
import _TGL._TKT._GTK.Menu
import _TGL._TKT._GTK.Menu_Bar
import _TGL._TKT._GTK.Menu_Item
import _TGL._TKT._GTK.Image_Menu_Item
import _TGL._TKT._GTK.Check_Menu_Item
import _TGL._TKT._GTK.Separator_Menu_Item

import _TGL._TKT._GTK.Toolbar
import _TGL._TKT._GTK.Tool_Button
import _TGL._TKT._GTK.Toggle_Tool_Button
import _TGL._TKT._GTK.Menu_Tool_Button
import _TGL._TKT._GTK.Separator_Tool_Item
import _TGL._TKT._GTK.Image

import _TGL._TKT._GTK.Frame
import _TGL._TKT._GTK.H_Button_Box
import _TGL._TKT._GTK.Button
import _TGL._TKT._GTK.Toggle_Button
import _TGL._TKT._GTK.Constants

import  weakref
import  traceback

GTK = TGL.TKT.GTK

class Boolean_Variable (object) :
    """Variable used by the Command Manager for a checkbox style command
       interfacer element.
    """

    def __init__ (self, default = False, states = (False, True)) :
        self._state            = default
        self._clients          = weakref.WeakKeyDictionary ()
    # end def __init__

    def register (self, client) :
        self._clients [client] = True
    # end def register

    def unregister (self, client) :
        del self._clients [client]
    # end def unregister

    def _set_state (self, state) :
        if self._state != state :
            self._state = state
            for c in self._clients.iterkeys () :
                c.active = state
    # end def _set_state

    state = property (lambda s : s._state, _set_state)

# end class Boolean_Variable

class _CI_ (TFL.TKT.Command_Interfacer) :
    """Base class for all command interfacers"""

    active_help = None

    def _push_help (self, event = None, item = None) :
        ### XXX is this the correct way to find the help ???
        cmd   = getattr (item, "_command", None)
        msg   = cmd.__doc__
        label = item.label.label
        if cmd :
            try :
                if hasattr (cmd, "im_self") :
                    msg = cmd.im_self.menu_help (label, cmd, msg)
                else :
                    msg = cmd.menu_help         (label, cmd, msg)
            except (SystemExit, KeyboardInterrupt), exc :
                raise
            except :
                pass
        self.help_widget.push_help (msg)
    # end def _push_help

    def _pop_help (self, event = None) :
        self.help_widget.pop_help ()
    # end def _pop_help

# end class _CI_

class _CI_Item_Mixin_ (_CI_) :
    """Base class for all command interfacers using a `NO_List` to store the
       position of the `child`
    """

    def __init__ (self, balloon = None, help = None, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._items      = TFL.NO_List ()
        self.balloon     = balloon
        self.help_widget = help
    # end def __init__

    def index (self, name) :
        return self._items [name]
    # end def index

    ### command specific methods
    def add_command ( self, name, callback
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
            fct = self._new_check_item
            kw ["variable"] = state_var
        else :
            fct = self._new_item
        item = fct \
            ( label       = name
            , command     = callback
            , underline   = underline
            , icon        = icon
            , accelerator = accelerator
            , ** kw
            )
        item._command = callback
        return self._insert_item (index, delta, item)
    # end def add_command

    def remove_command (self, index) :
        self._remove (index)
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, icon = None, ** kw) :
        item, result = self._new_group (name, icon)
        self._insert_item              (index, delta, item)
        return result
    # end def add_group

    def remove_group (self, index) :
        self._remove (index)
    # end def remove_group

    ### separator specific methods
    def add_separator (self, name = None, index = None, delta = 0) :
        item =  self.Separator_Class ()
        return self._insert_item     (index, delta, item)
    # end def add_separator

    def remove_separator (self, index) :
        self._remove (index)
    # end def remove_separator

    def enable_entry (self, name) :
        try :
            self._items [name].sensitive = True
        except (KeyError, AttributeError) :
            if 1 and __debug__ :
                traceback.print_exc ()
                print "Enable_entry", self, name, self._items.keys ()
    # end def enable

    def disable_entry (self, name) :
        try :
            self._items [name].sensitive = False
        except (KeyError, AttributeError) :
            if 1 and __debug__ :
                traceback.print_exc ()
                print "Disable_entry", self, name, self._items.keys ()
    # end def disable_entry

# end class _CI_Item_Mixin_

class CI_Button_Box (_CI_Item_Mixin_, GTK.H_Button_Box) :
    """Implement a button box command interfacer for GTK"""

    def _new_group (self, name, icon = None) :
        item              = CI_Button_Box   (AC = self.AC)
        frame             = self.TNS.Frame  (AC = self.AC, name = name)
        frame.shadow_type = self.TNS.SHADOW_OUT
        frame.add (item)
        item.show ()
        return frame, item
    # end def _new_group

    def _insert_item (self, index, delta, item) :
        self._items.insert (index, item, delta)
        self.pack          (item, fill = True, expand = True)
        item.show          ()
        return item
    # end def _insert_item

    def add_separator (self, * args, ** kw) :
        return None
    # end def add_separator

    def _button_box_item ( self
                         , cls
                         , label
                         , command     = None
                         , underline   = None
                         , icon        = None
                         , accelerator = None
                         , ** kw
                         ) :
        item = cls (label = label, name = label, AC = self.AC)
        if command :
            item.bind_add (self.TNS.Signal.Clicked, command)
        if self.help_widget :
            item.bind_add (self.TNS.Signal.Enter_Notify, self._push_help)
            item.bind_add (self.TNS.Signal.Leave_Notify, self._pop_help)
        return item
    # end def _button_box_item

    def _new_item ( self
                  , label
                  , command     = None
                  , underline   = None
                  , icon        = None
                  , accelerator = None
                  , ** kw
                  ) :
        return self._button_box_item \
            ( self.TNS.Button
            , label       = label
            , command     = command
            , underline   = underline
            , icon        = icon
            , accelerator = accelerator
            , ** kw
            )
    # end def _new_item

    def _new_check_item ( self
                        , label
                        , command     = None
                        , underline   = None
                        , icon        = None
                        , accelerator = None
                        , variable    = None
                        , ** kw
                         ) :
        item = self._button_box_item \
            ( self.TNS.Toggle_Button
            , label       = label
            , command     = command
            , underline   = underline
            , icon        = icon
            , accelerator = accelerator
            , ** kw
            )
        item.stock_id = icon
        item.variable = variable
        variable.register (item)
        item.bind_add (self.TNS.Signal.Toggled, self._update_variable)
        return item
    # end def _new_check_item

    def _update_variable (self, event) :
        item                = event.widget
        item.variable.state = item.active
    # end def _update_variable

# end class CI_Button_Box

class CI_Event_Binder (_CI_) :
    """Implement an event-bound interfacer for Tkinter (i.e., commands
       triggered by key-presses, mouse-clicks and other such events)
    """

    def __init__ (self, AC = None, * widgets, ** kw) :
        self.__super.__init__ (AC = AC)
        self.bindings = {}
        self.widgets  = dict_from_list (widgets)
    # end def __init__

    def add_widget (self, * widgets) :
        for w in widgets :
            self.widgets [w] = None
        ### a new widget has been added -> enable the bindings
        for name in self.bindings.iterkeys () :
            self.enable_entry (name)
    # end def add_widget

    def remove_widget (self, * widgets) :
        for w in widgets :
            try :
                del self.widgets [w]
            except KeyError :
                pass
    # end def remove_widget

    def destroy (self) :
        for b in self.bindings.iterkeys () :
            self.disable_entry (b)
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
        info                 = info or name
        event                = getattr \
            (self.TNS.Eventname, info, getattr (self.TNS.Signal, info, None))
        assert event, "%r:%r" % (info, name)
        self.bindings [name] = [event, callback, []]
        ### all other command interfacers (menu, toolbar) are enabled by
        ### default -> enable the binding as well
        self.enable_entry (name)
    # end def add_command

    def remove_command (self, index) :
        self.disable_entry (index)
        del self.bindings  [index]
    # end def remove_command

    ### event specific methods
    def enable_entry (self, index) :
        signal, callback, conn_ids = self.bindings [index]
        self.disable_entry (index)
        conn_ids = self.bindings [index] [-1]
        for w in self.widgets :
            conn_ids.append ((w, w.bind_add (signal, callback)))
    # end def enable

    def disable_entry (self, index) :
        signal, callback, conn_ids = self.bindings [index]
        for w, cid in conn_ids :
            w.unbind (signal, cid)
        self.bindings [index] [-1] = []
    # end def disable_entry

# end class CI_Event_Binder

class _CI_Menu_Mixin_ (_CI_Item_Mixin_) :
    """Mixin for menu and menubar"""

    Separator_Class = GTK.Separator_Menu_Item

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self._short_map          = {}
        self._pending_short_cuts = {}
    # end def __init__

    def _new_group (self, name, icon = None) :
        TNS = self.TNS
        AC  = self.AC
        if icon :
            item            = TNS.Image_Menu_Item \
                ( label     = name
                , icon      = icon
                , AC        = AC
                )
        else :
            item            = TNS.Menu_Item \
                ( label     = name
                , AC        = AC
                )
        if name == "Help" :
            item.right_justified = True
        self._handle_shortcut (item, name, None)
        item.submenu        = menu = CI_Menu \
            ( AC            = AC
            , name          = name
            , balloon       = self.balloon
            , help          = self.help_widget
            , accel_group   = self.accel_group
            )
        menu.show         ()
        #item.bind_add (TNS.Signal.Activate, self._activate_menuentry)
        return item, menu
    # end def _new_group

    def _activate_menuentry (self, event) :
        menu    = event.widget.submenu
        print menu.wtk_object.child_focus (self.TNS.gtk.DIR_DOWN)
        default = [c for c in menu.children if c.sensitive]
        if 0 and default :
            w = default [0].wtk_object
            print w.child_focus (self.TNS.gtk.DIR_DOWN)
            w.grab_focus ()
    # end def _activate_menuentry

    def _menu_item ( self
                   , cls
                   , label
                   , command     = None
                   , underline   = None
                   , accelerator = None
                   , ** kw
                   ) :
        item = cls \
            ( label     = label
            , name      = label
            , underline = underline
            , AC        = self.AC
            , ** kw
            )
        if command :
            item.bind_add (self.TNS.Signal.Activate, command)
        if self.help_widget :
            item.bind_add (self.TNS.Signal.Select,   self._push_help, item)
            item.bind_add (self.TNS.Signal.Deselect, self._pop_help)
        if accelerator and self.accel_group :
            if isinstance (accelerator, str) :
                kv, km = GTK.gtk.accelerator_parse (accelerator)
            else :
                kv, km = accelerator.key_spec
            item.add_accelerator \
                ("activate", self.accel_group, kv, km, self.TNS.ACCEL_VISIBLE)
        self._handle_shortcut (item, label, underline)
        return item
    # end def _menu_item

    def _new_item ( self
                  , label
                  , command     = None
                  , underline   = None
                  , icon        = None
                  , accelerator = None
                  , ** kw
                  ) :
        if icon :
            cls         = self.TNS.Image_Menu_Item
            kw ["icon"] = icon
        else :
            cls = self.TNS.Menu_Item
        return self._menu_item \
            ( cls
            , label       = label
            , command     = command
            , underline   = underline
            , accelerator = accelerator
            , ** kw
            )
    # end def _new_item

    def _new_check_item ( self
                        , label
                        , command     = None
                        , underline   = None
                        , icon        = None
                        , accelerator = None
                        , variable    = None
                        , ** kw
                        ) :
        item = self._menu_item \
            ( self.TNS.Check_Menu_Item
            , label       = label
            , command     = command
            , underline   = underline
            , accelerator = accelerator
            , ** kw
            )
        item.variable = variable
        variable.register (item)
        item.bind_add (self.TNS.Signal.Toggled, self._update_variable)
        return item
    # end def _new_check_item

    def _update_variable (self, event) :
        item                = event.widget
        item.variable.state = item.active
    # end def _update_variable

    def _insert_item (self, index, delta, item) :
        ### insert the new item to the `_items` NO-list and add the new item
        ### to the menu/menubar/toolbar
        self._items.insert (index, item, delta)
        self.insert        (item, self._items.n_index  (item.name))
        item.show          ()
        return item
    # end def _insert_item

    def _remove (self, index) :
        item = self._items [index]
        del self._items    [index]
        self.remove (item)
    # end def _remove

    def _handle_shortcut (self, item, label, underline) :
        if underline is not None :
            short_cut = label [underline]
            if (   self._short_map.has_key (short_cut)
               and not short_cut.isdigit ()
               ) :
                msg = ( "Duplicate short cut `%s' for "
                        "menu entries `%s' and `%s'"
                      )
                print msg % (short_cut, self._short_map [short_cut], label)
                self._add_pending_short_cut (item, short_cut, label)
            else :
                self._short_map [short_cut] = label
        else :
            sc, i = self._letter_shortcut (label, label [0], 0)
            if sc :
                self._add_pending_short_cut (item, sc, label)
    # end def _handle_shortcut

    def _letter_shortcut (self, label, sc, i) :
        while not sc.isalpha () :
            i = i + 1
            if i > len (label) : return None, None
            sc = label [i]
        return sc, i
    # end def _letter_shortcut

    def _add_pending_short_cut (self, item, short_cut, label) :
        self._pending_short_cuts.setdefault \
            (short_cut.lower (), []).append ((item, label))
    # end def _add_pending_short_cut

    def set_auto_short_cuts (self) :
        """Set short cuts automatically for all menu entries for which no
           unique short cut was explicitly set.
        """
        items = sorted \
            ( self._pending_short_cuts.items ()
            , lambda (scl,  ll), (scr, lr) :
                  cmp (scl, scr) or cmp (len (ll), len (lr))
            )
        for sc, labels in items :
            del self._pending_short_cuts [sc]
            for (item, label) in labels :
                i     = label.lower ().index (sc)
                sc, i = self._unique_short_cut (label, sc, i)
                if sc is not None :
                    self._short_map [sc] = label
                    item.update_label (label, i)
    # end def set_auto_short_cuts

    def _unique_short_cut (self, label, sc, i) :
        sc, i = self._letter_shortcut (label, sc, i)
        if sc and self._short_map.has_key (sc) :
            for i in range (i, len (label)) :
                sc = label [i].lower ()
                if not sc.isalpha ()                : continue
                if not self._short_map.has_key (sc) : return sc, i
            return None, None
        else :
            return sc, i
    # end def _unique_short_cut

# end class _CI_Menu_Mixin_

class CI_Menu (_CI_Menu_Mixin_, GTK.Menu) :
    """Implement a menu command interfacer for GTK"""

    def __init__ (self, accel_group = None, ** kw) :
        self.__super.__init__ (** kw)
        self.accel_group = accel_group
    # end def __init__

    ### event specific methods
    def bind_to_activation (self, callback) :
        self.wtk_object.bind_add (self.TNS.Realize, callback)
    # end def bind_to_activation

    def bind_to_widget (self, widget, event_name) :
        ### use Event_Name/Event_Binder for the event_name <-> event_name
        event = getattr (self.TNS.Eventname, event_name)
        widget.bind_add (event, self.popup)
    # end def bind_to_widget

# end class CI_Menu

class CI_Menubar (_CI_Menu_Mixin_, GTK.Menu_Bar) :
    """Implement a menubar command interfacer for GTK"""

    def __init__ (self, accel_group = None, ** kw) :
        self.__super.__init__ (** kw)
        self.accel_group = accel_group
    # end def __init__

    def bind_to_sync (self, callback) :
        self.bind_replace (self.TNS.Signal.Enter_Notify, callback)
    # end def bind_to_sync

# end class CI_Menubar

class _CI_Toolbar_Mixin_ (_CI_Item_Mixin_) :

    Separator_Class  = GTK.Separator_Tool_Item
    group_seperators = 0

    def _insert_item (self, index, delta, item, correction = 0) :
        self._items.insert        (index, item, delta)
        pos = self._items.n_index (item.name)
        if isinstance (item, self.TNS.Tool_Item) :
            self.insert    (item, pos + correction)
            item.show      ()
        else :
            if len (self._items) > 1 :
                ### a group inserted as first group
                pos = 1
            if pos > 0 :
                ### this is a group which is not the first, so let's insert and
                ### seperator
                g = _CI_Toolbar_Group_ \
                    ( name    = "GS_%d" % self.group_seperators
                    , toolbar = item.toolbar
                    , balloon = item.balloon
                    , help    = item.help_widget
                    , AC      = self.AC
                    )
                self.__class__.group_seperators += 1
                self._items.insert     (pos, g)
                g.add_separator        ()
        return item
    # end def _insert_item

    def _remove (self, index) :
        item = self._items [index]
        del self._items    [index]
        self.remove (item)
    # end def _remove

    def _toolbar_item ( self
                  , cls
                  , label
                  , command     = None
                  , underline   = None
                  , icon        = None
                  , accelerator = None
                  , ** kw
                  ) :
        if icon :
            icon = self.TNS.Image \
                ( stock_id = icon
                , size     = GTK.gtk.ICON_SIZE_SMALL_TOOLBAR
                , AC       = self.AC
                )
            icon.show ()
        item = cls (icon = icon, label = label, name = label, AC = self.AC)
        if command :
            item.bind_add (self.TNS.Signal.Clicked, command)
        if self.help_widget :
            item.bind_add (self.TNS.Signal.Enter_Notify, self._push_help)
            item.bind_add (self.TNS.Signal.Leave_Notify, self._pop_help)
        return item
    # end def _toolbar_item

    def _new_item ( self
                  , label
                  , command     = None
                  , underline   = None
                  , icon        = None
                  , accelerator = None
                  , ** kw
                  ) :
        return self._toolbar_item \
            ( self.TNS.Tool_Button
            , label       = label
            , command     = command
            , underline   = underline
            , icon        = icon
            , accelerator = accelerator
            , ** kw
            )
    # end def _new_item

    def _new_check_item ( self
                        , label
                        , command     = None
                        , underline   = None
                        , icon        = None
                        , accelerator = None
                        , variable    = None
                        , ** kw
                         ) :
        item = self._toolbar_item \
            ( self.TNS.Toggle_Tool_Button
            , label       = label
            , command     = command
            , underline   = underline
            , icon        = icon
            , accelerator = accelerator
            , ** kw
            )
        item.stock_id = icon
        item.variable = variable
        variable.register (item)
        item.bind_add (self.TNS.Signal.Toggled, self._update_variable)
        return item
    # end def _new_check_item

    def _update_variable (self, event) :
        item                = event.widget
        item.variable.state = item.active
    # end def _update_variable

# end class _CI_Toolbar_Mixin_

class CI_Toolbar (_CI_Toolbar_Mixin_, GTK.Toolbar) :
    """Implement a toolbar command interfacer for GTK"""

    Separator_Class = GTK.Separator_Menu_Item

    def bind_to_sync (self, callback) :
        self.bind_replace (self.TNS.Signal.Enter_Notify, callback)
    # end def bind_to_sync

    def _new_group (self, name, icon = None) :
        group = _CI_Toolbar_Group_ \
            ( name    = name
            , toolbar = self
            , balloon = self.balloon
            , help    = self.help_widget
            , AC      = self.AC
            )
        return group, group
    # end def _new_group

# end class CI_Toolbar

class _CI_Toolbar_Group_ (_CI_Toolbar_Mixin_) :

    insert = property (lambda s : s.toolbar.insert)
    remove = property (lambda s : s.toolbar.remove)

    def __init__ (self, AC, name, toolbar, balloon = None, help = None) :
        self.__super.__init__ (AC = AC, balloon = balloon, help = help)
        self.name         = name
        self.toolbar      = toolbar
    # end def __init__

    def _insert_item (self, index, delta, item) :
        correction = 0
        for i in range (self.toolbar._items.n_index (self.name)) :
            correction += len (self.toolbar._items [i])
        result = self.__super._insert_item (index, delta, item, correction)
        return result
    # end def _insert_item

    def _new_group (self, name, icon = None) :
        item             = self._toolbar_item \
            ( self.TNS.Menu_Tool_Button
            , label      = name
            , icon       = icon
            )
        item.menu = menu = CI_Menu \
            ( AC         = self.AC
            , name       = name
            , balloon    = self.balloon
            , help       = self.help_widget
            )
        menu.show         ()
        return item, menu
    # end def _new_group

    def __len__ (self) : return len (self._items)

# end class _CI_Toolbar_Group_

if __name__ != "__main__" :
    TGL.TKT.GTK._Export ("*")
### __END__ TGL.TKT.GTK.Command_Interfacer



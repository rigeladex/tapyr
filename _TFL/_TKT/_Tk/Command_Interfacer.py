# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TOM.TKT.Tk.Command_Interfacer
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
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _TOM                 import TOM
import _TOM._TKT.Command_Interfacer

from   CTK                  import *
from   Regexp               import *
import CTK_Toolbar

_name_clean = Regexp ("[^a-zA-Z_0-9]+")


class _CI_ (TOM.TKT.Command_Interfacer) :

    name_clean = _name_clean

    def __init__ (self, parent, ** kw) :
        self.widget = self.Widget_Type (parent, ** kw)
    # end def __init__

    def destroy (self) :
        self.widget.destroy ()
    # end def destroy

# end class _CI_Mixin_

class CI_Menu (_CI_) :
    """Implement a menu command interfacer for Tkinter"""

    Widget_Type = CTK.Menu

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = info
            , as_check_button = False
            , cmd_name        = None
            , ** kw
            ) :
        if as_check_button :
            fct = self.widget.insert_checkbutton
        else :
            fct = self.widget.insert_command
        return fct \
            ( index + delta + 1
            , label       = name
            , command     = callback
            , underline   = underline
            , accelerator = accelerator
            , ** kw
            )
    # end def add_command

    def remove_command (self, index) :
        self._remove (index)
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        result = CTK.C_Menu \
            ( self.widget
            , name       = name.lower ()
            , balloon    = self.widget.balloon
            , help       = self.widget.help_widget
            , tearoff    = 0
            )
        self.widget.insert_cascade \
            ( index + delta + 1
            , label      = name
            , menu       = result
            , underline  = kw.get ("underline")
            )
        return result
    # end def add_group

    def remove_group (self, index) :
        self._remove (index)
    # end def remove_group

    ### separator specific methods
    def add_separator (self, name = None, index = None, delta = 0) :
        self.widget.insert_separator (index + delta + 1)
    # end def add_separator

    def remove_separator (self, index) :
        self._remove (index)
    # end def remove_separator

    ### event specific methods
    def bind_to_activation (self, callback) :
        self.widget.configure (postcommand = callback)
    # end def bind_to_activation

    def bind_to_sync (self, callback) :
        self.widget.configure (postcommand = callback)
    # end def bind_to_sync

    def bind_to_widget (self, widget) :
        widget.bind ("<ButtonPress-3>", self.widget.post)
    # end def bind_to_widget

    def enable_entry (self, name) :
        self.widget.enable_entry (name)
    # end def enable

    def disable_entry (self, name) :
        self.widget.disable_entry (name)
    # end def disable_entry

    ### internals
    def _remove (self, index) :
        self.widget.delete (index)
    # end def _remove

# end class CI_Menu

class CI_Menubar (CI_Menu) :
    """Implement a menubar command interfacer for Tkinter"""

    def __init__ (self, parent, ** kw) :
        self.__super.__init__ (parent, ** kw)
        parent.toplevel.configure (menu = self.widget)
        ### the following hacks around a bug in Tkinter 1.63 which doesn't
        ### correctly handle menus configured as menubar
        hacked_name = string.replace (str (self.widget), ".", "#")
        parent.toplevel.children [hacked_name] = self.widget
    # end def __init__

# end class CI_Menubar

class CI_Toolbar (_CI_) :
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
            , info            = info
            , as_check_button = False
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
        self.widget.add_category (name, index, delta)
        result = CI_Toolbar_Category (name, self)
        return result
    # end def add_group

    def remove_group (self, index) :
        raise NotImplementedError, "Toolbar.remove_group"
    # end def remove_group

    ### event specific methods
    def bind_to_sync (self, callback) :
        self.widget.bind ("<Any-Enter>", callback)
    # end def bind_to_sync

# end class CI_Toolbar

class CI_Toolbar_Category (TOM.TKT.Command_Interfacer) :

    name_clean = _name_clean

    def __init__ (self, category, widget) :
        self.widget   = widget
        self.category = category
    # end def __init__

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , icon            = None
            , info            = info
            , as_check_button = False
            , cmd_name        = None
            , ** kw
            ) :
        if as_check_button :
            raise NotImplementedError, "as_check_button"
        b_name = self.name_clean.sub ("_", name.lower ())
        return self.widget.add_button \
            ( category    = self.name
            , name        = b_name
            , command     = callback
            , image       = icon         ### XXX ???
            , cmd_name    = cmd_name
            )
    # end def add_command

    def remove_command (self, index) :
        raise NotImplementedError, "Toolbar.remove_command"
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        raise NotImplementedError, "Toolbar.add_group"
    # end def add_group

    def remove_group (self, index) :
        raise NotImplementedError, "Toolbar.remove_group"
    # end def remove_group

    ### event specific methods
    def enable_entry (self, name) :
        self.widget.toolbar [self.name].enable_entry (name)
    # end def enable

    def disable_entry (self, name) :
        self.widget.toolbar [self.name].disable_entry (name)
    # end def disable_entry

# end class CI_Toolbar_Category

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TOM.TKT.Tk.Command_Interfacer

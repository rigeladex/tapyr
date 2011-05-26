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
#    TFL.TKT.Command_Interfacer
#
# Purpose
#    Model a toolkit command interface like menu, toolbar, etc.
#
# Revision Dates
#    21-Dec-2004 (CT) Creation
#    10-Jan-2005 (CT) `destroy` added
#    11-Jan-2005 (CT) `as_check_button` added to `add_command`
#    11-Jan-2005 (CT) `bind_to_widget` added
#    18-Jan-2005 (MG) `Command_Interfacer.add_command` fixed
#    18-Jan-2005 (CT) Derive from `TFL.TKT.Mixin` instead of `TFL.Meta.Object`
#    26-Jan-2005 (CT) s/as_check_button/state_var/
#    26-Jan-2005 (CT) `add_group` changed to return self
#    28-Jan-2005 (CT) `index` added
#    31-Jan-2005 (CT) `_Test_CI_` added
#     3-Feb-2005 (CT) `max_cmds_per_group` added
#    16-Feb-2005 (MG) `bind_to_widget`: parameter `event_name` added
#     6-Apr-2005 (CT) `clear` added
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL           import TFL
import _TFL._TKT.Mixin

import sys

class Command_Interfacer (TFL.TKT.Mixin) :
    """Model a toolkit command interface like menu, toolbar, etc."""

    max_cmds_per_group = sys.maxint

    def clear (self) :
        """Remove all commands/groups/separators from command interfacer"""
        pass
    # end def clear

    def destroy (self) :
        """Destroy the command interfacer widget"""
        pass
    # end def destroy

    def index (self, name) :
        """Return the index of `name` in the interface. If you pass `-1` for
           name, the index of the end is returned
        """
        return 0
    # end def index

    def set_auto_short_cuts (self) :
        pass
    # end def set_auto_short_cuts

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , info            = None
            , icon            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        """Insert and return interface object for command `name` with action
           `callback` at position `index + delta` into list of entries
           (`index` can be a entry name or a numeric index; if it isn't
           specified, the command is appended to the list).
        """
        pass
    # end def add_command

    def remove_command (self, index) :
        """Remove command at `index` from list of entries (`index` can be
           a command name or a numeric index)
        """
        pass
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        """Insert and return interface object for command group `name` at
           position `index + delta` into list of entries (`index` can be a
           entry name or a numeric index; if it isn't specified, the group is
           appended to the list)
        """
        return self
    # end def add_group

    def remove_group (self, index) :
        """Remove command group at `index` from list of entries
           (`index` can be a group name or a numeric index)
        """
        pass
    # end def remove_group

    ### separator specific methods
    def add_separator (self, name = None, index = None, delta = 0) :
        """Insert separator with optional `name` at position `index + delta`
           into list of entries (`index` can be a entry name or a numeric
           index; if it isn't specified, the group is appended to the list)
        """
        pass
    # end def add_separator

    def remove_separator (self, index) :
        """Remove separator at `index` from list of entries
           (`index` can be a separator name or a numeric index)
        """
        pass
    # end def remove_separator

    ### event specific methods
    def bind_to_activation (self, callback) :
        """Bind `callback` to activation event"""
        pass
    # end def bind_to_activation

    def bind_to_sync (self, callback) :
        """Bind `callback` to sync event"""
        pass
    # end def bind_to_sync

    def bind_to_widget (self, widget, event_name) :
        """Bind activation of `self` to `widget`.
        """
        pass
    # end def bind_to_widget

    def enable_entry (self, index) :
        """Enable entry at `index` (which can be a name or a numeric index)"""
        pass
    # end def enable

    def disable_entry (self, index) :
        """Disable entry at `index` (which can be a name or a numeric index)"""
        pass
    # end def disable_entry

# end class Command_Interfacer

class _Test_CI_ (Command_Interfacer) :

    def __init__ (self, AC) :
        from NO_List import NO_List
        self.__super.__init__ (AC = AC)
        self.elements   = NO_List ()
        self.activation = []
    # end def __init__

    def index (self, name) :
        if name == -1 :
            return len (self.elements)
        return self.elements.n_index (name)
    # end def index

    def add_command \
            ( self, name, callback
            , index           = None
            , delta           = 0
            , underline       = None
            , accelerator     = None
            , info            = None
            , icon            = None
            , state_var       = None
            , cmd_name        = None
            , ** kw
            ) :
        from Record import Record
        self.elements.insert \
            (index, Record (name = name, callback = callback))
    # end def add_command

    def remove_command (self, index) :
        del self.elements [index]
    # end def remove_command

    ### group specific methods
    def add_group (self, name, index = None, delta = 0, ** kw) :
        from Record import Record
        result = self.__class__ (self.AC)
        self.elements.insert (index, Record (name = name, group = result))
        return result
    # end def add_group

    def remove_group (self, index) :
        del self.elements [index]
    # end def remove_group

    ### separator specific methods
    def add_separator (self, name = None, index = None, delta = 0) :
        from Record import Record
        if name is None :
            name = "sep_%d" % (len (self.elements), )
        self.elements.insert (index, Record (name = name, is_sep = "-" * 20))
    # end def add_separator

    def remove_separator (self, index) :
        del self.elements [index]
    # end def remove_separator

    def bind_to_activation (self, callback) :
        self.activation.append (callback)
    # end def bind_to_activation

    def activate (self, prefix = "") :
        for cb in self.activation :
            cb ()
        for i, e in enumerate (self.elements) :
            print "%s%3d : %s" % (prefix, i, e)
            if hasattr (e, "group") :
                e.group.activate (prefix = prefix + "  ")
    # end def activate

# end class _Test_CI_

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TFL.TKT.Command_Interfacer

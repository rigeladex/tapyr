# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    Command_Interfacer
#
# Purpose
#    Model a toolkit command interface like menu, toolbar, etc.
#
# Revision Dates
#    21-Dec-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL           import TFL
import _TFL._Meta.Object
import _TFL._TKT

class Command_Interfacer (TFL.Meta.Object) :
    """Model a toolkit command interface like menu, toolbar, etc."""

    ### command specific methods
    def add_command \
            ( self, name, callback
            , index       = None
            , delta       = 0
            , underline   = None
            , accelerator = None
            , icon        = None
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
        pass
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

    def enable_entry (self, index) :
        """Enable entry at `index` (which can be a name or a numeric index)"""
        pass
    # end def enable

    def disable_entry (self, index) :
        """Disable entry at `index` (which can be a name or a numeric index)"""
        pass
    # end def disable_entry

# end class Command_Interfacer

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ Command_Interfacer

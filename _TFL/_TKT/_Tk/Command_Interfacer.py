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
#    TOM.TKT.Tk.Command_Interfacer
#
# Purpose
#    Model command interface for Tkinter based GUI
#
# Revision Dates
#    22-Dec-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _TOM                 import TOM
import _TOM._TKT.Command_Interfacer

from   CTK                  import *

class CI_Menu (TOM.TKT.Command_Interfacer) :
    """Implement a menu command interface for Tkinter"""

    def __init__ (self, widget) :
        self.widget = widget
    # end def __init__

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
        return self.widget.insert_command \
            ( index + delta + 1
            , label       = name
            , command     = callback
            , underline   = underline
            , accelerator = accelerator
            )
    # end def add_command

    def remove_command (self, index) :
        pass ### XXX
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
        return result
    # end def add_group

    def remove_group (self, index) :
        pass ### XXX
    # end def remove_group

    ### separator specific methods
    def add_separator (self, name = None, index = None, delta = 0) :
        pass ### XXX
    # end def add_separator

    def remove_separator (self, index) :
        pass ### XXX
    # end def remove_separator

    ### event specific methods
    def bind_to_activation (self, callback) :
        """Bind `callback` to activation event"""
        pass ### XXX
    # end def bind_to_activation

    def bind_to_sync (self, callback) :
        pass ### XXX
    # end def bind_to_sync

    def enable_entry (self, index) :
        pass ### XXX
    # end def enable

    def disable_entry (self, index) :
        pass ### XXX
    # end def disable_entry

# end class CI_Menu

if __name__ != "__main__" :
    TFL.TKT._Export ("*")
### __END__ TOM.TKT.Tk.Command_Interfacer

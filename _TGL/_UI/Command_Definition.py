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
#    TGL.UI.Command_Definition
#
# Purpose
#    Simple way of defining commands for a command manager
#
# Revision Dates
#    13-Aug-2005 (MG) Creation (factored from PMA.UI.Office)
#    ««revision-date»»···
#--

class Command_Definition (object) :

    precondition = None
    batchable    = True
    icon         = None
    eventname    = None
    accelerator  = None
    underline    = None

    class Group (object) :
        def __init__ (self, name, ci = (), ev = ()) :
            self.name = name
            if not isinstance (ci, (list, tuple)) :
                ci = (ci, )
            if not isinstance (ev, (list, tuple)) :
                ev = (ev, )
            self.ci = ci
            self.ev = ev
        # end def __init__

        def command_interfacers (self, eventname = None) :
            if not eventname :
                return self.ci
            return self.ci + tuple ("%s:%s" % (ev, eventname) for ev in self.ev)
        # end def command_interfacers

    # end class Group

    def __init__ (self, name, callback, * group_spec, ** kw) :
        self.name         = name
        self.callback     = callback
        self.group_spec   = group_spec
        self.__dict__.update (kw)
    # end def __init__

    def __call__ (self, Cmd, cmd_mgr, obj = None) :
        callback = self.callback
        if not callable (callback) :
            callback = getattr (obj, callback)
        cmd_dict = dict \
            ( precondition = self.precondition
            , batchable    = self.batchable
            )
        for group in self.group_spec :
            acc = self.accelerator
            if acc is not None :
                acc = getattr (obj.TNS.Eventname, acc)
            getattr (cmd_mgr.cmd, group.name).add_command \
                ( Cmd (self.name, callback, ** cmd_dict)
                , accelerator = acc
                , icon        = self.icon
                , if_names    = group.command_interfacers (self.eventname)
                , underline   = self.underline
                )
    # end def __call__

# end class Command_Definition

class Separator (object) :

    def __init__ (self, * group_spec) :
        self.group_spec = group_spec
    # end def __init__


    def __call__ (self, Cmd, cmd_mgr, obj = None) :
        for group in self.group_spec :
            getattr (cmd_mgr.cmd, group.name).add_separator \
                (if_names = group.command_interfacers ())
    # end def __call__

# end class Separator

class Command_Definition_Mixin (object) :
    """Mixin for handling the command definition."""
    
    deaf_commands = ()
    commands      = ()
    
    def _setup_commands (self, cmd_mgr) :
        Cmd     = self.ANS.UI.Command
        Def_Cmd = self.ANS.UI.Deaf_Command
        for cmd in self.deaf_commands :
            cmd (Def_Cmd, cmd_mgr, self)
        for cd in self.commands :
            cd (Cmd, cmd_mgr, self)
    # end def _setup_commands
    
# end class Command_Definition_Mixin

if __name__ != "__main__" :
    from   _TGL      import TGL
    import _TGL._UI
    TGL.UI._Export ("*")
### __END__ TGL.UI.Command_Definition

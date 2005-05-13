# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    TFL.UI.Clipboard
#
# Purpose
#    Implement common parts for clipboard
#
# Revision Dates
#    12-May-2005 (MZO)  Creation 
#    ««revision-date»»···
#--

from   _TFL                   import TFL
import _TFL._UI
import _TFL._UI.Mixin
import _TFL._UI.Command_Mgr

# 12-May-2005: Future Exentsion: (For example Tree)
#   Provide copy for Treeview (For example in selector) => cmd_mgr 
#   necessary (- maybe with data?), but also Text copy (like yet) necessary 
#   to copy gtk-native widget for example comboboxentry, Treeview Editing 
#   Entry. 
#
#   Suggested solution: Use Cmd_Delegator with is a intelligent delegator
#   function i.e if cmd_mgr of the focused widget found then use this 
#   command mgr if not, use a central cmd_mgr (wich uses current callbacks)
#
#   Difference to current solution: Easier precondition - currently every 
#   precondition seeks focused widget. 

class Clipboard (TFL.UI.Mixin) :

    def __init__ (self, AC = None) : 
        self.AC  = AC
        self.__super.__init__ (AC = AC)
        self.create_tkt ()
    # end def __init__

    def create_tkt (self) : 
        self.tkt = self.TNS.Clipboard (AC = self.AC)
    # end def create_tkt

    def setup_clipboard_menu \
            ( self
            , cmd_mgr
            , if_names   = None           # if none => group.if_names
            , group_name = "Edit"
            , index      = None
            ) :
        ### setup clipboard commands  - Expect defined callbacks 
        ### menu_cut/copy/paste_cmd and preconditions cut/copy/pasteable
        tkt       = self.tkt
        group     = cmd_mgr.group (group_name)
        Cmd       = self.ANS.UI.Deaf_Command
        add_cmd   = group.add_command
        pv        = self._ignore_precondition_violation
        if if_names is None : 
            if_names = group.if_names
        add_cmd ( Cmd ( "Cut"
                      , tkt.menu_cut_cmd
                      , precondition = tkt.cutable
                      , pv_callback  = pv  
                      )
                , icon        = "edit.cut"
                , index       = index
                , if_names    = if_names
                , underline   = 2
                , accelerator = self.TNS.Eventname.cut
                )
        add_cmd ( Cmd ( "Copy"
                      , tkt.menu_copy_cmd
                      , precondition = tkt.copyable
                      , pv_callback  = pv
                      )
                , icon        = "edit.copy"
                , if_names    = if_names
                , index       = index
                , underline   = 0
                , accelerator = self.TNS.Eventname.copy
                )
        add_cmd ( Cmd ( "Paste"
                      , tkt.menu_paste_cmd
                      , precondition = tkt.pasteable
                      , pv_callback  = pv
                      )
                , icon        = "edit.paste"
                , if_names    = if_names
                , index       = index
                , underline   = 4
                , accelerator = self.TNS.Eventname.paste
                )
    # end def setup_clipboard_menu_commands

    def _ignore_precondition_violation (self, *args, **kw) : 
        # open menu => tooltip => change of selection => pv possible
        #  => skip command request
        pass
    # end def _handle_precondition_violation

# end class Clipboard

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ TFL.UI.Clipboard

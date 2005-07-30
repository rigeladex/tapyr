# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.UI.Application
#
# Purpose
#    Application for PMA
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    21-May-2005 (MG) Allow `event` parameter for `commit_all`
#    21-May-2005 (MG) Interpreter added to menu and toolbar
#     7-Jun-2005 (MG) `_read_settings` added
#    10-Jun-2005 (MG) Use of `UI.Office` added
#    10-Jun-2005 (MG) Exception handler for the UI.Office creation added
#    11-Jun-2005 (MG) `_read_settings` removed and use `PMA.Office` instead
#    25-Jul-2005 (CT) `_quit` changed to call `office.save_status`
#    28-Jul-2005 (MG) `UI_State.__init__`: overwriting of status properties
#                     added, `Counting_Property` removed
#    28-Jul-2005 (MG) `s/Changes.changes/Changes.value/g`
#    28-Jul-2005 (MG) `Changes.__cmp__` and `Changes.__str__` added
#    28-Jul-2005 (CT) `_extend_status_props` and `_extend_status_prop` added
#    27-Jul-2005 (MG) `self.event_binders` added
#    27-Jul-2005 (MG) New command groups and commands added
#    28-Jul-2005 (MG) `File` menu removed, `_setup_*_menu` functions removed
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _PMA                   import PMA

import _TFL.App_State
import _TFL.Environment
import _TFL.sos
import _TFL._Meta.Object
import _TFL._Meta.Property

import _TGL._UI

import _PMA._UI
import _PMA._UI.Command_Mgr
import _PMA._UI.HTD
import _PMA._UI.Message
import _PMA._UI.Msg_Display
import _PMA._UI.Mixin
import _PMA._UI.Office

import sys

from   Record                 import Record

class _App_State_ (TFL.App_State) :
    product_name = "PMA"
# end class _App_State_

class Changes (TFL.Meta.Object) :

    def __init__ (self) :
        self.value = 0
    # end def __init__

    def inc (self) :
        self.value += 1
    # end def inc

    def __iadd__ (self, value) :
        self.value += value
    # end def __iadd__

    def __int__ (self) :
        return self.value
    # end def __int__

    def __str__ (self) :
        return str (self.value)
    # end def __str__

    def __cmp__ (self, rhs) :
        return cmp (self.value, int (rhs))
    # end def __cmp__

# end class Changes

class UI_State (TFL.Meta.Object) :

    def __init__ (self, ** kw) :
        self.__dict__.update (kw)
        self.changes = changes = Changes ()
        self._extend_status_props (changes)
    # end def __init__

    def _extend_status_props (self, changes) :
        ### define new properties for the status class to update the change
        ### counter of the application
        for cls, properties in \
            ( (PMA.Off_Status, ("current_box", "target_box"))
            , (PMA.Box_Status, ("current_message", ))
            ) :
            for name in properties :
                self._extend_status_prop (cls, name, changes)
    # end def _extend_status_props

    def _extend_status_prop (self, cls, name, changes) :
        prop       = getattr (cls, name)
        _old_set   = prop.fset
        def _set (obj, value) :
            result = _old_set (obj, value)
            changes.inc ()
            return result
        setattr \
            (cls, name, property (prop.fget, _set, prop.fdel, prop.__doc__))
    # end def _extend_status_prop

# end class UI_State

class Application (PMA.UI.Mixin) :
    """Main instance of PMA application"""

    product_name         = "PMA"
    startup_cmds         = []
    _started_quit        = False
    ipreter              = None

    _Office_Cmd_Group    = Record \
        ( name           = "Office"
        , if_names       = ("mb", "tb")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the office"
        )
    _Mbox_Cmd_Group      = Record \
        ( name           = "Mailbox"
        , if_names       = ("mb", "tb", "cm_bv", "cm_mv", "ev_bv", "ev_mv")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the currently "
          "selected mailbox"
        )
    _Message_Cmd_Group   = Record \
        ( name           = "Message"
        , if_names       = ("mb", "tb", "cm_md", "cm_mv", "ev_mv")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the currently "
          "selected message(s)"
        )
    _Msg_Part_Cmd_Group   = Record \
        ( name           = "Message-Part"
        , if_names       = ("mb", "cm_mo", )
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the currently "
          "selected message via the message outline display"
        )
    _Scripts_Cmd_Group   = Record \
        ( name             = "Scripts"
        , if_names         = ("mb", "tb")
        , batchable        = False
        , precondition     = None
        , description      =
          "This group provides access to various scripts."
        )
    _Help_Cmd_Group      = Record \
        ( name             = "Help"
        , if_names         = ("mb", "tb")
        , batchable        = False
        , precondition     = None
        , description      =
          "This group provides commands displaying information "
          "about various aspects of %(name)s."
        )
    Command_Groups       = \
        ( "_Office_Cmd_Group"
        , "_Mbox_Cmd_Group"
        , "_Message_Cmd_Group"
        , "_Msg_Part_Cmd_Group"
        , "_Scripts_Cmd_Group"
        , "_Help_Cmd_Group"
        )

    def __init__ (self, AC, cmd, _globals = {}) :
        self.__super.__init__ (AC = AC, cmd = cmd, _globals = _globals)
        self._globals      = _globals
        ANS                = self.ANS
        TNS                = self.TNS
        AC.ui_state        = UI_State                ()
        self.changes       = AC.ui_state.changes
        AC.memory          = _App_State_             (window_geometry = {})
        AC.memory.load                               ()
        self._interpret_cmd_line                     (cmd, TNS)
        self.tkt = tkt     = TNS.Application         (self)
        self.menubar       = tkt._setup_menubar      ()
        self.toolbar       = tkt._setup_toolbar      ()
        self.context_menus = tkt._setup_context_menu ()
        self.event_binders = tkt._setup_event_binder ()
        tkt._setup_geometry                          ()
        tkt._setup_stdout_redirect                   ()
        self._setup_cmd_mgr                          ()
        self._setup_office                           ()
        tkt.bind_to_sync                             (self.cmd_mgr.update_state)
    # end def __init__

    def commit_all (self, event = None) :
        """Commit all pending changes of mailboxes"""
        ### XXX
        try :
            self.office.commit ()
            return True
        except :
            return False
    # end def commit_all

    def exit (self) :
        """Terminate %(name)s after committing pending mailbox changes."""
        self._quit (self._try_exit)
    # end def exit

    def globals (self) :
        return self._globals
    # end def globals

    def interact (self) :
        """Provide interactive access to python interpreter."""
        self.tkt.interact ()
    # end def interact

    def is_interactive (self) :
        """You can use this command only in the interactive mode of %(name)s."""
        return not self.batch_mode
    # end def is_interactive

    def pending_changes (self) :
        return False ### XXX
    # end def pending_changes

    def quit (self, event = None) :
        """Terminate %(name)s without committing pending mailbox changes."""
        self._quit (self._try_quit)
    # end def quit

    def show_error (self, title = None, message = None, ** kw) :
        msg = message or title
        if msg :
            print msg
        return self.tkt.show_error (title, message, ** kw)
    # end def show_error

    def start_mainloop (self) :
        self.tkt.start_mainloop (self._after_start_mainloop)
    # end def start_mainloop

    def _after_start_mainloop (self) :
        ### this is called by self.tkt after mainloop was started
        self._run_prescripts      ()
        self.cmd_mgr.update_state ()
        self._run_postscripts     ()
        self._execute_commands    (self.startup_cmds)
    # end def _after_start_mainloop

    def _create_command_mgr (self) :

        self.cmd_mgr = self.AC.ui_state.cmd_mgr = self.ANS.UI.Command_Mgr \
            ( AC             = self.AC
            , change_counter = self.changes
            , interfacers    = dict
                ( self.context_menus
                , mb         = self.menubar
                , tb         = self.toolbar
                , ** self.event_binders
                )
            , pv_callback    = self._show_precondition_violation
            , batch_mode     = self.batch_mode
            , form_dict      = TFL.d_dict
                  ( name     = "PMA"
                  )
            , appl           = self
            )
        return self.cmd_mgr
    # end def _create_command_mgr

    def _execute_commands (self, commands) :
        for c in commands :
            self.cmd_mgr.run (c)
    # end def _execute_commands

    def _interpret_cmd_line (self, cmd, TNS) :
        self.cmd            = cmd
        self.batch_mode     = cmd.batch
        self.startup_cmds   = self.__class__.startup_cmds [:]
        self.verbose        = cmd.verbose
        if cmd.option ["commands"] :
            self.startup_cmds.extend (cmd.commands)
    # end def _interpret_cmd_line

    def _quit (self, quit_fct) :
        if quit_fct () :
            if not self._started_quit :
                self._started_quit = True
                try :
                    self.tkt._quit  ()
                finally :
                    try :
                        self.office.save_status ()
                        self.State.dump         ()
                    finally :
                        self._destroy   ()
                        print >> sys.__stdout__, "Leaving PMA, good bye"
            else :
                raise RuntimeError, "Quit called reentrantly"
    # end def _quit

    def _run_postscripts (self) :
        self._run_scripts (self._startup_scripts ())
    # end def _run_postscripts

    def _run_prescripts (self) :
        if self.cmd.option ["prescripts"] :
            self._run_scripts (self.cmd.prescripts)
    # end def _run_prescripts

    def _run_script (self, script) :
        script = script.strip ()
        if not script : return
        try :
            try :
                script = TFL.sos.expanded_path (script)
            except (SystemExit, KeyboardInterrupt) :
                raise
            except :
                pass
            if TFL.sos.path.isfile (script) :
                Script (script, self.globals (), self.script_locals) ()
            else :
                print "Script %s not found" % script
        except (SystemExit, KeyboardInterrupt) :
            raise
        except :
            print "Error during execution of", script
            traceback.print_exc ()
    # end def _run_script

    def _run_script_cmd (self) :
        """Run a python script"""
        return self.script_mgr.run_script ()
    # end def _run_script_cmd

    def _run_scripts (self, scripts) :
        for s in scripts :
            self._run_script (s)
    # end def _run_scripts

    def _save_pending (self, trailer) :
        ### result None  means `No'     was clicked
        ### result False means `Cancel' was clicked
        if not self.pending_changes () :
            result = None
        else :
            result = self.ask_yes_no_cancel \
                ( "Unsaved changes !"
                , ( "There pending changes to mailboxes.\n\n"
                    "Do you want to commit these before %s?"
                  ) % (trailer, )
                )
            if result == "no" :
                result = None
            if result == "cancel" :
                result = False
        return result
    # end def _save_pending

    def _set_title (self) :
        self.tkt.set_title (self._window_title_text ())
    # end def _set_title

    def _setup_cmd_mgr (self) :
        self._create_command_mgr ()
        add_group = self.cmd_mgr.add_group
        add_dyn_g = self.cmd_mgr.add_dyn_group
        for cmd_group in self.Command_Groups :
            if isinstance (cmd_group, str) :
                cmd_group = getattr (self, cmd_group, None)
            if not cmd_group :
                continue
            name = cmd_group.name
            desc = cmd_group.description
            p    = cmd_group.precondition
            if isinstance (p, (str, unicode)) :
                p = getattr (self, p)
            if not hasattr (cmd_group, "command_gen") :
                group = add_group \
                    ( name           = name
                    , desc           = desc
                    , precondition   = p
                    , if_names       = cmd_group.if_names
                    , batchable      = cmd_group.batchable
                    )
            else :
                cgen = cmd_group.command_gen
                if isinstance (cgen, str) :
                    cgen = getattr (self, cgen)
                group = add_dyn_g \
                    ( name           = name
                    , command_gen    = cgen
                    , desc           = desc
                    , precondition   = p
                    , if_names       = cmd_group.if_names
                    )
            setup_group = getattr \
                (self, "_setup_%s_group" % (name.lower (), ), None)
            if callable (setup_group) :
                setup_group (group)
        self.cmd_mgr.update_state ()
    # end def _setup_cmd_mgr

    def _setup_help_group (self, group) :
        Cmd     = self.ANS.UI.Deaf_Command
        Dyn     = self.ANS.UI.Dyn_Command
        add_cmd = group.add_command
        add_sep = group.add_separator
        #add_sep (If_Names = ("mb", ))
        add_cmd \
            ( Cmd ("Interpreter", self.interact)
            , if_names  = ("mb", "tb")
            , icon      = "gtk-harddisk"
            , underline = 5
            )
    # end def _setup_help_group

    def _setup_office (self) :
        self.office      = self.ANS.Office ()
        tkt              = self.tkt
        UI               = self.ANS.UI
        self.msg_display = md = UI.Message \
            ( AC         = self.AC
            , display_wc = tkt.wc_msg_display
            , outline_wc = tkt.wc_msg_outline
            )
        tkt.pack (tkt.wc_msg_display, md._display.tkt_text)
        tkt.pack (tkt.wc_msg_outline, md._outline.tkt_text)
        try :
            self.ui_office = UI.Office (self, AC = self.AC)
        except :
            import traceback
            traceback.print_exc ()
    # end def _setup_office

    def _setup_scripts_group (self, group) :
        Cmd     = self.ANS.UI.Deaf_Command
        Dyn     = self.ANS.UI.Dyn_Command
        add_cmd = group.add_command
        add_sep = group.add_separator
        #add_sep (if_names = ("mb", ))
    # end def _setup_scripts_group

    def _show_precondition_violation (self, name, msg) :
        self.show_error (name, msg)
    # end def _show_precondition_violation

    def _startup_scripts (self) :
        if not self.batch_mode :
            env_scripts = TFL.sos.environ.get ("PMA_STARTUP", "")
            for s in env_scripts.split (",") :
                yield s
        if self.cmd.option ["scripts"] :
            for s in self.cmd.scripts :
                yield s
    # end def _startup_scripts

    def _try_exit (self) :
        return self.commit_all ()
    # end def _try_exit

    def _try_quit (self) :
        if self.batch_mode :
            return True
        if self.pending_changes () :
            ans = self._save_changes ("exiting")
            if ans is not None :
                return False ### (ans is None)  means `No'     was clicked
                             ### (ans == False) means `Cancel' was clicked
            elif ans :
                return self.commit_all ()
        return True
    # end def _try_quit

    def _setup_script_locals (self) :
        self._update_script_locals \
            ( ask_string               = self.ask_string
            , ask_integer              = self.ask_integer
            , ask_open_file_name       = self.ask_open_file_name
            , ask_save_file_name       = self.ask_save_file_name
            , ask_dir_name             = self.ask_dir_name
            , ask_open_dir_name        = self.ask_open_dir_name
            , ask_save_dir_name        = self.ask_save_dir_name
            , keyword_value            = self.cmd.key_value
            , Main_Widget              = self
            , __name__                 = "__main__"
            , AC                       = AC
            )
    # end def _setup_script_locals

    def _update_script_locals (self, ** kw) :
        self._script_locals.update (kw)
    # end def _update_script_locals

    def _window_title_text (self) :
        result = ["PMA: "]
        if self.ui_state.current_mailbox :
            result.append (self.ui_state.current_mailbox.name)
            result.append ("/")
        if self.ui_state.current_message :
            result.append (self.ui_state.current_message.name)
        return "".join (result)
    # end def _window_title_text

    def __getattr__ (self, name) :
        result = getattr (self.tkt, name)
        setattr  (self, name, result)
        return result
    # end def __getattr__

# end class Application

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Application

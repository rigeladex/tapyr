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
#    CAL.UI.Application
#
# Purpose
#    Application for CAL
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _CAL                   import CAL

import _TFL.App_State
import _TFL.Environment
import _TFL.sos
import _TFL._Meta.Object
import _TFL._Meta.Property

import _TGL._UI

import _CAL._UI
import _CAL._UI.Command_Mgr
import _CAL._UI.HTD
import _CAL._UI.Mixin
import _CAL._UI.Week_View
import _CAL.Calendar
import _CAL.Date
import _CAL.Date_Time
import _CAL.Delta
import _CAL.Time
import _CAL.Year

import sys

from   Record                 import Record

class _App_State_ (TFL.App_State) :
    product_name = "CAL"
# end class _App_State_

class Changes (TFL.Meta.Object) :

    def __init__ (self) :
        self.changes = 0
    # end def __init__

    def inc (self) :
        self.changes += 1
    # end def inc

    def __iadd__ (self, value) :
        self.changes += value
    # end def __iadd__

    def __int__ (self) :
        return self.changes
    # end def __int__

# end class Changes

class UI_State (TFL.Meta.Object) :

    __metaclass__ = TFL.Meta.M_Class_SWRP

    class Counting_Property (TFL.Meta.RW_Property) :

        def set_value (self, obj, value) :
            if self.get_value (obj) != value :
                obj.changes += 1
            self.__super.set_value (obj, value)
        # end def set_value

        _set = set_value

    # end class Counting_Property

    __properties = \
        ( Counting_Property ("current_mailbox")
        , Counting_Property ("current_message")
        , Counting_Property ("message_selection")
        , Counting_Property ("target_mailbox")
        )

    def __init__ (self, ** kw) :
        self.__dict__.update   (kw)
        self.changes = Changes ()
    # end def __init__

# end class UI_State

class Application (CAL.UI.Mixin) :
    """Main instance of CAL application"""

    product_name         = "CAL"
    startup_cmds         = []
    _started_quit        = False
    ipreter              = None

    _File_Cmd_Group      = Record \
        ( name           = "File"
        , if_names       = ("mb", "tb", "cm:click_3")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the forest of mailboxes"
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
        ( "_File_Cmd_Group"
        , "_Mbox_Cmd_Group"
        , "_Message_Cmd_Group"
        , "_Scripts_Cmd_Group"
        , "_Help_Cmd_Group"
        )

    def __init__ (self, AC, cmd, _globals = {}) :
        self.__super.__init__ (AC = AC, cmd = cmd, _globals = _globals)
        self._globals     = _globals
        ANS               = self.ANS
        TNS               = self.TNS
        AC.ui_state       = UI_State                ()
        self.changes      = AC.ui_state.changes
        AC.memory         = _App_State_             (window_geometry = {})
        AC.memory.load                              ()
        self._interpret_cmd_line                    (cmd, TNS)
        self.tkt = tkt    = TNS.Application         (self)
        self.menubar      = tkt._setup_menubar      ()
        self.toolbar      = tkt._setup_toolbar      ()
        self.context_menu = tkt._setup_context_menu ()
        tkt._setup_geometry                         ()
        tkt._setup_stdout_redirect                  ()
        self._setup_cmd_mgr                         ()
        self._setup_calendar                        ()
        tkt.bind_to_sync                            (self.cmd_mgr.update_state)
    # end def __init__

    def commit_all (self, event = None) :
        """Commit all pending changes of mailboxes"""
        return True ### XXX
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
                ( mb         = self.menubar
                , tb         = self.toolbar
                , cm         = self.context_menu
                )
            , pv_callback    = self._show_precondition_violation
            , batch_mode     = self.batch_mode
            , form_dict      = TFL.d_dict
                  ( name     = "CAL"
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
                        self.State.dump ()
                    finally :
                        self._destroy   ()
                        print >> sys.__stdout__, "Leaving CAL, good bye"
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

    def _setup_calendar (self) :
        self.calendar    = cal = self.ANS.Calendar ()
        today            = self.ANS.Date ()
        self.AC.memory.add (current_day  = today)
        self.week_view   = self.ANS.UI.Week_View (self, AC = self.AC)
        tkt              = self.tkt
        tkt.pack (tkt.wc_weeks_view, self.week_view.tkt)
        self.week_view.tkt.scroll_policies (h = self.TNS.NEVER)
        self.week_view.see (cal.year [today.year].weeks [today.week])
    # end def _setup_calendar

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

    def _setup_file_group (self, group) :
        Cmd     = self.ANS.UI.Deaf_Command
        Dyn     = self.ANS.UI.Dyn_Command
        add_cmd = group.add_command
        add_sep = group.add_separator
        #add_sep (if_names = ("mb", ))
        add_cmd ( Cmd ("Commit and exit", self.exit)
                , if_names    = ("mb", )
                , underline   = 11
                , accelerator = "save_and_exit"
                )
        add_cmd ( Cmd ("Exit", self.quit)
                , if_names    = ("mb", )
                , underline   = 1
                , accelerator = "exit"
                )
    # end def _setup_file_group

    def _setup_help_group (self, group) :
        Cmd     = self.ANS.UI.Deaf_Command
        Dyn     = self.ANS.UI.Dyn_Command
        add_cmd = group.add_command
        add_sep = group.add_separator
        #add_sep (If_Names = ("mb", ))
        add_cmd \
            ( Cmd ("Interpreter", self.interact)
            , if_names  = ("mb", "tb")
            , underline = 5
            )
    # end def _setup_help_group

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
            env_scripts = TFL.sos.environ.get ("CAL_STARTUP", "")
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
        result = ["CAL: "]
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
    CAL.UI._Export ("*")
### __END__ CAL.UI.Application

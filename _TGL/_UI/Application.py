# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2007 Mag. Christian Tanzer. All rights reserved
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
#    TGL.IU.Application
#
# Purpose
#    Generic application framework.
#
# Revision Dates
#    12-Aug-2005 (MG) Creation (factored from PMA/CAL.UI.Application)
#    12-Aug-2005 (MG) Literal `CAL` replaced by `self.product_name`
#    12-Aug-2005 (MG) `s/_set_title/set_title/g` and call `set_title` in
#                     `__init__`
#    12-Aug-2005 (MG) Icon added to `interpreter` command
#    13-Sep-2005 (MG) Dummy import's added
#    21-Jan-2006 (MG) Imports fixed
#     7-Nov-2007 (CT) `UI_State._real_name` added
#    14-Dec-2007 (MG) Support for output redirection suppression added
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
import _TFL._Meta.Object
import _TFL.Environment
import _TFL.Record
import _TFL.sos
import _TGL._UI
import _TGL._UI.Mixin
import _TGL._UI.Command_Mgr
import  sys

### the folloing imports are just for py2exe
if 0 == 1 :
    import _TFL._UI.Mixin
    import _TFL._UI.Command_Mgr

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

class _UI_State_ (TFL.Meta.Object) :

    _real_name           = "UI_State"

    def __init__ (self, ** kw) :
        self.__dict__.update   (kw)
        self.changes = Changes ()
    # end def __init__

UI_State = _UI_State_ # end class

class _TGL_UI_Application_ (TGL.UI.Mixin) :
    """Generic application class"""

    _real_name           = "Application"

    product_name         = "TGL"
    show_menubar         = True
    show_toolbar         = True

    startup_cmds         = []
    _started_quit        = False
    ipreter              = None

    _File_Cmd_Group      = TFL.Record \
        ( name           = "File"
        , if_names       = ("mb", "tb", "cm:click_3")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the forest of mailboxes"
        )
    _Scripts_Cmd_Group   = TFL.Record \
        ( name             = "Scripts"
        , if_names         = ("mb", "tb")
        , batchable        = False
        , precondition     = None
        , description      =
          "This group provides access to various scripts."
        )
    _Help_Cmd_Group      = TFL.Record \
        ( name             = "Help"
        , if_names         = ("mb", "tb")
        , batchable        = False
        , precondition     = None
        , description      =
          "This group provides commands displaying information "
          "about various aspects of %(name)s."
        )

    def __init__ (self, AC, cmd, _globals = {}) :
        self.__super.__init__ (AC = AC, cmd = cmd, _globals = _globals)
        self._globals      = _globals
        ANS                = self.ANS
        TNS                = self.TNS
        AC.ui_state        = ANS.UI.UI_State         ()
        self.changes       = AC.ui_state.changes
        AC.memory.load                               ()
        self._interpret_cmd_line                     (cmd, TNS)
        self.tkt = tkt     = TNS.Application         (self)
        self.menubar       = tkt._setup_menubar      ()
        self.toolbar       = tkt._setup_toolbar      ()
        self.context_menus = tkt._setup_context_menu ()
        self.event_binders = tkt._setup_event_binder ()
        tkt._setup_geometry                          ()
        if not getattr (cmd, "Suppress_Redirect", False) :
            tkt._setup_stdout_redirect               ()
        self._setup_cmd_mgr                          ()
        self._setup_application                      ()
        self.set_title                               ()
        tkt.bind_to_sync                             (self.cmd_mgr.update_state)
    # end def __init__

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
            , form_dict      = dict
                  ( name     = self.product_name
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
                        self._quit_finally ()
                        self.State.dump    ()
                    finally :
                        self._destroy   ()
                        print >> sys.__stdout__, "Leaving %s, good bye" % \
                            (self.product_name, )
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

    def set_title (self) :
        self.tkt.set_title (self._window_title_text ())
    # end def set_title

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
            , icon      = "gtk-harddisk"
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

    def __getattr__ (self, name) :
        result = getattr (self.tkt, name)
        setattr  (self, name, result)
        return result
    # end def __getattr__

Application = _TGL_UI_Application_

if __name__ != "__main__" :
    TGL.UI._Export ("*")
### __END__ TGL.IU.Application

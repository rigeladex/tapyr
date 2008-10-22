# -*- coding: iso-8859-1 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
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
#    TFL.UI.Application
#
# Purpose
#    Base class for UI-Application framework
#
# Revision Dates
#    26-Jun-2008 (CT) Creation started (factored from TTA.UI.Application)
#    ...
#    24-Aug-2008 (CT)  Creation finished
#    28-Aug-2008 (CT)  `_logfile_name` added
#     9-Sep-2008 (PGO) `root` moved here from TOM.UI.Application
#    22-Oct-2008 (CED) `if_name_map` defined
#    ««revision-date»»···
#--

from   __future__               import with_statement

from   _TFL                     import TFL

import _TFL._Meta.Object
import _TFL._UI.Clipboard
import _TFL._UI.Command_Mgr
import _TFL._UI.Mixin
import _TFL._UI.Script_Menu_Mgr
import _TFL.App_State
import _TFL.Environment
import _TFL.Filename
import _TFL.Plugin
import _TFL.Script

from   _TFL                     import sos
from   _TFL.Record              import Record
from   _TFL._Meta.Once_Property import Once_Property

import itertools
import mailcap
import sys
import traceback

class _TFL_UI_Change_Observer_ (TFL.Meta.Object) :

    _real_name = "_Change_Observer_"

    def __init__ (self, application) :
        self.application = application
    # end def __init__

    def __int__ (self) :
        return -1
    # end def __int__

    def destroy (self) :
        self.application = None
    # end def destroy

_Change_Observer_ = _TFL_UI_Change_Observer_ # end class

class _TFL_UI_Application_ (TFL.UI.Mixin) :
    """Main instance of an application."""

    _real_name             = "Application"

    Change_Observer        = _Change_Observer_
    Plugin                 = TFL.Plugin
    Version                = None

    ### `State` most likely needs to be overwritten
    State                  = Once_Property \
        (lambda s : TFL.App_State (product_name = s.product_name))

    if_name_map            = {}
    ipreter                = None
    product_name           = "TFL" ### override
    powered                = False ### set to True for power users
    script_locals          = property (lambda s : s._script_locals)
    script_run_change_act  = None
    startup_cmds           = []
    tkt                    = None
    root                   = None
    verbose                = 1

    Tool_Supplier          = ""
    _needs_plugins         = False
    _pdf_mimetype          = "application/pdf"
    _plugin_env_vars     = property \
        (lambda s : ("%s_PLUGINS" % s.ANS.__name__, ))
    _script_env_vars     = property \
        (lambda s : ("%s_STARTUP" % s.ANS.__name__, ))
    _started_quit          = False

    _File_Cmd_Group        = TFL.Record \
        ( name             = "File"
        , if_names         = ("mb", "tb", "cm:click_3")
        , batchable        = True
        , precondition     = None
        )
    _Windows_Cmd_Group     = Record \
        ( name             = "Windows"
        , if_names         = ("mb", )
        , batchable        = False
        , precondition     = None
        , command_gen      = "_post_wndw_menu"
        , description      =
          "This group provides access to all currently existing "
          "top-level windows of %(name)s."
        )
    _Scripts_Cmd_Group     = TFL.Record \
        ( name             = "Scripts"
        , if_names         = ("mb", "tb")
        , batchable        = False
        , precondition     = None
        , description      =
          "This group provides access to various Python scripts."
        )
    _Help_Cmd_Group        = TFL.Record \
        ( name             = "Help"
        , if_names         = ("mb", "tb")
        , batchable        = False
        , precondition     = None
        , description      =
          "This group provides information about various aspects of "
          "%(name)s."
        )

    def __init__ (self, AC, cmd, _globals = {}, ** kw) :
        self.__super.__init__ (AC = AC, cmd = cmd, _globals = _globals, ** kw)
        TNS                 = self.TNS
        AC.memory           = self.State
        self.Version        = getattr (self.ANS, "Version", None)
        self.changes        = self.Change_Observer (self)
        self._globals       = _globals
        self._script_locals = {}
        self._interpret_cmd_line (cmd, TNS)
        self.State.load          ()
        self._setup_tkt          (cmd, TNS)
        self._setup_cmd_mgr      ()
        self._setup_application  ()
        self.tkt.bind_to_sync    (self.cmd_mgr.update_state)
    # end def __init__

    def destroy (self) :
        self.changes.destroy ()
    # end def destroy

    def exit (self, force = False) :
        """Terminate %(name)s after saving any changes to the current
           database.
        """
        if force :
            self._quit (self._force_exit)
        else :
            self._quit (self._try_exit)
    # end def exit

    def globals (self) :
        return self._globals
    # end def globals

    def interact (self) :
        """Use the force."""
        self.tkt.interact ()
    # end def interact

    def is_interactive (self) :
        """You can use this command only in the interactive mode of %(name)s."""
        return not self.batch_mode
    # end def is_interactive

    def quit (self) :
        """Terminate %(name)s. If there are unsaved changes, %(name)s will
           ask whether they should be discarded or saved to a database.
        """
        self._quit (self._try_quit)
    # end def quit

    def save (self) :
        pass
    # end def save

    def show_error (self, title = None, message = None, ** kw) :
        msg = message or title
        if msg :
            print msg
        return self.tkt.show_error (title, message, ** kw)
    # end def show_error

    def show_info (self, title = None, message = None, ** kw) :
        msg = message or title
        if msg :
            print msg
        return self.tkt.show_info (title, message, ** kw)
    # end def show_info

    def show_rel_notes (self) :
        """Show release notes of %(name)s."""
        if self.release_notes :
            self.tkt.show_rel_notes (self.release_notes)
    # end def show_rel_notes

    def start_mainloop (self) :
        self.tkt.start_mainloop (self._after_start_mainloop)
    # end def start_mainloop

    def _after_start_mainloop (self) :
        ### this is called by self.tkt after mainloop was started
        self._load_plugins        ()
        self._setup_script_locals ()
        self._run_prescripts      ()
        self.cmd_mgr.update_state ()
        self._run_postscripts     ()
        self._execute_commands    (self.startup_cmds)
    # end def _after_start_mainloop

    def _cmd_mgr_form_dict (self) :
        return dict \
            ( name       = self.product_name
            )
    # end def _cmd_mgr_form_dict

    def _cmd_mgr_interfacers (self) :
        return dict \
            ( self.context_menus
            , mb         = self.menubar
            , tb         = self.toolbar
            , bb         = self.buttbox
            , ** self.event_binders
            )
    # end def _cmd_mgr_interfacers

    def _create_command_mgr (self) :
        self.cmd_mgr = self.AC.ui_state.cmd_mgr = self.ANS.UI.Command_Mgr \
            ( AC             = self.AC
            , change_counter = self.changes
            , interfacers    = self._cmd_mgr_interfacers ()
            , pv_callback    = self._show_precondition_violation
            , batch_mode     = self.batch_mode
            , form_dict      = self._cmd_mgr_form_dict ()
            , appl           = self
            )
        return self.cmd_mgr
    # end def _create_command_mgr

    def _create_tkt_application (self, cmd, TNS) :
        return TNS.Application (self)
    # end def _create_tkt_application

    def _destroy (self) :
        self.tkt._destroy ()
    # end def _destroy

    def _execute_commands (self, commands) :
        for c in commands :
            c = c.replace ("_", " ")
            try :
                self.cmd_mgr.command [c]
            except TFL.Ambiguous_Key, exc :
                self.echo ("Error: %s" % exc.message)
                break
            except KeyError :
                self.echo ("Unknown command: '%s'. Execution aborted." % c)
                break
            else :
                self.cmd_mgr.run (c)
    # end def _execute_commands

    def _find_mime_app (self, mimetype, filename) :
        mimetypes = mailcap.getcaps   ()
        syscmd, _ = mailcap.findmatch (mimetypes, mimetype, filename = filename)
        if syscmd :
            return (sos.system, syscmd)
        else :
            error_text = "No mimetype '%s' defined for `%s`." % \
                (mimetype, filename)
            self.show_error (title = "Error", message = error_text)
            return (None, None)
    # end def _find_mime_app

    def _force_exit (self) :
        return self._try_exit () or True
    # end def _force_exit

    def _interpret_cmd_line (self, cmd, TNS) :
        self.cmd            = cmd
        self.batch_mode     = cmd.batch
        self.plugins        = ()
        self.startup_cmds   = self.__class__.startup_cmds [:]
        if cmd.option ["commands"] :
            self.startup_cmds.extend (cmd.commands)
        if cmd.option ["__plugins"] :
            ### use getattr because `__` prefix would get name-mangled
            ### if cmd.__plugins was used here
            self.plugins    = getattr (cmd, "__plugins")
        if cmd.option ["verbose"] :
            self.verbose    = cmd.verbose
    # end def _interpret_cmd_line

    def _load_plugin (self, p) :
        result = self.Plugin (p, self)
        if self.Version :
            self.Version.add_plugin (result._version, p)
        print "Loaded %s" % self.Plugin.Table [p]
        return result
    # end def _load_plugin

    def _load_plugins (self) :
        for p in self._plugins () :
            try :
                self._load_plugin (p)
            except ImportError :
                if __debug__ :
                    traceback.print_exc ()
                print "Could not locate plugin `%s`" % p
            except StandardError, exc :
                if __debug__ :
                    traceback.print_exc ()
                print \
                    ( "Could not load plugin `%s` due to exception:\n%s: %s"
                    % (p, exc.__class__.__name__, exc)
                    )
        for p in sorted \
            ( self.Plugin.Table.itervalues ()
            , key = lambda p : (p.rank, p.pns_name)
            ) :
            if __debug__ :
                print "Setting up plugin `%s`..." % p.name
            try :
                p.setup ()
            except StandardError, exc :
                if __debug__ :
                    traceback.print_exc ()
                print \
                    ( "Could not set up plugin `%s` due to exception:\n%s: %s"
                    % (p, exc.__class__.__name__, exc)
                    )
        if self.Plugin.Table :
            print \
                ("Finished loading plugins. Number of plugins: %d"
                % len (self.Plugin.Table)
                )
        elif self._needs_plugins :
            self.show_error \
                ( self.product_name
                , "%s can only be used in combination with plugins, but "
                  "you haven't installed any! Please use the %s Installer "
                  "to install the plugins you've bought."
                % (self.product_name, self.Tool_Supplier)
                )
    # end def _load_plugins

    def _logfile_name (self) :
        cmd = self.cmd
        if cmd.logfile :
            result = TFL.Filename (cmd.logfile)
            if cmd.unique_logfile :
                import time
                now = time.localtime (time.time ())
                result = TFL.Filename \
                    ( result.ext
                    , "%s_%s_%s"
                      % ( result.base
                        , time.strftime ("%Y%m%d_%H%M_%S", now)
                        , TFL.Environment.username
                        )
                    , default_dir = result.directory
                    )
            return result.name
    # end def _logfile_name

    def _open_manual (self, filename = "") :
        """Open the %(name)s user manual with the default PDF viewer."""
        if not filename :
            filename  = self._manual_filename
        if filename :
            if TFL.Environment.system == "win32" :
                cmd, para = sos.startfile, filename
                Exc       = WindowsError
            else :
                cmd, para = self._find_mime_app (self._pdf_mimetype, filename)
                Exc       = sos.error
            if cmd :
                try :
                    cmd (para)
                except Exc, exc:
                    self.show_error \
                        ( title   = "Error"
                        , message = "Cannot open manual '%s'\n    %s"
                          % (filename, exc)
                        )
    # end def _open_manual

    def _plugins (self) :
        seen = set ()
        for p in itertools.chain (self.plugins, self._plugins_from_env ()) :
            if p and p not in seen :
                yield p
                seen.add (p)
    # end def _plugins

    def _plugins_from_env (self) :
        for ev in self._plugin_env_vars :
            plugins = sos.environ.get (ev, "")
            for p in plugins.split (":") :
                p = p.strip ()
                yield p
    # end def _plugins_from_env

    def _quit (self, quit_fct) :
        if quit_fct () :
            if not self._started_quit :
                self._started_quit = True
                try :
                    self.tkt._quit ()
                finally :
                    try :
                        self._quit_after_tkt (quit_fct)
                    finally :
                        self._destroy ()
                        print >> sys.__stdout__, \
                            "Leaving %s, good bye" % self.product_name
            else :
                raise RuntimeError, "Quit called reentrantly"
    # end def _quit

    def _quit_after_tkt (self, quit_fct) :
        self.State.dump ()
    # end def _quit_after_tkt

    def _run_command (self, * args, ** kw) :
        with TFL.Context.attr_let (sys, "stdout", self.stdout) :
            self.cmd_mgr.run (* args, ** kw)
    # end def _run_command

    def _run_postscripts (self) :
        self._run_scripts (self._startup_scripts ())
    # end def _run_postscripts

    def _run_prescripts (self) :
        if self.cmd.option ["prescripts"] :
            self._run_scripts (self.cmd.prescripts)
    # end def _run_prescripts

    def _run_script (self, script) :
        script = script.strip ()
        if script :
            try :
                try :
                    script = sos.expanded_path (script)
                except KeyboardInterrupt :
                    raise
                except StandardError :
                    pass
                if sos.path.isfile (script) :
                    TFL.Script (script, self.globals (), self.script_locals) ()
                else :
                    print "Script %s not found" % script
            except KeyboardInterrupt :
                raise
            except StandardError :
                print "Error during execution of", script
                traceback.print_exc ()
    # end def _run_script

    def _run_script_cmd (self) :
        """Run a Python script"""
        return self.script_mgr.run_script ()
    # end def _run_script_cmd

    def _run_scripts (self, scripts) :
        for s in scripts :
            self._run_script (s)
    # end def _run_scripts

    def _set_title (self) :
        self.tkt.set_title (self._window_title_text ())
    # end def _set_title

    def _setup_application (self) :
        pass
    # end def _setup_application

    def _setup_cmd_mgr (self) :
        self._create_command_mgr   ()
        self._setup_cmd_mgr_groups ()
        self.cmd_mgr.update_state  ()
    # end def _setup_cmd_mgr

    def _setup_cmd_mgr_groups (self) :
        cmd_mgr   = self.cmd_mgr
        add_group = cmd_mgr.add_group
        add_dyn_g = cmd_mgr.add_dyn_group
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
    # end def _setup_cmd_mgr_groups

    def _setup_edit_group (self, group) :
        if self.clipboard :
            self.clipboard.setup_clipboard_menu \
                (self.cmd_mgr, if_names = self.tkt.edit_interfacers)
   # end def _setup_edit_group

    def _setup_help_group (self, group) :
        Cmd = self.ANS.UI.Deaf_Command
        add = group.add_command
        if callable (self.display_guide) :
            add ( Cmd ("Guide", self.display_guide)
                , if_names = ("mb", "tb")
                , icon     = "help.guide"
                )
        add ( Cmd ("Bug info ...", self.show_bug_info)
            , if_names  = ("mb", )
            , underline = 4
            , batchable = True
            )
        if callable (self.show_rel_notes) and \
               (self.release_notes or self.batch_mode) :
            ### In batch mode, we want to define the command even if no
            ### release notes file is found
            ### In interactive mode, we don't want to define the command
            ### unless there is a file to be shown
            add ( Cmd ( "Release notes", self.show_rel_notes
                      )
                , if_names  = ("mb", )
                )
        if callable (self._open_manual) and \
               (self._manual_filename or self.batch_mode) :
            add ( Cmd ("Manual", self._open_manual)
                , if_names    = ("mb", )
                , accelerator = "help"
                )
    # end def _setup_help_group

    def _setup_manual_filename (self) :
        self._manual_filename = None
    # end def _setup_manual_filename

    def _setup_rn (self) :
        self.release_notes = None
        for suffix in "doc", "" :
            fn  = TFL.Filename \
                ( "release_notes.txt"
                , default_dir = sos.path.join (self.cmd.script_path, suffix)
                , absolute = 1
                ).name
            if sos.path.isfile (fn) :
                self.release_notes = fn
                break
    # end def _setup_rn

    def _setup_scripts_group (self, group) :
        ANS     = self.ANS
        Cmd     = ANS.UI.Deaf_Command
        add_cmd = group.add_command
        add_cmd \
            ( Cmd ( ANS.UI.Script_Menu_Mgr.run_cmd_name
                  , self._run_script_cmd
                  , Change_Action = self.script_run_change_act
                  )
            , if_names  = ("mb", "tb")
            , icon      = "scripts.run"
            , batchable = True
            )
        self.script_mgr   = sm = ANS.UI.Script_Menu_Mgr \
            ( application = self
            , cmd_grp     = group
            , if_names    = ("mb", )
            , local_dict  = self.script_locals
            )
        gp = sos.path.join (self.cmd.script_path, "goodies")
        if sos.path.isdir (gp) :
            sm.add_category \
                ( gp
                , doc =
                  "Example scripts provided by %s as-is and without any "
                  "warranty."
                  "\n"
                  "You can find and enjoy these scripts in the directory "
                  "`cat_dir'."
                % self.Tool_Supplier
                )
            for g in self._goodies () :
                sm.add_category (g)
        self._update_script_locals (add_script_category = sm.add_category)
    # end def _setup_scripts_group

    def _setup_script_locals (self) :
        self._update_script_locals \
            ( ask_string               = self.ask_string
            , ask_integer              = self.ask_integer
            , ask_float                = self.ask_float
            , ask_list_element         = self.ask_list_element
            , ask_list_element_combo   = self.ask_list_element_combo
            , ask_list_element_spinner = self.ask_list_element_spinner
            , ask_open_file_name       = self.ask_open_file_name
            , ask_save_file_name       = self.ask_save_file_name
            , ask_dir_name             = self.ask_dir_name
            , ask_open_dir_name        = self.ask_open_dir_name
            , ask_save_dir_name        = self.ask_save_dir_name
            , auto_save                = self.auto_save
            , gauge                    = self.gauge
            , keyword_value            = self.cmd.key_value
            , show_error               = self.show_error
            , show_info                = self.show_info
            , __name__                 = "__main__"
            )
        if self.powered or self.batch_mode :
            self._update_script_locals (AC = self.AC)
    # end def _setup_script_locals

    def _setup_tkt (self, cmd, TNS) :
        self.tkt = tkt     = self._create_tkt_application (cmd, TNS)
        self.menubar       = tkt._setup_menubar      ()
        self.toolbar       = tkt._setup_toolbar      ()
        self.buttbox       = tkt._setup_buttbox      ()
        self.context_menus = tkt._setup_context_menu ()
        self.event_binders = tkt._setup_event_binder ()
        tkt._setup_geometry                          ()
        if not getattr (cmd, "Suppress_Redirect", False) :
            tkt._setup_stdout_redirect               ()
        tkt._setup_clipboard                         ()
        self._setup_manual_filename                  ()
        self._setup_rn                               ()
    # end def _setup_tkt

    def _setup_windows_group (self, group) :
        pass
    # end def _setup_windows_group

    def _show_precondition_violation (self, name, msg) :
        self.show_error (name, msg)
    # end def _show_precondition_violation

    def _startup_scripts (self) :
        if not self.batch_mode :
            for ev in self._script_env_vars :
                env_scripts = sos.environ.get (ev, "")
                for s in env_scripts.split (",") :
                    yield s
        if self.cmd.option ["scripts"] :
            for s in self.cmd.scripts :
                yield s
    # end def _startup_scripts

    def _try_exit (self) :
        ### Override to save whatever needs saving
        pass
    # end def _try_exit

    def _try_quit (self) :
        ### Override to return False in situations hwere information would be
        ### lost without explicit permission by the user
        return True
    # end def _try_quit

    def _update_script_locals (self, ** kw) :
        self._script_locals.update (kw)
    # end def _update_script_locals

    def _window_title_text (self) :
        result = "Override for concrete application"
        return result
    # end def _window_title_text

    def __getattr__ (self, name) :
        if self.tkt is not None :
            result = getattr (self.tkt, name)
            setattr          (self,     name, result)
            return result
        raise AttributeError, name
    # end def __getattr__

Application = _TFL_UI_Application_ # end class

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ TFL.UI.Application

# -*- coding: utf-8 -*-
# Copyright (C) 1999-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
#
#++
# Name
#    TFL.UI.Script_Menu_Mgr
#
# Purpose
#    Manager for scripts to be run from the menu
#
# Revision Dates
#    13-Dec-1999 (CT)  Creation
#    14-Dec-1999 (CT)  `doc' added and passed to `add_cascade'
#    14-Dec-1999 (CT)  Capitalize category labels in menu
#    30-Jun-2000 (CT)  `local_dict' added (replaces `application.__dict__')
#     8-Aug-2000 (CT)  `Script' factored into separate module
#    14-Aug-2000 (CT)  Don't add the `Run ...' entry to the menu (and don't
#                      clear it either)
#     4-Sep-2002 (CT)  `run_script` changed to pass `name` to
#                      `ask_open_file_name`
#    20-Mar-2003 (CT)  `script_map` added to `Script_Category`
#    29-Jan-2004 (CT)  `echo` calls added to `run_script`
#    29-Jan-2004 (CT)  `echo` calls moved to `Script.__call__`
#    28-Sep-2004 (CT)  Use `isinstance` instead of type comparison
#     2-Feb-2005 (CT)  Moved to `TFL.UI` and refactored
#     7-Apr-2005 (CT)  Don't add category to `cmd_grp` when it's emtpy
#     9-Aug-2006 (CT)  `Script_Category.__hash__` changed to return
#                      `hash (self.name)` instead of `id (self)`
#    21-May-2007 (PGO) Let `Script_Category` handle trailing slashes
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL        import TFL
import _TFL._UI
import _TFL._UI.Mixin

from   Script     import *

class Script_Category (TFL.UI.Mixin) :
    """Manage a category of scripts."""

    def __init__ (self, AC, cat_dir, glob_dict, local_dict, name = None, doc = "") :
        self.__super.__init__ (AC)
        if sos.path.isdir (cat_dir) :
            self.name    = name or Dirname (cat_dir).base
            assert self.name, cat_dir
            self.dir     = cat_dir
            self.scripts = \
                [   Script (s, glob_dict, local_dict)
                for s in sos.listdir_ext (cat_dir, ".py")
                ]
        else :
            self.name    = name or cat_dir
            self.dir     = None
            self.scripts = []
        self.gd          = glob_dict
        self.ld          = local_dict
        self.doc         = doc.replace ("`cat_dir'", self.dir or self.name)
        self.script_map  = sm = {}
        for s in self.scripts :
            sm [s.name]  = s
    # end def __init__

    def add (self, * scripts) :
        for script in scripts :
            if isinstance (script, str) :
                script = Script (script, self.gd, self.ld)
            self.scripts.append (script)
            self.script_map [script.name] = script
    # end def add

    def is_applicable (self) :
        return bool (self.scripts)
    # end def is_applicable

    def _post_cb (self) :
        for s in self.scripts :
            yield s.name, s, None
    # end def _post_cb

    def __cmp__ (self, other) :
        return cmp (self.name, other.name)
    # end def __cmp__

    def __hash__ (self) :
        return hash (self.name)
    # end def __hash__

# end class Script_Category

class Script_Menu_Mgr (TFL.UI.Mixin) :
    """Manager for scripts to be run from a menu"""

    run_cmd_name = "Run ..."

    def __init__ (self, application, cmd_grp, if_names, local_dict = {}) :
        self.__super.__init__ (application.AC)
        self.application    = application
        self.cmd_grp        = cmd_grp
        self.if_names       = if_names
        self.local_dict     = local_dict
        self.last_script    = Script ("")
        self.category       = {}
        self.scripts        = {}
        Dyn                 = self.ANS.UI.Dyn_Command
        cmd_grp.add_command   \
            ( Dyn ("Scripts", self.script_mru)
            , if_names      = if_names
            )
     # end def __init__

    def add_category (self, cat_dir, name = None, doc = "") :
        """Add a script category with all python scripts found in
           `cat_dir'. The name of the category is derived from the last
           directory in `cat_dir', unless `name' is passed in.
        """
        cat = Script_Category \
            ( self.AC, cat_dir
            , self.application.globals (), self.local_dict, name, doc
            )
        if cat.scripts :
            self.cmd_grp.add_dyn_group \
                ( name          = cat.name.capitalize ()
                , command_gen   = cat._post_cb
                , precondition  = cat.is_applicable
                , desc          = cat.doc
                , if_names      = self.if_names
                ### XXX , help          = self.AC.ui_state.help
                )
            self.category [cat.name] = cat
    # end def add_category

    def run_script (self) :
        """Run a python script"""
        file_name = self.application.ask_open_file_name \
            ( defaultextension  = "*.py"
            , filetypes         =
                  ( ("python script files", "*.py")
                  , ("all files", "*")
                  )
            , initialdir        = self.last_script.dir
            , title             = "Python script to run"
            , name              = "Script"
            )
        if file_name :
            script = self.last_script = Script \
                (file_name, self.application.globals (), self.local_dict)
            self.scripts [file_name]  = script
            script ()
    # end def run_script

    def script_mru (self) :
        """List of most recently used scripts"""
        for s in sorted (self.scripts.itervalues ()) :
            yield s.name, s, None
    # end def script_mru

# end class Script_Menu_Mgr

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ TFL.UI.Script_Menu_Mgr

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2008-2010 Mag. Christian Tanzer. All rights reserved
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
#    TFL.TKT.Batch.Application
#
# Purpose
#    Generic base class for Batch-specific functionality
#
# Revision Dates
#    14-Aug-2008 (CT) Creation (factored from TTA.TKT.Batch.Application)
#    11-Feb-2009 (CT) `interact` changed to include `model.globals ()` and
#                     `model.script_locals` in context of interpreter
#    10-Dec-2009 (CT) Adapted to change of `TFL.Context.attr_let`
#    21-Jun-2010 (CT) Use `TFL.Environment.py_shell` instead of home-grown code
#    ««revision-date»»···
#--

from   _TFL               import TFL

import _TFL.Context
import _TFL.Environment
import _TFL.Filename

import _TFL._TKT.Application
import _TFL._TKT._Batch.Clipboard
import _TFL._TKT._Batch.Command_Interfacer
import _TFL._TKT._Batch.Eventname
import _TFL._TKT._Batch.Gauge
import _TFL._TKT._Batch.Queued_Stdout
import _TFL._TKT._Batch.Toplevel

from   _TFL               import sos
from   _TFL.Regexp        import *

class No_Keyword_Value (StandardError) : pass

class _TFL_TKT_Batch_Application_ (TFL.TKT.Application) :

    _real_name             = "Application"

    default_verbosity      = 1

    _ask_key_pat           = Regexp ("[^a-zA-Z0-9_]")
    edit_interfacers       = ("mb", "tb")

    def __init__ (self, model, ** kw) :
        self.__super.__init__ (model, ** kw)
        self.gauge = model.AC.ui_state.gauge = TFL.Gauge_Logger \
            (TFL.TKT.Batch.Gauge (), log = model.verbose)
    # end def __init__

    def ask_dir_name \
        ( self
        , name       = None
        , title      = ""
        , prompt     = None
        , initialdir = ""
        , init_val   = ""
        , ** kw
        ) :
        try :
            result = self.ask_string (name, title, prompt)
        except No_Keyword_Value :
            result = init_val or initialdir
            if not result :
                raise
        return TFL.Filename ("", default_dir = result).name
    # end def ask_dir_name

    ask_open_dir_name = ask_save_dir_name = ask_dir_name

    def ask_float \
        ( self
        , name     = None
        , title    = ""
        , prompt   = None
        , init_val = None
        ) :
        return float (self.ask_string (name, title, prompt, init_val))
    # end def ask_float

    def ask_integer \
        ( self
        , name     = None
        , title    = ""
        , prompt   = None
        , init_val = None
        ) :
        return int (self.ask_string (name, title, prompt, init_val))
    # end def ask_integer

    def ask_list_element \
        (self, name = None, title = "", prompt = None, list = ()) :
        return self.ask_string (name, title, prompt)
    # end def ask_list_element

    ask_list_element_combo   = ask_list_element
    ask_list_element_spinner = ask_list_element

    ### XXX implement a decent batch version for the following method
    def ask_many (self, * args, ** kw) :
        return []
    # end def ask_many

    def ask_open_file_name (self, ** kw) :
        result = self.ask_save_file_name (** kw)
        if not sos.path.isfile (result) :
            raise IOError, ("Couldn't open %s" % (result, ))
        return result
    # end def ask_open_file_name

    def ask_save_file_name \
        ( self
        , name             = None
        , title            = ""
        , prompt           = None
        , defaultextension = None
        , initialdir       = ""
        , initialfile      = ""
        , init_val         = ""
        , ** kw
        ) :
        try :
            result = self.ask_string (name, title, prompt)
        except No_Keyword_Value :
            result = init_val or initialfile
            if not result :
                raise
        return TFL.Filename \
            ( result
            , initialfile
            , default_dir = initialdir
            ).name
    # end def ask_save_file_name

    def ask_string \
        (self, name = None, title = "", prompt = None, init_val = None) :
        key    = (name or prompt or title).replace (" ", "_")
        key    = self._ask_key_pat.sub ("", key)
        result = self.cmd.key_value    (key) or init_val
        if result is None:
            raise No_Keyword_Value, \
                  "Please specify `%s=<value>' on command line for \n  %s" % \
                  (key, prompt or title)
        return result
    # end def ask_string

    def ask_yes_no \
        ( self
        , name    = None
        , title   = ""
        , prompt  = None
        , default = "yes"
        , ** kw
        ) :
        lines = (prompt or title).split ("\n")
        width = max (len (l) for l in lines) + 1
        print "-" * width, "\n|", "\n| ".join (lines)
        print "|\n| >>>>> Your answer is:", default, "<<<<<\n", "-" * width
        return default.upper () == "YES"
    # end def ask_yes_no

    def bind_to_sync (self, callback) :
        pass
    # end def bind_to_sync

    def busy_cursor   (self, * args, ** kw) :
        pass
    # end def busy_cursor

    def interact (self, glob_dct = None, locl_dct = None) :
        model = self.model
        if glob_dct is None:
            glob_dct = TFL.d_dict (model.script_locals, model.globals ())
        TFL.Environment.py_shell \
            ( glob_dct, locl_dct
            , ps1    = "%s => " % (model.Tool_Supplier)
            , banner = "%s - %s python interpreter"
                % (model.Tool_Supplier, model.product_name)
            )
    # end def interact

    def normal_cursor (self, * args, ** kw) :
        pass
    # end def normal_cursor

    def set_title (self, * args, ** kw) :
        pass
    # end def set_title

    def show_error (self, name, msg, ** kw) :
        pass
    # end def show_error

    show_info    = show_error
    show_warning = show_error

    def show_rel_notes (self, release_notes) :
        with open (release_notes) as f :
            print f.read ()
    # end def show_rel_notes

    def start_mainloop (self, after_mainloop_cb) :
        after_mainloop_cb ()
    # end def start_mainloop

    def _clear_widgets (self) :
        pass
    # end def _clear_widgets

    def _del_rel_notes (self, event = None) :
        pass
    # end def _del_rel_notes

    def load_images_from_dir (self, * dir) :
        pass
    # end def load_images_from_dir

    def _quit (self) :
        pass
    # end def _quit

    def _run_script_cmd (self, script  = None) :
        """Run a python script"""
        self._run_script (script)
    # end def _run_script_cmd

    def _setup_buttbox (self) :
        result = self.buttbox = self.TNS.CI_Button_Box (self.AC)
        return result
    # end def _setup_buttbox

    def _setup_context_menu (self) :
        return dict (cm = self.TNS.CI_Menu (self.AC))
    # end def _setup_context_menu

    def _setup_geometry (self) :
        pass
    # end def _setup_geometry

    def _setup_menubar (self) :
        result = self.menubar = self.TNS.CI_Menubar (self.AC)
        return result
    # end def _setup_menubar

    def _setup_menu_mgrs (self) :
        pass
    # end def _setup_menu_mgrs

    def _setup_toolbar (self) :
        result = self.toolbar = self.TNS.CI_Toolbar (self.AC)
        return result
    # end def _setup_toolbar

    def _try_exit (self) :
        return 1
    # end def _try_exit

    def _try_quit (self) :
        return 1
    # end def _try_quit

Application = _TFL_TKT_Batch_Application_ # end class

if __name__ != "__main__" :
    TFL.TKT.Batch._Export ("Application")
### __END__ TFL.TKT.Batch.Application

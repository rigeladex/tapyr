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
#    PMA.TKT.GTK.Application
#
# Purpose
#    Implement GTK-specific functionality of PMA
#
# Revision Dates
#    20-May-2005 (MG) Creation
#    22-May-2005 (CT) `virtual_key_name` removed, spelling
#     3-Jun-2005 (MG) `show_*` and some `ask_*` functions added
#     3-Jun-2005 (MG) Ask functions for filenames and and directorynames added
#     6-Jun-2005 (CT) Superfluous `staticmethod`s removed
#    27-Jul-2005 (MG) `_setup_context_menu` changed to return a dict of
#                     context menus
#    27-Jul-2005 (MG) `_setup_event_binder` added
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _PMA                 import PMA
import _PMA._TKT
import _PMA._TKT.Application
import _PMA._TKT._GTK
import _PMA._TKT._GTK.Butcon
### XXX import _PMA._TKT._GTK.Clipboard
import _PMA._TKT._GTK.Command_Interfacer
import _PMA._TKT._GTK.Dialog
import _PMA._TKT._GTK.Eventname
import _PMA._TKT._GTK.File_Chooser_Dialog
import _PMA._TKT._GTK.H_Box
import _PMA._TKT._GTK.Interpreter_Window
import _PMA._TKT._GTK.Message_Dialog
import _PMA._TKT._GTK.Message_Window
import _PMA._TKT._GTK.Office
import _PMA._TKT._GTK.Paned
import _PMA._TKT._GTK.Progress_Window
import _PMA._TKT._GTK.Queued_Stdout
import _PMA._TKT._GTK.Text
import _PMA._TKT._GTK.Tree
import _PMA._TKT._GTK.Toplevel
import _PMA._TKT._GTK.V_Box

from   Gauge_Logger         import Gauge_Logger
from   Script_Menu_Mgr      import Script_Menu_Mgr

import _TFL.d_dict
import _TFL.Environment
from   _TFL                 import sos
from   glob                 import glob

### XXX todo
### - Clipboard
### - Fileview Widget
### - pane: .divide, lower/upper limit
### - balloon for toolbar and application ???
### - dialogs ???

class Application (PMA.TKT.Application) :
    """Main instance of GTK-based PMA"""

    default_verbosity     = 2
    widget_class          = "PMA"

    def __init__ (self, model, ** kw) :
        self.__super.__init__      (model, ** kw)
        self._setup_toplevel       ()
        self._setup_panes          ()
    # end def __init__

    def bind_to_sync (self, callback) :
        self.toplevel.bind_add (self.TNS.Eventname.any_enter, callback)
    # end def bind_to_sync

    def interact (self) :
        """Provide interactive access to python interpreter."""
        model = self.model
        if not model.ipreter :
            model.ipreter = self.TNS.Interpreter_Window \
                ( self
                , global_dict  = TFL.d_dict
                      (model.globals (), Main_Widget = self) # model.script_locals
                , name         = "interpreter"
                , AC           = self.AC
                ,# master_gauge = self.gauge
                )
            model.ipreter.bind_add (self.TNS.Signal.Delete, self._kill_interact)
        model.ipreter.present      ()
    # end def interact

    def pack (self, parent, child) :
        parent.add (child)
    # end def pack

    def set_title (self, title = "") :
        self.toplevel.title = title
    # end def set_title

    def show_rel_notes (self, release_notes) :
        if not self.rn_viewer :
            self.rn_viewer  = rnv = self.TNS.Window \
                ( name      = "release_notes_viewer"
                , title     = "PMA release notes"
                )
            ### XXX
            #rnv.body        = CTK.Fileview (rnv, file = release_notes)
            #rnv.body.pack     \
            #    ( side      = TOP
            #    , expand    = YES
            #    , fill      = BOTH
            #    , padx      = 4
            #    , pady      = 4
            #    )
        self.rn_viewer.present ()
    # end def show_rel_notes

    def start_mainloop (self, after_mainloop_cb) :
        w = self.gui
        w.show_all () ### XXX
        self._after_mainloop_cb = after_mainloop_cb
        self.model.cmd_mgr.set_auto_short_cuts ()
        w.update_idletasks                     ()
        self.toplevel.present                  ()
        w.idle_add                             (self.after_mainloop_cb)
        self.TNS.main                          ()
    # end def start_mainloop

    def after_mainloop_cb (self, * args) :
        #self.body.change_size   (frac = 0.25)
        #self.body_l.change_size (frac = 0.70)
        #self.body_r.change_size (frac = 0.35)
        self._after_mainloop_cb ()
    # end def after_mainloop_cb

    def _destroy (self) :
        self.__super._destroy ()
        try :
            self.TNS.quit         ()
        except self.TNS.Error :
            pass
        except KeyboardInterrupt :
            raise
        except StandardError :
            sys.stdout = sys.__stdout__ ### just to be save
            traceback.print_exc ()
    # end def _destroy

    def _image_by_name (self, name) :
        try :
            return self.TNS.image_mgr [name]
        except KeyError :
            return None
    # end def _image_by_name

    def _load_images_from_dir (self, * dir) :
        for d in dir :
            images = glob (sos.path.join (d, "*.gif"))
            map (self.TNS.image_mgr.add, images)
    # end def _load_images_from_dir

    def _quit (self) :
        try :
            self.save_widget_memory ()
        finally :
            self._destroy ()
    # end def _quit

    def _setup_context_menu (self) :
        CI_Menu = self.TNS.CI_Menu
        AC      = self.AC
        return dict \
            ( cm_bv      = CI_Menu (name = "cm_bv",      AC = AC)
            , cm_mv      = CI_Menu (name = "cm_mv",      AC = AC)
            , cm_md      = CI_Menu (name = "cm_md",      AC = AC)
            , cm_mo      = CI_Menu (name = "cm_mo",      AC = AC)
            , cm_status  = CI_Menu (name = "cm_status",  AC = AC)
            )
    # end def _setup_context_menu

    def _setup_event_binder (self) :
        CI_Event_Binder = self.TNS.CI_Event_Binder
        AC              = self.AC
        return dict \
            ( ev_bv = CI_Event_Binder (AC = AC)
            , ev_mv = CI_Event_Binder (AC = AC)
            )
    # end def _setup_event_binder
    
    def _setup_geometry (self) :
        ### XXX
        self.gui.add            (self.main)
        self.main.pack          (self.menubar, expand = False)
        self.main.pack          (self.toolbar, expand = False)
        self.main.pack          (self.o_pane)
        self.body_r.pack_top    (self.wc_mb_msg_view)
        self.body_r.pack_bottom (self.wc_msg_display)
        self.body_l.pack_top    (self.wc_po_box_view)
        self.body_l.pack_bottom (self.wc_msg_outline)
        return
        limit = 60
        self.pane_mgr.lower_limit_pixl = self.min_y - limit
        self.pane_mgr.upper_limit_pixl = limit
        self.pane_mgr.divide (1)
    # end def _setup_geometry

    def _setup_menubar (self) :
        result = self.menubar = self.TNS.CI_Menubar \
            ( AC          = self.AC
            , accel_group = self.gui.accel_group
            , name        = "menu"
            , help        = self.message
            )
        result.show ()
        return result
    # end def _setup_menubar

    def _setup_panes (self) :
        TNS           = self.TNS
        self.main     = TNS.V_Box   (AC = self.AC)
        self.message  = self.AC.ui_state.message = TNS.Message_Window \
            (name = "status", AC = self.AC)
        self.body_l   = TNS.V_Paned (name = "lpanes", AC = self.AC)
        self.body_r   = TNS.V_Paned (name = "rpanes", AC = self.AC)
        self.body     = TNS.H_Paned \
            (self.body_l, self.body_r, name = "bpanes", AC = self.AC)
        self.wc_msg_display = TNS.Frame (AC = self.AC)
        self.wc_msg_outline = TNS.Frame (AC = self.AC)
        self.wc_mb_msg_view = TNS.Frame (AC = self.AC)
        self.wc_po_box_view = TNS.Frame (AC = self.AC)
        self.o_pane   = TNS.V_Paned \
            (self.body, self.message, name = "panes",  AC = self.AC)
        for w in ( self.o_pane, self.body, self.body_l, self.body_r
                 , self.main, self.wc_msg_outline, self.wc_msg_display
                 , self.wc_mb_msg_view, self.wc_po_box_view
                 , self.message
                 ) :
            w.show ()
        gauge         = TNS.Progress_Window \
            ( self.gui
            , name          = "progress"
            , active        = 0
            , cancel_button = 1
            , AC            = self.AC
            )
        self.gauge    = self.AC.ui_state.gauge = Gauge_Logger \
            ( gauge, log = self.model.verbose)
    # end def _setup_panes

    def _setup_toolbar (self) :
        result = self.toolbar = self.TNS.CI_Toolbar \
            ( AC              = self.AC
            , name            = "toolbar"
            , help            = self.message
            ### XXX , balloon         = self.tool_balloon
            )
        result.show                ()
        self._load_images_from_dir (TFL.Environment.module_path ("_PMA"))
        return result
    # end def _setup_toolbar

    def _setup_toplevel (self, master = None) :
        self.gui   = gui = self.TNS.Toplevel \
            ( name = self.model.product_name
            , AC   = self.AC
            )
        self.toplevel.bind_add (self.TNS.Signal.Delete, self.model.quit)
        self.gui.manager = self
        self.spec_width  = gui.num_opt_val    ( "width",     600)
        self.spec_height = gui.num_opt_val    ( "height",    800)
        self.min_x       = gui.num_opt_val    ( "minWidth",  380)
        self.min_y       = gui.num_opt_val    ( "minHeight", 400)
        self.set_title                        ()
        self.toplevel.bind_add (self.TNS.Signal.Delete, self.model.commit_all)
        #self.tool_balloon = CTK.Balloon \
        #    ( self.gui
        #    , offx        =  10
        #    , offy        =   2
        #    , arrow       =   0
        #    )
    # end def _setup_toplevel

    def __getattr__ (self, name) :
        try :
            return self.__super.__getattr__ (name)
        except AttributeError :
            return getattr (self.gui, name)
    # end def __getattr__

    def _show_dialog_ (self, cls, * args, ** kw) :
        kw ["AC"] = AC
        dialog    = cls    (* args, ** kw)
        return dialog.run  ()
    # end def _show_dialog_

    def show_error (self, * args, ** kw) :
        return self._show_dialog_ (self.TNS.Error_Dialog, * args, ** kw)
    # end def show_error

    def show_warning (self, * args, ** kw) :
        return self._show_dialog_ (self.TNS.Warning_Dialog, * args, ** kw)
    # end def show_warning

    def show_info (self, * args, ** kw) :
        return self._show_dialog_ (self.TNS.Info_Dialog, * args, ** kw)
    # end def show_info

    def ask_question (self, * args, ** kw) :
        return self._show_dialog_ (self.TNS.Error_Dialog, * arg, ** kw)
    # end def ask_question

    def ask_ok_cancel (self, * args, ** kw) :
        return self._show_dialog_ (self.TNS.OK_Cancel_Question, * args, ** kw)
    # end def ask_ok_cancel

    def ask_yes_no (self, * args, ** kw) :
        return self._show_dialog_ (self.TNS.Yes_No_Question, * args, ** kw)
    # end def ask_ok_cancel

    def ask_yes_no_cancel (self, * args, ** kw) :
        return self._show_dialog_ \
            (self.TNS.Yes_No_Cancel_Question, * args, ** kw)
    # end def ask_yes_no_cancel

    def ask_retry_cancel (self, * args, ** kw) :
        return self._show_dialog_ \
            (self.TNS.Cancel_Retry_Question, * args, ** kw)
    # end def ask_retry_cancel

    ### provide CTK_Dialog.ask_* functions as member functions, too
    ### `self' will be passed as argument `master'
    ask_string               = PMA.TKT.GTK.Dialog.ask_string
    ask_integer              = PMA.TKT.GTK.Dialog.ask_integer
    ask_float                = PMA.TKT.GTK.Dialog.ask_float
### XXX    ask_list_element         = CTK_Dialog.ask_list_element
### XXX    ask_list_element_combo   = CTK_Dialog.ask_list_element_combo
### XXX    ask_list_element_spinner = CTK_Dialog.ask_list_element_spinner

    ask_open_file_name       = PMA.TKT.GTK.ask_open_file_name
    ask_save_file_name       = PMA.TKT.GTK.ask_save_file_name
    ask_dir_name             = PMA.TKT.GTK.ask_dir_name
    ask_open_dir_name        = PMA.TKT.GTK.ask_open_dir_name
    ask_save_dir_name        = PMA.TKT.GTK.ask_save_dir_name

# end class Application

if __name__ != "__main__" :
    PMA.TKT.GTK._Export ("*")
### __END__ PMA.TKT.GTK.Application

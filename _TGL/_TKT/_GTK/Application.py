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
#    TGL.TKT.GTK.Application
#
# Purpose
#    Generic application framework.
#
# Revision Dates
#    12-Aug-2005 (MG) Creation (factored from PMA/CAL.TKT.GTK.Application)
#    12-Aug-2005 (MG) `event_binders` added
#    16-Aug-2005 (MG) Don't call `show_all` anymore
#     3-Sep-2005 (MG) correct `_wrap_function`
#    21-Sep-2005 (MG) Obsolete import of ´Script_Menu_Mgr` removed
#     2-Jan-2006 (MG) `_quit` close the interpreter window to save the
#                     current state
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _TGL                 import TGL
import _TGL._TKT
import _TGL._TKT.Application
import _TGL._TKT._GTK.Butcon
import _TGL._TKT._GTK.Command_Interfacer
import _TGL._TKT._GTK.Dialog
import _TGL._TKT._GTK.Eventname
import _TGL._TKT._GTK.File_Chooser_Dialog
import _TGL._TKT._GTK.H_Box
import _TGL._TKT._GTK.Interpreter_Window
import _TGL._TKT._GTK.Image_Manager
import _TGL._TKT._GTK.Message_Dialog
import _TGL._TKT._GTK.Message_Window
import _TGL._TKT._GTK.Paned
import _TGL._TKT._GTK.Progress_Window
import _TGL._TKT._GTK.Queued_Stdout
import _TGL._TKT._GTK.Text
import _TGL._TKT._GTK.Tree
import _TGL._TKT._GTK.Toplevel
import _TGL._TKT._GTK.V_Box


from   Gauge_Logger         import Gauge_Logger

import _TFL.d_dict
import _TFL.Environment
from   _TFL                 import sos
from   glob                 import glob

class _TGL_TKT_GTK_Application_ (TGL.TKT.Application) :
    """Generice application framework."""

    default_verbosity     = 2
    widget_class          = "TGL"
    _real_name            = "Application"
    context_menus         = ()
    event_binders         = ()

    def __init__ (self, model, ** kw) :
        self.__super.__init__      (model, ** kw)
        self._setup_toplevel       ()
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
        w.show ()
        self._after_mainloop_cb = after_mainloop_cb
        self.model.cmd_mgr.set_auto_short_cuts ()
        w.update_idletasks                     ()
        self.toplevel.present                  ()
        w.idle_add                             (self.after_mainloop_cb)
        self.TNS.main                          ()
    # end def start_mainloop

    def after_mainloop_cb (self, * args) :
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
            if self.model.ipreter :
                self.model.ipreter.close_window ()
            self.save_widget_memory ()
        finally :
            self._destroy ()
    # end def _quit

    def _create_ci (self, cls, names) :
        return dict ([(n, cls (name = n, AC = self.AC)) for n in names])
    # end def _create_ci

    def _setup_context_menu (self) :
        CI_Menu = self.TNS.CI_Menu
        return self._create_ci (self.TNS.CI_Menu, self.context_menus)
    # end def _setup_context_menu

    def _setup_event_binder (self) :
        return self._create_ci (self.TNS.CI_Event_Binder, self.event_binders)
    # end def _setup_event_binder

    def _setup_geometry (self) :
        self.gui.add            (self.main)
        if self.model.show_menubar :
            self.main.pack      (self.menubar, expand = False)
        if self.model.show_toolbar :
            self.main.pack      (self.toolbar, expand = False)
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

    def _setup_toolbar (self) :
        result = self.toolbar = self.TNS.CI_Toolbar \
            ( AC              = self.AC
            , name            = "toolbar"
            , help            = self.message
            ### XXX , balloon         = self.tool_balloon
            )
        result.style = self.TNS.gtk.TOOLBAR_ICONS
        result.show ()
        self._load_images_from_dir \
            (TFL.Environment.module_path ("_%s" % (self.widget_class, )))
        return result
    # end def _setup_toolbar

    def _setup_toplevel (self, master = None) :
        TNS        = self.TNS
        self.gui   = gui = TNS.Toplevel \
            ( name = self.model.product_name
            , AC   = self.AC
            )
        self.gui.read_style_file \
            ("%s.rc" % (self.widget_class, ), search = True)
        self.toplevel.bind_add   (TNS.Signal.Delete, self.model.quit)
        self.gui.manager = self
        self.spec_width  = gui.num_opt_val    ( "width",     600)
        self.spec_height = gui.num_opt_val    ( "height",    800)
        self.min_x       = gui.num_opt_val    ( "minWidth",  380)
        self.min_y       = gui.num_opt_val    ( "minHeight", 400)
        self.set_title                        ()
        self.toplevel.bind_add (TNS.Signal.Delete, self.model.commit_all)
        gauge            = TNS.Progress_Window \
            ( self.gui
            , name          = "progress"
            , active        = 0
            , cancel_button = 1
            , AC            = self.AC
            )
        self.gauge       = self.AC.ui_state.gauge = Gauge_Logger \
            (gauge, log = self.model.verbose)
        self._setup_panes      ()
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
    def _wrap_function (f) :
        name = f.__name__
        def _prep_args (self, * args, ** kw) :
            return getattr (self.TNS.Dialog, name) \
                (self.toplevel.wtk_object, AC = self.AC, * args, ** kw)
        _prep_args.__name__ = f.__name__
        _prep_args.__doc__  = f.__doc__
        return _prep_args
    # end def _wrap_function

    @_wrap_function
    def ask_string  () : pass
    @_wrap_function
    def ask_integer () : pass
    @_wrap_function
    def ask_float   () : pass

### XXX    ask_list_element         = CTK_Dialog.ask_list_element
### XXX    ask_list_element_combo   = CTK_Dialog.ask_list_element_combo
### XXX    ask_list_element_spinner = CTK_Dialog.ask_list_element_spinner

    def _wrap_function (f) :
        name = f.__name__
        def _prep_args (self, * args, ** kw) :
            return getattr (self.TNS, name) \
                (self.toplevel.wtk_object, AC = self.AC, * args, ** kw)
        _prep_args.__name__ = f.__name__
        _prep_args.__doc__  = f.__doc__
        return _prep_args
    # end def _wrap_function

    @_wrap_function
    def ask_open_file_name () : pass
    @_wrap_function
    def ask_save_file_name () : pass
    @_wrap_function
    def ask_dir_name ()       : pass
    @_wrap_function
    def ask_open_dir_name ()  : pass
    @_wrap_function
    def ask_save_dir_name ()  : pass

Application =_TGL_TKT_GTK_Application_

if __name__ != "__main__" :
    TGL.TKT.GTK._Export ("Application")
### __END__ TGL.TKT.GTK.Application

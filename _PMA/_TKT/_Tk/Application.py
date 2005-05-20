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
#    PMA.TKT.Tk.Application
#
# Purpose
#    Implement Tkinter-specific functionality of PMA
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _PMA                 import PMA
import _PMA._TKT
import _PMA._TKT.Application
import _PMA._TKT._Tk
import _PMA._TKT._Tk.Butcon
import _PMA._TKT._Tk.Clipboard
import _PMA._TKT._Tk.Command_Interfacer
import _PMA._TKT._Tk.Eventname
import _PMA._TKT._Tk.Queued_Stdout
import _PMA._TKT._Tk.Text
import _PMA._TKT._Tk.Toplevel

from   CTK                  import *
from   CTK_Toolbar          import Toolbar
from   Gauge_Logger         import Gauge_Logger
from   Script_Menu_Mgr      import Script_Menu_Mgr

import CTK_Dialog

import _TFL.d_dict
import _TFL.Environment
from   _TFL                 import sos
from   glob                 import glob

class Application (PMA.TKT.Application) :
    """Main instance of Tkinter-based PMA"""

    default_verbosity     = 2
    widget_class          = "PMA"
    standard_option_files = ()
    option_files          = ()

    class C_Frame (CTK.C_Frame) :
        widget_class      = "PMA"
    # end class C_Frame

    def __init__ (self, model, ** kw) :
        self.__super.__init__      (model, ** kw)
        CTK.C_Toplevel.state_mgr   = self.State
        self._read_option_files    ()
        self._setup_toplevel       ()
        self._setup_panes          ()
    # end def __init__

    def bind_to_sync (self, callback) :
        CTK.root.bind ("<Any-Enter>", callback)
    # end def bind_to_sync

    def interact (self) :
        """Provide interactive access to python interpreter."""
        model = self.model
        if not model.ipreter :
            from _TFL.Power_User_Window import Power_User_Window ### XXX
            model.ipreter = Power_User_Window \
                ( self.gui
                , globals      = TFL.d_dict
                      (model.script_locals, model.globals ())
                , name         = "interpreter"
                , master_gauge = self.gauge
                )
            model.ipreter.protocol ("WM_DELETE_WINDOW", self._kill_interact)
        model.ipreter.deiconify ()
        model.ipreter.focus_set ()
    # end def interact

    def pack (self, parent, child) :
        child = getattr (child, "exposed_widget", child)
        child.pack (expand = YES, fill = BOTH)
    # end def pack

    def set_title (self, title = "") :
        self.toplevel.title (title)
    # end def set_title

    def show_rel_notes (self, release_notes) :
        if not self.rn_viewer :
            self.rn_viewer  = rnv = CTK.BB_Toplevel \
                ( self.gui
                , name      = "release_notes_viewer"
                , close_cmd = self._del_rel_notes
                , title     = "PMA release notes"
                )
            rnv.body        = CTK.Fileview (rnv, file = release_notes)
            rnv.body.pack     \
                ( side      = TOP
                , expand    = YES
                , fill      = BOTH
                , padx      = 4
                , pady      = 4
                )
        self.rn_viewer.deiconify   ()
        self.rn_viewer.focus_force ()
    # end def show_rel_notes

    def start_mainloop (self, after_mainloop_cb) :
        w = self.gui
        self._after_mainloop_cb = after_mainloop_cb
        self.model.cmd_mgr.set_auto_short_cuts ()
        w.update_idletasks ()
        w.winfo_toplevel   ().deiconify ()
        w.tkraise          ()
        w.focus_force      ()
        w.after_idle       (self._after_mainloop)
        w.mainloop         ()
    # end def start_mainloop

    def virtual_key_name (self, name) :
        return CTK.virtual_key_name (name)
    # end def virtual_key_name

    def _after_mainloop (self,) :
        self.body.change_size   (frac = 0.25)
        self.body_l.change_size (frac = 0.70)
        self.body_r.change_size (frac = 0.35)
        self._after_mainloop_cb ()
    # end def _after_mainloop

    def _destroy (self) :
        self.__super._destroy ()
        try :
            self.toplevel.destroy ()
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
            return CTK.image_mgr [name]
        except KeyError :
            return None
    # end def _image_by_name

    def _load_images_from_dir (self, * dir) :
        for d in dir :
            images = glob (sos.path.join (d, "*.gif"))
            map (CTK.image_mgr.add, images)
    # end def _load_images_from_dir

    def _quit (self) :
        try :
            self.save_geometry     (self.State, "PMA")
            self.toplevel.withdraw ()
            ### clear hash tables of image_mgr and bitmap_mgr to avoid
            ### TclError exceptions triggered when the garbage collector
            ### reaps those
            CTK.image_mgr.x_map  = {}
            CTK.bitmap_mgr.x_map = {}
        finally :
            self._destroy ()
    # end def _quit

    def _read_option_files (self) :
        root = CTK.root
        for f in self.standard_option_files :
            CTK.read_option_files (root, f)
        for f in self.option_files :
            CTK.read_option_files (root, f)
    # end def _read_option_files

    def _setup_context_menu (self) :
        result = self.context_menu = self.TNS.CI_Menu \
            ( AC      = self.AC
            , parent  = self.gui
            , tearoff = False
            )
        return result
    # end def _setup_context_menu

    def _setup_geometry (self) :
        for p in self.o_pane, self.body_l, self.body_r :
            p.pack                   (expand = YES, fill = BOTH)
        self.toolbar_frame.pack      (expand = NO,  fill = X)
        self.toolbar.wtk_widget.pack (expand = NO,  fill = X,    side = LEFT)
        self.message.pack        \
            ( side   = BOTTOM
            , fill   = BOTH
            , expand = YES
            , padx   = 6
            , pady   = 3
            # anchor = S
            )
        self.body.pack (expand = YES, fill = BOTH)
        limit = 60
        self.o_pane.lower_limit_pixl = self.min_y - limit
        self.o_pane.upper_limit_pixl = limit
        self.o_pane.divide (1)
    # end def _setup_geometry

    def _setup_menubar (self) :
        result = self.menubar = self.TNS.CI_Menubar \
            ( self.AC, self.gui
            , name   = "menu"
            , type   = "menubar"
            , help   = self.message
            )
        return result
    # end def _setup_menubar

    def _setup_panes (self) :
        self.o_pane   = CTK.V_Panedwindow ( self.gui, name = "opanes")
        upper         = self.o_pane.upper
        lower         = self.o_pane.lower
        self.message  = self.AC.ui_state.message = CTK.Message_Window \
            ( lower
            , name    = "status"
            , fill    = BOTH
            )
        gauge         = CTK.Progress_Gauge_T \
            ( self.gui
            , name          = "progress"
            , active        = 0
            , cancel_button = 1
            )
        self.gauge    = self.AC.ui_state.gauge = Gauge_Logger \
            ( gauge, log = self.model.verbose)
        self.body     = CTK.H_Panedwindow ( upper,           name = "bpanes")
        self.body_l   = CTK.V_Panedwindow ( self.body.left,  name = "lpanes")
        self.body_r   = CTK.V_Panedwindow ( self.body.right, name = "rpanes")
        self.wc_msg_display = self.body_r.lower
        self.wc_msg_outline = self.body_l.lower
        self.wc_folder_view = self.body_r.upper
        self.wc_folder_tree = self.body_l.upper
    # end def _setup_panes

    def _setup_toolbar (self) :
        self.toolbar_frame    = CTK.C_Frame (self.o_pane.upper)
        result = self.toolbar = self.TNS.CI_Toolbar \
            ( self.AC, self.toolbar_frame
            , name            = "toolbar"
            , help            = self.message
            , balloon         = self.tool_balloon
            )
        self._load_images_from_dir (TFL.Environment.module_path ("_PMA"))
        return result
    # end def _setup_toolbar

    def _setup_toplevel (self, master = None) :
        self.gui = gui = self.C_Frame \
            (master, name = self.model.product_name)
        self.gui.manager  = self
        self.set_maxsize                      ()
        self.gui.pack                         ( expand = YES, fill = BOTH)
        self.toplevel    = gui.toplevel \
                         = gui.winfo_toplevel ()
        self.spec_width  = gui.num_opt_val    ( "width",     600)
        self.spec_height = gui.num_opt_val    ( "height",    800)
        self.min_x       = gui.num_opt_val    ( "minWidth",  380)
        self.min_y       = gui.num_opt_val    ( "minHeight", 400)
        geom = "%dx%d" % (self.spec_width, self.spec_height)
        geom = self.State.window_geometry.get ( self.model.product_name, geom)
        self.toplevel.geometry                ( geom)
        self.toplevel.minsize                 ( self.min_x, self.min_y)
        self.set_title                        ()
        self.toplevel.protocol ( "WM_DELETE_WINDOW", self.model.quit)
        self.toplevel.protocol ( "WM_SAVE_YOURSELF", self.model.commit_all)
        self.tool_balloon = CTK.Balloon \
            ( self.gui
            , offx        =  10
            , offy        =   2
            , arrow       =   0
            )
    # end def _setup_toplevel

    def __getattr__ (self, name) :
        try :
            return self.__super.__getattr__ (name)
        except AttributeError :
            return getattr (self.gui, name)
    # end def __getattr__

    ### provide CTK_Dialog.ask_* functions as member functions, too
    ### `self' will be passed as argument `master'
    ask_string               = CTK_Dialog.ask_string
    ask_integer              = CTK_Dialog.ask_integer
    ask_float                = CTK_Dialog.ask_float
    ask_list_element         = CTK_Dialog.ask_list_element
    ask_list_element_combo   = CTK_Dialog.ask_list_element_combo
    ask_list_element_spinner = CTK_Dialog.ask_list_element_spinner

    ### these must be wrapped, because they don't accept `self' as argument
    ask_open_file_name       = staticmethod (CTK_Dialog.ask_open_file_name)
    ask_save_file_name       = staticmethod (CTK_Dialog.ask_save_file_name)
    ask_dir_name             = staticmethod (CTK_Dialog.ask_dir_name)
    ask_open_dir_name        = staticmethod (CTK_Dialog.ask_open_dir_name)
    ask_save_dir_name        = staticmethod (CTK_Dialog.ask_save_dir_name)

# end class Application

if __name__ != "__main__" :
    PMA.TKT.Tk._Export ("*")
### __END__ PMA.TKT.Tk.Application

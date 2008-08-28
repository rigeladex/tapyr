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
#    TFL.TKT.Tk.Application
#
# Purpose
#    Generic base class for Tk-specific functionality
#
# Revision Dates
#    15-Aug-2008 (CT) Creation (factored from TTA.TKT.Tk.Application)
#    18-Aug-2008 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL               import TFL

import _TFL.d_dict
import _TFL.Context
import _TFL.Filename
import _TFL.Gauge_Logger

import _TFL._TKT.Application
import _TFL._TKT._Tk.Butcon
import _TFL._TKT._Tk.Clipboard
import _TFL._TKT._Tk.Command_Interfacer
import _TFL._TKT._Tk.Eventname
import _TFL._TKT._Tk.Message_Window
import _TFL._TKT._Tk.Queued_Stdout
import _TFL._TKT._Tk.Text
import _TFL._TKT._Tk.Toplevel

from   _TFL                         import sos
from   _TFL._TKT._Tk.CTK            import *
import _TFL._TKT._Tk.CTK_Dialog     as     CTK_Dialog
from   _TFL._TKT._Tk.CTK_Toolbar    import Toolbar
from   _TFL.Regexp                  import *

from   glob                         import glob

import sys
import traceback

class _TFL_TKT_Tk_Application_ (TFL.TKT.Application) :

    _real_name            = "Application"

    default_verbosity     = 2
    widget_class          = "TFL_GUI_Application"
    """`widget_class' defines the class name of the widget used for accessing
       the TK resource database.
       """
    standard_option_files = ("_TFL/Model.opt", )
    option_files          = ()

    _body_widget_name     = "body"
    _normal_cursor_after_idle_pending = False

    empty_lines           = re.compile ("\n[. ]*\n")
    eol_dots              = re.compile (" *(\\. ?)(\\. ?)+\n")

    spec_width            = 600
    spec_height           = 400
    min_x                 = 380
    min_y                 = 200

    class C_Frame (CTK.C_Frame) :
        widget_class      = "TFL"
    # end class C_Frame

    def __init__ (self, model, ** kw) :
        self.__super.__init__      (model, ** kw)
        self._read_option_files    ()
        window_title_bar_icon_name = self._window_title_bar_icon_name ()
        CTK.C_Toplevel.window_title_bar_icon_name = window_title_bar_icon_name
        CTK.C_Toplevel.state_mgr   = self.State
        self.C_Frame.widget_class  = self.widget_class
        self._setup_widgets ()
        self._setup_window_title_bar_icon (window_title_bar_icon_name)
    # end def __init__

    def bind_to_sync (self, callback) :
        CTK.root.bind ("<Any-Enter>", callback)
    # end def bind_to_sync

    def busy_cursor (self, cursor = "watch") :
        self.gui.busy_cursor (cursor)
        for w in self._sub_widgets () :
            if w :
                try :
                    w.busy_cursor (cursor)
                except AttributeError :
                    pass
    # end def busy_cursor

    def interact (self, globals = None, locals = None) :
        """Provide interactive access to python interpreter."""
        model = self.model
        if not model.ipreter :
            from _TFL._TKT._Tk.Power_User_Window import Power_User_Window
            if globals is None :
                globals = TFL.d_dict (model.script_locals, model.globals ())
            if locals  is None :
                locals  = {}
            model.ipreter = Power_User_Window \
                ( self
                , globals      = globals
                , locals       = locals
                , name         = "interpreter"
                )
            model.ipreter.protocol ("WM_DELETE_WINDOW", self._kill_interact)
        model.ipreter.deiconify ()
        model.ipreter.focus_set ()
    # end def interact

    def normal_cursor (self) :
        if not self._normal_cursor_after_idle_pending :
            self._normal_cursor_after_idle_pending = \
                self.after_idle (self._normal_cursor_after_idle)
    # end def normal_cursor

    def set_title (self, title = "") :
        self.toplevel.title \
            ( "%s - %s%s"
            % (self.model.Tool_Supplier, self.model.product_name, title)
            )
    # end def set_title

    def show_error (self, title = None, message = None, ** kw) :
        return self.gui.show_error (title, message, ** kw)
    # end def show_error

    def show_info (self, title = None, message = None, ** kw) :
        return self.gui.show_info (title, message, ** kw)
    # end def show_info

    def show_rel_notes (self, release_notes) :
        if not self.rn_viewer :
            self.rn_viewer  = rnv = CTK.BB_Toplevel \
                ( self.gui
                , name      = "release_notes_viewer"
                , close_cmd = self._del_rel_notes
                , title     = "%s - %s release notes"
                    % (self.model.Tool_Supplier, self.model.product_name)
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
        self.model.cmd_mgr.set_auto_short_cuts ()
        w.update_idletasks ()
        w.winfo_toplevel   ().deiconify ()
        w.tkraise          ()
        w.focus_force      ()
        w.after_idle       (after_mainloop_cb)
        w.mainloop         ()
    # end def start_mainloop

    def virtual_key_name (self, name) :
        return CTK.virtual_key_name (name)
    # end def virtual_key_name

    def _destroy (self) :
        self.__super._destroy ()
        try :
            self.toplevel.destroy ()
        except self.TNS.Error :
            pass
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

    def load_images_from_dir (self, * directories) :
        for d in directories :
            images = glob (sos.path.join (d, "*.gif"))
            map (CTK.image_mgr.add, images)
    # end def load_images_from_dir

    def _normal_cursor_after_idle (self) :
        self._normal_cursor_after_idle_pending = False
        self.gui.normal_cursor ()
        for w in self._sub_widgets () :
            if w :
                try :
                    w.normal_cursor ()
                except AttributeError :
                    pass
        self.message.replace_matches (self.empty_lines, "\n")
        self.message.replace_matches (self.eol_dots,    ".\n")
        self.message.see             (END)
    # end def _normal_cursor_after_idle

    def _quit (self) :
        try :
            self.save_geometry     (self.State, self.model.product_name)
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

    def _setup_buttbox (self) :
        result = self.buttbox = self.TNS.CI_Button_Box \
            ( self.AC, self.toolbar_frame
            , name            = self.model.Tool_Supplier
            , help            = self.message
            , balloon         = self.tool_balloon
            , height          = 23
            )
        return result
    # end def _setup_buttbox

    def _setup_context_menu (self) :
        result = self.TNS.CI_Menu \
            ( self.AC, self.gui
            , name    = "context_menu"
            , help    = self.message
            , tearoff = False
            )
        return dict (cm = result)
    # end def _setup_context_menu

    def _setup_geometry (self) :
        self.pane_mgr.pack      (expand = YES, fill = BOTH)
        self.toolbar_frame.pack (expand = NO,  fill = X)
        if __debug__ and (not TFL.Environment.frozen ()) :
            self.toolbar.wtk_widget.pack \
                (expand = YES, fill = X,    side = LEFT)
            self.buttbox.wtk_widget.pack \
                (expand = NO,  fill = BOTH, side = RIGHT)
        else :
            self.buttbox.wtk_widget.pack \
                (expand = NO,  fill = BOTH, side = RIGHT)
            self.toolbar.wtk_widget.pack \
                (expand = NO,  fill = X,    side = LEFT)
        self.message.pack \
            ( side   = BOTTOM
            , fill   = BOTH
            , expand = YES
            , padx   = 6
            , pady   = 3
            )
        self.body.pack (expand = YES, fill = BOTH)
        limit = 60
        self.pane_mgr.lower_limit_pixl = self.min_y - limit
        self.pane_mgr.upper_limit_pixl = limit
        self.pane_mgr.divide (1)
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
        self.pane_mgr = CTK.V_Panedwindow (self.gui, name = "panes")
        upper         = self.pane_mgr.upper
        lower         = self.pane_mgr.lower
        self.message  = self.AC.ui_state.message = self.TNS.Message_Window \
            ( AC      = self.AC
            , wc      = lower
            , name    = "status"
            , fill    = BOTH
            )
        gauge         = CTK.Progress_Gauge_T \
            ( self.gui
            , name          = "progress"
            , active        = 0
            , cancel_button = 1
            )
        self.gauge    = self.AC.ui_state.gauge = TFL.Gauge_Logger \
            ( gauge, log = self.model.verbose)
        self.body     = CTK.C_Frame  \
            ( upper
            , name    = self._body_widget_name
            )
    # end def _setup_panes

    def _setup_toolbar (self) :
        self.toolbar_frame    = CTK.C_Frame (self.pane_mgr.upper)
        result = self.toolbar = self.TNS.CI_Toolbar \
            ( self.AC, self.toolbar_frame
            , name            = "toolbar"
            , help            = self.message
            , balloon         = self.tool_balloon
            )
        return result
    # end def _setup_toolbar

    def _setup_toplevel (self, master = None) :
        self.gui = gui = self.C_Frame (master, name = self.model.product_name)
        gui.manager    = self
        gui.set_maxsize                       ()
        gui.pack                              ( expand = YES, fill = BOTH)
        self.toplevel    = gui.toplevel \
                         = gui.winfo_toplevel ()
        self.spec_width  = gui.num_opt_val    ( "width",     self.spec_width)
        self.spec_height = gui.num_opt_val    ( "height",    self.spec_height)
        self.min_x       = gui.num_opt_val    ( "minWidth",  self.min_x)
        self.min_y       = gui.num_opt_val    ( "minHeight", self.min_y)
        geom = "%dx%d" % (self.spec_width, self.spec_height)
        geom = self.State.window_geometry.get ( self.model.product_name, geom)
        self.toplevel.geometry                ( geom)
        self.toplevel.minsize                 ( self.min_x, self.min_y)
        self.set_title                        ()
        self.toplevel.protocol ( "WM_DELETE_WINDOW", self.model.quit)
        self.toplevel.protocol ( "WM_SAVE_YOURSELF", self.model.save)
        self.tool_balloon = CTK.Balloon \
            ( self.gui
            , offx        =  10
            , offy        =   2
            , arrow       =   0
            )
    # end def _setup_toplevel

    def _setup_widgets (self) :
        self._setup_toplevel ()
        self._setup_panes    ()
    # end def _setup_widgets

    def _setup_window_title_bar_icon (self, path_to_icon) :
        if path_to_icon :
            head = "@" if sys.platform != "win32" else ""
            try :
                for window in (self.toplevel, self.gauge) :
                    window.iconbitmap ("%s%s" % (head, path_to_icon))
            except :
                if __debug__ and (not TFL.Environment.frozen ()) :
                    raise
    # end def set_window_title_bar_icon

    def _sub_widgets (self) :
        return \
            ( self.menubar.wtk_widget
            , self.toolbar.wtk_widget
            , self.buttbox.wtk_widget
            , self.message
            )
    # end def _sub_widgets

    def _window_title_bar_icon_name (self) :
        if sys.platform == "win32" :
            ext = "ico"
        else :
            ext = "xbm"
        icon_name    = self.model.product_name
        path_to_icon = TFL.Environment.script_path ()
        path_to_icon = sos.path.join (path_to_icon, "%s.%s" % (icon_name, ext))
        if not sos.path.exists (path_to_icon) :
            path_to_icon = None
        return path_to_icon
    # end def _window_title_bar_icon_name

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

Application = _TFL_TKT_Tk_Application_ # end class

if __name__ != "__main__" :
    TFL.TKT.Tk._Export ("Application")
### __END__ TFL.TKT.Tk.Application

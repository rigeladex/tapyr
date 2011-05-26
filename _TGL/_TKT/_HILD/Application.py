# -*- coding: iso-8859-15 -*-
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
#    TGL.TKT.HILD.Application
#
# Purpose
#    Generic application framework.
#
# Revision Dates
#    12-Aug-2005 (MG) Creation (factored from PMA/CAL.TKT.GTK.Application)
#    12-Aug-2005 (MG) `event_binders` added
#    16-Aug-2005 (MG) Don't call `show_all` anymore
#     3-Sep-2005 (MG) correct `_wrap_function`
#    21-Sep-2005 (MG) Obsolete import of ŽScript_Menu_Mgr` removed
#     2-Jan-2006 (MG) `_quit` close the interpreter window to save the
#                     current state
#    03-Jan-2006 (MG) `ask_invisible_string` added
#    21-Jan-2006 (MG) Imports fixed
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _TGL                 import TGL
import _TGL._TKT
import _TGL._TKT._GTK
import _TGL._TKT._GTK.Application
import _TGL._TKT._HILD.App
import _TGL._TKT._HILD.App_View

class _TGL_TKT_HILD_Application_ (TGL.TKT.GTK.Application) :
    """Generice application framework."""

    _real_name            = "Application"

    def set_title (self, title = "") :
        view_title = ""
        if "-" in title :
            title, view_title = title.split ("-", 1)
        self.toplevel_app.title = title
        self.toplevel.title     = view_title
    # end def set_title

    def start_mainloop (self, after_mainloop_cb) :
        w = self.gui
        w.show ()
        self._after_mainloop_cb = after_mainloop_cb
        self.model.cmd_mgr.set_auto_short_cuts ()
        w.update_idletasks                     ()
        w.idle_add                             (self.after_mainloop_cb)
        self.TNS.main                          ()
    # end def start_mainloop

    def _setup_geometry (self) :
        self.gui.add            (self.main)
        if self.model.show_menubar :
            self.menubar.show_all ()
        if self.model.show_toolbar :
           self.gui.vbox.pack      (self.toolbar, expand = False, start = False)
           self.toolbar.show_all   ()
    # end def _setup_geometry

    def _setup_menubar (self) :
        result = self.menubar = self.TNS.CI_Menu \
            ( AC          = self.AC
#            , accel_group = self.gui.accel_group
            , name        = "menu"
            , help        = self.message
            , wtk_object  = self.gui.menu.wtk_object
            )
        result.show ()
        return result
    # end def _setup_menubar

    def _setup_toplevel (self, master = None) :
        TNS        = self.TNS
        AC         = self.AC
        self.gui   = gui = TNS.App_View \
            ( title = ""
            , name  = self.model.product_name
            , AC    = AC
            )
        self.toplevel_app = TNS.App (gui, AC = AC)
        self.gui.read_style_file \
            ("%s.rc" % (self.widget_class, ), search = True)
        self.toplevel.bind_add   (TNS.Signal.Delete, self.model.quit)
        self.gui.manager = self
        self.set_title                        ()
        self.toplevel.bind_add (TNS.Signal.Delete, self.model.commit_all)
        gauge            = TNS.Progress_Window \
            ( self.gui
            , name          = "progress"
            , active        = 0
            , cancel_button = 1
            , AC            = AC
            )
        self.gauge       = self.AC.ui_state.gauge = TFL.Gauge_Logger \
            (gauge, log = self.model.verbose)
        self._setup_panes      ()
        self.toplevel.show     ()
        self.toplevel_app.show     ()
    # end def _setup_toplevel

Application =_TGL_TKT_HILD_Application_

if __name__ != "__main__" :
    TGL.TKT.HILD._Export ("Application")
### __END__ TGL.TKT.HILD.Application

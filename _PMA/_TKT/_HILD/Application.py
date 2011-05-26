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
#    PMA.TKT.HILD.Application
#
# Purpose
#    Implement HILD-specific functionality of PMA
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
#    28-Jul-2005 (MG) `_setup_toplevel`: read of style file added
#    28-Jul-2005 (MG) `ask_*` function handling changed
#    10-Aug-2005 (CT) `show_menubar` and `show_toolbar` considered
#    12-Aug-2005 (MG) `TGL.TKT.GTK.Application` factored
#     2-Jan-2006 (CT) `context_menus` and `event_binders` added
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _TGL                 import TGL
from   _PMA                 import PMA
import _TGL._TKT
import _TGL._TKT._HILD
import _TGL._TKT._HILD.Application
import _PMA._TKT
import _PMA._TKT._HILD
import _TGL._TKT._HILD.import_GTK

class Application (TGL.TKT.HILD.Application) :
    """Main instance of HILD-based PMA"""

    widget_class          = "PMA"
    context_menus         = \
        ( "cm_bv", "cm_dv"
        , "cm_mv", "cm_md", "cm_mo"
        , "cm_status"
        )
    event_binders         = ("ev_bv", "ev_dv", "ev_mv", "ev_md")

    def _setup_geometry (self) :
        ### XXX
        self.__super._setup_geometry ()
        self.main.pack               (self.o_pane)
        self.body_r.pack_top         (self.wc_mb_msg_view)
        self.body_r.pack_bottom      (self.wc_msg_display)
        self.body_l.pack_top         (self.wc_po_box_view)
        self.body_l.pack_bottom      (self.wc_msg_outline)
        return
        limit = 60
        self.pane_mgr.lower_limit_pixl = self.min_y - limit
        self.pane_mgr.upper_limit_pixl = limit
        self.pane_mgr.divide (1)
    # end def _setup_geometry

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
    # end def _setup_panes

# end class Application

if __name__ != "__main__" :
    PMA.TKT.HILD._Export ("*")
### __END__ PMA.TKT.HILD.Application

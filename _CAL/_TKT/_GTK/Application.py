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
#    CAL.TKT.GTK.Application
#
# Purpose
#    Implement GTK-specific functionality of CAL
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    12-Aug-2005 (MG) `TGL.TKT.GTK.Application` factored
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _TGL                 import TGL
from   _CAL                 import CAL
import _TGL._TKT
import _TGL._TKT._GTK
import _TGL._TKT._GTK.Application
import _CAL._TKT
import _CAL._TKT._GTK
import _CAL._TKT._GTK.Day_Cell_Renderer

### XXX todo
### - Clipboard
### - Fileview Widget
### - pane: .divide, lower/upper limit
### - balloon for toolbar and application ???
### - dialogs ???

class Application (TGL.TKT.GTK.Application) :
    """Main instance of GTK-based CAL"""

    widget_class          = "CAL"
    context_menus         = ("cm", )

    def _setup_geometry (self) :
        ### XXX
        self.__super._setup_geometry ()
        self.main.pack               (self.o_pane)
        return
        limit = 60
        self.pane_mgr.lower_limit_pixl = self.min_y - limit
        self.pane_mgr.upper_limit_pixl = limit
        self.pane_mgr.divide (1)
    # end def _setup_geometry

    def _setup_panes (self) :
        TNS           = self.TNS
        AC            = self.AC
        self.main     = TNS.V_Box   (AC = AC)
        self.message  = self.AC.ui_state.message = TNS.Message_Window \
            (name = "status", AC = AC)
        self.wc_weeks_view   = TNS.Frame   (AC = AC)
        self.wc_day_view     = TNS.Frame   (AC = AC)
        self.wc_detail_view  = TNS.Frame   (AC = AC)
        self.day_detail_pane = ddp = TNS.V_Paned \
            (self.wc_day_view, self.wc_detail_view, name = "dd_pane", AC = AC)
        self.week_day_pane   = wdp = TNS.V_Paned \
            (self.wc_weeks_view, ddp, name = "wd_pane", AC = AC)
        self.o_pane          = TNS.V_Paned \
            (wdp, self.message, name = "panes",  AC = self.AC)
        for w in ( self.o_pane, wdp, ddp
                 , self.main
                 , self.wc_weeks_view,  self.wc_day_view
                 , self.wc_detail_view
                 , self.message
                 ) :
            w.show ()
    # end def _setup_panes

# end class Application

if __name__ != "__main__" :
    CAL.TKT.GTK._Export ("*")
### __END__ CAL.TKT.GTK.Application

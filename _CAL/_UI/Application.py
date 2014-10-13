# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.UI.Application
#
# Purpose
#    Application for CAL
#
# Revision Dates
#    17-Jun-2005 (MG) Creation
#    12-Aug-2005 (MG) `TGL.UI.Application` factored
#    12-Aug-2005 (MG) `_quit_finally` fixed
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _CAL                   import CAL

import _TFL.App_State

import _TGL._UI
import _TGL._UI.Application

import _CAL._UI
import _CAL._UI.HTD
import _CAL._UI.Mixin
import _CAL._UI.Week_View
import _CAL.Calendar
import _CAL.Date
import _CAL.Date_Time
import _CAL.Delta
import _CAL.Time
import _CAL.Year

class _App_State_ (TFL.App_State) :
    product_name = "CAL"
# end class _App_State_

class Application (TGL.UI.Application) :
    """Main instance of CAL application"""

    product_name         = "CAL"
    show_toolbar         = False
    
    Command_Groups       = \
        ( "_File_Cmd_Group"
        , "_Mbox_Cmd_Group"
        , "_Message_Cmd_Group"
        , "_Scripts_Cmd_Group"
        , "_Help_Cmd_Group"
        )

    def __init__ (self, AC, cmd, _globals = {}) :
        AC.memory         = _App_State_             (window_geometry = {})
        self.__super.__init__ (AC = AC, cmd = cmd, _globals = _globals)
    # end def __init__

    def commit_all (self, event = None) :
        """Commit all pending changes of mailboxes"""
        return True ### XXX
    # end def commit_all

    def _quit_finally (self) :
        pass ### XXX
    # end def _quit_finally

    def _setup_application (self) :
        self.calendar    = cal = self.ANS.Calendar ()
        today            = self.ANS.Date ()
        self.AC.memory.add (current_day  = today)
        self.week_view   = self.ANS.UI.Week_View (self, AC = self.AC)
        tkt              = self.tkt
        tkt.pack (tkt.wc_weeks_view, self.week_view.tkt)
        self.week_view.tkt.scroll_policies (h = self.TNS.NEVER)
        self.week_view.see (cal.year [today.year].weeks [today.week])
    # end def _setup_application

    def _window_title_text (self) :
        result = ["CAL: "]
        return "".join (result)
    # end def _window_title_text

# end class Application

if __name__ != "__main__" :
    CAL.UI._Export ("*")
### __END__ CAL.UI.Application

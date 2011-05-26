# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005-2007 Mag. Christian Tanzer. All rights reserved
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
#    PMA.UI.Application
#
# Purpose
#    Application for PMA
#
# Revision Dates
#    20-May-2005 (CT) Creation
#    21-May-2005 (MG) Allow `event` parameter for `commit_all`
#    21-May-2005 (MG) Interpreter added to menu and toolbar
#     7-Jun-2005 (MG) `_read_settings` added
#    10-Jun-2005 (MG) Use of `UI.Office` added
#    10-Jun-2005 (MG) Exception handler for the UI.Office creation added
#    11-Jun-2005 (MG) `_read_settings` removed and use `PMA.Office` instead
#    25-Jul-2005 (CT) `_quit` changed to call `office.save_status`
#    28-Jul-2005 (MG) `UI_State.__init__`: overwriting of status properties
#                     added, `Counting_Property` removed
#    28-Jul-2005 (MG) `s/Changes.changes/Changes.value/g`
#    28-Jul-2005 (MG) `Changes.__cmp__` and `Changes.__str__` added
#    28-Jul-2005 (CT) `_extend_status_props` and `_extend_status_prop` added
#    27-Jul-2005 (MG) `self.event_binders` added
#    27-Jul-2005 (MG) New command groups and commands added
#    28-Jul-2005 (MG) `File` menu removed, `_setup_*_menu` functions removed
#    10-Aug-2005 (CT) `show_menubar` and `show_toolbar` added
#    12-Aug-2005 (MG) `TGL.UI.Application` factored
#    12-Aug-2005 (MG) `_quit_finally` fixed
#    12-Aug-2005 (MG) `_window_title_text` fixed
#     2-Jan-2006 (CT) Additional `if_names` added to `_Mbox_Cmd_Group` and
#                     `_Message_Cmd_Group`
#     2-Jan-2006 (MG) `_window_title_text` changed
#     5-Jan-2006 (CT) Attribute `office` moved to `UI.Office`
#     5-Jan-2006 (CT) `_window_title_text` changed to guard against
#                     `AttributeError` (during startup, `office` isn't there
#                     yet)
#     7-Nov-2007 (CT) Use `Getter` instead of `lambda`
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _TGL                   import TGL
from   _PMA                   import PMA

import _TFL.Accessor
import _TFL.App_State
import _TFL.Record

import _TGL._UI
import _TGL._UI.Application

import _PMA._UI
import _PMA._UI.Command_Mgr
import _PMA._UI.HTD
import _PMA._UI.Message
import _PMA._UI.Msg_Display
import _PMA._UI.Mixin
import _PMA._UI.Office

class _App_State_ (TFL.App_State) :
    product_name = "PMA"
# end class _App_State_

class UI_State (TGL.UI.UI_State) :

    def __init__ (self, ** kw) :
        self.__super.__init__ (** kw)
        self._extend_status_props (self.changes)
    # end def __init__

    def _extend_status_props (self, changes) :
        ### define new properties for the status class to update the change
        ### counter of the application
        for cls, properties in \
            ( (PMA.Off_Status, ("current_box", "target_box"))
            , (PMA.Box_Status, ("current_message", ))
            ) :
            for name in properties :
                self._extend_status_prop (cls, name, changes)
    # end def _extend_status_props

    def _extend_status_prop (self, cls, name, changes) :
        prop       = getattr (cls, name)
        _old_set   = prop.fset
        def _set (obj, value) :
            result = _old_set (obj, value)
            changes.inc ()
            return result
        setattr \
            (cls, name, property (prop.fget, _set, prop.fdel, prop.__doc__))
    # end def _extend_status_prop

# end class UI_State

class Application (TGL.UI.Application) :
    """Main instance of PMA application"""

    office               = property (TFL.Getter.ui_office.office)

    product_name         = "PMA"
    show_menubar         = True
    show_toolbar         = True

    startup_cmds         = []
    _started_quit        = False
    ipreter              = None

    _Office_Cmd_Group    = TFL.Record \
        ( name           = "Office"
        , if_names       = ("mb", "tb")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the office"
        )
    _Mbox_Cmd_Group      = TFL.Record \
        ( name           = "Mailbox"
        , if_names       =
            ("mb", "tb", "cm_bv", "cm_dv", "cm_mv", "ev_bv", "ev_dv", "ev_mv")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the currently "
          "selected mailbox"
        )
    _Message_Cmd_Group   = TFL.Record \
        ( name           = "Message"
        , if_names       = ("mb", "tb", "cm_md", "cm_mv", "ev_mv", "ev_md")
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the currently "
          "selected message(s)"
        )
    _Msg_Part_Cmd_Group   = TFL.Record \
        ( name           = "Message-Part"
        , if_names       = ("mb", "cm_mo", )
        , batchable      = True
        , precondition   = None
        , description    =
          "This group provides commands for managing the currently "
          "selected message via the message outline display"
        )

    Command_Groups       = \
        ( "_Office_Cmd_Group"
        , "_Mbox_Cmd_Group"
        , "_Message_Cmd_Group"
        , "_Msg_Part_Cmd_Group"
        , "_Scripts_Cmd_Group"
        , "_Help_Cmd_Group"
        )

    def __init__ (self, AC, cmd, _globals = {}) :
        AC.memory = _App_State_ (window_geometry = {})
        self.__super.__init__ (AC = AC, cmd = cmd, _globals = _globals)
    # end def __init__

    def commit_all (self, event = None) :
        """Commit all pending changes of mailboxes"""
        ### XXX
        try :
            self.office.commit ()
            return True
        except :
            return False
    # end def commit_all

    def _quit_finally (self) :
        self.office.save_status ()
    # end def _quit_finally

    def _setup_application (self) :
        tkt              = self.tkt
        UI               = self.ANS.UI
        self.msg_display = md = UI.Message \
            ( AC         = self.AC
            , display_wc = tkt.wc_msg_display
            , outline_wc = tkt.wc_msg_outline
            )
        tkt.pack (tkt.wc_msg_display, md._display.tkt_text)
        tkt.pack (tkt.wc_msg_outline, md._outline.tkt_text)
        try :
            self.ui_office = UI.Office (self, AC = self.AC)
        except :
            import traceback
            traceback.print_exc ()
    # end def _setup_application

    def _window_title_text (self) :
        result = ["PMA: "]
        try :
            cb = self.office.status.current_box
        except AttributeError :
            pass
        else :
            if cb :
                result.append (cb.qname)
                result.append ("/")
                if cb.status.current_message :
                    result.append ("%d" % (cb.status.current_message.number, ))
        return "".join (result)
    # end def _window_title_text

# end class Application

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Application

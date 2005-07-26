# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@undefined.dontknow
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
#    PMA.UI.Office
#
# Purpose
#    Abstract user interface for office
#
# Revision Dates
#     8-Jun-2005 (MG) Creation
#    10-Jun-2005 (MG) Exception handler removed
#    10-Jun-2005 (MG) Message selection handling added
#    11-Jun-2005 (MG) `select_message`: Update of mailbox tree added
#    11-Jun-2005 (MG) Changed to use `PMA.Office`
#    25-Jul-2005 (CT) `select_folder` changed to call `msg_display.clear`
#    25-Jul-2005 (CT) `select_message` simplified
#    26-Jul-2005 (CT) `select_message` changed to set
#                     `mailbox.status.current_message`
#    26-Jul-2005 (CT) `select_folder` changed to set
#                     `office.status.current_box`
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Mailbox_BV
import _PMA._UI.Mailbox_MV
import _PMA.Office

class Office (PMA.UI.Mixin) :
    """Abstract user interface for PMA office."""

    def __init__ ( self, model, AC = None) :
        self.__super.__init__ (AC = AC)
        self.office            = office = model.office
        self.model             = model
        self.box_views         = {}
        self.delivery_views    = []
        self.storage_views     = []
        memory                 = self.AC
        memory.current_folder  = (None, ())
        memory.current_message = None
        UI                     = self.ANS.UI
        TNS                    = self.TNS
        for boxes, l in ( (office.storage_boxes,  self.storage_views)
                        , (office.delivery_boxes, self.delivery_views)
                        ) :
            for box in boxes :
                bv = UI.Mailbox_BV (AC = self.AC, show_header = False)
                bv.update_model    (box)
                l.append           (bv)
                self.box_views [box] = bv
        self.tkt = TNS.Office \
            (self.delivery_views, self.storage_views, AC = AC)
        self.mb_msg_view = mmv = UI.Mailbox_MV \
            (sort = True, AC = self.AC)
        mmv.tkt.scroll_policies (TNS.AUTOMATIC)
        tkt = model.tkt
        tkt.pack (tkt.wc_mb_msg_view, mmv.tkt)
        tkt.pack (tkt.wc_po_box_view, self.tkt)
        self._setup_bv_cmd_mgr (model)
        self._setup_mv_cmd_mgr (model)
    # end def __init__

    def select_folder (self, event = None) :
        tree    = event.widget
        memory  = self.AC
        old_tree, selection = memory.current_folder
        if old_tree and old_tree is not tree :
            old_tree.clear_selection ()
        folder                = tree.selection ()
        memory.current_folder = tree, folder
        self.office.status.current_box = folder [0]
        self.mb_msg_view.update_model (folder [0])
        self.model.msg_display.clear  ()
    # end def select_folder

    def select_message (self, event = None) :
        tree    = self.mb_msg_view
        message = (tree.selection () or (None, )) [0]
        memory  = self.AC
        if message and message is not memory.current_message :
            mailbox                = message.mailbox
            memory.current_message = mailbox.status.current_message = message
            self.model.msg_display.display       (message)
            self.mb_msg_view.update              (message)
            self.box_views [mailbox.root].update (mailbox)
    # end def select_message

    def _setup_bv_cmd_mgr (self, model) :
        AC          = self.AC
        UI          = self.ANS.UI
        TNS         = self.TNS
        tkt_trees   = [b.tkt for b in self.box_views.itervalues ()]
        interfacers = dict \
            ( cm = TNS.CI_Menu         (name = "context_menu", AC = AC)
            , ev = TNS.CI_Event_Binder (AC, * tkt_trees)
            )
        self.bv_cmd = UI.Command_Mgr \
            ( change_counter = model.changes
            , interfacers    = interfacers
            , if_names       = ("cm:click_3", )
            , AC             = AC
            )
        self.bv_cmd.add_command \
            ( UI.Command ("Select", self.select_folder)
            , if_names = ("cm", "ev:Cursor_Changed")
            )
        self.bv_cmd.bind_interfacers (* tkt_trees)
    # end def _setup_bv_cmd_mgr

    def _setup_mv_cmd_mgr (self, model) :
        AC          = self.AC
        UI          = self.ANS.UI
        TNS         = self.TNS
        interfacers = dict \
            ( cm = TNS.CI_Menu         (name = "context_menu", AC = AC)
            , ev = TNS.CI_Event_Binder (AC, self.mb_msg_view.tkt)
            )
        self.mv_cmd = UI.Command_Mgr \
            ( change_counter = model.changes
            , interfacers    = interfacers
            , if_names       = ("cm:click_3", )
            , AC             = AC
            )
        self.mv_cmd.add_command \
            ( UI.Command ("Select", self.select_message)
            , if_names = ("cm", "ev:Cursor_Changed")
            )
        self.mv_cmd.bind_interfacers (self.mb_msg_view.tkt)
    # end def _setup_bv_cmd_mgr

# end class Office

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Office



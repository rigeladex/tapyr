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
#    26-Jul-2005 (MG) `select_folder` and `select_message` changed
#    26-Jul-2005 (MG) `s/select_folder/select_box/g`
#    26-Jul-2005 (MG) Allow multiselection of messages
#    28-Jul-2005 (MG) New commands added
#    28-Jul-2005 (CT) s/next_unseen_message/next_unseen/
#    27-Jul-2005 (MG) Handling of commands changed (use command manager of
#                     main application instead of defining new command
#                     managers)
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
        UI                     = self.ANS.UI
        TNS                    = self.TNS
        AC                     = self.AC
        for boxes, views in ( (office.storage_boxes,  self.storage_views)
                            , (office.delivery_boxes, self.delivery_views)
                            ) :
            for box in boxes :
                box._ui_tree = bv = UI.Mailbox_BV \
                    (AC = AC, show_header = False, quick_search = False)
                bv.update_model    (box)
                views.append       (bv)
                self.box_views [box] = bv
        self.tkt = TNS.Office \
            (self.delivery_views, self.storage_views, AC = AC)
        self.mb_msg_view = mmv = UI.Mailbox_MV \
            ( sort           = True
            , multiselection = True
            , quick_search   = False
            , AC             = self.AC
            )
        mmv.tkt.scroll_policies (TNS.AUTOMATIC)
        tkt = model.tkt
        tkt.pack (tkt.wc_mb_msg_view, mmv.tkt)
        tkt.pack (tkt.wc_po_box_view, self.tkt)
        self._setup_common_cmds ()
        self._setup_bv_commands ()
        self._setup_mv_commands ()
    # end def __init__

    def select_box (self, event = None) :
        for tree in self.box_views.itervalues () :
            if tree.selection :
                break
        selection = tree.selection
        if not selection :
            ### ignore the callback if the slection has be canceled
            return
        box      = selection [0]
        curr_box = self.office.status.current_box
        if curr_box and curr_box.root != box.root :
           self.box_views [curr_box.root].selection = ()
        self.office.status.current_box = box
        self.mb_msg_view.update_model (box)
        if box.status.current_message :
            ### select and display the previous selected message
            self._select_message          (box.status.current_message)
        else :
            self.model.msg_display.clear  ()
    # end def select_box

    def show_message (self, event = None) :
        selection = self.mb_msg_view.selection
        if not selection or len (selection) > 1:
            ### clear message display in case of multi message selection or
            ### if no message is selected in this box
            self.model.msg_display.clear  ()
        else :
            ### display the selected message
            message = selection [0]
            mailbox = message.mailbox
            if mailbox.status.current_message != message :
                mailbox.status.current_message = message
                self._display_message (mailbox)
    # end def show_message

    def show_next_message (self, event = None) :
        """Show the next message of the current folder"""
        self._select_message (self.mb_msg_view.tkt._selection.next ())
    # end def show_next_message

    def show_prev_message (self, event = None) :
        """Show the previous message of the current folder"""
        self._select_message (self.mb_msg_view.tkt._selection.prev ())
    # end def show_prev_message

    def show_next_folder (self, event = None) :
        """Show the next folder"""
        print "N", event.widget
    # end def show_next_folder

    def show_prev_folder (self, event = None) :
        """Show the previous folder"""
        print "P", event.widget
    # end def show_prev_folder

    def show_next_unseen (self, event = None) :
        """Show the next unseen message."""
        print "Unseen"
    # end def show_next_unseen

    def _display_message (self, mailbox) :
        message = mailbox.status.current_message
        self.model.msg_display.display       (message)
        self.mb_msg_view.update              (message)
        self.box_views [mailbox.root].update (mailbox)
    # end def _display_message

    def _setup_bv_commands (self) :
        Cmd    = self.ANS.UI.Command
        grp    = self.model.cmd_mgr.cmd.Mailbox
        grp.add_command \
            ( Cmd ("Select", self.select_box)
            , if_names = ("cm_bv", "ev_bv:Select")
            )
        event_binder = grp.interfacers ["ev_bv"]
        cm           = grp.interfacers ["cm_bv"]
        for w in (b.tkt for b in self.box_views.itervalues ()) :
            cm.bind_to_widget       (w, "click_3")
            event_binder.add_widget (w)
    # end def _setup_bv_commands

    def _setup_common_cmds (self) :
        Cmd    = self.ANS.UI.Command
        cmd    = self.model.cmd_mgr.cmd
        for grp, cms, evb in ( (cmd.Office,  ("mb", "tb"),             ())
                             , (cmd.Mailbox, ("mb", "cm_mv", "cm_bv"), "ev_bv")
                             , (cmd.Message, ("mb", "cm_md", "cm_mv"), "ev_mv")
                             ) :
            add  = grp.add_command
            for name, callback, ev_name in \
                ( ( "Next Message",     self.show_next_message, "next_message")
                , ( "Previous Message", self.show_prev_message, "prev_message")
                , ( "Next Unseen",      self.show_next_unseen,  "next_unseen")
                ) :
                ev_bind = ()
                if evb :
                    ev_bind = ("%s:%s" % (evb, ev_name), )
                add (Cmd (name, callback), if_names = cms + ev_bind)
    # end def _setup_common_cmds

    def _setup_mv_commands (self) :
        Cmd    = self.ANS.UI.Command
        grp    = self.model.cmd_mgr.cmd.Message
        grp.add_command \
            (Cmd ("Select", self.show_message), if_names = ("ev_mv:Select", ))
        grp.interfacers ["cm_mv"].bind_to_widget (self.mb_msg_view, "click_3")
        grp.interfacers ["ev_mv"].add_widget     (self.mb_msg_view)
    # end def _setup_mv_commands

    def _select_message (self, msg) :
        if msg :
            box                        = msg.mailbox
            box.status.current_message = self.mb_msg_view.selection = msg
            self.mb_msg_view.see  (msg)
            self._display_message (box)
    # end def _select_message

# end class Office

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Office

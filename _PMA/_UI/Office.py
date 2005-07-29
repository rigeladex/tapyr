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
#    28-Jul-2005 (MG) `_setup_office_commands` added,
#                     `s/_setup_bv_cmmands/_setup_box_cmmands/g` and
#                     `s/_setup_mv_cmmands/_setup_msg_cmmands/g`
#    29-Jul-2005 (MG) Restoring of old selected box and message added
#    29-Jul-2005 (MG) Update of box views after adding/deleting of a sub box
#    29-Jul-2005 (MG) `_restore_selection`: allow restoration of a delivery
#                     box
#    29-Jul-2005 (MG) `new_message` changed and `_mail_sent` added
#    29-Jul-2005 (MG) Icons for commands added
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Mailbox_BV
import _PMA._UI.Mailbox_MV
import _PMA.Office
import _PMA.Composer
import _PMA.Sender

import _TFL.sos
import time

class Office (PMA.UI.Mixin) :
    """Abstract user interface for PMA office."""

    def __init__ ( self, model, AC = None) :
        self.__super.__init__ (AC = AC)
        self.office            = office = model.office
        self.model             = model
        self.box_views         = {}
        self.delivery_views    = []
        self.storage_views     = []
        ### XXX replace me, please (o;
        # execfile ("/home/lucky/PMA/.config.py", dict (PMA = PMA))
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
        self._setup_common_cmds     ()
        self._setup_office_commands ()
        self._setup_box_commands    ()
        self._setup_msg_commands    ()
        self._restore_selection     ()
    # end def __init__

    def delete_subbox (self, event = None) :
        """Delete the currently selected subbox and all messages in this
           subbox
        """
        cb     = self.office.status.current_box
        self.box_views [cb.root].remove (cb)
        self._delete_box (cb)
    # end def delete_subbox

    def _delete_box (self, box) :
        for sb in box.sub_boxes :
            self._delete_box (sb)
        parent = PMA.Mailbox.instance (TFL.sos.path.split (box.qname) [0])
        parent.delete_subbox (box)
    # end def _delete_box

    def new_message (self, event = None) :
        """Start the default editor with a new message and send this message
           after finishing of editing.
        """
        ANS  = self.ANS
        smtp = ANS.Sender     ()
        comp = ANS.Composer   (smtp = smtp, send_cb = self._mail_sent)
        comp.compose          ()
        time.sleep            (0.1)
        print "Starting editor for Send..."
    # end def new_message

    def _mail_sent (self, email) :
        receivers = set ()
        for kind in "to", "cc", "bcc" :
            recs = email [kind]
            if recs :
                for r in recs.split (",") :
                    receivers.add (r)
        time.sleep (0.1)
        print "Mail sent to %s" % (", ".join (receivers))
        time.sleep (0.1)
        return email
    # end def _mail_sent

    def new_subbox (self, event = None) :
        """Create a new subbox below the currently selected mailbox"""
        name = self.model.ask_string (title = "Add new subbox", prompt = "Name")
        if name :
            cb   = self.office.status.current_box
            box  = cb.add_subbox (name)
            self.box_views [cb.root].add (box, parent = cb)
    # end def new_subbox

    def select_box (self, event = None) :
        curr_box = self.office.status.current_box
        if event and isinstance (event.widget, self.TNS.Tree) :
            tree = event.widget
        else :
            if curr_box :
                tree = keyboard-quitself.box_views [curr_box.root]
            else :
                return
        selection = tree.selection
        if not selection :
            ### ignore the callback if the slection has be canceled
            return
        box      = selection [0]
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

    def show_next_unseen (self, event = None) :
        """Show the next unseen message."""
        print "Unseen N"
    # end def show_next_unseen

    def show_prev_unseen (self, event = None) :
        """Show the previous unseen message."""
        print "Unseen P"
    # end def show_prev_unseen

    def _display_message (self, mailbox) :
        message = mailbox.status.current_message
        self.model.msg_display.display       (message)
        self.mb_msg_view.update              (message)
        self.box_views [mailbox.root].update (mailbox)
    # end def _display_message

    def _restore_selection (self) :
        box   = self.office.status.current_box
        if box :
            name  = ""
            view  = self.box_views [box.root]
            for b_name in box.qname.split (TFL.sos.path.sep) :
                name = TFL.sos.path.join  (name, b_name)
                try :
                    box  = PMA.Mailbox.instance (name)
                    view.see                    (box)
                except KeyError :
                    ### ignore parts of the box path which don't have it's
                    ### own mailbox object
                    pass
            view.selection = box
    # end def _restore_selection

    def _setup_box_commands (self) :
        Cmd     = self.ANS.UI.Deaf_Command
        grp     = self.model.cmd_mgr.cmd.Mailbox
        add_cmd = grp.add_command
        add_sep = grp.add_separator
        add_cmd \
            ( self.ANS.UI.Command
               ("Select", self.select_box), if_names = ("ev_bv:Select", )
            )
        add_sep (if_names = ("cm_bv", "mb"))
        add_cmd \
            ( Cmd ("New Subbox", self.new_subbox)
            , if_names = ("cm_bv", "mb")
            )
        add_cmd \
            ( Cmd ("Delete Subbox", self.delete_subbox)
            , if_names = ("cm_bv", "mb")
            )
        event_binder = grp.interfacers ["ev_bv"]
        cm           = grp.interfacers ["cm_bv"]
        for w in (b.tkt for b in self.box_views.itervalues ()) :
            cm.bind_to_widget       (w, "click_3")
            event_binder.add_widget (w)
    # end def _setup_box_commands

    def _setup_common_cmds (self) :
        Cmd    = self.ANS.UI.Command
        cmd    = self.model.cmd_mgr.cmd
        for grp, cms, evb in ( (cmd.Office,  ("mb", "tb"),             ())
                             , (cmd.Mailbox, ("mb", "cm_mv", "cm_bv"), "ev_bv")
                             , (cmd.Message, ("mb", "cm_md", "cm_mv"), "ev_mv")
                             ) :
            add  = grp.add_command
            for name, callback, ev_name, icon in \
                ( ( "Previous Message", self.show_prev_message
                  , "prev_message", "gtk-media-previous"
                  )
                , ( "Next Message",     self.show_next_message
                  , "next_message", "gtk-media-next"
                  )
                , ( "Previous Unseen",  self.show_prev_unseen
                  ,  "prev_unseen", "gtk-media-rewind"
                  )
                , ( "Next Unseen",      self.show_next_unseen
                  , "next_unseen", "gtk-media-forward"
                  )
                ) :
                ev_bind = ()
                if evb :
                    ev_bind = ("%s:%s" % (evb, ev_name), )
                add ( Cmd (name, callback)
                    , if_names = cms + ev_bind
                    , icon = icon
                    )
    # end def _setup_common_cmds

    def _setup_msg_commands (self) :
        Cmd    = self.ANS.UI.Command
        grp    = self.model.cmd_mgr.cmd.Message
        grp.add_command \
            (Cmd ("Select", self.show_message), if_names = ("ev_mv:Select", ))
        grp.interfacers ["cm_mv"].bind_to_widget (self.mb_msg_view, "click_3")
        grp.interfacers ["ev_mv"].add_widget     (self.mb_msg_view)
    # end def _setup_msg_commands

    def _setup_office_commands (self) :
        UI     = self.ANS.UI
        Cmd    = UI.Command
        grp    = self.model.cmd_mgr.cmd.Office
        grp.add_separator (if_names = ("mb", ))
        grp.add_command \
            ( Cmd ("New Message", self.new_message)
            , if_names = ("mb", "tb"), icon = "gtk-new"
            )
        grp.add_separator (if_names = ("mb", ))
        grp.add_command \
            ( UI.Deaf_Command ("Commit and exit", self.model.exit)
            , if_names    = ("mb", )
            , underline   = 0
            , icon        = "gtk-quit"
            , accelerator = self.TNS.Eventname.save_and_exit
            )
        grp.add_command \
            ( UI.Deaf_Command ("Exit", self.model.quit)
            , if_names    = ("mb", )
            , underline   = 1
            , accelerator = self.TNS.Eventname.exit
            )
    # end def _setup_office_commands

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

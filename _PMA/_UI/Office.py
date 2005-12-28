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
#    30-Jul-2005 (MG) New commands
#    30-Jul-2005 (MG) `Command_Definition` added and used (for all commands)
#    30-Jul-2005 (MG) New commands (continued)
#    31-Jul-2005 (CT) `set_target_mailbox` protected against undefined
#                     `status.current_box`
#    31-Jul-2005 (CT) `_message_command` protected against undefined
#                     `target_box`
#    31-Jul-2005 (MG) Commands changes/added
#    31-Jul-2005 (MG) Commands changes/added
#     1-Aug-2005 (MG) `_commit` clear the selection bofore the commit
#                     (objects which are selected could be removed)
#     1-Aug-2005 (MG) `select_box`: only `change` the box if a new box has
#                     been selected
#    12-Aug-2005 (MG) Calls to `set_title` added
#    13-Aug-2005 (MG) `Command_Definition` factored
#    14-Aug-2005 (MG) `_setup_commands` replaced by `command_bindings`
#    16-Sep-2005 (MG) Change to use new `Msg_Scope` object provided by
#                     `mb_msg_view`
#    28-Dec-2005 (CT) `_message_command` fixed (pass `msg_scope` instead of
#                     `msg` to `view.update`)
#    28-Dec-2005 (CT) Output format of `_message_command` and `_commit` changed
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Command_Definition
import _PMA._UI.Mailbox_BV
import _PMA._UI.Mailbox_MV
import _PMA.Office
import _PMA.Composer
import _PMA.Sender

import _TFL.sos
import time

class Office (PMA.UI.Mixin, PMA.UI.Command_Definition_Mixin) :
    """Abstract user interface for PMA office."""

    CD = PMA.UI.Command_Definition

    ### command definition
    box_view_widgets        = property \
        (lambda s : [b.tkt for b in s.box_views.itervalues ()])
    command_bindings        = dict \
        ( mb_msg_view       = dict
            ( context_menu  = "Message.cm_mv"
            , event_binder  = "Message.ev_mv"
            )
        , box_view_widgets  = dict
            ( context_menu  = "Mailbox.cm_bv"
            , event_binder  = "Mailbox.ev_bv"
            )
        )
    box_cmd_grps     = (CD.Group ("Mailbox", ("mb", "cm_bv"), "ev_bv"), )
    msg_cmd_grps     = (CD.Group ("Message", ("mb", "cm_mv"), "ev_mv"), )
    off_cmd_grps     = (CD.Group ("Office",  ("mb", "tb")), )
    box_msg_cmd_grps = \
        ( CD.Group ("Mailbox", ("mb", "tb", "cm_bv"), "ev_bv")
        , CD.Group ("Message", "cm_mv",               "ev_mv")
        )

    deaf_commands = \
        ( ### mailbox/message commands
          CD ( "Previous Message", "show_prev_message"
             , eventname = "prev_message"
             , icon      = "gtk-media-previous"
             , * box_msg_cmd_grps
             )
        , CD ( "Next Message",     "show_next_message"
             , eventname = "next_message"
             , icon      = "gtk-media-next"
             , * box_msg_cmd_grps
             )
        , CD ( "Previous Unseen",  "show_prev_unseen"
             , eventname = "prev_unseen"
             , icon      = "gtk-media-rewind"
             , * box_msg_cmd_grps
             )
        , CD ( "Next Unseen",      "show_next_unseen"
             , eventname = "next_unseen"
             , icon      = "gtk-media-forward"
             , * box_msg_cmd_grps
             )
          ### mailbox commands
        , PMA.UI.Separator (* box_cmd_grps)
        , CD ( "Commit", "commit_box"
             , eventname = "commit_box"
             , * box_cmd_grps
             )
        , CD ( "Delete Message", "delete_message"
             , CD.Group ("Mailbox", "cm_bv", "ev_bv")
             , eventname = "delete_message"
             , icon      = "gtk-delete"
             )
        , PMA.UI.Separator (* box_cmd_grps)
        , CD ( "New Subbox",         "new_subbox"
             , * box_cmd_grps
             )
        , CD ( "Delete Subbox",      "delete_subbox"
             , * box_cmd_grps
             )
        , CD ( "Set target mailbox", "set_target_mailbox"
             , * box_cmd_grps
             )

          ### message commands
        , PMA.UI.Separator (CD.Group ("Message", "cm_mv"))
        , CD ( "Reply",          "reply"
             , eventname = "reply"
             , underline = 0
             , * msg_cmd_grps
             )
        , CD ( "Reply All",          "reply_all"
             , eventname = "reply_all"
             , underline = 6
             , * msg_cmd_grps
             )
        , CD ( "Forward Message", "forward_message"
             , eventname = "forward_message"
             , * msg_cmd_grps
             )
        , CD ( "Resend Message", "resend_message"
             , eventname = "resend_message"
             , underline = 2
             , * msg_cmd_grps
             )
        , PMA.UI.Separator (CD.Group ("Message", ("cm_mv", "mb")))
        , CD ( "Copy to subbox", "copy_message"
             , eventname = "copy_message"
             , icon      = "gtk-copy"
             , * msg_cmd_grps
             )
        , CD ( "Move to subbox", "move_message"
             , eventname = "move_message"
             , icon      = "gtk-cut"
             , * msg_cmd_grps
             )
        , CD ( "Delete",         "delete_message"
             , eventname = "delete_message"
             , icon      = "gtk-delete"
             , * msg_cmd_grps
             )
        , CD ( "Commit",         "commit_message"
             , eventname = "commit_message"
             , icon      = "gtk-apply"
             , * msg_cmd_grps
             )
        , CD ( "Unmark",         "unmark_message"
             , eventname = "unmark_message"
             , icon      = "gtk-cancel"
             , * msg_cmd_grps
             )
        , PMA.UI.Separator (CD.Group ("Message", ("cm_mv", "mb")))
        , CD ( "Select All",     "select_all_messages"
             , eventname = "select_all"
             , * msg_cmd_grps
             )
        , CD ( "Commit All",     "commit_box"
             , eventname = "commit_box"
             , * msg_cmd_grps
             )
          ### office  commands
        , CD ( "New Message", "new_message"
             , icon = "gtk-new"
             ,  * off_cmd_grps
             )
        , PMA.UI.Separator (* off_cmd_grps)
        , CD ( "Commit and exit", "model_exit"
             , CD.Group ("Office", ("mb", "tb"))
             , accelerator = "save_and_exit"
             , icon        = "gtk-quit"
             , underline   = 0
             )
        , CD ( "Exit", "model_quit"
             , CD.Group ("Office", "mb")
             , accelerator = "exit"
             , underline   = 1
             )
        )

    commands = \
        ( ### mailbox commands
          CD ( "Select", "select_box"
             , CD.Group ("Mailbox", ev = "ev_bv")
             , eventname = "Select"
             )
        , CD ( "Select", "show_message"
             , CD.Group ("Message", ev = "ev_mv")
             , eventname = "Select"
             )
        )

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
                    ( AC = AC, show_header = False, quick_search = False
                    , adapter_kw = dict (office = self.office)
                    )
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
        self._setup_commands    (self.model.cmd_mgr)
        self._restore_selection ()
    # end def __init__

    def copy_message (self, event = None) :
        """Copy the currently selected message to the default target
           mailbox.
        """
        self._message_command \
            ( "copy"
            , "Mark `%(cb_qname)s` for %(cmd)s to mailbox `%(tb_qname)s`:"
            , self.office.status.target_box
            )
    # end def copy_message

    def commit_box (self, event = None) :
        """Commit all pending actions of the currently selected box."""
        box = self.office.status.current_box
        self._commit (m for m in box.messages if m.pending)
    # end def commit_box

    def commit_message (self, event = None) :
        """Commit all pending changes of the currently selected message."""
        self._commit \
            ((self.office.status.current_box.status.current_message, ))
    # end def commit_message

    def _commit (self, messages) :
        boxes    = set ()
        text     = []
        view     = self.mb_msg_view
        self.mb_msg_view.selection = ()
        for msg in messages :
            text.append (str (msg.number))
            update = True
            if msg.pending.deleted or msg.pending.moved :
                update = False
                view.remove (msg.scope)
            boxes.update    (msg.pending.commit ())
            if update :
                view.update (msg.scope)
        for box in boxes :
            self.box_views [box.root].update (box)
        print "Commit `%s`: %s" % (msg.mailbox.qname, ", ".join (text))
    # end def _commit

    def delete_message (self, event = None) :
        """Delete the currently selected message from this mailbox."""
        self._message_command \
            ( "delete"
            , "Mark `%(cb_qname)s` for %(cmd)s:"
            , self.office.status.current_box
            )
    # end def delete_message

    def move_message (self, event = None) :
        """Move the currently selected message from teh current mailbox into
           the default target mailbox."""
        self._message_command \
            ( "move"
            , "Mark `%(cb_qname)s` for %(cmd)s to mailbox `%(tb_qname)s`:"
            , self.office.status.current_box
            , self.office.status.target_box
            )
    # end def move_message

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

    def forward_message (self, event = None) :
        """Forward the selected message."""
        msg  = self.office.status.current_box.status.current_message
        self._mail_compose \
            ( "forward"
            , "Start editor for forwarding the message `%s`"
            % (msg.scope.subject [:30])
            , msg
            )
    # end def forward_message

    def new_message (self, event = None) :
        """Start the default editor with a new message and send this message
           after finishing of editing.
        """
        self._mail_compose ("compose", "Starting editor with a new message...")
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

    def reply (self, event = None) :
        """Reply to the selected message."""
        msg  = self.office.status.current_box.status.current_message
        self._mail_compose \
            ( "reply"
            , "Start editor for a reply to message `%s`"
              % (msg.scope.subject [:30])
            , msg
            )
    # end def reply

    def reply_all (self, event = None) :
        """Reply to the selected message."""
        msg  = self.office.status.current_box.status.current_message
        self._mail_compose \
            ( "reply_all"
            , "Start editor for a reply all to message `%s`"
            % (msg.scope.subject [:30])
            , msg
            )
    # end def reply_all

    def resend_message (self, event = None) :
        """Resend the selected message."""
        msg  = self.office.status.current_box.status.current_message
        self._mail_compose \
            ( "resend"
            , "Start editor for resending the message `%s`"
            % (msg.scope.subject [:30])
            , msg
            )
    # end def resend_message

    def _mail_compose (self, cmd, text, * args) :
        ANS    = self.ANS
        smtp   = ANS.Sender     ()
        comp   = ANS.Composer   (smtp = smtp, send_cb = self._mail_sent)
        result = getattr        (comp, cmd) (* args)
        time.sleep (0.1)
        print text
        time.sleep (0.1)
        return result
    # end def _mail_compose

    def select_all_messages (self, event = None) :
        """Select all message of the current mailbox."""
        self.mb_msg_view.selection.all ()
    # end def select_all_messages

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
        if self.office.status.current_box != box :
            self.office.status.current_box = box
            self.mb_msg_view.update_model (box)
            if box.status.current_message :
                ### select and display the previous selected message
                self._select_message         (box.status.current_message)
            else :
                self.model.msg_display.clear ()
            self.model.set_title             ()
    # end def select_box

    def set_target_mailbox (self, event = None) :
        """Set the currently selected mailbox as target mailbox for copy and
           move operations.
        """
        status            = self.office.status
        old               = status.target_box
        status.target_box = status.current_box
        for box in old, status.current_box :
            if box is not None :
                self.box_views [box.root].update (box)
    # end def set_target_mailbox

    def show_message (self, event = None) :
        selection = self.mb_msg_view.selection
        if not selection or len (selection) > 1:
            ### clear message display in case of multi message selection or
            ### if no message is selected in this box
            self.model.msg_display.clear  ()
        else :
            ### display the selected message
            scope   = selection [0]
            message = scope.msg
            mailbox = message.mailbox
            if mailbox.status.current_message != message :
                mailbox.status.current_message = message
                self._display_message (mailbox)
        self.model.set_title          ()
    # end def show_message

    def show_next_message (self, event = None) :
        """Show the next message of the current folder"""
        self._select_message (scope = self.mb_msg_view.next ())
    # end def show_next_message

    def show_prev_message (self, event = None) :
        """Show the previous message of the current folder"""
        self._select_message (scope = self.mb_msg_view.prev ())
    # end def show_prev_message

    def show_next_unseen (self, event = None) :
        """Show the next unseen message."""
        print "Unseen N"
    # end def show_next_unseen

    def show_prev_unseen (self, event = None) :
        """Show the previous unseen message."""
        print "Unseen P"
    # end def show_prev_unseen

    def _message_command (self, cmd, text, * args) :
        status   = self.office.status
        view     = self.mb_msg_view
        scopes   = self.mb_msg_view.selection
        if not len (scopes) : ### XXX add __nonzero__ to scopes.__class__ to
                              ### avoid the need for `len`
            scopes = (status.current_box.status.current_message.scope, )
        if scopes :
            print text % dict \
                    ( cb_qname = status.current_box.qname
                    , cmd      = cmd
                    , tb_qname = getattr (status.target_box, "qname", "")
                    ),
            for msg_scope in scopes :
                msg    = msg_scope.msg
                result = getattr (msg.pending, cmd) (* args)
                print msg_scope.number,
                view.update  (msg_scope)
            print
        next = view.next ()
        if next :
            view.see               (next)
            view.selection = next
        return result
    # end def _message_command

    def model_exit (self, * args, ** kw) :
        return self.model.exit (* args, ** kw)
    # end def model_exit

    def model_quit (self, * args, ** kw) :
        return self.model.quit (* args, ** kw)
    # end def model_quit

    def unmark_message (self, event = None) :
        """Reset all pending actions for the selected message."""
        self._message_command ("reset", "Unmark `%(cb_qname)s`:")
    # end def unmark_message

    def _display_message (self, mailbox) :
        message = mailbox.status.current_message
        self.model.msg_display.display       (message)
        self.mb_msg_view.update              (message.scope)
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

    def _select_message (self, msg = None, scope = None) :
        if msg or scope :
            msg   = msg   or scope.msg
            scope = scope or msg.scope
            box                        = msg.mailbox
            box.status.current_message = msg
            self.mb_msg_view.selection = scope
            self.mb_msg_view.see  (scope)
            self._display_message (box)
    # end def _select_message

# end class Office

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Office

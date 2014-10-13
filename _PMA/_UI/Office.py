# -*- coding: utf-8 -*-
# Copyright (C) 2005-2014 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@undefined.dontknow
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    28-Dec-2005 (MG) `select_box`: new parameter `force` added
#    28-Dec-2005 (MG) `_restore_selection` fixed
#     1-Jan-2006 (MG) Delivery box view changed (use new V_Mailbox and
#                     Mbx_Filter)
#     2-Jan-2006 (CT) `Sync` command added
#     2-Jan-2006 (CT) `box_cmd_grps` split into `sbx_cmd_grps` and
#                     `dbx_cmd_grps`
#     2-Jan-2006 (CT) `_create_delivery_view` changed to use
#                     `office.dbx_matchers`
#     2-Jan-2006 (MG) `sync_box` finished
#     3-Jan-2006 (MG) `sync_box` update of delivery box view and status
#                     message added
#    03-Jan-2006 (MG) `box_views` contains now a list of views for a mailbox
#    03-Jan-2006 (MG) `_create_delivery_view` Add all sub boxes of the
#                     delivery  box into the`box_views` dict
#    03-Jan-2006 (MG) `ask_passwd` added
#     5-Jan-2006 (CT) `PMA.office` instantiated here (after setting up
#                     `POP3_Mailbox.passwd_cb`)
#     5-Jan-2006 (CT) SB-related commands (`train_ham`, etc.) added
#     5-Jan-2006 (CT) `_message_command` split into `_message_command` and
#                     `_message_command_n`
#     5-Jan-2006 (CT) Failed to make `next_unseen` and `prev_unseen` work
#     5-Jan-2006 (CT) `_display_message` changed to `push_help` of
#                     `str (msg.pending)`
#    09-Jan-2006 (MG) `PMA.UI.Mailbox_MV` uses message objects as `UI`
#                     objects again
#    09-Jan-2006 (MG) Unseen commands implemented
#    24-Jan-2006 (MG) Methods alphabetical ordered
#    24-Jan-2006 (MG) Started to rewrite using new `PMA.V_Mailbox` features
#    26-Jan-2006 (MG) Update after `sync` command implemented
#    ««revision-date»»···
#--

from   __future__              import print_function

from   _TFL                    import TFL
from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Command_Definition
import _PMA._UI.Mailbox_BV
import _PMA._UI.Mailbox_MV
import _PMA._UI.Mailbox_DBV
import _PMA.Composer
import _PMA.Filter_Mailbox
import _PMA.Matcher
import _PMA.Office
import _PMA.POP3_Mailbox
import _PMA.Pop3_Maildir
import _PMA.Sender
import _PMA.V_Mailbox
import _PMA._SCM.Mailbox

import _TFL.sos
import  time

def update_mailbox_msg_view (self, mailbox, view) :
    for msg in self.messages_from_box (mailbox) :
        view.add (msg)
PMA.SCM.Add_Messages.update_mailbox_msg_view = update_mailbox_msg_view

class Office (PMA.UI.Mixin, PMA.UI.Command_Definition_Mixin) :
    """Abstract user interface for PMA office."""

    CD = PMA.UI.Command_Definition

    ### command definition
    command_bindings        = dict \
        ( mb_msg_view       = dict
            ( context_menu  = "Message.cm_mv"
            , event_binder  = "Message.ev_mv"
            )
        , storage_views     = dict
            ( context_menu  = "Mailbox.cm_bv"
            , event_binder  = "Mailbox.ev_bv"
            )
        , delivery_view     = dict
            ( context_menu  = "Mailbox.cm_dv"
            , event_binder  = "Mailbox.ev_dv"
            )
        )
    sbx_cmd_grps     = (CD.Group ("Mailbox", ("mb", "cm_bv"), "ev_bv"), )
    dbx_cmd_grps     = (CD.Group ("Mailbox", ("mb", "cm_dv"), "ev_dv"), )
    msg_cmd_grps     = (CD.Group ("Message", ("mb", "cm_mv"), "ev_mv"), )
    off_cmd_grps     = (CD.Group ("Office",  ("mb", "tb")), )
    box_cmd_grps     = \
        ( CD.Group ("Mailbox", ("mb", "cm_bv"), "ev_bv")
        , CD.Group ("Mailbox", "cm_dv",         "ev_dv")
        )
    box_msg_cmd_grps = \
        ( CD.Group ("Mailbox", ("mb", "tb", "cm_bv"), "ev_bv")
        , CD.Group ("Mailbox", "cm_dv",               "ev_dv")
        , CD.Group ("Message", "cm_mv",               "ev_mv")
        )

    deaf_commands    = \
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
          ### delivery mailbox commands
        , CD ( "Sync", "sync_box"
             , eventname = "sync_box"
             , * dbx_cmd_grps
             )
          ### storage mailbox commands
        , PMA.UI.Separator (* sbx_cmd_grps)
        , CD ( "New Subbox",         "new_subbox"
             , * sbx_cmd_grps
             )
        , CD ( "Delete Subbox",      "delete_subbox"
             , * sbx_cmd_grps
             )
        , CD ( "Set target mailbox", "set_target_mailbox"
             , * sbx_cmd_grps
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
        , CD ( "Copy to box", "copy_message"
             , eventname = "copy_message"
             , icon      = "gtk-copy"
             , * msg_cmd_grps
             )
        , CD ( "Move to box", "move_message"
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
        , CD ( "Train ham", "train_ham"
             , eventname = "train_ham"
             # icon      = ???
             , * msg_cmd_grps
             )
        , CD ( "Un-Train ham", "untrain_ham"
             # icon      = ???
             , * msg_cmd_grps
             )
        , CD ( "Train spam", "train_spam"
             , eventname = "train_spam"
             # icon      = ???
             , * msg_cmd_grps
             )
        , CD ( "Un-Train spam", "untrain_spam"
             # icon      = ???
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
             , CD.Group ("Mailbox", ev = ("ev_bv", "ev_dv"))
             , eventname = "Select"
             )
        , CD ( "Select", "show_message"
             , CD.Group ("Message", ev = "ev_mv")
             , eventname = "Select"
             )
        )

    def __init__ ( self, model, AC = None) :
        self.__super.__init__ (AC = AC)
        ### set the passwd_cb as soon as possible
        PMA.POP3_Mailbox.passwd_cb = PMA.Pop3_Maildir.passwd_cb \
                               = lambda s : self.ask_passwd (s)
        self.office            = office = self.ANS.Office ()
        self.model             = model
        self.box_views         = {} ### XXX still required ???
        self.storage_views     = []
        self.delivery_box      = self.ANS.V_Mailbox \
            ("inbox", office.delivery_boxes)
        UI                     = self.ANS.UI
        TNS                    = self.TNS
        AC                     = self.AC
        for box in office.storage_boxes :
            box._ui_tree = bv = UI.Mailbox_BV \
                ( AC = AC, show_header = False, quick_search = False
                , adapter_kw = dict (office = self.office)
                )
            bv.update_model           (box)
            self.storage_views.append (bv)
            self.box_views [box] = bv
        self.mb_msg_view = mmv = UI.Mailbox_MV \
            ( sort           = True
            , multiselection = True
            , quick_search   = False
            , AC             = self.AC
            )
        mmv.tkt.scroll_policies (TNS.AUTOMATIC)
        self._create_delivery_view (mmv)
        self.tkt = TNS.Office (self.delivery_view, self.storage_views, AC = AC)
        tkt      = model.tkt
        tkt.pack                (tkt.wc_mb_msg_view, mmv.tkt)
        tkt.pack                (tkt.wc_po_box_view, self.tkt)
        self._setup_commands    (self.model.cmd_mgr)
        self._restore_selection ()
    # end def __init__

    def ask_passwd (self, mailbox) :
        return self.model.ask_invisible_string \
            ( title  = "Password for mailbox"
            , prompt = "For user `%s` on `%s:%s`"
                     % (mailbox.user, mailbox.host, mailbox.port)
            )
    # end def ask_passwd

    def commit_box (self, event = None) :
        """Commit all pending actions of the selected box."""
        box = self.office.status.current_box
        if box :
            self._update_commit_action (box.commit_all (transitive = True))
    # end def commit_box

    def commit_message (self, event = None) :
        """Commit pending changes of the selected message."""
        msg = self.office.status.current_box.status.current_message
        if msg :
            view   = self.mb_msg_view
            box    = getattr (msg, "v_mailbox", msg.mailbox)
            delete = msg.pending.deleted or msg.pending.moved
            self.mb_msg_view.selection = ()
            msg.pending.commit           ()
            self._update_commit_action   ((msg, ))
    # end def commit_message

    def copy_message (self, event = None) :
        """Copy the currently selected message(s) to the default target
           mailbox.
        """
        self._message_command_n \
            ( "copy"
            , "Mark `%(cb_qname)s` for %(cmd)s to mailbox `%(tb_qname)s`:"
            , self.office.status.target_box
            )
    # end def copy_message

    def delete_message (self, event = None) :
        """Delete the currently selected message(s) from this mailbox."""
        self._message_command_n \
            ( "delete"
            , "Mark `%(cb_qname)s` for %(cmd)s:"
            )
    # end def delete_message

    def delete_subbox (self, event = None) :
        """Delete the currently selected subbox and all messages in this
           subbox
        """
        cb = self.office.status.current_box
        try :
            self._delete_box (cb)
            self.box_views [cb.root].remove (cb)
        except OSError :
            self.model.show_error \
                (title = "Error", message = "Cannot delete subbox")
    # end def delete_subbox

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

    def model_exit (self, * args, ** kw) :
        dbox = self.delivery_box
        dbox.save_status ()
        for box in self.office.sub_boxes (dbox, transitive = True) :
            box.save_status ()
        return self.model.exit (* args, ** kw)
    # end def model_exit

    def model_quit (self, * args, ** kw) :
        return self.model.quit (* args, ** kw)
    # end def model_quit

    def move_message (self, event = None) :
        """Move the currently selected message(s) from the current mailbox into
           the default target mailbox.
        """
        self._message_command_n \
            ( "move"
            , "Mark `%(cb_qname)s` for %(cmd)s to mailbox `%(tb_qname)s`:"
            , self.office.status.target_box
            )
    # end def move_message

    def new_message (self, event = None) :
        """Start the default editor with a new message and send this message
           after finishing of editing.
        """
        self._mail_compose ("compose", "Starting editor with a new message...")
    # end def new_message

    def new_subbox (self, event = None) :
        """Create a new subbox below the currently selected mailbox."""
        name = self.model.ask_string \
            (title = "Add new subbox", prompt = "Name")
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

    def sync_box (self, event = None) :
        """Synchronizes selected the mailbox"""
        box = self.office.status.current_box
        if box :
            box.root.add_messages (* box.sync ())
            ### update of the UI is handled via the change counter callbacks
    # end def sync_box

    def select_all_messages (self, event = None) :
        """Select all message of the current mailbox."""
        self.mb_msg_view.selection.all ()
    # end def select_all_messages

    def select_box (self, event = None, force = False) :
        curr_box = self.office.status.current_box
        if event and isinstance (event.widget, self.TNS.Tree) :
            tree = event.widget
        else :
            if curr_box :
                tree = self.box_views [curr_box.root]
            else :
                return
        selection = tree.selection
        if not selection :
            ### ignore the callback if the selection has been canceled
            return
        box = selection [0]
        if curr_box and curr_box.root != box.root :
            self.box_views [curr_box.root].selection = ()
        if force or self.office.status.current_box != box :
            self.office.status.current_box.deregister_change_observer \
                (self._update_mailbox_msg_view)
            self.office.status.current_box = box
            self.mb_msg_view.update_model (box)
            if box.status.current_message :
                ### select and display the previous selected message
                self._select_message         (box.status.current_message)
            else :
                self.model.msg_display.clear ()
            self.model.set_title             ()
            box.register_change_observer     (self._update_mailbox_msg_view)
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
            message = selection [0]
            mailbox = getattr (message, "v_mailbox", message.mailbox)
            if mailbox.status.current_message != message :
                mailbox.status.current_message = message
                self._display_message (mailbox)
        self.model.set_title          ()
    # end def show_message

    def show_next_message (self, event = None) :
        """Show the next message of the current folder"""
        self._select_message (msg = self.mb_msg_view.next ())
    # end def show_next_message

    def show_prev_message (self, event = None) :
        """Show the previous message of the current folder"""
        self._select_message (msg = self.mb_msg_view.prev ())
    # end def show_prev_message

    def show_next_unseen (self, event = None) :
        """Show the next unseen message."""
        if not self._show_unseen ("next") :
            pass ### select next message in next folder
    # end def show_next_unseen

    def show_prev_unseen (self, event = None) :
        """Show the previous unseen message."""
        if not self._show_unseen ("prev") :
            pass ### select prev message in prev folder
    # end def show_prev_unseen

    def train_ham (self, event = None) :
        """Train the currently selected message(s) as ham."""
        self._message_command_n \
            ( "train_ham"
            , "Train as ham `%(cb_qname)s`:"
            )
    # end def train_ham

    def train_spam (self, event = None) :
        """Train the currently selected message(s) as spam."""
        self._message_command \
            ( "train_spam"
            , "Train as spam `%(cb_qname)s`:"
            )
        self.delete_message (event)
    # end def train_spam

    def unmark_message (self, event = None) :
        """Reset all pending actions for the selected message."""
        self._message_command_n ("reset", "Unmark `%(cb_qname)s`:")
    # end def unmark_message

    def untrain_ham (self, event = None) :
        """Un-Train the currently selected message(s) as ham."""
        self._message_command_n \
            ( "untrain_ham"
            , "Un-Train as ham `%(cb_qname)s`:"
            )
    # end def untrain_ham

    def untrain_spam (self, event = None) :
        """Un-Train the currently selected message(s) as spam."""
        self._message_command_n \
            ( "untrain_spam"
            , "Un-Train as spam `%(cb_qname)s`:"
            )
    # end def untrain_spam

    def _commit (self, messages) :
        boxes    = set ()
        text     = []
        view     = self.mb_msg_view
        if messages :
            self.mb_msg_view.selection = ()
            for msg in messages :
                text.append (str (msg.number))
                update = True
                if msg.pending.deleted or msg.pending.moved :
                    update = False
                    view.remove (msg)
                boxes.update    (msg.pending.commit ())
                if update :
                    view.update (msg)
            for box in boxes :
                try :
                    self.box_views [box.root].update (box)
                except Exception as exc :
                    print \
                        ( "*** PMA.UI.Office._commit:"
                        , exc.__class__.__name__, exc
                        )
            print ("Commit `%s`: %s" % (msg.mailbox.qname, ", ".join (text)))
    # end def _commit

    def _create_delivery_view (self, mbx_msg_view) :
        AC           = self.AC
        db           = self.delivery_box
        dbx_matchers = self.office.dbx_matchers
        rest_matcher = PMA.Not_Matcher \
            ( PMA.Or_Matcher (* (m for (n, m) in dbx_matchers)))
        for name, matcher in (("INBOX", rest_matcher),) + dbx_matchers :
            self.delivery_box.add_filter_mailbox (name, matcher)
        self.delivery_view = self.ANS.UI.Mailbox_DBV \
            ( self.delivery_box
            , show_header  = False
            , adapter_kw   = dict (office = self.office)
            , AC           = AC
            )
        self.delivery_view.tkt.scroll_policies (self.TNS.AUTOMATIC)
        for box in self.delivery_box.sub_boxes :
            self.box_views [box] = self.delivery_view
            box.register_change_observer (self._update_box_status)
        for box in self.delivery_box.mailboxes :
            self.box_views [box] = self.delivery_view
        self.box_views [self.delivery_box] = self.delivery_view
    # end def _create_delivery_view

    def _delete_box (self, box) :
        for sb in box.sub_boxes :
            self._delete_box (sb)
        parent = PMA.Mailbox.instance (TFL.sos.path.split (box.qname) [0])
        parent.delete_subbox (box)
    # end def _delete_box

    def _display_message (self, mailbox) :
        message = mailbox.status.current_message
        self.model.msg_display.display (message)
        self.mb_msg_view.update        (message)
        self.box_views [mailbox.root].update (mailbox)
        return # XXX
        help = self.AC.ui_state.message
        help.pop_help  ()
        help.push_help (str (message.pending))
    # end def _display_message

    def _mail_compose (self, cmd, text, * args) :
        ANS    = self.ANS
        smtp   = ANS.Sender     ()
        comp   = ANS.Composer   (smtp = smtp, send_cb = self._mail_sent)
        result = getattr        (comp, cmd) (* args)
        time.sleep (0.1)
        print (text)
        time.sleep (0.1)
        return result
    # end def _mail_compose

    def _mail_sent (self, email) :
        receivers = set ()
        for kind in "to", "cc", "bcc" :
            recs = email [kind]
            if recs :
                for r in recs.split (",") :
                    receivers.add (r)
        time.sleep (0.1)
        print ("Mail sent to %s" % (", ".join (receivers)))
        time.sleep (0.1)
        return email
    # end def _mail_sent

    def _mail_sent (self, email) :
        receivers = set ()
        for kind in "to", "cc", "bcc" :
            recs = email [kind]
            if recs :
                for r in recs.split (",") :
                    receivers.add (r)
        time.sleep (0.1)
        print ("Mail sent to %s" % (", ".join (receivers)))
        time.sleep (0.1)
        return email
    # end def _mail_sent

    def _message_command (self, cmd, text, * args) :
        status   = self.office.status
        view     = self.mb_msg_view
        msgs     = self.mb_msg_view.selection
        if not msgs :
            msgs = (status.current_box.status.current_message, )
        if msgs :
            print \
                ( text
                % dict
                    ( cb_qname = status.current_box.qname
                    , cmd      = cmd
                    , tb_qname = getattr (status.target_box, "qname", "")
                    )
                , end = " "
                )
            for msg in msgs :
                result = getattr (msg.pending, cmd) (* args)
                print (msg.number, end = " ")
                view.update  (msg)
            print
        return result
    # end def _message_command

    def _message_command_n (self, cmd, text, * args) :
        result = self._message_command (cmd, text, * args)
        view   = self.mb_msg_view
        next   = view.next ()
        if next :
            view.see (next)
            view.selection = next
        return result
    # end def _message_command_n

    def _show_unseen (self, fct_name) :
        fct = getattr (self.mb_msg_view, fct_name)
        msg = fct ()
        while msg and not msg.status.unseen :
            msg = fct (current = msg)
        if msg :
            self._select_message (msg = msg)
        return msg
    # end def _show_unseen

    def _restore_selection (self) :
        box   = self.office.status.current_box
        if box :
            box.register_change_observer (self._update_mailbox_msg_view)
            names  = []
            for b_name in box.qname.split (PMA.Mailbox.name_sep) :
                names.append (b_name)
                name = PMA.Mailbox.name_sep.join  (names)
                try :
                    box  = PMA.Mailbox.instance (name)
                    self.box_views [box.root].see (box)
                except KeyError :
                    ### ignore parts of the box path which don't have it's
                    ### own mailbox object
                    pass
            self.box_views [box.root].selection = box
            self.select_box (force = True)
    # end def _restore_selection

    def _select_message (self, msg = None) :
        if msg :
            box                        = msg.mailbox
            box.status.current_message = msg
            self.mb_msg_view.selection = msg
            self.mb_msg_view.see  (msg)
            self._display_message (getattr (msg, "v_mailbox", box))
    # end def _select_message

    def _update_commit_action (self, messages) :
        view  = self.mb_msg_view
        boxes = {}
        for msg in messages :
            if msg not in msg.mailbox :
                ### message has been move or deleted -> remove it from display
                view.remove (msg)
            else :
                ### only the state of the message has changed -> update display
                view.update (msg)
            boxes.setdefault \
                (getattr (msg, "v_mailbox", msg.mailbox), []).append (msg)
        text = []
        for box, msgs in boxes.iteritems () :
            self.box_views [box.root].update (box)
            text.append \
                ( "`%s`: %s"
                % (box.qname, ", ".join (str (m.number) for m in msgs))
                )
        print ("Commit %s" % (", ".join (text), ))
    # end def _update_commit_action

    def _update_box_status (self, old, new, mailbox) :
        ### call this function to reset the peding changes
        mailbox.changes_for_observer (self._update_box_status)
        ### possible that some message have been added -> update the box to
        ### change the unseen count
        self.box_views [mailbox.root].update (mailbox)
    # end def _update_box_status

    def _update_mailbox_msg_view (self, old, new, mailbox) :
        ### maybe a complete rebuild of mb_msg_view is required since it is
        ### possible that all message number have changed
        for c in mailbox.changes_for_observer (self._update_mailbox_msg_view) :
            if hasattr (c, "update_mailbox_msg_view") :
                c.update_mailbox_msg_view (mailbox, self.mb_msg_view)
    # end def _update_filter_mailbox

# end class Office

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Office

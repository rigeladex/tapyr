# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    PMA.Composer
#
# Purpose
#    Support composing and sending of emails
#
# Revision Dates
#    26-Jul-2005 (CT) Creation
#    27-Jul-2005 (CT) Creation continued
#    28-Jul-2005 (CT) Creation continued...
#    28-Jul-2005 (CT) Renamed from `Sender` to `Composer`
#    28-Jul-2005 (CT) `Sender` factored
#    28-Jul-2005 (CT) Creation continued.... (resend, attachements)
#    29-Jul-2005 (CT) Creation continued..... (forward)
#    29-Jul-2005 (CT) `main` and `command_spec` renamed to `_main` and
#                     `_command_spec` to avoid name clashes in PMA namespace
#    29-Jul-2005 (CT) `_formatted` factored and changed to handle non-ASCII
#    29-Jul-2005 (CT) `locals` extended
#    29-Jul-2005 (CT) `sos.unlink` of temporary file moved to avoid deletion
#                     in case of exceptions
#    29-Jul-2005 (CT) Use `subprocess.call` instead of `sos.system`
#    29-Jul-2005 (CT) `forward` changed to allow multiple messages
#    31-Jul-2005 (CT) `reply_all` added
#     9-Aug-2005 (CT) s/default_charset/default_encoding/g
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _PMA.Message
import _PMA.Mime
import _PMA.Sender
import _TFL._Meta.Object
import _TFL.Environment

from   _TFL.Regexp             import *
import _TFL.sos

from   smtplib                 import SMTP
import subprocess
import textwrap
import threading

class Editor_Thread (TFL.Meta.Object, threading.Thread) :
    """Thread running an editor instance"""

    def __init__ (self, buffer, editor, finish_callback, * args, ** kw) :
        name = None
        if "name" in kw :
            name = kw ["name"]
            del kw ["name"]
        self.buffer          = buffer
        self.editor          = editor
        self.finish_callback = finish_callback
        #print "Editor_Thread.__init__"
        self.__super.__init__ \
            ( group  = None
            , name   = name
            , args   = args
            , kwargs = kw
            )
    # end def __init__

    def run (self) :
        bfn = self._write_buffer (self.buffer)
        cmd = "%s %s" % (self.editor, bfn)
        #print "Editor_Thread.run", bfn
        subprocess.call (cmd, shell  = True)
        #print "Editor_Thread.run after subprocess"
        result = self._read_buffer  (bfn)
        if result != self.buffer :
            self.finish_callback    (result, bfn)
        else :
            TFL.sos.unlink          (bfn)
    # end def run

    def _read_buffer (self, bfn) :
        result = None
        try :
            f = open (bfn)
        except (IOError, TFL.sos.error) :
            pass
        else :
            try :
                result = f.read ()
            finally :
                f.close ()
        return result
    # end def _read_buffer

    def _write_buffer (self, buffer) :
        result = TFL.sos.tempfile_name \
            (TFL.sos.expanded_path ("~/PMA/.drafts"), create_dir = True)
        f = open (result, "w")
        try :
            f.write (buffer)
        finally :
            f.close ()
        return result
    # end def _write_buffer

# end class Editor_Thread

class Composer (TFL.Meta.Object) :
    """Support interactive sending of emails"""

    body_marker    = "--text follows this line--"
    domain         = TFL.Environment.mailname ()
    editor         = "emacsclient --alternate-editor vi"
    user           = TFL.Environment.username
    email_address  = "%s@%s" % (user, domain)

    compose_format = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          """
          , """Subject:     """
          , """Bcc:         %(email_address)s"""
          , """X-mailer:    PMA %(version)s"""
          , """%(body_marker)s"""
          , """"""
          )
        )

    forward_format = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          """
          , """Subject:     FW: %(subject)s"""
          , """Cc:          """
          , """Bcc:         %(email_address)s"""
          , """X-mailer:    PMA %(version)s"""
          , """%(body_marker)s"""
          , """see attached mail"""
          , """"""
          )
        )

    reply_format   = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          %(reply_address)s"""
          , """Subject:     Re: %(subject)s"""
          , """Bcc:         %(email_address)s"""
          , """X-mailer:    PMA %(version)s"""
          , """In-reply-to: Your message of "%(message_date)s" """
          , """             %(message_id)s"""
          , """References:  %(message_id)s"""
          , """%(body_marker)s"""
          , """%(sender)s wrote at %(message_date)s:"""
          , """"""
          )
        )

    reply_all_format = "\n".join \
        ( ( """Cc:          %(reply_address_cc)s"""
          , reply_format
          )
        )

    resend_format  = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          """
          , """Cc:          """
          , """Bcc:         """
          )
        )

    _attachement_header       = "PMA-Attach-File"
    _reply_subject_prefix_pat = Regexp \
        ( "^(Subject: *)(Re|AW|FW): *((Re|AW|FW): *)+"
        , re.IGNORECASE | re.MULTILINE
        )

    def __init__ (self, editor = None, user = None, domain = None, smtp = None, send_cb = None) :
        if editor is not None : self.editor = editor
        if user   is not None : self.user   = user
        if domain is not None : self.domain = domain
        if user is not None or domain is not None :
            self.email_address = "%s@%s" % (self.user, self.domain)
        self.smtp    = smtp
        self.send_cb = send_cb
        self.locals  = dict \
            ( body_marker   = self.body_marker
            , email_address = self.email_address
            , domain        = self.domain
            , user          = self.user
            , version       = PMA.version
            )
    # end def __init__

    def compose (self) :
        """Compose and send a new email."""
        self._send (self._formatted (self.compose_format), self._finish_edit)
    # end def compose

    def forward (self, msg, * more_msgs) :
        """Forward `msg` as attachement of a new email."""
        buffer = self._formatted (self.forward_format, msg)
        self._send \
            (buffer, lambda * a : self._finish_forward (msg, more_msgs, * a))
    # end def forward

    def reply (self, msg, _format = None) :
        """Compose and send a reply to `msg`."""
        buffer = self._formatted (_format or self.reply_format, msg)
        if self._reply_subject_prefix_pat.search (buffer) :
            buffer = self._reply_subject_prefix_pat.sub (r"\1Re: ", buffer)
        self._send (buffer, self._finish_edit)
    # end def reply

    def reply_all (self, msg) :
        """Compose and send a reply to all receviers of `msg`."""
        return self.reply (msg, self.reply_all_format)
    # end def reply_all

    def resend (self, msg) :
        """Resend `msg` to other addresses unchanged (except for `Resent-`
           headers).
        """
        buffer = self._formatted (self.resend_format, msg)
        self._send (buffer, lambda * a : self._finish_resend (msg, * a))
    # end def resend

    def _as_message (self, buffer) :
        return Lib.message_from_string (buffer.replace (self.body_marker, ""))
    # end def _as_message

    def _as_multipart (self, email) :
        result = email
        if not email.is_multipart () :
            result = Lib.MIMEMultipart ()
            ignore = set (result.keys ())
            for k, v in email.items () :
                if k not in ignore :
                    result [k] = v
            cs = email.get_charset () or PMA.default_encoding
            result.attach \
                ( Lib.MIMEText
                    (email.get_payload (decode = True), _charset = cs)
                )
        return result
    # end def _as_multipart

    def _finish_edit (self, buffer, bfn) :
        if buffer :
            email = self._as_message (buffer)
            if email.get ("Date", None) is None :
                ### just to be safe (del of non-existing key is a no-op)
                del email ["Date"]
                email ["Date"] = Lib.formatdate ()
            subject = email.get ("Subject")
            email   = self._process_attachement_headers (email)
        if email and self.smtp :
            self._finish__send (email, send_cb = self.send_cb)
        TFL.sos.unlink (bfn)
    # end def _finish_edit

    def _finish_forward (self, msg, more_msgs, buffer, bfn) :
        if buffer :
            email    = msg.email
            envelope = self._as_multipart (self._as_message (buffer))
            envelope.attach (Lib.MIMEMessage (email))
            for m in more_msgs :
                envelope.attach (Lib.MIMEMessage (m.email))
            self._finish__send (envelope)
        TFL.sos.unlink (bfn)
    # end def _finish_forward

    def _finish_resend (self, msg, buffer, bfn) :
        if buffer :
            email    = msg.email
            envelope = self._as_message (buffer)
            for k in envelope.keys () :
                if k.lower () not in ("bcc", "dcc") :
                    n = "Resent-%s" % k
                    for h in envelope.get_all (k, []) :
                        if h :
                            email [n] = h
            email ["Resent-date"]       = Lib.formatdate ()
            email ["Resent-message-id"] = Lib.make_msgid ()
            self._finish__send (email, envelope = envelope)
        TFL.sos.unlink (bfn)
    # end def _finish_resend

    def _finish__send (self, email, envelope = None, send_cb = None) :
        if send_cb is not None :
            email = send_cb (email)
        if email and self.smtp :
            self.smtp (email, envelope)
    # end def _finish__send

    def _formatted (self, format, msg = None) :
        mapping = self.locals
        if msg is not None :
            mapping = PMA.Msg_Scope (msg, mapping)
        return (unicode (format, PMA.default_encoding) % mapping).encode \
            (PMA.default_encoding, "replace" )
    # end def _formatted

    def _process_attachement_headers (self, email) :
        ah = self._attachement_header
        for value in email.get_all (ah, []) :
            if value :
                if "\n" in value :
                    name, rest  = value.split ("\n", 1)
                    add_headers = Lib.message_from_string \
                        (textwrap.dedent (rest))
                else :
                    name        = value
                    add_headers = None
                p = PMA.Mime.Part \
                    (TFL.sos.expanded_path (name.strip (";")), add_headers)
                if p :
                    if not email.is_multipart () :
                        email = self._as_multipart (email)
                    email.attach (p)
        del email [ah]
        return email
    # end def _process_attachement_headers

    def _send (self, buffer, finish_cb) :
        Editor_Thread (buffer, self.editor, finish_cb).start ()
    # end def _send

# end class Composer

def _command_spec (arg_array = None) :
    from _TFL.Command_Line import Command_Line
    return Command_Line \
        ( option_spec =
            ( "-bounce:S?Message to resend"
            , "-domain:S?Domain of sender"
            , "-editor:S?Command used to start editor"
            , "-forward:S?Message to forward"
            , "-mail_host:S?Name of SMTP server to use"
            , "-reply:S?Message to reply to"
            , "-Reply_all:S?Message to reply to"
            , "-user:S?Name of sender"
            )
        , description =
          "Send mail message (newly composed or reply to existing email)"
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def _command_spec

def _main (cmd) :
    smtp = PMA.Sender   (cmd.mail_host)
    comp = PMA.Composer (cmd.editor, cmd.user, cmd.domain, smtp)
    if cmd.forward :
        comp.forward    (PMA.message_from_file (cmd.forward))
    elif cmd.reply :
        comp.reply      (PMA.message_from_file (cmd.reply))
    elif cmd.Reply_all :
        comp.reply_all  (PMA.message_from_file (cmd.Reply_all))
    elif cmd.bounce :
        comp.resend     (PMA.message_from_file (cmd.bounce))
    else :
        comp.compose    ()
# end def _main

if __name__ != "__main__" :
    PMA._Export ("*")
else :
    import _PMA.Composer
    PMA.load_user_config ()
    _main (_command_spec ())
### __END__ PMA.Composer

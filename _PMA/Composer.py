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
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _PMA.Message
import _PMA.Mime
import _TFL._Meta.Object
import _TFL.Environment

from   _TFL.Regexp             import *

from   smtplib                 import SMTP
import sos
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
        self.__super.__init__ \
            ( group  = None
            , name   = name
            , args   = args
            , kwargs = kw
            )
    # end def __init__

    def run (self) :
        bfn    = self._write_buffer (self.buffer)
        cmd    = "%s %s" % (self.editor, bfn)
        sos.system                  (cmd)
        result = self._read_buffer  (bfn)
        if result != self.buffer :
            self.finish_callback    (result)
    # end def run

    def _read_buffer (self, bfn) :
        result = None
        try :
            f = open (bfn)
        except (IOError, sos.error) :
            pass
        else :
            try :
                result = f.read ()
            finally :
                f.close    ()
                sos.unlink (bfn)
        return result
    # end def _read_buffer

    def _write_buffer (self, buffer) :
        result = sos.tempfile_name ()
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

    compose_format = "\n".join \
        ( ( """From:        %(user)s@%(domain)s"""
          , """To:          """
          , """Subject:     """
          , """Bcc:         %(user)s@%(domain)s"""
          , """X-mailer:    PMA"""
          , body_marker
          , """"""
          )
        )

    forward_format = "\n".join \
        ( ( """From:        %(user)s@%(domain)s"""
          , """To:          """
          , """Subject:     FW: %(subject)s"""
          , """Cc:          """
          , """Bcc:         %(user)s@%(domain)s"""
          , body_marker
          , """see attached mail"""
          , """"""
          )
        )

    reply_format   = "\n".join \
        ( ( """From:        %(user)s@%(domain)s"""
          , """To:          """
          , """Subject:     Re: %(subject)s"""
          , """Bcc:         %(user)s@%(domain)s"""
          , """X-mailer:    PMA"""
          , """In-reply-to: Your message of "%(message_date)s" """
          , """             %(message_id)s"""
          , """References:  %(message_id)s"""
          , body_marker
          , """%(From)s wrote at %(message_date)s:"""
          , """"""
          )
        )

    resend_format  = "\n".join \
        ( ( """From:        %(user)s@%(domain)s"""
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
        if editor is not None : self.user   = user
        if editor is not None : self.domain = domain
        self.smtp    = smtp
        self.send_cb = send_cb
        self.locals  = dict (domain = self.domain, user = self.user)
    # end def __init__

    def compose (self) :
        """Compose and send a new email."""
        self._send (self.compose_format % self.locals, self._finish_edit)
    # end def compose

    def forward (self, msg) :
        """Forward `msg` as attachement of a new email."""
        buffer = self.forward_format % PMA.Msg_Scope (msg, self.locals)
        self._send (buffer, lambda b : self._finish_forward (msg, b))
    # end def forward

    def reply (self, msg) :
        """Compose and send a reply to `msg`."""
        buffer = self.reply_format % PMA.Msg_Scope (msg, self.locals)
        if self._reply_subject_prefix_pat.search (buffer) :
            buffer = self._reply_subject_prefix_pat.sub (r"\1Re: ", buffer)
        self._send (buffer, self._finish_edit)
    # end def reply

    def resend (self, msg) :
        """Resend `msg` to other addresses unchanged (except for `Resent-`
           headers).
        """
        buffer = self.resend_format % PMA.Msg_Scope (msg, self.locals)
        self._send (buffer, lambda b : self._finish_resend (msg, b))
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
            cs = email.get_charset () or PMA.Mime.default_charset
            result.attach \
                ( Lib.MIMEText
                    ( email.get_payload (decode = True)
                    , _charset = cs
                    )
                )
        return result
    # end def _as_multipart

    def _finish_edit (self, buffer) :
        if buffer :
            email = self._as_message (buffer)
            if email.get ("Date", None) is None :
                ### just to be safe (del of non-existing key is a no-op)
                del email ["Date"]
                email ["Date"] = Lib.formatdate ()
            subject = email.get ("Subject")
            email   = self._process_attachement_headers (email)
        if self.send_cb is not None :
            email = self.send_cb (email)
        if email and self.smtp :
            self._finish__send (email, send_cb = self.send_cb)
    # end def _finish_edit

    def _finish_forward (self, msg, buffer) :
        if buffer :
            email    = msg.email
            envelope = self._as_multipart (self._as_message (buffer))
            envelope.attach    (Lib.MIMEMessage (email))
            self._finish__send (envelope)
    # end def _finish_forward

    def _finish_resend (self, msg, buffer) :
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
    # end def _finish_resend

    def _finish__send (self, email, envelope = None, send_cb = None) :
        if send_cb is not None :
            email = send_cb (email)
        if email and self.smtp :
            self.smtp (email, envelope)
    # end def _finish__send

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
                p = PMA.Mime.Part (name.strip (";"), add_headers)
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

def command_spec (arg_array = None) :
    from _TFL.Command_Line import Command_Line
    return Command_Line \
        ( option_spec =
            ( "-domain:S?Domain of sender"
            , "-editor:S?Command used to start editor"
            , "-forward:S?Message to forward"
            , "-mail_host:S=mails?Name of SMTP server to use"
            , "-reply:S?Message to reply to"
            , "-Resend:S?Message to resend"
            , "-user:S?Name of sender"
            )
        , description =
          "Send mail message (newly composed or reply to existing email)"
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    import _PMA.Sender
    smtp = PMA.Sender (cmd.mail_host)
    comp = Composer   (cmd.editor, cmd.user, cmd.domain, smtp)
    if cmd.forward :
        comp.forward  (PMA.message_from_file (cmd.forward))
    elif cmd.reply :
        comp.reply    (PMA.message_from_file (cmd.reply))
    elif cmd.Resend :
        comp.resend   (PMA.message_from_file (cmd.Resend))
    else :
        comp.compose  ()
# end def main

_emacs_compose_buffer = """
To:          «text»
Subject:     «text»
BCC:         tanzer@swing.cluster
««mail-cc»»
««mail-bcc»»
««mail-from»»
Reply-to:    tanzer@swing.cluster (Christian Tanzer)
--text follows this line--

«text»

--
Christian Tanzer                                    http://www.c-tanzer.at/
"""

_exmh_resend_buffer  = """
Resent-To:
Resent-cc:
Resent-fcc:
"""

_exmh_compose_buffer = """
To:          «text»
Subject:     «text»
From:        tanzer@swing.cluster (Christian Tanzer)
Reply-to:    tanzer@swing.cluster (Christian Tanzer)
DCC:         tanzer@swing.cluster (Christian Tanzer)
««mail-cc»»
««mail-bcc»»
--------

«text»
"""

_exmh_reply_buffer = """
To:          "Pichler Fruhstorfer" <pichler.fruhstorfer@chello.at>
Subject:     Re: LV 7/05
In-reply-to: Your message of "Mon, 18 Jul 2005 15:44:02 +0200."
             <GEEMLHOFMGMPMIIOKFNLOEJJCHAA.pichler.fruhstorfer@chello.at>
DCC:         tanzer@swing.co.at
Reply-to:    tanzer@swing.co.at
From:        tanzer@swing.cluster (Christian Tanzer)
««mail-cc»»
««mail-bcc»»
--------

«text»
"""

if __name__ != "__main__" :
    PMA._Export ("*")
else :
    main (command_spec ())
### __END__ PMA.Composer

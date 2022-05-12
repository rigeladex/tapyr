# -*- coding: utf-8 -*-
# Copyright (C) 2005-2022 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#     5-Jan-2006 (CT) `Thread` factored
#    24-Feb-2009 (CT) `_add_header_maybe` factored
#    24-Feb-2009 (CT) Add headers for `Content-type`,
#                     `Content-transfer-encoding` and `Mime-version`
#    19-Mar-2009 (CT) Use `with open_tempfile` instead of `sos.tempfile_name`
#    27-Dec-2010 (CT) Options for mail sending added and passed to `PMA.Sender`
#    27-Dec-2010 (CT) Use `TFL.CAO` instead of `TFL.Command_Line`
#     6-Jul-2012 (CT) Remove stale import of `smtplib.SMTP`
#    27-Mar-2013 (CT) Add options `-HTML`, `-receiver`, `-subject`
#    28-Mar-2013 (CT) Put `receiver`, `subject` in `defaults`
#    28-Mar-2013 (CT) Use `Msg_Scope` even if there isn't a `msg`
#    27-Aug-2013 (CT) Change `_as_message` to include `plain` with `html`
#    27-Aug-2013 (CT) Add `addressee` to `forward_format`, `resend_format`,
#                     `defaults`
#    17-Mar-2014 (CT) Add option `-msg_base_dirs`
#     4-Nov-2014 (CT) Add `-attach` options, factor `_process_attachement`
#     2-Apr-2015 (CT) Add option `-Bcc`, alias expansion for it
#     2-Apr-2015 (CT) Add option `-Debug`
#     8-May-2015 (CT) Pass encoded string to `Lib.message_from_string`
#                     in `_as_html`
#    29-Oct-2015 (CT) Improve Python 3 compatibility
#     3-Nov-2015 (CT) Improve encoding/decoding in `_as_message`, `_as_html`
#     3-Nov-2015 (CT) Factor `_as_text_part`, work around issue25545
#     4-Nov-2015 (CT) Use pyk.email_message_from_bytes,
#                     not `Lib.message_from_string` because Python 3
#     6-Nov-2015 (CT) Move `.encode` from `_formatted` to `_send`
#    10-Dec-2015 (CT) Add option `-Short_body`
#    14-Mar-2016 (CT) Change option types from `S` to `U` for `-subject`...
#    11-Oct-2016 (CT) Change `GTW.HTML` to `TFL.HTML`
#    18-Sep-2017 (CT) Pass `use_file__mime` to `Mime.Part`
#    25-Mar-2020 (CT) Use `Lib.policy.default`
#                     * with the default policy (`Lib.policy.compat32`),
#                       unicode headers are broken
#    25-Mar-2020 (CT) Add option `-content_transfer_encoding`, default `8bit`
#    10-May-2022 (CT) Use `PMA.Sender.mail_host` as default value, if existing
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _PMA.Alias
import _PMA.Message
import _PMA.Mime
import _PMA.Sender
import _PMA.Thread

from   _TFL._Meta.Once_Property import Once_Property
import _TFL._Meta.Object
import _TFL.CAO
import _TFL.Environment
import _TFL.FCM
from   _TFL.predicate          import callable, first
from   _TFL.Regexp             import *
import _TFL.sos

from   itertools               import chain as ichain

import subprocess
import textwrap

class Editor_Thread (PMA.Thread) :
    """Thread running an editor instance"""

    def __init__ (self, buffer, editor, finish_callback, ** kw) :
        self.buffer          = buffer
        self.editor          = editor
        self.finish_callback = finish_callback
        self.__super.__init__ (auto_start = True, ** kw)
    # end def __init__

    def run (self) :
        bfn = self._write_buffer (self.buffer)
        cmd = "%s %s" % (self.editor, bfn)
        subprocess.call (cmd, shell  = True)
        result = self._read_buffer  (bfn)
        if result != self.buffer :
            self.finish_callback    (result, bfn)
        else :
            TFL.sos.unlink          (bfn)
    # end def run

    def _read_buffer (self, bfn) :
        result = None
        try :
            with open (bfn, "rb") as f :
                result = f.read ()
        except (IOError, TFL.sos.error) :
            pass
        return result
    # end def _read_buffer

    def _write_buffer (self, buffer) :
        with TFL.open_tempfile \
            ( dir         = TFL.sos.expanded_path ("~/PMA/.drafts")
            , auto_remove = False
            , create_dir  = True
            , mode        = "wb"
            ) as (f, result) :
            f.write (buffer)
        return result
    # end def _write_buffer

# end class Editor_Thread

class Composer (TFL.Meta.Object) :
    """Support interactive sending of emails"""

    addressee              = ""
    attach                 = None
    body_marker            = "--text follows this line--"
    domain                 = TFL.Environment.mailname ()
    editor                 = "emacsclient --alternate-editor vi"
    formatted_replacers    = Multi_Re_Replacer ()
    formatted_replacers_sb = Multi_Re_Replacer ()
    user                   = TFL.Environment.username
    email_address          = "%s@%s" % (user, domain)
    receiver               = ""
    short_body             = ""
    subject                = ""

    compose_format = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          %(receiver)s"""
          , """Subject:     %(subject)s"""
          , """Bcc:         %(bcc_addr)s"""
          , """X-mailer:    PMA %(version)s"""
          , """%(body_marker)s"""
          , ""
          )
        )

    forward_format = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          %(addressee)s"""
          , """Subject:     FW: %(subject)s"""
          , """Cc:          """
          , """Bcc:         %(bcc_addr)s"""
          , """X-mailer:    PMA %(version)s"""
          , """%(body_marker)s"""
          , """see attached mail"""
          , ""
          )
        )

    reply_format   = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          %(reply_address)s"""
          , """Subject:     Re: %(subject)s"""
          , """Bcc:         %(bcc_addr)s"""
          , """X-mailer:    PMA %(version)s"""
          , """In-reply-to: Your message of "%(message_date)s" """
          , """             %(message_id)s"""
          , """References:  %(message_id)s"""
          , """%(body_marker)s"""
          , """%(sender)s wrote at %(message_date)s:"""
          , ""
          )
        )

    reply_all_format = "\n".join \
        ( ( """Cc:          %(reply_address_cc)s"""
          , reply_format
          )
        )

    resend_format  = "\n".join \
        ( ( """From:        %(email_address)s"""
          , """To:          %(addressee)s"""
          , """Cc:          """
          , """Bcc:         """
          )
        )

    _attachement_header       = "PMA-Attach-File"
    _reply_subject_prefix_pat = Regexp \
        ( "^(Subject: *)(Re|AW|FW): *((Re|AW|FW): *)+"
        , re.IGNORECASE | re.MULTILINE
        )
    _rest2html_header         = "PMA-Rest-2-HTML"
    _sig_pat                  = Regexp \
        ( "^--$.*\Z"
        , re.IGNORECASE | re.MULTILINE | re.DOTALL
        )

    def __init__ \
            ( self
            , editor           = None
            , user             = None
            , domain           = None
            , smtp             = None
            , send_cb          = None
            , rst2html         = False
            , receiver         = None
            , short_body       = None
            , subject          = None
            , attach           = None
            , bcc              = None
            , debug            = False
            ) :
        if editor     is not None  : self.editor     = editor
        if user       is not None  : self.user       = user
        if domain     is not None  : self.domain     = domain
        if receiver   is not None  : self.receiver   = receiver
        if short_body is not None  : self.short_body = short_body
        if subject    is not None  : self.subject    = subject
        if attach     is not None  : self.attach     = attach
        if user is not None or domain is not None :
            self.email_address = "%s@%s" % (self.user, self.domain)
        self.bcc_addr          = self.email_address if bcc is None else bcc
        self.debug             = debug
        self.smtp              = smtp
        self.send_cb           = send_cb
        self.rst2html          = rst2html
        self.locals            = dict \
            ( bcc_addr         = self.bcc_addr
            , body_marker      = self.body_marker
            , email_address    = self.email_address
            , domain           = self.domain
            , user             = self.user
            , version          = PMA.version
            )
        self.defaults          = dict \
            ( addressee        = receiver or ""
            , receiver         = receiver or self.receiver
            , subject          = self.subject
            )
    # end def __init__

    @Once_Property
    def to_html (self) :
        from   _ReST import ReST
        import _ReST.To_Html
        import _TFL.HTML
        ReST.to_html.add_replacers \
            ( TFL.HTML.Styler
            , Re_Replacer (r'border="1"', r"")
            )
        return ReST.to_html
    # end def to_html

    def compose (self) :
        """Compose and send a new email."""
        message = self._formatted (self.compose_format)
        self._send (message, self._finish_edit)
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

    def _add_header_maybe (self, email, name, value) :
        if email.get (name, None) is None :
            ### just to be safe (del of non-existing key is a no-op)
            del email [name]
            if callable (value) :
                value = value ()
            email [name] = value
    # end def _add_header_maybe

    def _as_html (self, buffer) :
        encoding   = "utf-8"
        bm         = self.body_marker
        head, body = buffer.split (bm, 1)
        body       = self._remove_sig (body)
        html       = "\n".join \
            ( ( "<html>"
              , "<head></head>"
              , "<body>"
              , self.to_html (body, encoding = encoding)
              , "</body>"
              , "</html>"
              )
            )
        html_buffer = "\n\n".join ((head, html))
        result = pyk.email_message_from_bytes \
            (pyk.encoded (html_buffer, encoding))
        del result [self._rest2html_header]
        del result ["Content-Type"]
        result ["Content-Type"] = "text/html; charset=%s" % encoding
        return result
    # end def _as_html

    def _as_message (self, buffer_x) :
        bm_rep = "\n" + self.short_body if self.short_body else ""
        buffer = pyk.decoded (buffer_x, PMA.default_encoding)
        result = pyk.email_message_from_bytes \
            ( pyk.encoded
                ( buffer.replace (self.body_marker, bm_rep)
                , PMA.default_encoding
                )
            , policy = Lib.policy.default
            )
        if self.rst2html or self._rest2html_header in buffer :
            plain    = result
            html     = self._as_html      (buffer)
            result   = self._as_multipart (html, _subtype = "alternative")
            result.attach (self._as_text_part (plain))
        else :
            self._add_header_maybe \
                ( result
                , "Content-Type"
                , "text/plain; charset=%s" % PMA.default_encoding
                )
        return result
    # end def _as_message

    def _as_multipart (self, email, ** kw) :
        result = email
        if not email.is_multipart () :
            result = Lib.MIMEMultipart (** kw)
            ignore = set (result.keys ())
            for k, v in email.items () :
                if k not in ignore :
                    result [k] = v
            result.attach (self._as_text_part (email))
        return result
    # end def _as_multipart

    def _as_text_part (self, email, charset = None) :
        ### In Python 3.5, `email.get_payload` returns bytes encoded in latin-1,
        ### even if `charset` is "utf-8"
        ### http://bugs.python.org/issue25545
        if charset is None :
            charset = email.get_content_charset () or PMA.default_encoding
        sub_typ     = email.get_content_subtype ()
        text        = pyk.decoded \
            (email.get_payload (decode = True), charset, "latin-1")
        return Lib.MIMEText \
            (_text = text, _subtype = sub_typ, _charset = charset)
    # end def _as_text_part

    def _finish_edit (self, buffer, bfn = None) :
        if buffer :
            email = self._as_message (buffer)
            self._add_header_maybe (email, "Date", Lib.formatdate)
            email = self._process_attachement_headers (email)
            if email and self.smtp :
                self._finish__send (email, send_cb = self.send_cb)
        if bfn is not None :
            TFL.sos.unlink (bfn)
    # end def _finish_edit

    def _finish_forward (self, msg, more_msgs, buffer, bfn = None) :
        if buffer :
            email    = msg.email
            envelope = self._as_multipart (self._as_message (buffer))
            envelope.attach (Lib.MIMEMessage (email))
            for m in more_msgs :
                envelope.attach (Lib.MIMEMessage (m.email))
            self._finish__send (envelope)
        if bfn is not None :
            TFL.sos.unlink (bfn)
    # end def _finish_forward

    def _finish_resend (self, msg, buffer, bfn = None) :
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
        if bfn is not None :
            TFL.sos.unlink (bfn)
    # end def _finish_resend

    def _finish__send (self, email, envelope = None, send_cb = None) :
        self._add_header_maybe (email, "Mime-Version", "1.0")
        if email.is_multipart () :
            self._add_header_maybe (email, "Content-Transfer-Encoding", "8bit")
        if send_cb is not None :
            email = send_cb (email)
        if email and self.smtp :
            if self.debug :
                print (email)
                print ()
            self.smtp (email, envelope)
    # end def _finish__send

    def _formatted (self, format, msg = None) :
        replacer = self.formatted_replacers_sb \
            if self.short_body else self.formatted_replacers
        mapping  = PMA.Msg_Scope (msg, self.locals, self.defaults)
        result   = pyk.decoded   (format, PMA.default_encoding) % mapping
        result   = replacer      (result)
        return result
    # end def _formatted

    def _process_attachement (self, email, name, add_headers = None) :
        p = PMA.Mime.Part \
            ( TFL.sos.expanded_path (name.strip (";")), add_headers
            , use_file__mime = True
            )
        if p :
            if not email.is_multipart () :
                email = self._as_multipart (email)
            email.attach (p)
        return email
    # end def _process_attachement

    def _process_attachement_headers (self, email) :
        ah = self._attachement_header
        for value in email.get_all (ah, []) :
            if value :
                if "\n" in value :
                    name, rest  = value.split ("\n", 1)
                    encoding    = PMA.default_encoding
                    add_headers = pyk.email_message_from_bytes \
                        (pyk.encoded (textwrap.dedent (rest), encoding))
                else :
                    name        = value
                    add_headers = None
                email = self._process_attachement (email, name, add_headers)
        del email [ah]
        if self.attach :
            for name in self.attach :
                email = self._process_attachement (email, name)
        return email
    # end def _process_attachement_headers

    def _remove_sig (self, body) :
        pat = self._sig_pat
        if pat.search (body) :
            sig = pat.group (0).strip ().split ("\n")
            if len (sig) < 5 :
                body = body [:pat.start (0)]
        return body.strip ()
    # end def _remove_sig

    def _send (self, msg, finish_cb) :
        buffer = pyk.encoded (msg, PMA.default_encoding)
        if self.short_body :
            finish_cb (buffer)
        else :
            Editor_Thread (buffer, self.editor, finish_cb)
    # end def _send

# end class Composer

def _main (cmd) :
    Sender = PMA.Sender_Tester if cmd.Debug else PMA.Sender
    smtp   = Sender \
        ( local_hostname            = cmd.mail_local_hostname
        , mail_host                 = cmd.mail_host or
                                      getattr (PMA.Sender, "mail_host", None)
        , mail_port                 = cmd.mail_port
        , password                  = cmd.mail_word
        , user                      = cmd.mail_user
        , use_tls                   = cmd.tls
        , content_transfer_encoding = cmd.content_transfer_encoding
        )
    attach = sorted \
        ( ichain
            ( ichain
                (  * tuple
                     ( TFL.CAO.Rel_Path.resolved_paths
                         ( cmd.msg_base_dirs, m
                         , single_match = False
                         , skip_missing = True
                         )
                     for m in cmd.Attach_Message
                     )
                )
            , cmd.attach
            )
        )
    bcc    = None
    if cmd.Bcc :
        try :
            alias_mgr = PMA.Alias_Mgr \
                ("/etc/aliases", "~/.aliases", "~/.mh_aliases")
            alias = alias_mgr [cmd.Bcc]
            bcc   = str (alias)
        except KeyError :
            bcc = cmd.Bcc
        except Exception as exc :
            print (exc)
    comp   = PMA.Composer \
        ( cmd.editor, cmd.user, cmd.domain, smtp
        , attach     = attach
        , bcc        = bcc
        , debug      = cmd.Debug
        , receiver   = cmd.To
        , rst2html   = cmd.HTML
        , short_body = cmd.Short_body
        , subject    = cmd.subject
        )
    def message_from_arg (cmd, arg) :
        try :
            return first (PMA.messages_from_args ([arg], cmd.msg_base_dirs))
        except LookupError :
            raise SystemExit (1)
    if cmd.forward :
        comp.forward    (message_from_arg (cmd, cmd.forward))
    elif cmd.reply :
        comp.reply      (message_from_arg (cmd, cmd.reply))
    elif cmd.Reply_all :
        comp.reply_all  (message_from_arg (cmd, cmd.Reply_all))
    elif cmd.bounce :
        comp.resend     (message_from_arg (cmd, cmd.bounce))
    else :
        comp.compose    ()
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler     = _main
    , max_args    = 0
    , opts        =
        ( "-attach:P ?File to attach"
        , "-Attach_Message:P ?Message to attach"
        , "-Bcc:S"
            "?Email(s) to be put on blind carbon copy (default: sender's email)"
        , "-bounce:S?Message to resend"
        , "-config:C?File specifying defaults for options"
        , "-content_transfer_encoding:S=8bit"
            "?Possible values: 7bit, 8bit, quoted-printable, base64"
        , "-Debug:B?Use SMTP_Tester for debugging"
        , "-domain:S?Domain of sender"
        , "-editor:S?Command used to start editor"
        , "-forward:S?Message to forward"
        , "-HTML:B?Convert ReST message to HTML"
        , "-mail_host:S?Name of SMTP server to use"
        , "-mail_local_hostname:S?Name of host sending the email"
        , "-mail_port:I=25?Number of port of SMTP server to use"
        , "-mail_user:S?User name for login into SMTP server"
        , "-mail_word:S?Password for login into SMTP server"
        , "-msg_base_dirs:Q:?Base directories for searching `message`"
        , "-reply:S?Message to reply to"
        , "-Reply_all:S?Message to reply to"
        , "-Short_body:U"
            "?Don't start an editor, use supplied value as body instead"
        , "-subject:U?Subject of email"
        , "-tls:B?Use SMTP in TLS (Transport Layer Security) mode."
        , "-To:U?Email of receiver"
        , "-user:U?Name of sender"
        )
        , description =
          "Send mail message (newly composed or reply to existing email)"
    )

if __name__ != "__main__" :
    PMA._Export ("*")
else :
    import _PMA.Composer
    PMA.load_user_config   ()
    _PMA.Composer._Command ()
### __END__ PMA.Composer

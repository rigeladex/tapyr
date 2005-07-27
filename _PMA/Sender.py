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
#    PMA.Sender
#
# Purpose
#    Support sending of emails
#
# Revision Dates
#    26-Jul-2005 (CT) Creation
#    27-Jul-2005 (CT) Creation continued
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _PMA                    import PMA
from   _PMA                    import Lib

import _PMA.Message
import _TFL._Meta.Object

from   _TFL.Regexp             import *

from   smtplib                 import SMTP
import sos
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

class Sender (TFL.Meta.Object) :
    """Support interactive sending of emails"""

    compose_format = "\n".join \
        ( ( """From:        %(user)s@%(domain)s"""
          , """To:          """
          , """Subject:     """
          , """X-mailer:    PMA"""
          , """--text follows this line--"""
          , """"""
          )
        )

    reply_format   = "\n".join \
        ( ( """From:        %(user)s@%(domain)s"""
          , """To:          """
          , """Subject:     Re: %(subject)s"""
          , """X-mailer:    PMA"""
          , """In-reply-to: Your message of "%(message_date)s" """
          , """             %(message_id)s"""
          , """References:  %(message_id)s"""
          , """--text follows this line--"""
          , """%(From)s wrote at %(message_date)s:"""
          , """"""
          )
        )

    _reply_subject_prefix_pat = Regexp \
        ("^(Subject: *)(Re|AW): *((Re|AW): *)+", re.IGNORECASE | re.MULTILINE)

    def __init__ (self, editor, user, domain, mail_host, send_cb = None) :
        self.editor    = editor
        self.user      = user
        self.domain    = domain
        self.mail_host = mail_host
        self.send_cb   = send_cb
        self.locals    = dict (domain = domain, user = user)
    # end def __init__

    def compose (self) :
        """Compose and send a new email."""
        self._send (self.compose_format % self.locals)
    # end def compose

    def reply (self, msg) :
        """Compose and send a reply to `msg`."""
        buffer = self.reply_format % PMA.Msg_Scope (msg, self.locals)
        if self._reply_subject_prefix_pat.search (buffer) :
            buffer = self._reply_subject_prefix_pat.sub (r"\1Re: ", buffer)
        self._send (buffer)
    # end def reply

    def _finish_edit (self, buffer) :
        if buffer :
            buffer = buffer.replace ("--text follows this line--", "")
            msg    = Lib.message_from_string (buffer)
            if not "Date" in msg :
                del msg ["Date"]
                msg ["Date"] = Lib.formatdate ()
            subject = msg.get ("Subject")
            ### XXX process X-PMA-attach headers
        if self.send_cb is not None :
            msg = self.send_cb (msg)
        if msg :
            self._smtp_send (msg)
    # end def _finish_edit

    def _send (self, buffer) :
        editor = Editor_Thread (buffer, self.editor, self._finish_edit)
        editor.start ()
    # end def _send

    def _smtp_send (self, msg) :
        to = msg ["To"].split (",")
        for k in "cc", "bcc", "dcc" :
            for h in msg.get_all (k, []) :
                to.extend (h.split (","))
            if k != "cc" :
                del msg [k]
        server = SMTP   (self.mail_host)
        server.helo     ()
        server.sendmail (msg ["From"], to, msg.as_string ())
        server.quit     ()
    # end def _smtp_send

# end class Sender

def command_spec (arg_array = None) :
    from   Command_Line import Command_Line
    import Environment
    return Command_Line \
        ( option_spec =
            ( "-domain:S=%s?Domain of sender"
              % open ("/etc/mailname").read ().strip ()
            , "-editor:S=emacsclient?Command used to start editor"
            , "-mail_host:S=mails?Name of SMTP server to use"
            , "-reply:S?Message to reply to"
            , "-user:S=%s?Name of sender" % (Environment.username, )
            )
        , description =
          "Send mail message (newly composed or reply to existing email)"
        , max_args    = 0
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    s = Sender    (cmd.editor, cmd.user, cmd.domain, cmd.mail_host)
    if cmd.reply :
        s.reply   (PMA.message_from_file (cmd.reply))
    else :
        s.compose ()
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
### __END__ PMA.Sender

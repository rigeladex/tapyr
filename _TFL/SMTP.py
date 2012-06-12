# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.SMTP
#
# Purpose
#    Support sending of emails via SMTP
#
# Revision Dates
#    19-Feb-2010 (CT) Creation (factored from `PMA.Sender`)
#    21-Feb-2010 (MG) Support for authentication added
#    16-Jun-2010 (CT) s/print/pyk.fprint/
#    27-Dec-2010 (CT) Optional init-arguments added,
#                     `open` and `close` factored and extended (`use_tls`)
#                     `connection` added and used
#    12-Jun-2012 (CT) Import `email.utils`, not `email.Utils` (<= Python 2.4)
#    19-Jun-2012 (CT) Add `header` and apply it in `send_message`
#    ««revision-date»»···
#--

from   _TFL                    import TFL

from   _TFL                    import pyk

import _TFL._Meta.Object
import _TFL.Context

from   email                   import message, message_from_string
from   email.header            import Header, decode_header, make_header
from   email.utils             import formatdate

import smtplib
import socket

class SMTP (TFL.Meta.Object) :
    """Send emails via SMTP"""

    charset        = "iso-8859-15"
    local_hostname = None
    mail_host      = "localhost"
    mail_port      = None
    password       = None
    user           = None
    use_tls        = False

    def __init__ \
            ( self
            , mail_host      = None
            , mail_port      = None
            , local_hostname = None
            , user           = None
            , password       = None
            , use_tls        = None
            , charset        = None
            ) :
        if mail_host is not None :
            self.mail_host = mail_host
        if mail_port is not None :
            self.mail_port = mail_port
        if local_hostname is not None :
            self.local_hostname = local_hostname
        if user is not None :
            self.user = user
        if password is not None :
            self.password = password
        if use_tls is not None :
            self.use_tls = use_tls
        if charset is not None :
            self.charset = charset
        self.server = None
    # end def __init__

    def __call__ (self, text, mail_opts = (), rcpt_opts = None) :
        if isinstance (text, unicode) :
            raise TypeError \
                ("SMTP () expects a byte string, got unicode: %r" % text)
        email = message_from_string (text)
        self.send_message (email, mail_opts = mail_opts, rcpt_opts = rcpt_opts)
    # end def __call__

    def close (self) :
        assert self.server is not None
        try :
            self.server.quit ()
        except socket.sslerror :
            self.server.close ()
        finally :
            self.server = None
    # end def close

    @TFL.Contextmanager
    def connection (self) :
        close_p = self.server is not None
        server  = self.open ()
        try :
            yield server
        finally :
            if close_p :
                self.close ()
    # end def connection

    def header (self, s, charset = None, ** kw) :
        """Wrap `s` in `email.header.Header` if necessary.

           Wrapping is done only if `s` contains non-ASCII characters;
           applying `Header` to pure ASCII strings adds stupid line noise to
           email addresses!

        >>> from email.header import Header
        >>> print Header ("christian.tanzer@swing.co.at", charset = "utf-8")
        =?utf-8?q?christian=2Etanzer=40swing=2Eco=2Eat?=
        """
        if charset is None :
            charset = self.charset
        result = s
        if isinstance (result, str) :
            decoded = decode_header (result)
            if any (c for ds, c in decoded) :
                result = make_header \
                    (list ((ds, c or charset) for ds, c in decoded), ** kw)
        if not isinstance (result, Header) :
            if isinstance (result, str) :
                try :
                    result  = result.decode (charset)
                except UnicodeError :
                    charset = "utf-8"
                    result  = result.decode (charset)
            try :
                result.encode ("ascii")
            except UnicodeError :
                result = Header (s, charset = charset, ** kw)
        return result
    # end def header

    def open (self) :
        if self.server is None :
            result = self.server = smtplib.SMTP \
                (self.mail_host, self.mail_port, self.local_hostname)
            if self.use_tls :
                result.ehlo     ()
                result.starttls () ### Still need another `ehlo` after this
            result.ehlo ()
            if self.user :
                result.login (self.user, self.password)
        return self.server
    # end def open

    def send (self, from_addr, to_addrs, msg, mail_opts = (), rcpt_opts = None) :
        with self.connection () as server :
            server.sendmail (from_addr, to_addrs, msg, mail_opts, rcpt_opts)
    # end def send

    def send_message (self, email, envelope = None, mail_opts = (), rcpt_opts = None) :
        assert isinstance (email, message.Message)
        if envelope is None :
            envelope = email
        to = set (t.strip () for t in envelope ["To"].split (","))
        for k in "cc", "bcc", "dcc" :
            for h in envelope.get_all (k, []) :
                if h :
                    to.update (t.strip () for t in h.split (","))
            if k != "cc" :
                del email [k]
        if "Date" not in email :
            email ["Date"] = formatdate ()
        if "Content-type" not in email :
            charset = self.charset
            email ["Content-type"] = \
                """text/plain; charset="%s" """ % (charset, )
        else :
            charset = email.get_charset ()
        for k in "Subject", "To", "From", "CC", "BCC" :
            vs = email.get_all (k)
            if vs :
                del email [k]
                for v in vs :
                    email [k] = self.header (v, charset, header_name = k)
        self.send \
            ( envelope ["From"], list (to), email.as_string ()
            , mail_opts, rcpt_opts
            )
    # end def send_message

# end class SMTP

class SMTP_Tester (SMTP) :
    """Tester writing to stdout instead of connecting to SMTP server."""

    def send (self, from_addr, to_addrs, msg, mail_opts = None, rcpt_opts = None) :
        pyk.fprint \
            ("Email via", self.mail_host, "from", from_addr, "to", to_addrs)
        pyk.fprint (msg)
    # end def send

# end class SMTP_Tester

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.SMTP

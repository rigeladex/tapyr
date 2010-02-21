# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _TFL                    import TFL

import _TFL._Meta.Object

from   email                   import message, message_from_string
from   email.Utils             import formatdate

import smtplib

class SMTP (TFL.Meta.Object) :
    """Send emails via SMTP"""

    mail_host = "localhost"

    def __init__ (self, mail_host = None, user = None, password = None) :
        if mail_host is not None :
            self.mail_host = mail_host
        self.user          = user
        self.password      = password
    # end def __init__

    def __call__ (self, text, mail_opts = (), rcpt_opts = None) :
        if isinstance (text, unicode) :
            raise TypeError \
                ("SMTP () expects a byte string, got unicode: %r" % text)
        email = message_from_string (text)
        self.send_message (email, mail_opts = mail_opts, rcpt_opts = rcpt_opts)
    # end def __call__

    def send (self, from_addr, to_addrs, msg, mail_opts = (), rcpt_opts = None) :
        server = smtplib.SMTP (self.mail_host)
        if self.user :
            server.login (self.user, self.password)
        server.helo      ()
        server.sendmail  (from_addr, to_addrs, msg, mail_opts, rcpt_opts)
        server.quit      ()
    # end def send

    def send_message (self, email, envelope = None, mail_opts = None, rcpt_opts = None) :
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
            email ["Content-type"] = """text/plain; charset="iso-8859-1" """
        self.send \
            ( envelope ["From"], list (to), email.as_string ()
            , mail_opts, rcpt_opts
            )
    # end def send_message

# end class SMTP

class SMTP_Tester (SMTP) :
    """Tester writing to stdout instead of connecting to SMTP server."""

    def send (self, from_addr, to_addrs, msg, mail_opts = None, rcpt_opts = None) :
        print "Email via", self.mail_host, "from", from_addr, "to", to_addrs
        print msg
    # end def send

# end class SMTP_Tester

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.SMTP

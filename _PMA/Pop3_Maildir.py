# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    PMA.Pop3_Maildir
#
# Purpose
#    Maildir getting mails from remote server using the POP3 protocol
#    (http://www.faqs.org/rfcs/rfc1939.html)
#
# Revision Dates
#     4-Jan-2006 (CT) Creation
#     5-Jan-2006 (CT) `Polling_Thread` factored
#     5-Jan-2006 (CT) `Pop3_Maildir_SSL` added
#    ««revision-date»»···
#--

from   _TFL                       import TFL
from   _PMA                       import PMA
from   _PMA                       import Lib

import _PMA.Mailbox
import _PMA.Thread
import _TFL._Meta.Object
import _TFL.sos as sos

import poplib
import sys

class Pop3_Poller (PMA.Polling_Thread) :
    """Thread polling mailbox on Pop3 server"""

    def __init__ ( self, maildir, host, user
                 , passwd              = None
                 , port                = 110
                 , poll_interval       = 10 ### in seconds
                 , ** kw
                 ) :
        self.maildir       = maildir
        self.host          = host
        self.port          = port
        self.user          = user
        self.passwd        = passwd
        self.poll_interval = poll_interval
        self.finish        = False
        self.parser        = Lib.Parser ()
        self.__super.__init__ (** kw)
    # end def __init__

    def connect (self) :
        mdir   = self.maildir
        result = mdir.POP3_class (self.host, self.port)
        result.user (self.user)
        if self.passwd is None :
            self.passwd = mdir.passwd_cb ()
        if self.passwd != "" :
            result.pass_ (self.passwd)
        return result
    # end def connect

    def download_pop (self, server, mdir) :
        md_name = PMA._Mailbox_.md_name
        result  = 0
        for msg_no, msg_size in self.pop_list (server) :
            email = self._new_email ("\n".join (server.retr (msg_no) [1]))
            name  = md_name         ()
            tname = sos.path.join   (mdir.path, "tmp", name)
            nname = sos.path.join   (mdir.path, "new", name)
            PMA.save    (tname, email.as_string ())
            sos.link    (tname, nname)
            sos.unlink  (tname)
            server.dele (msg_no)
            result += 1
            if self.finish :
                break
        return result
    # end def download_pop

    def pop_list (self, server) :
        return (x.split (" ") for x in server.list () [1])
    # end def pop_list

    def _poll (self) :
        server = self.connect ()
        try :
            try :
                self.maildir.unsynced.value += \
                    self.download_pop (server, self.maildir)
            except Exception, exc :
                print >> sys.__stderr__, \
                    "Exception during `download_pop`: %s" % (exc, )
        finally :
            server.quit ()
    # end def _poll

    def _new_email (self, msg_text) :
        if PMA.SB is not None :
            msg_text = PMA.SB.filter (msg_text)
        return self.parser.parsestr (msg_text)
    # end def _new_email

# end class Pop3_Poller

class Pop3_Maildir (PMA.Maildir) :
    """Model a Maildir style mailbox getting mails from remote server using
       the POP3 protocol.
    """

    POP3_class = poplib.POP3

    def __init__ ( self, path, host, user
                 , passwd              = None
                 , prefix              = None
                 , root                = None
                 , port                = 110
                 , poll_interval       = 60 ### in seconds
                 ) :
        self.__super.__init__ (path, prefix, root)
        self.poller = Pop3_Poller \
            (self, host, user, passwd, port, poll_interval, auto_start = True)
    # end def __init__

    def passwd_cb (self) :
        raise NotImplemented, "Must pass passwd to Pop3_Maildir"
    # end def passwd_cb

# end class Pop3_Maildir

class Pop3_Maildir_SSL (Pop3_Maildir) :
    """Model a Pop3_Maildir using a SSL conection to the POP server."""

    POP3_class = poplib.POP3_SSL

# end class Pop3_Maildir_SSL

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Pop3_Maildir

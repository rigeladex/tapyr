# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    PMA.POP3_Mailbox
#
# Purpose
#    Handle a Mailbox on a remote server using the POP3 access protocol
#
# Revision Dates
#     8-Aug-2005 (MG) Creation
#     2-Jan-2006 (CT) `reparsed` and `_new_message` added
#     2-Jan-2006 (CT) Optional argument `headersonly` added to `_new_email`
#     2-Jan-2006 (CT) `_new_email` changed to use `SB.filter` if available
#     2-Jan-2006 (CT) `MB_Type` changed to use `pop.top` instead or `pop.retr`
#    ««revision-date»»···
#--

from   _TFL                       import TFL
from   _PMA                       import PMA
import _PMA.Mailbox
import _TFL._Meta.Object
import  poplib
import _TFL.sos as sos

class POP3_Mailbox (PMA._Mailbox_) :
    """A POP3 mailbox which receives the messages from the account and adds
       them to a different mailbox (based on the message ID only once).
    """

    def __init__ ( self, host, user, passwd
                 , name   = None
                 , prefix = None
                 , root   = None
                 , port   = 110
                 ) :
        self.host   = host
        self.port   = port
        self.user   = user
        self.passwd = passwd
        self.__super.__init__ (host, name, prefix, root)
    # end def __init__

    def reparsed (self, msg) :
        pop = poplib.POP3 (self.host, self.port)
        pop.user  (self.user)
        pop.pass_ (self.passwd)
        try :
            msg_no = msg.path
            result = self._new_email \
                ("\n".join (pop.retr (msg_no) [1]), headersonly = False)
            result._pma_msg_no = msg_no
        finally :
            pop.quit ()
        return result
    # end def reparsed

    def _new_email (self, msg_text, headersonly = True) :
        if PMA.SB is not None :
            msg_text = PMA.SB.filter (msg_text)
        parser = PMA.Lib.Parser  ()
        email  = parser.parsestr (msg_text, headersonly = headersonly)
        email._pma_parsed_body = not headersonly
        email._pma_path = sos.path.join (self.path, email ["message-id"])
        return email
    # end def _new_email

    def _new_message (self, m) :
        result = self.__super._new_message (m)
        result.path = result.email._pma_msg_no
        return result
    # end def _new_message

    def _setup_messages (self) :
        pop = poplib.POP3 (self.host, self.port)
        pop.user  (self.user)
        pop.pass_ (self.passwd)
        try :
            self._add \
                ( * ( self._new_message (m)
                     for m in self.MB_Type (pop, self._new_email)
                    )
                )
        finally :
            pop.quit ()
    # end def _setup_messages

    @classmethod
    def MB_Type (cls, pop, factory) :
        for msg_spec in pop.list () [1] :
            msg_no, _ = msg_spec.split (" ", 1)
            m = factory ("\n".join (pop.top (msg_no, 0) [1]))
            m._pma_msg_no = msg_no
            yield m
    # end def MB_Type

# end class POP3_Mailbox

"""
from _PMA.POP3_Mailbox import *

mb = POP3_Mailbox ("mx.wavenet.at", "g9505a00", "5secyba3")
mb = POP3_Mailbox ("localhost", "tanzer", "", port = 1100)
"""
if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ POP3_Mailbox

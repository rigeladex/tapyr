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
#     2-Jan-2006 (CT) `connect` factored
#     2-Jan-2006 (CT) Methods `msg_no` and `uidl` added
#     3-Jan-2006 (CT) Derive from `_Mailbox_in_Dir_S_` instead of `_Mailbox_`
#     3-Jan-2006 (CT) `path` added to `__init__`
#     3-Jan-2006 (CT) s/msg_no/_msg_no/ (for the method)
#     3-Jan-2006 (CT) `_pop_msg_query` factored, `pop_list` added
#     3-Jan-2006 (CT) `_save` added and used
#     3-Jan-2006 (CT) `lazy_download_limit` added and used
#     3-Jan-2006 (CT) `passwd_cb` added
#    ««revision-date»»···
#--

from   _TFL                       import TFL
from   _PMA                       import PMA
import _PMA.Mailbox
import _TFL._Meta.Object
import  poplib
import _TFL.sos as sos

class POP3_Mailbox (PMA._Mailbox_in_Dir_S_) :
    """A POP3 mailbox which receives the messages from the account and adds
       them to a different mailbox (based on the message ID only once).
    """

    supports_status     = True
    lazy_download_limit = 1024 * 10

    def __init__ ( self, path, host, user
                 , passwd              = None
                 , prefix              = None
                 , root                = None
                 , port                = 110
                 , lazy_download_limit = None
                 ) :
        self.host   = host
        self.port   = port
        self.user   = user
        self.passwd = passwd
        if lazy_download_limit is not None :
            self.lazy_download_limit = lazy_download_limit
        self._msg_count = 0
        self._mbx_size  = 0
        self.__super.__init__ (path, prefix, root)
    # end def __init__

    def connect (self) :
        pop = poplib.POP3 (self.host, self.port)
        pop.user  (self.user)
        if self.passwd is None :
            self.passwd = self.passwd_cb ()
        if self.passwd != "" :
            pop.pass_ (self.passwd)
        return pop
    # end def connect

    def delete (self, * messages) :
        pop = self.connect ()
        try :
            for msg in messages :
                msg_no = self._msg_no (pop, msg.name, msg.msg_no)
                if msg_no :
                    pop.dele (msg_no)
                else :
                    print \
                        ( "Couldn't delete `%s (%s)`: POP3 msg-number %s"
                          "not found"
                        % (msg.number, msg.name, msg.msg_no)
                        )
        finally :
            pop.quit ()
        self.__super.delete (* messages)
    # end def delete

    def MB_Type (self, pop, factory) :
        self._msg_count, self._mbx_size = c, s = pop.stat ()
        _msg_dict = self._msg_dict
        seen      = set (_msg_dict)
        if not _msg_dict :
            cached = self._emails_from_dir (self.path, self.__super._new_email)
            for m in cached :
                m._pma_msg_no = c
                m._pma_size   = 0
                m._pma_cached = True
                seen.add (m._pma_path)
                yield m
        for msg_no, msg_uid in self.pop_uidl (pop) :
            if msg_uid not in seen :
                msg_size      = int (self.pop_list (pop, msg_no) [1])
                headersonly   = msg_size > self.lazy_download_limit
                if headersonly :
                    lines     = pop.top  (msg_no, 0) [1]
                else :
                    lines     = pop.retr (msg_no)    [1]
                m = factory ("\n".join (lines), headersonly = headersonly)
                m._pma_msg_no = msg_no
                m._pma_path   = msg_uid
                m._pma_size   = msg_size
                m._pma_cached = False
                seen.add (m._pma_path)
                yield m
        for msg in _msg_dict.values () :
            ### can't use `itervalues` here because dict might change in loop
            if msg.name not in seen :
                self.__super.delete (msg)
    # end def MB_Type

    def passwd_cb (self) :
        raise NotImplemented, "Must pass passwd to POP3_Mailbox"
    # end def passwd_cb

    def pop_list (self, pop, msg_no = None) :
        return self._pop_msg_query (pop.list, msg_no)
    # end def pop_list

    def pop_uidl (self, pop, msg_no = None) :
        return self._pop_msg_query (pop.uidl, msg_no)
    # end def pop_uidl

    def reparsed (self, msg) :
        if msg.email._pma_cached :
            result = self.__super.reparsed (msg)
        else :
            pop = self.connect ()
            try :
                msg_no = self._msg_no (pop, msg.name, msg.msg_no)
                if msg_no :
                    lines  = pop.retr (msg_no) [1]
                    result = self._new_email \
                        ("\n".join (lines), headersonly = False)
                    result._pma_msg_no = msg_no
                    self._save (msg, result)
                else :
                    print "This shouldn't happen!"
            finally :
                pop.quit ()
        return result
    # end def reparsed

    def sync (self) :
        """Sync with `new` messages"""
        return self._setup_messages ()
    # end def sync

    def _msg_no (self, pop, uid, msg_no) :
        max_no = int (pop.stat () [0])
        msg_no = max (int (msg_no), max_no)
        while msg_no > 0 :
            m, u = self.pop_uidl (pop, str (msg_no))
            if u == uid :
                return m
            msg_no -= 1
    # end def _msg_no

    def _new_email (self, msg_text, headersonly = True) :
        if PMA.SB is not None :
            msg_text = PMA.SB.filter (msg_text)
        parser = self.parser
        email  = parser.parsestr (msg_text, headersonly = headersonly)
        email._pma_parsed_body = not headersonly
        return email
    # end def _new_email

    def _new_message (self, m) :
        result        = self.__super._new_message (m)
        result.msg_no = result.email._pma_msg_no
        if m._pma_parsed_body and not m._pma_cached :
            self._save (result, m)
        return result
    # end def _new_message

    def _new_subbox (self, path) :
        raise TypeError, "POP3_Mailbox doesn't support sub-boxes"
    # end def _new_subbox

    def _pop_msg_query (self, cmd, msg_no) :
        if msg_no :
            return cmd (msg_no).split (" ") [1:]
        else :
            return (x.split (" ") for x in cmd () [1])
    # end def _pop_msg_query

    def _save (self, msg, email) :
        try :
            msg._save \
                (sos.path.join (self.path, msg.name), email.as_string ())
        except IOError :
            pass
        else :
            email._pma_cached = True
    # end def _save

    def _setup_messages (self) :
        result = []
        try :
            pop = self.connect ()
        except Exception :
            pass
        else :
            try :
                if (self._msg_count, self._mbx_size) != pop.stat () :
                    result = \
                        [   self._new_message (m)
                        for m in self.MB_Type (pop, self._new_email)
                        ]
                    self._add (* result)
            finally :
                pop.quit ()
        return result
    # end def _setup_messages

    def _subdirs (self, path) :
        return ()
    # end def _subdirs

# end class POP3_Mailbox

"""
from _PMA.POP3_Mailbox import *

mb = POP3_Mailbox ("mx.wavenet.at", "g9505a00", "5secyba3")
mb = POP3_Mailbox ("localhost", "tanzer", "", port = 1100)
"""
if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ POP3_Mailbox

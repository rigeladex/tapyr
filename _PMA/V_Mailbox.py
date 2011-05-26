# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.V_Mailbox
#
# Purpose
#    A virtual mailbox (combing several real mailboxes into one mailbox)
#
# Revision Dates
#    30-Dec-2005 (MG) Creation
#     2-Jan-2006 (CT) `sync` added
#    23-Jan-2006 (MG) Rewritten using the change counter
#    26-Jan-2006 (MG) `remove_msg` reordered
#    26-Jan-2006 (MG) Use new `changes_for_observer` feature
#    ««revision-date»»···
#--
#
from   _TFL                    import TFL
import _TFL.sos                as     sos
from   _PMA                    import PMA
import _TFL._Meta.Object
import _PMA.Mailbox
import  weakref

class _Proxy_ (TFL.Meta.Object) :
    """A proxy around an object which overrides some of the attributes."""

    def __init__ (self, obj, ** overrides) :
        self.obj = weakref.proxy (obj)
        self.__dict__.update (overrides)
    # end def __init__

    def __getattr__ (self, name) :
        return getattr (self.obj, name)
    # end def __getattr__

# end class _Proxy_

class _V_Mailbox_ (PMA._Mailbox_) :
    """Root class for all kind of virtual mailboxes"""

    supports_status = True

    def __init__ (self, name, prefix = None, root = None) :
        path = sos.path.join \
            (PMA.Office.virtual_mailbox_path (), name)
        if not sos.path.isdir (path) :
            sos.mkdir (path)
        self.__super.__init__ \
            ( name     = name
            , path     = path
            , prefix   = prefix
            , root     = root
            )
        for mb in self.mailboxes :
            mb.register_change_observer (self._mailbox_changed)
    # end def __init__

    def add_filter_mailbox (self, name, matcher) :
        s = PMA.Filter_Mailbox \
            (name, matcher, self, prefix = self.qname, root = self.root)
        self._box_dict [s.name] = s
        self.change_list.append (PMA.SCM.Add_Filter_Subbox (s))
        self.change_count      += 1
        return s
    # end def add_filter_mailbox

    def add_messages (self, * messages) :
        msgs = []
        for m in self._eligible (messages) :
            if m.name not in self._msg_dict :
                msgs.append (m)
        self._add (* msgs)
        return msgs
    # end def add_messages

    def add_subbox (self, * args, ** kw) :
        raise TypeError, "Only adding of a Filter_Mailbox supported!"
    # end def add_subbox

    def delete (self, * messages) :
        for m in messages :
            deleted.setdefault (m.mailbox, []).append (m)
        for mb, msgs in deleted.iteritems () :
            mb.delete (* msgs)
    # end def delete

    def sync (self) :
        result = []
        for b in self.mailboxes :
            result.extend (b.sync ())
        return result
    # end def sync

    def remove_msg (self, * msg_names) :
        msg_names = [n for n in msg_names if n in self._msg_dict]
        if msg_names :
            for name  in msg_names :
                del self._msg_dict [name]
            self.change_list.append (PMA.SCM.Remove_Messages (* msg_names))
            self.change_count += len (msg_names)
    # end def remove_msg

    def _add (self, * messages) :
        return self.__super._add \
            ( * ( _Proxy_ (m, number = None, v_mailbox = self)
                  for m in messages
                )
            )
    # end def _add

    def _get_messages (self) :
        if self._messages is None :
            self._messages = []
            msgs           = []
            for mb in self.mailboxes :
                for m in self._eligible (mb.messages) :
                    if m.name not in self._msg_dict :
                        ### this is necessary in case that the virual mailbox
                        ### is created before the messages of the mailboxes
                        ### have been materialized (to avoid doouble adding of
                        ### messages based on the change list AND during the
                        ### first creation of the _messages list).
                        msgs.append (m)
            self._add  (* msgs)
            self._messages = self._msg_dict.values ()
            self._sort ()
        return self._messages
    # end def _get_messages

    def _mailbox_changed (self, old, new, mailbox = None) :
        for chg in \
            ( c for c in mailbox.changes_for_observer (self._mailbox_changed)
                    if callable (c)
            ) :
            chg (self, mailbox)
    # end def _mailbox_changed

# end class _V_Mailbox_

class V_Mailbox (_V_Mailbox_) :
    """Virtual mailbox (combing several real mailboxes into one mailbox)."""

    def __init__ (self, name, mailboxes, prefix = None) :
        self.mailboxes  = mailboxes
        self.__super.__init__ \
            ( name      = name
            , prefix    = prefix
            )
    # end def __init__

    def _eligible (self, messages) :
        return messages
    # end def _eligible

# end class V_Mailbox

"""
from _PMA                  import PMA
import _PMA.Mailbox
import _PMA.V_Mailbox
import _PMA.Matcher

mbi = PMA.Maildir    ("/home/glueck/PMA/D/inbox")
mb1 = PMA.Mailbox    ("/home/glueck/PMA/TTTech/planung")
mb2 = PMA.Mailbox    ("/home/glueck/PMA/TTTech/BIKA")
mbs = PMA.MH_Mailbox ("/home/glueck/work/MH/Installscript")
vmb = PMA.V_Mailbox  ("f1", (mb1, mb2))
vmb.messages
m   = mbs.messages [58]
"""

if __name__ != "__main__" :
    PMA._Export ("V_Mailbox", "_V_Mailbox_")
### __END__ PMA.V_Mailbox

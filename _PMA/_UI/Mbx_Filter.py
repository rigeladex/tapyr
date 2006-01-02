# -*- coding: iso-8859-1 -*-
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
#    PMA.UI.Mbx_Filter
#
# Purpose
#    A filter for a mailbox.
#
# Revision Dates
#    30-Dec-2005 (MG) Creation
#     2-Jan-2006 (CT) `__init__` fixed
#     2-Jan-2006 (MG)  Make ` Mbx_Filter` a descendent of `PMA._Mailbox_`
#     2-Jan-2006 (MG) `Mbx_Filter.sync` added
#     2-Jan-2006 (MG) `add_messages` added
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _PMA                 import PMA
import _PMA._UI.Mixin
import _PMA.Matcher
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

class Mbx_Filter (PMA._Mailbox_) :
    """A mailbox filter which acts like a real mailbox"""

    supports_status = True

    def __init__ (self, mailbox, name, matcher, AC = None, ** ckw) :
        self.__super.__init__ \
            ( name   = name
            , path   = mailbox._boxes [0].path ### XXX
            , prefix = mailbox.qname
            , root   = mailbox
            )
        self.mailbox   = mailbox
        if not isinstance (matcher, PMA._Matcher_) :
            matcher    = PMA.Matcher (matcher, ** ckw)
        self._matcher  = matcher
    # end def __init__

    def add_messages (self, * msgs) :
        result       = []
        for m in self._matcher.filter (* msgs) :
            sp       = _Proxy_ (m.scope)
            mp       = _Proxy_ (m, mailbox = self, scope = sp)
            sp.msg   = mp
            m.number = len (self._messages)
            self._messages.append (mp)
            result.append         (mp)
            self._msg_dict [m.name] = mp
        return result
    # end def add_message

    def _get_messages (self) :
        if self._messages is None :
            self._messages = []
            self.add_messages (* self.mailbox.messages)
        return self._messages
    # end def _get_messages

    def sync (self) :
        return self.mailbox.sync ()
    # end def sync

# end class Mbx_Filter

class F_Mailbox (PMA.UI.Mixin) :
    """A mailbox with attached filters"""

    messages = ()
    unseen   = 0
    status   = property (lambda s: s.mailbox.status)

    def __init__ (self, mailbox, * mbx_filter, ** kw) :
        self.__super.__init__ (** kw)
        self.mailbox    = mailbox
        self.sub_boxes  = mbx_filter
    # end def __init__

    def add_messages (self, * msgs) :
        result = []
        for bf in self.sub_boxes :
            result.extend (bf.add_messages (* msgs))
        return result
    # end def add_messages

# end class F_Mailbox

if __name__ != "__main__" :
    PMA.UI._Export ("Mbx_Filter", "F_Mailbox")
### __END__ PMA.UI.Mbx_Filter

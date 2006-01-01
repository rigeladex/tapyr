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
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _PMA                 import PMA
import _PMA._UI.Mixin
import _PMA.Matcher
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

class Mbx_Filter (PMA.UI.Mixin) :
    """A mailbox filer which acts like a real mailbox"""

    messages           = property (lambda s : s._get_messages ())
    msg_dict           = property \
        (lambda s : (s._get_messages (), s._msg_dict) [-1])
    unseen             = property \
        (lambda s : sum ([m.status.unseen for m in s._get_messages ()]))
    pending            = property \
        (lambda s : sum ([len (m.pending) for m in s._get_messages ()]))
    _box_dict          = {}

    def __init__ (self, mailbox, name, condition, AC = None, matcher = None, ** ckw) :
        self.__super.__init__ (AC = AC)
        self.mailbox   = self.root  = mailbox
        self.name      = name
        self.qname     = PMA.Mailbox.name_sep.join \
            ((mailbox.qname, name))
        if matcher is None :
            matcher    = self.ANS.Matcher (condition, ** ckw)
        self._matcher  = matcher
        self._messages = None
        self._msg_dict = {}
        self.status    = self.ANS.Box_Status (self)
    # end def __init__

    def _get_messages (self) :
        if self._messages is None :
            self._messages = []
            for m in self._matcher.filter (* self.mailbox.messages) :
                sp     = _Proxy_ (m.scope)
                mp     = _Proxy_ (m, mailbox = self, scope = sp)
                sp.msg = mp
                self._messages.append (mp)
                self._msg_dict [m.name] = mp
        return self._messages
    # end def _get_messages

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

# end class F_Mailbox

if __name__ != "__main__" :
    PMA.UI._Export ("Mbx_Filter", "F_Mailbox")
### __END__ PMA.UI.Mbx_Filter

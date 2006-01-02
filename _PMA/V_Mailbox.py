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
#    PMA.V_Mailbox
#
# Purpose
#    A virtual mailbox (combing several real mailboxes into one mailbox)
#
# Revision Dates
#    30-Dec-2005 (MG) Creation
#     2-Jan-2006 (CT) `sync` added
#    ««revision-date»»···
#--
#
from   _PMA                    import PMA
from   _TFL                    import TFL
import _TFL._Meta.Object

class V_Mailbox (TFL.Meta.Object) :
    """Virtual mailbox (combing several real mailboxes into one mailbox)."""

    messages           = property (lambda s : s._get_messages ())

    def __init__ (self, name, * boxes) :
        self.name      = self.qname = name
        self._boxes    = boxes
        self.root      = self
        self.status    = PMA.Box_Status (self)
    # end def __init__

    def sync (self) :
        result = []
        for b in self._boxes :
            result.extend (b.sync ())
        return result
    # end def sync

    def _get_messages (self) :
        for b in self._boxes :
            for m in b.messages :
                yield m
    # end def _get_messages

    # XXX missing interfaces
    # - add_subbox
    # - add_messages
    # - delete_subbox
    # - delete (messages)
    # - commit

# end class V_Mailbox

if __name__ != "__main__" :
    PMA._Export ("V_Mailbox")
### __END__ PMA.V_Mailbox

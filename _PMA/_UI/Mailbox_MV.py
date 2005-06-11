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
#    PMA.UI.Mailbox_MV
#
# Purpose
#    Abstract user interface for message-view of PMA.Mailbox
#
# Revision Dates
#     6-Jun-2005 (CT) Creation
#     6-Jun-2005 (MG) `_MB_TA_`: methods converted to classmethods
#     7-Jun-2005 (MG) Superfluous `@classmethod` removed
#    11-Jun-2005 (MG) `Message_Cell` added and used
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Mailbox

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Tree
import _PMA._UI.Tree_Adapter

class Message_Cell (TGL.UI.Text_Cell) :
    """A cell which uses attributes of a PMA.Message object to set style
       related attributes (background, foreground, ...)
    """

    def setup_column_types (self, column_types) :
        self.__super.setup_column_types (column_types)
        index                   = len (column_types)
        column_types.append (int)
        self.renderer_attr_dict ["weight"] = index
        self.attr_order.append (("weight", self._get_weight))
        index += 1
    # end def setup_column_types

    def _get_weight (self, message, attr) :
        if message.status.unseen :
            return 800
        return 400
    # end def _get_weight

# end class Message_Cell

class _MB_TA_ (PMA.UI.Tree_Adapter) :
    """Tree adapter for mailbox"""

    schema = \
        ( TGL.UI.Column ( "No"
                        , Message_Cell (("number", int))
                        )
        , TGL.UI.Column ( "Date"
                        , Message_Cell ("date")
                        )
        , TGL.UI.Column ( "Sender"
                        , Message_Cell ("sender")
                        , alignment = 0
                        )
        , TGL.UI.Column ( "Subject"
                        , Message_Cell ("subject")
                        , alignment = 0
                        )
        , TGL.UI.Column ( "Body"
                        , Message_Cell ("body_start")
                        , alignment = 0
                        )
        )

    def has_children (cls, message) :
        return False ### XXX threaded mails
    # end def has_children

    def children (cls, message) :
        return () ### XXX threaded mails
    # end def children

    def root_children (cls, mailbox) :
        return mailbox.messages
    # end def root_children

# end class _MB_TA_

class Mailbox_MV (PMA.UI.Tree) :
    """Message view of mailbox"""

    Adapter = _MB_TA_

# end class Mailbox_MV

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Mailbox_MV

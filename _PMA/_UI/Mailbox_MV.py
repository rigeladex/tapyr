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
#    17-Jun-2005 (MG) `Message_Cell` changed: Use new `auto_attributes` feature
#    17-Jun-2005 (MG) `Body` cell made lazy (performance reasons)
#    28-Jul-2005 (MG) `Message_Cell` style handling changed
#    30-Jul-2005 (MG) New styles added and used
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Mailbox

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Tree
import _PMA._UI.Tree_Adapter

class Message_Cell (PMA.UI.Text_Cell) :
    """A cell which uses attributes of a PMA.Message object to set style
       related attributes (background, foreground, ...)
    """

    Normal = TGL.UI.Style ("Normal")
    Unseen = TGL.UI.Style \
        ( "Unseen"
        , Normal
        , foreground = "red"
        , background = "yellow"
        )
    Copied = TGL.UI.Style \
        ( "Copied"
        , Normal
        , background = "blue"
        )
    Deleted = TGL.UI.Style \
        ( "Unseen"
        , Normal
        , foreground = "white"
        , background = "red"
        )
    Moved  = TGL.UI.Style \
        ( "Unseen"
        , Copied
        , foreground = "white"
        )

    auto_attributes     = dict \
        ( PMA.UI.Cell.auto_attributes
        , foreground    = ("foreground", str, "_style_get")
        , background    = ("background", str, "_style_get")
        )

    def _style (self, message, office = None) :
        if message.status.unseen :
            return self.Unseen
        if message.pending.deleted :
            return self.Deleted
        if message.pending.copied :
            return self.Copied
        if message.pending.moved:
            return self.Moved
        return self.Normal
    # end def _style

    def _style_get (self, message, attr_name, office = None) :
        return getattr (self._style (message, office), attr_name)
    # end def _style_get

# end class Message_Cell

class _MB_TA_ (PMA.UI.Tree_Adapter) :
    """Tree adapter for mailbox"""

    Model_Type = "List_Model"
    rules_hint = False
    schema     = \
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
                        , Message_Cell ("body_start", lazy = True)
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

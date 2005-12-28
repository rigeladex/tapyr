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
#    30-Jul-2005 (MG) `Message_Cell`: new property `no_wrap` added,
#                     `Message_Cell_FW` added and used
#    31-Jul-2005 (MG) Styles changed
#    31-Jul-2005 (CT) Styles changed (and style names fixed)
#    15-Sep-2005 (CT) `root_children` changed to return `Msg_Scope` instances
#    16-Sep-2005 (MG) `root_children` changed to use `.scope` property of
#                     message
#    28-Dec-2005 (MG) `Message_Cell._style` fixed (a msg_scope is now passed
#                     instead of the message object)
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Mailbox

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Tree
import _PMA._UI.Tree_Adapter

#  * Current message    gray92    background
# must be changed in the RC-File -> but I don't know how )o:

class Message_Cell (PMA.UI.Text_Cell) :
    """A cell which uses attributes of a PMA.Message object to set style
       related attributes (background, foreground, ...)
    """

    Normal = TGL.UI.Style ("Normal")
    Unseen = TGL.UI.Style \
        ( "Unseen", Normal
        , foreground = "red"
        , background = "yellow"
        )
    Copied = TGL.UI.Style \
        ( "Copied", Normal
        , background = "MediumAquamarine"
        )
    Deleted = TGL.UI.Style \
        ( "Deleted", Normal
        , background = "grey76"
        )
    Moved  = TGL.UI.Style \
        ( "Moved", Normal
        , background = "cyan"
        )

    auto_attributes     = dict \
        ( PMA.UI.Cell.auto_attributes
        , foreground    = ("foreground",            str,  "_style_get")
        , background    = ("background",            str,  "_style_get")
        , no_wrap       = ("single-paragraph-mode", bool, True)
        )

    def _style (self, msg_scope, office = None) :
        msg     = msg_scope.msg
        pending = msg.pending
        if msg.status.unseen :
            return self.Unseen
        if pending.deleted :
            return self.Deleted
        if pending.copied :
            return self.Copied
        if pending.moved:
            return self.Moved
        return self.Normal
    # end def _style

    def _style_get (self, msg_scope, attr_name, office = None) :
        return getattr (self._style (msg_scope, office), attr_name)
    # end def _style_get

# end class Message_Cell

class Message_Cell_FW (Message_Cell):

    width               = 15

    auto_attributes     = dict \
        ( Message_Cell.auto_attributes
        , ellipsize     = ("ellipsize",             int,  3)
        , width         = ("width-chars",           int,  "width")
        )

# end class Message_Cell_FW

class _MB_TA_ (PMA.UI.Tree_Adapter) :
    """Tree adapter for mailbox"""

    Model_Type = "List_Model"
    rules_hint = False
    schema     = \
        ( TGL.UI.Column ( "No"
                        , Message_Cell    (("number", int))
                        )
        , TGL.UI.Column ( "Date"
                        , Message_Cell    ("date")
                        )
        , TGL.UI.Column ( "Sender"
                        , Message_Cell_FW ("sender")
                        , alignment = 0
                        )
        , TGL.UI.Column ( "Subject"
                        , Message_Cell_FW ("subject", width = 35)
                        , alignment = 0
                        )
        , TGL.UI.Column ( "Body"
                        , Message_Cell    ("body_start", lazy = True)
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
        return (m.scope for m in mailbox.messages)
    # end def root_children

# end class _MB_TA_

class Mailbox_MV (PMA.UI.Tree) :
    """Message view of mailbox"""

    Adapter = _MB_TA_

# end class Mailbox_MV

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Mailbox_MV

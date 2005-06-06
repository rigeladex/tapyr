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
#    PMA.UI.Mailbox_BV
#
# Purpose
#    Abstract user interface for box-view of PMA.Mailbox
#
# Revision Dates
#     6-Jun-2005 (CT) Creation
#     6-Jun-2005 (MG) `_MB_TA_`: methods converted to classmethods
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA.Mailbox

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Tree
import _PMA._UI.Tree_Adapter

class _MB_TA_ (PMA.UI.Tree_Adapter) :
    """Tree adapter for mailbox"""

    schema = \
        ( TGL.UI.Column
            ( "Name"
            , TGL.UI.Text_Cell ("name")
            )
        ,
        )

    @classmethod
    def has_children (self, mailbox) :
        return bool (mailbox._box_dict)
    # end def has_children

    @classmethod
    def children (self, mailbox) :
        return mailbox.sub_boxes
    # end def children

# end class _MB_TA_

class Mailbox_BV (PMA.UI.Rooted_Tree) :
    """Box view of mailbox"""

    Adapter = _MB_TA_

# end class Mailbox_BV

if __name__ != "__main__" :
    PMA.UI._Export ("*")
### __END__ PMA.UI.Mailbox_BV

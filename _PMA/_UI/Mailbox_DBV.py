# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
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
#    PMA.UI.Mailbox_DBV
#
# Purpose
#    Abstract user interface for the delivery box-view
#
# Revision Dates
#    30-Dec-2005 (MG) Creation
#    ««revision-date»»···
#--

from   _TGL                    import TGL
from   _PMA                    import PMA

import _PMA._UI
import _PMA._UI.Mixin
import _PMA._UI.Tree
import _PMA._UI.Tree_Adapter
import _PMA._UI.Mailbox_BV

class Mailbox_DBV (PMA.UI.Tree) :
    """Box view of mailbox"""

    Adapter = PMA.UI._MB_TA_

# end class Mailbox_DBV

if __name__ != "__main__" :
    PMA.UI._Export ("Mailbox_DBV")
### __END__ PMA.UI.Mailbox_DBV

# -*- coding: utf-8 -*-
# Copyright (C) 2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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

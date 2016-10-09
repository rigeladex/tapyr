# -*- coding: utf-8 -*-
# Copyright (C) 2005-2016 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA.Msg_Status
#
# Purpose
#    Encapsulate status of mail message
#
# Revision Dates
#     4-Jan-2005 (CT) Creation
#    25-Jul-2005 (CT) `new` and `_Table` added (plus `load` and `save`)
#    25-Jul-2005 (CT) `_Status_` factored
#    26-Jul-2005 (CT) `load` and `save` moved back in here from `_Status_`
#    26-Jul-2005 (CT) `_Status_C_` factored
#    14-Aug-2005 (MG) use new `TGL._Status_` instead of `PMA._Status_`
#     9-Oct-2016 (CT) Move `_Status_` back to `PMA`
#    ««revision-date»»···
#--

from   _PMA                    import PMA
import _PMA._Status_

import time

class Msg_Status (PMA._Status_C_) :
    """Status of mail message"""

    first_read = property (lambda s : s._attr.get ("first_read"))
    last_read  = property (lambda s : s._attr.get ("last_read"))
    unseen     = property (lambda s : s.first_read is None)

    _Table     = {}

    def set_read (self, t = None) :
        if t is None :
            t = time.time ()
        _attr = self._attr
        if self.unseen :
            _attr ["first_read"] = t
        _attr ["last_read"] = t
        return t
    # end def set_read

# end class Msg_Status

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Msg_Status

# -*- coding: utf-8 -*-
# Copyright (C) 2005-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    PMA.Box_Status
#
# Purpose
#    Encapsulate status of mailbox
#
# Revision Dates
#    26-Jul-2005 (CT) Creation
#    26-Jul-2005 (CT) `_Status_I_` factored
#    14-Aug-2005 (MG) Use new `TGL._Status_` instead of `PMA._Status_`
#    24-Sep-2009 (CT) `prop` decorator removed
#    25-Sep-2009 (CT) Use `property` as decorator (thanks to `.setter`)
#    ««revision-date»»···
#--

from   _PMA                    import PMA
from   _TGL                    import TGL
import _TGL._Status_

class Box_Status (TGL._Status_I_) :
    """Status of mailbox"""

    def __init__ (self, box, * attr) :
        self.__dict__ ["box"] = box
        self.__super.__init__ (* attr)
    # end def __init__

    @property
    def current_message () :
        result = None
        cmn    = self._attr.get ("current_message")
        if cmn is not None :
            result = self.box.msg_dict.get (cmn)
        return result
    # end def current_message

    @current_message.setter
    def current_message () :
        self._set_attr (current_message = cm and cm.name)
    # end def current_message

# end class Box_Status

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Box_Status

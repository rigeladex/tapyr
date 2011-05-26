# -*- coding: iso-8859-15 -*-
# Copyright (C) 2005-2009 Mag. Christian Tanzer. All rights reserved
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

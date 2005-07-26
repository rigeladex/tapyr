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
#    PMA.Off_Status
#
# Purpose
#    Encapsulate status of office
#
# Revision Dates
#    26-Jul-2005 (CT) Creation
#    ««revision-date»»···
#--

from   _PMA                    import PMA
import _PMA.Mailbox
import _PMA._Status_

class Off_Status (PMA._Status_I_) :
    """Status of mailbox"""

    def __init__ (self, office, * attr) :
        self.__dict__ ["office"] = office
        self.__super.__init__ (* attr)
    # end def __init__

    def _box_prop (f) :
        name = f.__name__
        def get (self) :
            result = None
            bn     = self._attr.get (name)
            if bn is not None :
                result = PMA.Mailbox._Table.get (bn)
            return result
        def set (self, box) :
            self._set_attr (** {name : box and box.qname})
        return property (get, set)
    # end def _box_prop

    @_box_prop
    def current_box () : pass

    @_box_prop
    def target_box  () : pass

# end class Off_Status

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Off_Status

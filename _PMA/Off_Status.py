# -*- coding: utf-8 -*-
# Copyright (C) 2005-2016 Christian Tanzer. All rights reserved
# tanzer@gg32.com                                      https://www.gg32.com
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
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
#    14-Aug-2005 (MG) use new `TGL._Status_` instead of `PMA._Status_`
#     9-Oct-2016 (CT) Move `_Status_` back to `PMA`
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
        return property (get, set, doc = f.__doc__)
    # end def _box_prop

    @_box_prop
    def current_box () : pass

    @_box_prop
    def target_box  () : pass

# end class Off_Status

if __name__ != "__main__" :
    PMA._Export ("*")
### __END__ PMA.Off_Status

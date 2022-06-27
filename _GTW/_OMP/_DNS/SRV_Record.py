# -*- coding: utf-8 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This package is part of the package GTW.OMP.DNS.
# 
# This package is licensed under the terms of the BSD 3-Clause License
# <https://www.gg32.com/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    DNS.SRV_Record
#
# Purpose
#    Model a DNS SRV Record
#
# Revision Dates
#    06-Sep-2012 (RS) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _GTW._OMP._DNS           import DNS
from   _GTW._OMP._DNS.Attr_Type import *
import _GTW._OMP._DNS.Record

_Ancestor_Essence = DNS.Record

class SRV_Record (_Ancestor_Essence) :
    """A DNS SRV record"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class service (A_String) :
            """Symbolic name of service without leading `_`."""

            kind               = Attr.Primary

        # end class service

        class protocol (A_String) :
            """Symbolic name of protocol without leading `_`."""

            kind               = Attr.Primary

        # end class protocol

        class target (A_DNS_Name) :
            """Target of SRV alias."""

            kind               = Attr.Required

        # end class target

        class port (A_Int) :
            """Port of this Service."""

            kind               = Attr.Required
            min_value          = 1
            max_value          = 0xFFFF

        # end class port

        class priority (A_Int) :
            """Priority of this Service."""

            kind               = Attr.Required
            min_value          = 0
            max_value          = 0xFFFF

        # end class priority

        class weight (A_Int) :
            """Weight of this Service."""

            kind               = Attr.Required
            min_value          = 0
            max_value          = 0xFFFF

        # end class weight

    # end class _Attributes

# end class SRV_Record

if __name__ != "__main__" :
    DNS._Export ("*")
### __END__ DNS.SRV_Record

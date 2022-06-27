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
#    DNS.A_Record
#
# Purpose
#    Model a DNS A Record
#
# Revision Dates
#    06-Sep-2012 (RS) Creation
#    ««revision-date»»···
#--

from   _MOM.import_MOM          import *
from   _GTW._OMP._DNS           import DNS
from   _GTW._OMP._NET.Attr_Type import A_IP4_Address
import _GTW._OMP._DNS.Record

_Ancestor_Essence = DNS.Record

class A_Record (_Ancestor_Essence) :
    """A DNS A record"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class address (A_IP4_Address) :
            """IPv4 address for this name."""

            kind               = Attr.Primary

        # end class name

    # end class _Attributes

# end class A_Record

if __name__ != "__main__" :
    DNS._Export ("*")
### __END__ DNS.A_Record

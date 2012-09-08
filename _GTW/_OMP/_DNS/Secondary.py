# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
# #*** <License> ************************************************************#
# This package is part of the package GTW.OMP.DNS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    DNS.Secondary
#
# Purpose
#    Model a secondary DNS server
#
# Revision Dates
#    27-Aug-2012 (RS) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM          import *
from   _GTW._OMP._DNS           import DNS
from   _GTW._OMP._NET.Attr_Type import _A_Composite_IP_Address_
import _GTW._OMP._DNS.Entity
import _GTW._OMP._DNS.Zone

_Ancestor_Essence = DNS.Link1

class Secondary (_Ancestor_Essence) :
    """ Secondary DNS server.
        A secondary server is allowed Zone transfers and will be
        notified on updates.
    """

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """The zone for which this server is a secondary"""

            role_type          = DNS.Zone
            role_name          = "zone"
            ui_allow_new       = False

        # end class name

        class address (_A_Composite_IP_Address_) :
            """IP Address of secondary server"""

            kind               = Attr.Primary

        # end class address

    # end class _Attributes

# end class Secondary

if __name__ != "__main__" :
    DNS._Export ("*")
### __END__ DNS.Secondary

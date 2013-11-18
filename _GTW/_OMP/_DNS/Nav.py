# -*- coding: utf-8 -*-
# Copyright (C) 2012 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A-3411 Weidling, Austria. rsc@runtux.com
# ****************************************************************************
# This module is part of the package GTW.OMP.DNS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.DNS.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#     6-Sep-2012 (RS) Creation
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    AAAA_Record          = dict \
        ( ETM            = "GTW.OMP.DNS.AAAA_Record"
        )

    A_Record             = dict \
        ( ETM            = "GTW.OMP.DNS.A_Record"
        )

    CNAME_Record         = dict \
        ( ETM            = "GTW.OMP.DNS.CNAME_Record"
        )

    MX_Record            = dict \
        ( ETM            = "GTW.OMP.DNS.MX_Record"
        )

    NS_Record            = dict \
        ( ETM            = "GTW.OMP.DNS.NS_Record"
        )

    Secondary_IP4        = dict \
        ( ETM            = "GTW.OMP.DNS.Secondary_IP4"
        )

    Secondary_IP6        = dict \
        ( ETM            = "GTW.OMP.DNS.Secondary_IP6"
        )

    SRV_Record           = dict \
        ( ETM            = "GTW.OMP.DNS.SRV_Record"
        )

    TXT_Record           = dict \
        ( ETM            = "GTW.OMP.DNS.TXT_Record"
        )

    Zone                 = dict \
        ( ETM            = "GTW.OMP.DNS.Zone"
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.DNS._Export_Module ()
### __END__ GTW.OMP.DNS.Nav

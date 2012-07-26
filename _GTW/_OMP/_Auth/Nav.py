# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.Auth.
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
#    GTW.OMP.Auth.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    26-Feb-2010 (CT) Creation
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Remove `Form_args`, `*_completer`,
#                     i.e., stuff related to non-AFS forms
#    22-May-2012 (CT) Fix typo (`Account_P = dict`, not `Account = dict`)
#    26-Jul-2012 (CT) Import `_GTW._RST.Permission`, not `_GTW._NAV.Permission`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL.I18N                import _
from   _GTW                     import GTW

from   _GTW._RST.Permission     import Is_Superuser

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Account_P        = dict \
        ( ETM        = "GTW.OMP.Auth.Account_P"
        , permission = Is_Superuser ()
        )

    Group            = dict \
        ( ETM        = "GTW.OMP.Auth.Group"
        , permission = Is_Superuser ()
        )

    Account_in_Group = dict \
        ( ETM        = "GTW.OMP.Auth.Account_in_Group"
        , permission = Is_Superuser ()
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.Auth._Export_Module ()
### __END__ GTW.OMP.Auth.Nav

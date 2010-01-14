# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This package is part of the package GTW.
#
# This package is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this package. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.OMP.Auth.Account
#
# Purpose
#    Model an user account
#
# Revision Dates
#    13-Jan-2010 (MG) Creation
#    14-Jan-2010 (CT) `password` defined as `Required` instead of `Primary`
#    14-Jan-2010 (CT) s/Password_Account/Account_P/g
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

from   _GTW._OMP._Auth        import Auth
import _GTW._OMP._Auth.Entity

_Ancestor_Essence = MOM.Object

class _Auth_Account_ (Auth.Entity, _Ancestor_Essence) :
    """Model an user account."""

    _real_name = "Account"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class user_name (A_String) :
            """User name associated with this account"""

            kind       = Attr.Primary
            max_length = 50
            rank       = 1
            ui_name    = "Account name"

        # end class user_name

    # end class _Attributes

Account = _Auth_Account_ # end class _Auth_Account_

_Ancestor_Essence = Account

class Account_P (_Ancestor_Essence) :
    """An acount which uses passwords for authorization."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        class password (A_String) :
            """Password for this account"""

            kind       = Attr.Required
            max_length = 50

        # end class password

    # end class _Attributes

# end class Account_P

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Account

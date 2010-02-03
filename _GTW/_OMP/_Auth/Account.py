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
#    16-Jan-2010 (CT) Derive from `Auth.Object` (thus s/usernamer/name/)
#     3-Feb-2010 (MG) Password hashing added
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

from   _GTW._OMP._Auth        import Auth
import _GTW._OMP._Auth.Entity

from   _TFL.I18N              import _, _T, _Tn
import  hashlib

_Ancestor_Essence = Auth.Object

class _Auth_Account_ (_Ancestor_Essence) :
    """Model an user account."""

    _real_name = "Account"

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class active (A_Boolean) :
            """This account is currently active."""

            kind       = Attr.Optional
            default    = False
            ui_name    = _T ("User active")

        # end class active

        class name (_Ancestor.name) :
            """User name associated with this account"""

            ui_name    = _T ("Account name")

        # end class name

        class superuser (A_Boolean) :
            """This account has super-user permissions."""

            kind       = Attr.Optional
            default    = False
            ui_name    = _T ("Superuser")

        # end class superuser

    # end class _Attributes

    authenticated = True

Account = _Auth_Account_ # end class _Auth_Account_

_Ancestor_Essence = Account

class Account_Anonymous (_Ancestor_Essence) :
    """Default account for users which are not logging in."""

    max_count    = 1
    refuse_links = set (("GTW.OMP.Auth.Account_in_Group", ))

    class _Attributes (_Ancestor_Essence._Attributes) :

        class active (_Ancestor_Essence._Attributes.active) :

            kind       = Attr.Const
            default    = True

        # end class active

        class superuser (_Ancestor_Essence._Attributes.superuser) :

            kind       = Attr.Const
            default    = False

        # end class superuser

    # end class _Attributes

    authenticated = False

# end class Account_Anonymous

_Ancestor_Essence = Account

class Account_P (_Ancestor_Essence) :
    """An acount which uses passwords for authorization."""

    Hash_Method = "sha224"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class password (A_String) :
            """Password for this account"""

            kind       = Attr.Required
            max_length = 50

        # end class password

    # end class _Attributes

    @classmethod
    def password_hash (cls, password, salt = None) :
        hash = hashlib.new (cls.Hash_Method)
        if salt :
            hash.update (salt)
        hash.update     (password)
        return hash.hexdigest ()
    # end def password_hash

    def verify_password (self, password, salt = None) :
        return self.password == self.password_hash (password, salt)
    # end def verify_password

# end class Account_P

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Account

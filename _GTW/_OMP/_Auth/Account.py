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
#    18-Feb-2010 (MG) `Account_P`: `salt` added as class attribute
#    19-Feb-2010 (MG) `Account_P_Manager` added, `Account` is no longer a
#                     `Named_Object` due to restrictions of the name (could
#                     not be an email address)
#    19-Feb-2010 (MG) Change password handling added
#    ��revision-date�����
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

from   _GTW._OMP._Auth        import Auth
import _GTW._OMP._Auth.Entity

import  hashlib
import  uuid

_Ancestor_Essence = MOM.Object

class _Auth_Account_ (Auth.Entity, _Ancestor_Essence) :
    """Model an user account."""

    _real_name = "Account"

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_Email) :
            """User name associated with this account"""

            kind       = Attr.Primary

        # end class name

        class active (A_Boolean) :
            """This account is currently active."""

            kind       = Attr.Optional
            default    = False

        # end class active

        class superuser (A_Boolean) :
            """This account has super-user permissions."""

            kind       = Attr.Optional
            default    = False

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

class Account_P_Manager (_Ancestor_Essence.M_E_Type.Manager) :
    """E-Type manager for password accounts"""

    def __call__ (self, name, password) :
        etype    = self._etype
        salt     = uuid.uuid4().hex
        password = etype.password_hash (password, salt)
        return self.__super.__call__   (name, password = password, salt = salt)
    # end def __call__

    def force_password_change (self, account) :
        Auth          = self.home_scope.GTW.OMP.Auth
        if isinstance (account, basestring) :
            account   = self.query (name = account).one ()
        pw_change_for = Auth.Account_Password_Change_Required.query \
            (account  = account).first ()
        if not pw_change_for :
            pw_change_for = Auth.Account_Password_Change_Required (account)
    # end def force_password_change

# end class Account_P_Manager

class Account_P (_Ancestor_Essence) :
    """An acount which uses passwords for authorization."""

    Hash_Method = "sha224"
    Manager     = Account_P_Manager

    class _Attributes (_Ancestor_Essence._Attributes) :

        class password (A_String) :
            """Password for this account"""

            kind       = Attr.Required
            max_length = 50

        # end class password

        class salt (A_String) :
            """The salt used for the password hash."""

            kind               = Attr.Required
            max_length         = 50

        # end class salt

    # end class _Attributes

    def change_password (self, new_password) :
        self.set (password = self.password_hash (new_password, self.salt))
        pwdr = self.password_change_required
        if pwdr :
            pwdr.destroy ()
    # end def change_password

    @classmethod
    def password_hash (cls, password, salt) :
        hash = hashlib.new    (cls.Hash_Method, salt)
        hash.update           (password)
        return hash.hexdigest ()
    # end def password_hash

    def verify_password (self, password) :
        return self.password == self.password_hash (password, self.salt)
    # end def verify_password

    ### XXX remove me once cached roles are supported for Link1
    @property
    def password_change_required (self) :
        return self.home_scope.Auth.Account_Password_Change_Required.query \
            (account = self).first ()
    # end def password_change_required

# end class Account_P

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Account

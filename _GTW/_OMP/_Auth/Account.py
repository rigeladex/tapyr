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
#    19-Feb-2010 (MG) `Account`: new attributes `enabled` and `suspended`
#                     added, kind `active` changed to `Attr.Query`
#    19-Feb-2010 (MG) `reset_password` implemented
#    19-Feb-2010 (MG) Account activation added
#    20-Feb-2010 (MG) Account management functions added
#    26-Feb-2010 (CT) `authenticated` defined as alias for `active`
#    26-Feb-2010 (CT) `kind` of `suspended`, `password`, and `salt` changed
#                     to `Internal` (set by the application, not the user)
#    18-May-2010 (CT) `Account_P_Manager.__call__` replaced by
#                     `Account_P_Manager.create_new_account_x`
#    14-Oct-2010 (CT) `Init_Only_Mixin` added to `salt`
#    ««revision-date»»···
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
            """Email that serves as user name for this account"""

            kind       = Attr.Primary

        # end class name

        class active (A_Boolean) :
            """This account is currently active."""

            kind            = Attr.Query
            auto_up_depends = ("suspended", "enabled")
            query           = (Q.suspended != True) & (Q.enabled == True)

        # end class active

        class enabled (A_Boolean) :
            """This account is currently enabled (the user can login)."""

            kind       = Attr.Optional
            default    = False

        # end class enabled

        class superuser (A_Boolean) :
            """This account has super-user permissions."""

            kind       = Attr.Optional
            default    = False

        # end class superuser

        class suspended (A_Boolean) :
            """This account is currently suspended (due to a pending action)."""

            kind       = Attr.Internal
            default    = True

        # end class suspended

    # end class _Attributes

    authenticated = TFL.Meta.Alias_Property ("active")

Account = _Auth_Account_ # end class _Auth_Account_

_Ancestor_Essence = Account

class Account_Anonymous (_Ancestor_Essence) :
    """Default account for users which are not logging in."""

    max_count    = 1
    refuse_links = set (("GTW.OMP.Auth.Account_in_Group", ))

    class _Attributes (_Ancestor_Essence._Attributes) :

        class active (_Ancestor_Essence._Attributes.active) :

            kind       = Attr.Const
            default    = False

        # end class active

        class superuser (_Ancestor_Essence._Attributes.superuser) :

            kind       = Attr.Const
            default    = False

        # end class superuser

    # end class _Attributes


# end class Account_Anonymous

_Ancestor_Essence = Account

class Account_P_Manager (_Ancestor_Essence.M_E_Type.Manager) :
    """E-Type manager for password accounts"""

    def create_new_account_x (self, name, password, ** kw) :
        etype    = self._etype
        salt     = uuid.uuid4 ().hex
        password = etype.password_hash (password, salt)
        return self (name, password = password, salt = salt, ** kw)
    # end def create_new_account_x

    def create_new_account (self, name, password) :
        account = self.create_new_account_x \
            (name, password, enabled = True, suspended = True)
        AEV = self.home_scope.GTW.OMP.Auth.Account_EMail_Verification
        return account, AEV (account).token
    # end def create_new_account

    def force_password_change (self, account) :
        Auth = self.home_scope.GTW.OMP.Auth
        if isinstance (account, basestring) :
            account = self.query (name = account).one ()
        if not Auth.Account_Password_Change_Required.query \
            (account = account).count () :
            Auth.Account_Password_Change_Required (account)
    # end def force_password_change

    def reset_password (self, account) :
        Auth = self.home_scope.GTW.OMP.Auth
        if isinstance (account, basestring) :
            account = self.query (name = account).one ()
        if not account.enabled :
            raise TypeError (u"Account has been disabled")
        ### first we set the password to someting random nobody knows
        account.change_password (self._etype.random_password (32))
        ### than we create the password change request action
        self.force_password_change (account)
        ### now create a reset password action which contains the new password
        new_password = self._etype.random_password (16)
        Auth.Account_Pasword_Reset (account, password = new_password)
        ### and temporarily suspend the account
        account.set (suspended = True)
        return new_password
    # end def reset_password

# end class Account_P_Manager

class Account_P (_Ancestor_Essence) :
    """An acount which uses passwords for authorization."""

    Hash_Method = "sha224"
    Manager     = Account_P_Manager

    class _Attributes (_Ancestor_Essence._Attributes) :

        class password (A_String) :
            """Password for this account"""

            kind       = Attr.Internal
            max_length = 60

        # end class password

        class salt (A_String) :
            """The salt used for the password hash."""

            kind          = Attr.Internal
            Kind_Mixins   = (Attr.Init_Only_Mixin, )
            max_length    = 50

        # end class salt

    # end class _Attributes

    def change_email_prepare (self, new_email) :
        return self.home_scope.GTW.OMP.Auth.Account_EMail_Verification \
            (self, new_email = new_email).token
    # end def change_email_prepare

    def change_password (self, new_password, remove_actions = True, ** kw) :
        self.set \
            (password = self.password_hash (new_password, self.salt), ** kw)
        if remove_actions :
            Auth = self.home_scope.GTW.OMP.Auth
            for et in ( Auth.Account_Activation
                      , Auth.Account_Password_Change_Required
                      ) :
                for l in et.query (account = self) :
                    l.destroy ()
    # end def change_password

    @classmethod
    def password_hash (cls, password, salt) :
        hash = hashlib.new    (cls.Hash_Method, salt)
        hash.update           (password)
        return hash.hexdigest ()
    # end def password_hash

    def prepare_activation (self) :
        password = self.random_password (16)
        self.set \
            ( password  = self.password_hash (password, self.salt)
            , suspended = True
            )
        self.home_scope.GTW.OMP.Auth.Account_Activation (self)
        return password
    # end def prepare_activation

    @classmethod
    def random_password (cls, length = 16) :
        from   random import choice
        import string
        chars = string.letters + string.digits
        return "".join \
            ( [choice (chars) for i in xrange (length)])
    # end def random_password

    def verify_password (self, password) :
        return self.password == self.password_hash (password, self.salt)
    # end def verify_password

# end class Account_P

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Account

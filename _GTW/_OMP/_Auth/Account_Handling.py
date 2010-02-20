# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.OMP.Auth.Account_Handling
#
# Purpose
#    Define the links used during the create/modify process for accounts
#
# Revision Dates
#    18-Feb-2010 (MG) Creation
#    19-Feb-2010 (MG) `Account_Token_Manager` added
#    19-Feb-2010 (MG) Reorganized
#    20-Feb-2010 (MG) Account management functions added
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

from   _GTW._OMP._Auth        import Auth
import _GTW._OMP._Auth.Entity
import _GTW._OMP._Auth.Account

from   _TFL.I18N              import _, _T, _Tn
import  uuid
import  datetime

_Ancestor_Essence = Auth.Link1

class _Account_Action_ (Auth.Entity, _Ancestor_Essence) :
    """Base class for different actions for a account."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Account which this action is bound to."""

            role_type     = Auth.Account

        # end class left

    # end class _Attributes

# end class _Account_Action_

_Ancestor_Essence = _Account_Action_

class Account_Activation (_Ancestor_Essence) :
    """Activation of the account"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Account which this action is bound to."""

            auto_cache = "activation"
            max_links  = 1

        # end class left

    # end class _Attributes

# end class Account_Activation

_Ancestor_Essence = _Account_Action_

class Account_Password_Change_Required (_Ancestor_Essence) :
    """The password of the linked account must be changed after the next
       login.
    """

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class left (_Ancestor.left) :
            """Account which this action is bound to."""

            auto_cache = "password_change_required"
            max_links  = 1

        # end class left

    # end class _Attributes

# end class Account_Password_Change_Required

_Ancestor_Essence = _Account_Action_

class Account_Token_Manager (_Ancestor_Essence.M_E_Type.Manager) :
    """E-Type manager for token based account actions"""

    def __call__ (self, account, expires = None, ** kw) :
        token = uuid.uuid4 ().hex
        if not expires :
            etype   = self._etype
            expires = datetime.datetime.now ()+ etype.expire_duration_default
        return self.__super.__call__ (account, token = token, ** kw)
    # end def __call__

# end class Account_Token_Manager

class _Account_Token_Action_ (_Ancestor_Essence) :
    """Base class for account actions which have an token to identify the
       action without the account.
    """

    is_partial              = True
    Manager                 = Account_Token_Manager

    expire_duration_default = datetime.timedelta (hours = 1)

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class token (A_String) :
            """Unique token which identifies this action."""

            kind         = Attr.Primary

        # end class token

        class expires (A_Date_Time) :
            """Exipre time of this action"""

            kind         = Attr.Required

        # end class expires

    # end class _Attributes

# end class _Account_Token_Action_

_Ancestor_Essence = _Account_Token_Action_

class Account_EMail_Verification (_Ancestor_Essence) :
    """Pending email verification."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class new_email (A_Email) :
            """The new email address for the linked account."""

            kind               = Attr.Optional

        # end class new_email

    # end class _Attributes

    def handle (self, nav = None) :
        account = self.account
        next    = "/"
        if self.new_email :
            ### this the verification of a email change request
            account.set (name = self.new_email, suspended = False)
        else :
            account.set (suspended = False)
        for l in self.home_scope.GTW.OMP.Auth.Account_EMail_Verification.query \
                     (account = account) :
            l.destroy ()
        return next
    # end def handle

# end class Account_EMail_Verification

_Ancestor_Essence = _Account_Token_Action_

class Account_Pasword_Reset (_Ancestor_Essence) :
    """A password reset is pending for the linked account."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class password (A_Email) :
            """The temporaty password."""

            kind               = Attr.Required

        # end class password

    # end class _Attributes

    def handle (self, nav = None) :
        account = self.account
        account.change_password (self.password, False)
        for l in self.home_scope.GTW.OMP.Auth.Account_Pasword_Reset.query \
                     (account = account) :
            l.destroy ()
        if nav :
            return nav.href_change_pass (account)
    # end def handle

# end class Account_Pasword_Reset

if __name__ != "__main__" :
    GTW.OMP.Auth._Export ("*")
### __END__ GTW.OMP.Auth.Account_Handling

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Auth.
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
#    GTW.Form.Auth
#
# Purpose
#    Forms for authorization (login, change password, forgot password, ...)
#
# Revision Dates
#    15-Jan-2010 (MG) Creation
#    17-Jan-2010 (CT) Adapted to change of Auth.Account (s/name/username/)
#    17-Jan-2010 (MG) Clear `request_data` if the login vailed to prevent
#                     population of defaults
#    17-Jan-2010 (MG) Moved into package `GTW.Form`
#     3-Feb-2010 (MG) Pass salt to `verify_password`
#    18-Feb-2010 (MG) `salt` moved into `Account_P` e_type
#    19-Feb-2010 (MG) `Change_Password` form added
#    19-Feb-2010 (MG) `Reset_Password` form added
#    19-Feb-2010 (MG) Reorganized, Account activation added
#    20-Feb-2010 (MG) Remaining forms added
#    20-Feb-2010 (MG) `ui_name` for fields added
#    23-Feb-2010 (MG) Debug errors added to `_Login_Mixin_`
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
from   _TFL.I18N          import _T, _

from   _GTW               import GTW
import _GTW._Form.Plain
import _GTW._Form.Field
import _GTW._Form.Field_Group_Description

PWD_WS = GTW.Form.Widget_Spec ("html/field.jnj, password")

class _Login_Mixin_ (TFL.Meta.Object) :
    """Handles the login form processing."""

    active_account_required = True
    fields                  = \
        ( GTW.Form.Field ("username", ui_name = _("Username"))
        , GTW.Form.Field ("password", ui_name = _("Password"), widget = PWD_WS)
        )

    def __init__ (self, account_manager, * args, ** kw) :
        self.account_manager          = account_manager
        self.account                  = None
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _validate (self) :
        username     = self.get_required \
            ("username", _T (u"A user name is required to login."))
        password     = self.get_required \
            ("password", _T (u"The password is required."))
        if not self.field_errors :
            if not self._authenticate (username, password) :
                self.errors.append (_T (u"Username or password incorrect"))
            elif self.active_account_required and not self.account.active :
                self.errors.append (_T (u"This account is currently inactive"))
                self.account = None
        elif getattr (self.kw, "debug", False) :
            self.errors.append (repr (self.request_data))
        self.__super._validate ()
        self.request_data = {}
    # end def _validate

    def _authenticate (self, username, password) :
        debug = getattr (self.kw, "debug", False)
        try :
            self.account = self.account_manager.query (name = username).one ()
        except IndexError :
            if debug :
                self.field_errors ["username"].append \
                    (u"No account with username `%s` found" % (username, ))
            ### look's like no account with this username exists
            return False
        result = self.account.verify_password (password)
        if not result and debug :
            self.field_errors ["password"].append \
                    ( u"Password is wrong:\n"
                       "  %s\n"
                       "  hash db `%s`\n"
                       "  hash in `%s`"
                    % ( password
                      , self.account.password
                      , self.account.password_hash (password, self.account.salt)
                      )
                    )
        return result
    # end def _authenticate

# end class _Login_Mixin_

class _New_Password_ (TFL.Meta.Object) :
    """Verifies two password entries"""

    fields = \
        ( GTW.Form.Field
            ("npassword1", ui_name = _("New password"), widget = PWD_WS)
        , GTW.Form.Field
            ("npassword2", ui_name = _("Repeat new password"), widget = PWD_WS)
        )

    def _validate (self) :
        self.new_password = None
        pwd_1             = self.get_required \
            ("npassword1", _T (u"The new password is required."))
        pwd_2             = self.get_required \
            ("npassword2", _T (u"Please repeat the new password."))
        if not self.field_errors and (pwd_1 != pwd_2) :
            self.errors.append (_T (u"Passwords don't match."))
        else :
            self.new_password = pwd_1
        self.__super._validate ()
    # end def _validate

# end class _New_Password_

class _Activate_Account_Mixin_ (_Login_Mixin_, _New_Password_) :
    """Form to activate a user account after initail creation"""

    active_account_required = False
    fields                  = _Login_Mixin_.fields + _New_Password_.fields

# end class _Activate_Account_Mixin_

class _Change_Password_Mixin_ (_New_Password_) :
    """Change password form."""

    fields = \
        ( GTW.Form.Field ("password", ui_name = _("Password"), widget = PWD_WS)
        ,
        ) + _New_Password_.fields

    def __init__ (self, account, * args, ** kw) :
        self.account = account
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _validate (self) :
        self.__super._validate ()
        old_pwd      = self.get_required \
            ("password", _T (u"The old password is required."))
        if (   not (self.field_errors or self.errors)
           and not self.account.verify_password (old_pwd)
           ) :
            self.errors.append \
                (_T ("One of the passwords is incorrect"))
        self.request_data = {}
    # end def _validate

# end class _Change_Password_Mixin_

class _Change_EMail_Mixin_ (TFL.Meta.Object) :
    """Change the e-mail address of account"""

    fields = \
        ( GTW.Form.Field
            ( "new_email"
            , ui_name = _("New email address")
            , widget  = "html/field.jnj, email"
            )
        , GTW.Form.Field
            ("password", ui_name = _("Password"), widget = PWD_WS)
        )

    def __init__ (self, account, * args, ** kw) :
        self.account = account
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _validate (self) :
        old_pwd      = self.get_required \
            ("password", _T (u"The old password is required."))
        self.new_email = self.get_required \
            ("new_email", _T (u"The new E-Mail address is required."))
        if (   not self.field_errors
           and not self.account.verify_password (old_pwd)
           ) :
            self.field_errors ["password"].append \
                (_T ("The password is incorrect"))
        self.request_data.pop ("password", None)
    # end def _validate

# end class _Change_EMail_Mixin_

class _Register_Account_ (_New_Password_) :
    """Register a new account"""

    fields = \
        ( GTW.Form.Field ("username", ui_name = _("Username"))
        ,
        ) + _New_Password_.fields

    def __init__ (self, account_manager, * args, ** kw) :
        self.account_manager = account_manager
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _validate (self) :
        self.username = username = self.get_required \
            ("username", _T (u"A user name is required to login."))
        if not self.field_errors :
            account = self.account_manager.query (name = username).first ()
            if account :
                self.field_errors ["username"].append \
                    (_T ("This username is already in use."))
        self.__super._validate ()
        self.request_data = {}
    # end def _validate

# end class _Register_Account_

class _Reset_Password_Mixin_ (TFL.Meta.Object) :
    """Convert the user name into an account."""

    fields = (GTW.Form.Field ("username", ui_name = _("Username")), )

    def __init__ (self, account_manager, * args, ** kw) :
        self.account         = None
        self.account_manager = account_manager
        self.__super.__init__       (* args, ** kw)
    # end def __init__

    def _validate (self) :
        self.account = username = self.get_required \
            ("username", _T (u"A user name is required."))
        if not self.field_errors and self.account_manager :
            self.account = self.account_manager.query (name = username).first ()
            if not self.account :
                self.field_errors ["username"].append \
                    (_T ("This username is not registered"))
        self.request_data = {}
    # end def _validate

# end class _Reset_Password_Mixin_

def Define_Form (name, mixin) :
    return GTW.Form.Plain.New \
        ( name
        , GTW.Form.Field_Group_Description (* mixin.fields)
        , head_mixins = (mixin, )
        )
# end def Define_Form


Activate        = Define_Form ("Activate",        _Activate_Account_Mixin_)
Change_Email    = Define_Form ("Change_Email",    _Change_EMail_Mixin_)
Change_Password = Define_Form ("Change_Password", _Change_Password_Mixin_)
Login           = Define_Form ("Login",           _Login_Mixin_)
Register        = Define_Form ("Register",        _Register_Account_)
Reset_Password  = Define_Form ("Reset",           _Reset_Password_Mixin_)

if __name__ != "__main__" :
    GTW.Form._Export_Module ()
### __END__ GTW.Form.Auth

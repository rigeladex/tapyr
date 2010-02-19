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
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL._Meta.Object
import _TFL.I18N

from   _GTW               import GTW
import _GTW._Form.Plain
import _GTW._Form.Field
import _GTW._Form.Field_Group_Description

class _Login_Mixin_ (TFL.Meta.Object) :
    """Handles the login form processing."""

    def __init__ (self, account_manager, * args, ** kw) :
        self.account_manager          = account_manager
        self.account                  = None
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _validate (self) :
        _T           = TFL.I18N._T
        username     = self.get_required \
            ("username", _T (u"A user name is required to login."))
        password     = self.get_required \
            ("password", _T (u"The password is required."))
        if (    not self.field_errors
           and not self._authenticate (username, password)
           ) :
            self.errors.append (_T (u"Username or password incorrect"))
        self.request_data = {}
    # end def _validate

    def _authenticate (self, username, password) :
        try :
            self.account = self.account_manager.query (name = username).one ()
        except IndexError :
            ### look's like no account with this username exists
            return False
        return self.account.verify_password (password)
    # end def _authenticate

# end class _Login_Mixin_

class _Change_Password_Mixin_ (TFL.Meta.Object) :
    """The suer wnat's to change his/her password"""

    def __init__ (self, account, * args, ** kw) :
        self.account = account
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _validate (self) :
        _T           = TFL.I18N._T
        old_pwd      = self.get_required \
            ("opassword", _T (u"The old password is required."))
        pwd_1        = self.get_required \
            ("npassword1", _T (u"The new password is required."))
        pwd_2        = self.get_required \
            ("npassword2", _T (u"Please repeat the new password."))
        if not self.field_errors :
            if not self.account.verify_password (old_pwd) :
                self.field_errors ["opassword"].append \
                    (_T ("The old password is incorrect"))
            elif (pwd_1 != pwd_2) :
                self.errors.append (_T (u"Passwords don't match."))
            else :
                self.account.change_password (pwd_1)
        self.__super._validate ()
    # end def _validate

# end class _Change_Password_Mixin_

PWD_WS = GTW.Form.Widget_Spec ("html/field.jnj, password")

Login  = GTW.Form.Plain.New \
    ( "Login"
    , GTW.Form.Field_Group_Description
        ( GTW.Form.Field ("username")
        , GTW.Form.Field ("password", widget = PWD_WS)
        )
    , head_mixins = (_Login_Mixin_, )
    )
Change_Password = GTW.Form.Plain.New \
    ( "Change_Password"
    , GTW.Form.Field_Group_Description
        ( GTW.Form.Field ( "opassword",  widget = PWD_WS)
        , GTW.Form.Field ( "npassword1", widget = PWD_WS)
        , GTW.Form.Field ( "npassword2", widget = PWD_WS)
        )
    , head_mixins = (_Change_Password_Mixin_, )
    )

if __name__ != "__main__" :
    GTW.Form._Export_Module ()
### __END__ GTW.Form.Auth

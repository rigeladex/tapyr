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
#    GTW.Auth.Forms
#
# Purpose
#    Forms for authorization (login, change password, forgot password, ...)
#
# Revision Dates
#    15-Jan-2010 (MG) Creation
#    17-Jan-2010 (CT) Adapted to change of Auth.Account (s/name/username/)
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.I18N

from   _GTW             import GTW
import _GTW._Auth
import _GTW._Form.Plain
import _GTW._Form.Field
import _GTW._Form.Field_Group_Description

class Login (GTW.Form.Plain) :
    """The login form."""

    username_field = "username"
    password_field = "password"

    def __init__ \
            ( self, account_manager
            , action         = "/login/"
            , username_field = None
            , password_field = None
            ) :
        self.account_manager = account_manager
        self.username_field  = username_field or self.username_field
        self.password_field  = password_field or self.password_field
        F   = GTW.Form.Field
        fgd = GTW.Form.Field_Group_Description \
            ( F (self.username_field)
            , F (self.password_field, widget = "html/field.jnj, password")
            )
        self.__super.__init__ (action, None, fgd)
    # end def __init__

    def __call__ (self, request_data) :
        self.request_data.update (request_data)
        _T           = TFL.I18N._T
        errors       = []
        field_errors = TFL.defaultdict (list)
        username     = self.get_field \
            ( self.username_field
            , field_errors
            , _T (u"A user name is required to login.")
            )
        password     = self.get_field \
            ( self.password_field
            , field_errors
            , _T (u"The password is required.")
            )
        if not field_errors and not self._authenticate (username, password) :
            self.errors.append (_T (u"Username or password incorrect"))
        return self.__super.__call__ (request_data, errors, field_errors)
    # end def __call__

    def _authenticate (self, username, password) :
        try :
            account = self.account_manager.query (name = username).one ()
        except IndexError :
            ### look's like no account with this username exists
            return False
        return account.verify_password (password)
    # end def _authenticate

# end class Login

if __name__ != "__main__" :
    GTW.Auth._Export_Module ()
### __END__ GTW.Auth.Forms

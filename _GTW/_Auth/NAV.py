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
#    GTW.Auth.NAV
#
# Purpose
#    Navigation classes for authorization (login, logout, change password, ...)
#
# Revision Dates
#    15-Jan-2010 (MG) Creation
#    ��revision-date�����
#--

from   _TFL               import TFL
import _TFL.I18N

from   _GTW             import GTW
import _GTW._Auth.Forms
import _GTW._NAV.Base

class Login (GTW.NAV.Page) :
    """The login handling page in the navigation"""

    hidden         = False
    username_field = "username"
    password_field = "password"

    def _view (self, handler) :
        try :
            return self.__super._view (handler)
        except self.top.HTTP.Redirect_302 :
            ### Authentication was successful, let's set the username as a
            ### cookie
            handler.set_secure_cookie \
                ("username", handler.get_argument (self.username_field))
            raise
    # end def _view

    def rendered (self, context) :
        request = context ["request"]
        lf      = GTW.Auth.Forms.Login \
            ( self.account_manager
            , self.name
            , self.username_field
            , self.password_field
            )
        context ["login_form"] = lf
        if request.method == "POST" :
            if not lf (request.arguments) :
                next = request.arguments.get ("next") [0]
                raise self.top.HTTP.Redirect_302 (next)
        return self.__super.rendered (context)
    # end def rendered

# end class Login

class Logout (GTW.NAV.Page) :
    """Handle the logout process for a user."""

    def _view (self, handler) :
        handler.clear_cookie ("username")
        print "Redirect to ", handler.request.headers.get ("Referer", "/")
        raise self.top.HTTP.Redirect_302 \
            (handler.request.headers.get ("Referer", "/"))
    # end def _view

# end class Logout

if __name__ != "__main__" :
    GTW.Auth._Export_Module ()
### __END__ GTW.Auth.NAV

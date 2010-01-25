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
#    GTW.NAV.Auth
#
# Purpose
#    Navigation classes for authorization (login, logout, change password, ...)
#
# Revision Dates
#    15-Jan-2010 (MG) Creation
#    17-Jan-2010 (MG) Moved into package `GTW.NAV`
#    17-Jan-2010 (MG) `Logout`: Redirect the `/` if the new page after logout
#                     requires a login
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.I18N

from   _GTW             import GTW
import _GTW._Form.Auth
import _GTW._NAV.Base
import _GTW._Tornado.Request_Data

import  urlparse

class Login (GTW.NAV.Page) :
    """The login handling page in the navigation"""

    hidden         = False

    def rendered (self, handler, template = None) :
        context   = handler.context
        request   = handler.request
        req_data  = GTW.Tornado.Request_Data (request.arguments)
        form      = GTW.Form.Auth.Login (self.account_manager, self.name)
        context ["login_form"] = form
        if request.method == "POST" :
            errors = form (req_data)
            if not errors :
                next = req_data.get ("next")
                handler.set_secure_cookie ("username", req_data  ["username"])
                raise self.top.HTTP.Redirect_302 (next)
        return self.__super.rendered (handler, template)
    # end def rendered

# end class Login

class Logout (GTW.NAV.Page) :
    """Handle the logout process for a user."""

    def _view (self, handler) :
        handler.clear_cookie ("username")
        top       = self.top
        next      = handler.request.headers.get ("Referer", "/")
        next_page = top.page_from_href          (urlparse.urlsplit (next).path)
        if getattr (next_page, "login_required", False) :
            next = "/"
        raise top.HTTP.Redirect_302 (next)
    # end def _view

# end class Logout

if __name__ != "__main__" :
    GTW.NAV._Export_Module ()
### __END__ GTW.NAV.Auth

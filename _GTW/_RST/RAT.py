# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.MOM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.MOM
#
# Purpose
#    RESTful resource for REST authentication token
#
# Revision Dates
#     1-May-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Auth_Mixin
import _GTW._RST.Resource
import _GTW._RST.HTTP_Method
import _GTW._RST.Mime_Type

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe

import _TFL.Password_Hasher

import datetime
import time

_Ancestor = GTW.RST.Leaf

class RAT (GTW.RST.Auth_Mixin, _Ancestor) :
    """RESTful resource for REST authentication token"""

    cookie_kw                  = dict \
        ( httponly             = True
        , secure               = True
        )
    exclude_robots             = True
    hidden                     = True
    ignore_picky_accept        = True
    pid                        = "RAT"
    use_name_for_cookie        = True

    GET                        = None
    HEAD                       = None

    if __debug__ :
        class RAT_GET (_Ancestor.GET) :

            _real_name             = "GET"
            _renderers             = (GTW.RST.TOP.HTML, )

            def _response_body (self, resource, request, response) :
                return """
                    <html>
                      <head><title>RAT Test Form</title></head>
                      <body>
                        <form class="Login" method="post" action="/RAT">
                          <p>
                          <label>
                            Username
                            <input name="username" type="text">
                          </label>
                          <p>
                          <label>
                            Password
                            <input name="password" type="password">
                          </label>
                          <p>
                          <input type="submit" name="Submit" value="Login"
                            title="Submit username and password"
                          >
                        </form>
                      </body>
                    </html>
                """
            # end def _response_body

        GETXXX =  RAT_GET # end class


    class RAT_POST (GTW.RST.Auth_Mixin.POST) :

        _real_name             = "POST"
        _renderers             = (GTW.RST.Mime_Type.JSON, )

        def _response_body (self, resource, request, response) :
            debug    = getattr (resource.top, "DEBUG", False)
            req_data = request.req_data
            result   = {}
            self.errors = GTW.RST.Errors ()
            username, password = self._credentials_validation \
                (resource, request, debug = debug)
            if self.errors :
                result ["errors"]    = self.errors
                response.status_code = 400
            else :
                account = self.account
                cn      = resource.pid
                scope   = account.home_scope
                rat     = result [cn] = response.set_secure_cookie \
                    ( name     = cn
                    , data     = account.name if resource.use_name_for_cookie
                                     else str (account.pid)
                    , expires  = None
                    , max_age  = resource.session_ttl
                    , secrets  =
                        ( account.password
                        , scope.db_meta_data.dbid
                        )
                    , ** resource.cookie_kw
                    )
            return result
        # end def _response_body

    POST = RAT_POST # end class

# end class RAT

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.MOM

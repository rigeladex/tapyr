# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    Navigation directory for handling authorization (of a single user)
#
# Revision Dates
#    18-Feb-2010 (CT) Creation
#    19-Feb-2010 (MG) `Login` fixed
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL
from   _MOM.import_MOM          import Q

import _GTW._NAV.Base
import _GTW._Form.Auth
import _GTW._Tornado.Request_Data

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pjoin

import urlparse

class Auth (GTW.NAV.Dir) :
    """Navigation directory for handling authorization (of a single user)."""

    T = TFL.I18N.Name

    class _Cmd_ (GTW.NAV._Site_Entity_) :

        implicit     = True

    # end class _Cmd_

    class Action (_Cmd_) :

#       template     = "???"

        def rendered (self, handler, template = None) :
            pass
        # end def rendered

    # end class Action

    class Change_Email (_Cmd_) :

#       template     = "???"

        def rendered (self, handler, template = None) :
            pass
        # end def rendered

    # end class Change_Email

    class Change_Password (_Cmd_) :

#       template     = "???"

        def rendered (self, handler, template = None) :
            pass
        # end def rendered

    # end class Change_Password

    class Login (_Cmd_) :

        template = "login.jnj"

        def rendered (self, handler, template = None) :
            context   = handler.context
            request   = handler.request
            form      = GTW.Form.Auth.Login (self.account_manager, self.name)
            context ["login_form"] = form
            if request.method == "POST" :
                HTTP      = self.top.HTTP
                req_data  = HTTP.Request_Data (request.arguments)
                errors    = form (req_data)
                if not errors :
                    next = req_data.get ("next")
                    handler.set_secure_cookie \
                        ("username", req_data  ["username"])
                    raise HTTP.Redirect_302 (next)
                ### after a failed login, clear the current username
                handler.clear_cookie ("username")
            return self.__super.rendered (handler, template)
        # end def rendered

    # end class Login

    class Logout (_Cmd_) :

        def _view (self, handler) :
            handler.clear_cookie ("username")
            top       = self.top
            next      = handler.request.headers.get ("Referer", "/")
            next_page = top.page_from_href (urlparse.urlsplit (next).path)
            if getattr (next_page, "login_required", False) :
                next = "/"
            raise top.HTTP.Redirect_302 (next)
        # end def _view

    # end class Logout

    class Register (_Cmd_) :

#       template     = "???"

        def rendered (self, handler, template = None) :
            pass
        # end def rendered

    # end class Register

    class Reset_Password (_Cmd_) :

#       template     = "???"

        def rendered (self, handler, template = None) :
            pass
        # end def rendered

    # end class Reset_Password

    @Once_Property
    def href (self) :
        return pjoin (self.prefix, u"")
    # end def href

    def href_account (self, obj) :
        return pjoin (self.abs_href, self.T.account, obj.lid)
    # end def href_account

    def href_action (self, obj, token) :
        return pjoin (self.abs_href, self.T.action, obj.lid, token)
    # end def href_action

    def href_change_email (self, obj) :
        return pjoin (self.href_account (obj), self.T.change_email)
    # end def href_change_email

    def href_change_pass (self, obj) :
        return pjoin (self.href_account (obj), self.T.change_password)
    # end def href_change_pass

    def href_login (self) :
        return pjoin (self.abs_href, self.T.login)
    # end def href_login

    def href_logout (self) :
        return pjoin (self.abs_href, self.T.login)
    # end def href_logout

    def href_register (self) :
        return pjoin (self.abs_href, self.T.register)
    # end def href_register

    def href_reset_pass (self, obj) :
        return pjoin (self.href_account (obj), self.T.reset_password)
    # end def href_reset_pass

    def rendered (self, handler, template = None) :
        page = self._get_child (self.T.login)
        return page.rendered (handler, template)
    # end def rendered

    _child_name_map = dict \
        ( action          = (Action,              2)
        , change_email    = (Change_Email,        2)
        , change_password = (Change_Password,     2)
        , login           = (Login,               0)
        , logout          = (Logout,              0)
        , register        = (Register,            0)
        , reset_password  = (Reset_Password,      2)
        )

    def _get_child (self, child, * grandchildren) :
        if child in self._child_name_map : ### XXX L10N kills this
            T, n = self._child_name_map [child]
            if len (grandchildren) == n :
                name = pjoin (child, * grandchildren)
                return T (parent = self, name = name, args = grandchildren)
    # end def _get_child

# end class Auth

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Auth

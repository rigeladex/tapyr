# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
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
#    19-Feb-2010 (MG) `Change_Password`, `Reset_Password`, and
#                     `Request_Reset_Password` implemented
#    19-Feb-2010 (CT) `SUPPORTED_METHODS` added
#    19-Feb-2010 (MG) `Activate` added
#    20-Feb-2010 (MG) Missing functions added
#    20-Feb-2010 (MG) Action expiration handling added
#    20-Feb-2010 (MG) Notification added
#    20-Feb-2010 (CT) Use symbolic names for templates
#    22-Feb-2010 (CT) Use `request.req_data` instead of home-grown code
#    23-Feb-2010 (MG) `Login.rendered` handling of password reset added
#    23-Feb-2010 (MG) Pass debug option to login form
#    23-Feb-2010 (MG) `Login.rendered` password reset handling changed
#    24-Feb-2010 (CT) `_Cmd_`: s/GTW.NAV._Site_Entity_/GTW.NAV.Page/
#    24-Feb-2010 (CT) `own_links` redefined
#    12-May-2010 (CT) Use `pid`, not `lid`
#    29-Jun-2010 (CT) Use `request.host` instead of `site_url`
#    23-Jul-2010 (MG) Notification handling simplified
#    10-Dec-2010 (CT) `Request_Reset_Password.rendered` fixed
#                     (s/add_notifications/add_notification/)
#    15-Dec-2010 (CT) `request.url_root` added to `href_action`
#    15-Dec-2010 (CT) Calls to `send_email` guarded with exception handler
#    15-Dec-2010 (CT) `Request_Reset_Password` implemented
#     3-Jan-2011 (CT) Introduce `template_name`
#    11-Mar-2011 (CT) Moved `username` from cookie to `session`
#    11-Jun-2012 (CT) Remove trailing `/` from `href`
#    18-Jun-2012 (CT) Rename `email` to `email_from`
#    28-Jan-2013 (CT) Fix spelling of `Action_Expired`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL
from   _MOM.import_MOM          import Q

import _GTW.Notification
import _GTW._NAV.Base
import _GTW._Form.Auth

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pjoin

import urlparse

class Auth (GTW.NAV.Dir) :
    """Navigation directory for handling authorization (of a single user)."""

    pid      = "Auth"
    T        = TFL.I18N.Name

    class _Cmd_ (GTW.NAV.Page) :

        implicit          = True
        SUPPORTED_METHODS = set (("GET", "POST"))

    # end class _Cmd_

    class Action (_Cmd_) :

        SUPPORTED_METHODS = set (("GET", ))

        def rendered (self, handler, template = None) :
            top       = self.top
            HTTP      = top.HTTP
            ETM       = top.account_manager
            account   = ETM.pid_query (self.args [0])
            action    = top.scope.GTW.OMP.Auth._Account_Token_Action_.query \
                (account = account, token = self.args [1]).first ()
            if action :
                try :
                    next = action.handle (self)
                    handler.session.notifications.append \
                        ( GTW.Notification
                            (_T ("EMail verification successful."))
                        )
                    raise HTTP.Redirect_302 (next)
                except GTW.OMP.Auth.Action_Expired :
                    action.destroy       ()
                    top.scope.commit     ()
                    raise HTTP.Error_404 ()
            raise HTTP.Error_404 ()
        # end def rendered

    # end class Action

    class Activate (_Cmd_) :
        """Account activation"""

        template_name = "account_activate"

        def rendered (self, handler, template = None) :
            top     = self.top
            ETM     = top.account_manager
            form    = GTW.Form.Auth.Activate (ETM, self.abs_href)
            context = handler.context
            request = handler.request
            context ["form"] = form
            if request.method == "POST" :
                HTTP      = top.HTTP
                req_data  = request.req_data
                errors    = form (req_data)
                if not errors :
                    account = form.account
                    next    = req_data.get ("next", "/")
                    account.change_password \
                        (form.new_password, suspended = False)
                    handler.username = account.name
                    handler.session.notifications.append \
                        (GTW.Notification (_T ("Activation successful.")))
                    raise HTTP.Redirect_302   (next)
            return self.__super.rendered (handler, template)
        # end def rendered

    # end class Activate

    class Change_Email (_Cmd_) :

        template_name      = "account_change_email"
        new_email_template = "account_verify_new_email"
        old_email_template = "account_change_email_info"

        def rendered (self, handler, template = None) :
            top     = self.top
            ETM     = top.account_manager
            account = ETM.pid_query (self.args [0])
            form    = GTW.Form.Auth.Change_Email (account, self.abs_href)
            context = handler.context
            request = handler.request
            host    = request.host
            context ["form"] = form
            if request.method == "POST" :
                HTTP     = top.HTTP
                req_data = request.req_data
                errors   = form (req_data)
                if not errors :
                    next  = req_data.get ("next", "/")
                    token = account.change_email_prepare (form.new_email)
                    link  = self.parent.href_action (account, token, request)
                    try :
                        self.send_email \
                            ( self.new_email_template
                            , email_to      = form.new_email
                            , email_subject =
                                _T ("Email confirmation for %s") % (host, )
                            , email_from    = self.email_from
                            , link          = link
                            , NAV           = self.top
                            , page          = self
                            , host          = host
                            )
                    except Exception as exc :
                        form.errors.add (form, None, str (exc))
                    else :
                        handler.session.notifications.append \
                            ( GTW.Notification
                                (_T ( "A confirmation email has been sent to "
                                      "the new email address."
                                    )
                                )
                            )
                        ### XXX Send info email to old email
                        raise HTTP.Redirect_302 (next)
            return self.__super.rendered (handler, template)
        # end def rendered

    # end class Change_Email

    class Change_Password (_Cmd_) :

        template_name = "account_change_password"

        def rendered (self, handler, template = None) :
            top     = self.top
            ETM     = top.account_manager
            account = ETM.pid_query (self.args [0])
            form    = GTW.Form.Auth.Change_Password (account, self.abs_href)
            context = handler.context
            request = handler.request
            context ["form"] = form
            if request.method == "POST" :
                HTTP     = top.HTTP
                req_data = request.req_data
                errors   = form (req_data)
                if not errors :
                    next  = req_data.get ("next", "/")
                    account.change_password \
                        (form.new_password, suspended = False)
                    handler.username = account.name
                    handler.session.notifications.append \
                        ( GTW.Notification
                            (_T ("The password has been changed."))
                        )
                    raise HTTP.Redirect_302   (next)
            return self.__super.rendered (handler, template)
        # end def rendered

    # end class Change_Password

    class Login (_Cmd_) :

        template_name = "login"

        def rendered (self, handler, template = None) :
            context   = handler.context
            request   = handler.request
            top       = self.top
            form      = GTW.Form.Auth.Login \
                (top.account_manager, self.abs_href)
            context ["login_form"] = form
            if request.method == "POST" :
                HTTP      = top.HTTP
                req_data  = request.req_data
                if req_data.get ("Reset") :
                    ### Ths user has clicked on the rest password button
                    return self.parent._get_child \
                        (self.T.request_reset_password).rendered (handler)
                else :
                    errors = form (req_data)
                    if not errors :
                        next = req_data.get ("next", "/")
                        if form.account.password_change_required :
                            ### a password change is required -> redirect to
                            ### that page
                            next = self.href_change_pass (form.account)
                        else :
                            handler.username = username = req_data ["username"]
                            handler.add_notification \
                                (_T ("Welcome %s.") % (username, ))
                        raise HTTP.Redirect_302 (next)
                    ### after a failed login, clear the current username
                    handler.username = None
            else :
                context ["next"] = handler.request.headers.get ("Referer", "/")
            return self.__super.rendered (handler, template)
        # end def rendered

    # end class Login

    class Logout (_Cmd_) :

        def _view (self, handler) :
            handler.username = None
            top       = self.top
            next      = handler.request.headers.get ("Referer", "/")
            next_page = top.page_from_href (urlparse.urlsplit (next).path)
            if getattr (next_page, "login_required", False) :
                next = "/"
            handler.add_notification (_T ("Logout successful."))
            raise top.HTTP.Redirect_302 (next)
        # end def _view

    # end class Logout

    class Register (_Cmd_) :

        template_name  = "account_register"
        email_template = "account_verify_email"

        def rendered (self, handler, template = None) :
            context   = handler.context
            request   = handler.request
            host      = request.host
            top       = self.top
            form      = GTW.Form.Auth.Register \
                (top.account_manager, self.abs_href)
            context ["form"] = form
            if request.method == "POST" :
                HTTP      = top.HTTP
                req_data  = request.req_data
                errors    = form (req_data)
                if not errors :
                    Auth  = top.scope.GTW.OMP.Auth
                    next  = req_data.get ("next", "/")
                    account, token = Auth.Account_P.create_new_account \
                        (form.username, form.new_password)
                    link  = self.parent.href_action (account, token, request)
                    try :
                        self.send_email \
                            ( self.email_template
                            , email_to      = form.username
                            , email_subject =
                                _T ("Email confirmation for %s") % (host, )
                            , email_from    = self.email_from
                            , link          = link
                            , NAV           = self.top
                            , page          = self
                            , host          = host
                            )
                    except Exception as exc :
                        form.errors.add (form, None, str (exc))
                    else :
                        handler.add_notification \
                            (_T ( "A confirmation has been sent to your email "
                                  "address."
                                )
                            )
                        raise HTTP.Redirect_302 (next)
                ### after a failed login, clear the current username
                handler.username = None
            return self.__super.rendered (handler, template)
        # end def rendered

    # end class Register

    class Request_Reset_Password (_Cmd_) :
        """Initiate the reset password procedure."""

        template_name  = "account_reset_password"
        email_template = "account_reset_password_email"

        def rendered (self, handler, template = None) :
            context   = handler.context
            request   = handler.request
            top       = self.top
            host      = request.host
            form      = GTW.Form.Auth.Reset_Password \
                (top.account_manager, self.abs_href)
            context ["form"] = form
            if request.method == "POST" :
                HTTP      = top.HTTP
                req_data  = request.req_data
                errors    = form (req_data)
                if not errors :
                    Auth    = top.scope.GTW.OMP.Auth
                    account = form.account
                    passwd, token = Auth.Account_P.reset_password (account)
                    next      = handler.request.headers.get ("Referer", "/")
                    next_page = top.page_from_href \
                        (urlparse.urlsplit (next).path)
                    link  = self.parent.href_action (account, token, request)
                    self.send_email \
                        ( self.email_template
                        , email_to      = form.username
                        , email_subject =
                            ( _T ("Password reset for user %s on website %s")
                            % (form.username, host)
                            )
                        , email_from    = self.email_from
                        , new_password  = passwd
                        , link          = link
                        , NAV           = self.top
                        , page          = self
                        , host          = host
                        )
                    handler.add_notification \
                        ( GTW.Notification
                            (_T ( "The reset password instructions have been "
                                  "sent to your email address."
                                )
                            )
                        )
                    raise HTTP.Redirect_302 (next)
            return self.__super.rendered    (handler, template)
        # end def rendered

    # end class Request_Reset_Password

    @Once_Property
    def href (self) :
        return self.prefix.rstrip ("/")
    # end def href

    def href_action (self, obj, token, request) :
        result = \
            ( request.url_root
            + pjoin (self.abs_href, self.T.action, str (obj.pid), token)
            )
        return result
    # end def href_action

    def href_change_email (self, obj) :
        return pjoin (self.abs_href, self.T.change_email, str (obj.pid))
    # end def href_change_email

    def href_change_pass (self, obj) :
        return pjoin (self.abs_href, self.T.change_password, str (obj.pid))
    # end def href_change_pass

    @property
    def href_login (self) :
        return pjoin (self.abs_href, self.T.login)
    # end def href_login

    @property
    def href_logout (self) :
        return pjoin (self.abs_href, self.T.logout)
    # end def href_logout

    @property
    def href_register (self) :
        return pjoin (self.abs_href, self.T.register)
    # end def href_register

    @property
    def href_reset_password (self) :
        return pjoin (self.abs_href, self.T.request_reset_password)
    # end def href_reset_password

    @property
    def own_links (self) :
        return ()
    # end def own_links

    def rendered (self, handler, template = None) :
        page = self._get_child (self.T.login)
        return page.rendered (handler, template)
    # end def rendered

    _child_name_map = dict \
        ( action                  = (Action,                 2)
        , activate                = (Activate,               0)
        , change_email            = (Change_Email,           1)
        , change_password         = (Change_Password,        1)
        , login                   = (Login,                  0)
        , logout                  = (Logout,                 0)
        , register                = (Register,               0)
        , request_reset_password  = (Request_Reset_Password, 0)
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

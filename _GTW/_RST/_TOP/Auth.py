# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.
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
#    GTW.RST.TOP.Auth
#
# Purpose
#    Authorization for tree of pages
#
# Revision Dates
#     9-Jul-2012 (CT) Creation (based on GTW.NAV.Auth)
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.Notification
import _GTW._Form.Auth
import _GTW._RST.HTTP_Method
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pp_join
from   urllib                   import urlencode

import urlparse

_Ancestor = GTW.RST.TOP.Page

class _Cmd_ (_Ancestor) :

    implicit = True

# end class _Cmd_

class _Form_Cmd_ (_Cmd_) :

    class _Form_Cmd__GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        _rc_form_name          = "form"

        _do_change_info        = _Ancestor.GET._do_change_info_skip

        def _render_context (self, resource, request, response, ** kw) :
            kw [self._rc_form_name] = resource.form
            return self.__super._render_context \
                (resource, request, response, ** kw)
        # end def _render_context

    GET = _Form_Cmd__GET_ # end class

    class _Form_Cmd__POST_ (GTW.RST.TOP.HTTP_Method_Mixin, GTW.RST.POST) :

        _real_name             = "POST"

        _do_change_info        = GTW.RST.POST._do_change_info_skip

    POST = _Form_Cmd__POST_ # end class

    @Once_Property
    def form (self) :
        name = self.__class__.__name__.strip ("_")
        T    = getattr (GTW.Form.Auth, name)
        return T (self.top.account_manager, self.abs_href)
    # end def form

# end class _Form_Cmd_

_Ancestor = _Cmd_

class _Action_ (_Ancestor) :

    class _Action__GET_ (_Ancestor.GET) :

        ### XXX should be done with POST, not GET !!!

        _real_name             = "GET"

        def _response_body (self, resource, request, response) :
            req_data     = request.req_data
            top          = resource.top
            HTTP_Status  = top.Status
            ETM          = top.account_manager
            account      = ETM.pid_query (req_data ["p"])
            action       = top.scope.GTW.OMP.Auth._Account_Token_Action_.query \
                (account = account, token = req_data ["t"]).first ()
            if action :
                try :
                    next = action.handle (resource)
                    response.add_notification \
                        ( GTW.Notification
                            (_T ("Email verification successful."))
                        )
                    raise HTTP_Status.See_Other (next)
                except GTW.OMP.Auth.Action_Exipred :
                    action.destroy      ()
                    top.scope.commit    ()
            raise HTTP_Status.Not_Found ()
        # end def _response_body

    GET = _Action__GET_ # end class

# end class _Action_

_Ancestor = _Form_Cmd_

class _Activate_ (_Ancestor) :

    page_template_name = "account_activate"

    class _Activate__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data    = request.req_data
            top         = resource.top
            HTTP_Status = top.Status
            form        = resource.form
            errors      = form (req_data)
            if errors :
                result  = resource.GET ()._response_body \
                    (resource, request, response)
                return result
            else :
                account = form.account
                next    = req_data.get ("next", "/")
                account.change_password (form.new_password, suspended = False)
                response.username = account.name
                response.add_notification \
                    (GTW.Notification (_T ("Activation successful.")))
                raise HTTP_Status.See_Other (next)
        # end def _response_body

    POST = _Activate__POST_ # end class

# end class _Activate_

_Ancestor = _Form_Cmd_

class _Change_Email_ (_Ancestor) :

    page_template_name = "account_change_email"
    new_email_template = "account_verify_new_email"
    old_email_template = "account_change_email_info"

    class _Change_Email__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data    = request.req_data
            top         = resource.top
            HTTP_Status = top.Status
            ETM         = top.account_manager
            account     = ETM.pid_query (req_data ["p"])
            form        = resource.form
            errors      = form (req_data)
            if not errors :
                next  = req_data.get ("next", "/")
                host  = request.host
                token = account.change_email_prepare (form.new_email)
                link  = resource.parent.href_action (account, token, request)
                try :
                    resource.send_email \
                        ( resource.new_email_template
                        , email_to      = form.new_email
                        , email_subject =
                            _T ("Email confirmation for %s") % (host, )
                        , email_from    = resource.email_from
                        , link          = link
                        , NAV           = top
                        , page          = resource
                        , host          = host
                        )
                except Exception as exc :
                    form.errors.add (form, None, str (exc))
                else :
                    response.add_notification \
                        ( GTW.Notification
                            (_T ( "A confirmation email has been sent to "
                                  "the new email address."
                                )
                            )
                        )
                    ### XXX Send info email to old email
                    raise HTTP_Status.See_Other (next)
            result = resource.GET ()._response_body \
                (resource, request, response)
            return result
        # end def _response_body

    POST = _Change_Email__POST_ # end class

# end class _Change_Email_

_Ancestor = _Form_Cmd_

class _Change_Password_ (_Ancestor) :

    page_template_name = "account_change_password"

    class _Change_Password__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data    = request.req_data
            top         = resource.top
            HTTP_Status = top.Status
            ETM         = top.account_manager
            account     = ETM.pid_query (req_data ["p"])
            form        = resource.form
            errors      = form (req_data)
            if errors :
                result  = resource.GET ()._response_body \
                    (resource, request, response)
                return result
            else :
                next = req_data.get ("next", "/")
                account.change_password (form.new_password, suspended = False)
                response.username = account.name
                response.add_notification \
                    (GTW.Notification (_T ("The password has been changed.")))
                raise HTTP_Status.See_Other (next)
        # end def _response_body

    # end class _Change_Password__POST_

# end class _Change_Password_

_Ancestor = _Form_Cmd_

class _Login_ (_Ancestor) :
    """Login page"""

    page_template_name = "login"

    class _Login__GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        _rc_form_name          = "login_form"

        def _render_context (self, resource, request, response, ** kw) :
            kw.setdefault ("next", request.referrer or "/")
            return self.__super._render_context \
                (resource, request, response, ** kw)
        # end def _render_context

    GET = _Login__GET_ # end class

    class _Login__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data = request.req_data
            if req_data.get ("Reset") :
                resetter = resource._get_child ("request_reset_password")
                result   = resetter.POST ()._response_body \
                    (resetter, request, response)
                return result
            else :
                form   = resource.form
                errors = form (req_data)
                if errors :
                    ### clear `username` in re-displayed form
                    response.username = None
                    result = resource.GET ()._response_body \
                        (resource, request, response)
                    return result
                else :
                    next = req_data.get ("next", "/")
                    if form.account.password_change_required :
                        ### a password change is required -> redirect to
                        ### that page
                        next = resource.href_change_pass (form.account)
                    else :
                        username          = req_data ["username"]
                        response.username = username
                        response.add_notification \
                            (_T ("Welcome %s.") % (username, ))
                    raise resource.Status.See_Other (next)
        # end def _response_body

    POST = _Login__POST_ # end class

# end class _Login_

_Ancestor = _Cmd_

class _Logout_ (_Ancestor) :

    GET = None

    class _Logout__POST_ (_Form_Cmd_.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            top       = resource.top
            next      = request.referrer or "/"
            next_page = top.resource_from_href (urlparse.urlsplit (next).path)
            if getattr (next_page, "login_required", False) :
                next = "/"
            response.username = None
            response.add_notification (_T ("Logout successful."))
            raise top.Status.See_Other (next)
        # end def _response_body

    POST = _Logout__POST_ # end class

# end class _Logout_

_Ancestor = _Form_Cmd_

class _Register_ (_Ancestor) :

    page_template_name = "account_register"
    email_template     = "account_verify_email"

    class _Register__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data  = request.req_data
            top       = resource.top
            form      = resource.form
            errors    = form (req_data)
            if not errors :
                next  = req_data.get ("next", "/")
                host  = request.host
                Auth  = top.scope.GTW.OMP.Auth
                account, token = Auth.Account_P.create_new_account \
                    (form.username, form.new_password)
                link  = resource.parent.href_action (account, token, request)
                try :
                    resource.send_email \
                        ( resource.email_template
                        , email_to      = form.username
                        , email_subject =
                            _T ("Email confirmation for %s") % (host, )
                        , email_from    = resource.email_from
                        , link          = link
                        , NAV           = top
                        , page          = resource
                        , host          = host
                        )
                except Exception as exc :
                    form.errors.add (form, None, str (exc))
                else :
                    response.add_notification \
                        (_T ( "A confirmation has been sent to your email "
                              "address."
                            )
                        )
                    raise top.Status.See_Other (next)
            response.username = None
            result = resource.GET ()._response_body \
                (resource, request, response)
            return result
        # end def _response_body

    POST = _Register__POST_ # end class

# end class _Register_

_Ancestor = _Form_Cmd_

class _Request_Reset_Password_ (_Ancestor) :

    page_template_name  = "account_reset_password"
    email_template      = "account_reset_password_email"

    class _Request_Reset_Password__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data  = request.req_data
            top       = resource.top
            form      = resource.form
            errors    = form (req_data)
            if errors :
                result  = resource.GET ()._response_body \
                    (resource, request, response)
                return result
            else :
                Auth      = top.scope.GTW.OMP.Auth
                account   = form.account
                host      = request.host
                next      = request.referrer or "/"
                next_page = top.page_from_href (urlparse.urlsplit (next).path)
                passwd, token = Auth.Account_P.reset_password (account)
                link = resource.parent.href_action (account, token, request)
                resource.send_email \
                    ( resource.email_template
                    , email_to      = form.username
                    , email_subject =
                        ( _T ("Password reset for user %s on website %s")
                        % (form.username, host)
                        )
                    , email_from    = resource.email_from
                    , new_password  = passwd
                    , link          = link
                    , NAV           = top
                    , page          = resource
                    , host          = host
                    )
                response.add_notification \
                    ( GTW.Notification
                        (_T ( "The reset password instructions have been "
                              "sent to your email address."
                            )
                        )
                    )
                raise top.Status.See_Other (next)
        # end def _response_body

    POST = _Request_Reset_Password__POST_ # end class

# end class _Request_Reset_Password_

_Ancestor = GTW.RST.TOP.Dir_V

class Auth (_Ancestor) :
    """Navigation directory supporting user authorization."""

    pid      = "Auth"
    T        = TFL.I18N.Name

    _entry_type_map = dict \
        ( action                  = _Action_
        , activate                = _Activate_
        , change_email            = _Change_Email_
        , change_password         = _Change_Password_
        , login                   = _Login_
        , logout                  = _Logout_
        , register                = _Register_
        , request_reset_password  = _Request_Reset_Password_
        )

    @property
    def href_login (self) :
        return pp_join (self.abs_href, "login")
    # end def href_login

    @property
    def href_logout (self) :
        return pp_join (self.abs_href, "logout")
    # end def href_logout

    @property
    def href_register (self) :
        return pp_join (self.abs_href, "register")
    # end def href_register

    @property
    def href_reset_password (self) :
        return pp_join (self.abs_href, "request_reset_password")
    # end def href_reset_password

    @Once_Property
    def _effective (self) :
        return self._get_child ("login")
    # end def _effective

    def href_action (self, obj, token, request) :
        result = self._href_q \
            ( request.url_root, self.href, "action"
            , p = str (obj.pid)
            , t = token
            )
        return result
    # end def href_action

    def href_change_email (self, obj) :
        return self._href_q \
            (self.abs_href, "change_email", p = str (obj.pid))
    # end def href_change_email

    def href_change_pass (self, obj) :
        return self._href_q \
            (self.abs_href, "change_password", p = str (obj.pid))
    # end def href_change_pass

    def _href_q (self, * args, ** kw) :
        return "%s?%s" % (pp_join (args), urlencode (kw))
    # end def _href_q

    def _new_child (self, T, child, grandchildren) :
        result = T (name = child, parent = self)
        if not grandchildren :
            return result
    # end def _new_child

# end class Auth

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("*")
### __END__ GTW.RST.TOP.Auth

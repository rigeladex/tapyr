# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#     6-Aug-2012 (CT) Replace `_do_change_info_skip` by `skip_etag`
#    16-Aug-2012 (MG) Remove form dependecy
#    17-Aug-2012 (MG) Fix bug in `_Login_.POST`
#    19-Aug-2012 (MG) Big in _Login_ fixed
#     9-Oct-2012 (CT) Fix `_Login_.POST._response_body` call to `_get_child`
#     9-Oct-2012 (CT) Add `get_title` to `_Activate_`, `_Change_Password_`
#     9-Oct-2012 (CT) Fix error messages, fix typo, display `username` after
#                     empty `password`
#     9-Oct-2012 (CT) Use `.host_url`, not `.url_root`, for `href_action`
#     5-Jan-2013 (CT) Adapt to change of `password_hash`
#     8-Jan-2013 (CT) Add `_Make_Cert_`
#     8-Jan-2013 (CT) Add `_login_required` to various classes
#    15-Jan-2013 (CT) Implement `_Make_Cert_.POST._response_body`
#    15-Jan-2013 (CT) Set `O` of `SPKAC` to `cert.get_subject ().O`
#    28-Jan-2013 (CT) Fix spelling of `Action_Expired`
#    28-Jan-2013 (CT) Split `_Reset_Password_` from `_Change_Password_`
#                     (no `_login_required` for reset password)
#     2-Mar-2013 (CT) Use `response.set_header`, not `.headers [] = `
#     2-May-2013 (CT) Factor `GTW.RST.Auth_Mixin`
#     2-May-2013 (CT) Use `self.hash_fct`, `self.b64_encoded`
#     3-May-2013 (CT) Rename `login_required` to `auth_required`
#     6-May-2013 (CT) Try to `commit` before sending emails/notifications
#     4-Dec-2013 (CT) Add `href_request_reset_password`
#                     fix some stylos
#     5-Dec-2013 (CT) Fix `_Make_Cert_.POST._response_body` (missing `SPKAC`)
#     5-Dec-2013 (CT) `send_error_email` if `SPKAC` is missing from `request`
#     5-Dec-2013 (CT) Improve error message for missing `SPKAC`
#     9-Dec-2013 (CT) Add call to `resource.csrf_check` to `POST._response_body`
#    10-Dec-2013 (CT) Add `_Cmd_Method_Mixin_` to redefine `_skip_render` to
#                     check `request.is_secure`
#    11-Dec-2013 (CT) DRY `.csrf_check`: move to `_Form_Cmd_.POST._skip_render`
#    11-Dec-2013 (CT) Use `sane_referrer` in `Login.GET._render_context`
#     7-Jan-2014 (CT) Change `Logout.POST` to redirect to non-cc domain
#     7-Jan-2014 (CT) Fix ancestor of `_Logout_.POST`
#                     (use `_Cmd_`, not `_Form_Cmd_`)
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _GTW._RST.Auth_Mixin     import Errors

import _GTW.Notification
import _GTW._RST.HTTP_Method
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.Decorator           import getattr_safe
from   _TFL.Filename            import Filename
from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pp_join
from   urllib                   import urlencode

import datetime
import time
import urlparse

_Ancestor = GTW.RST.TOP.Page

class _Cmd_ (_Ancestor) :

    implicit = True

    class _Cmd_Method_Mixin_ (GTW.RST.HTTP_Method) :

        def _skip_render (self, resource, request, response) :
            result = self.__super._skip_render (resource, request, response)
            if not result :
                if not (resource.TEST or request.is_secure) :
                    Status = resource.top.Status
                    if resource.s_domain :
                        raise Status.See_Other (resource.secure_url)
                    else :
                        raise Status.Forbidden ()
            return result
        # end def _skip_render

    # end class _Cmd_Method_Mixin_

    class _Cmd__GET_ (_Cmd_Method_Mixin_, _Ancestor.GET) :

        _real_name             = "GET"

    GET = _Cmd__GET_ # end class

# end class _Cmd_

class _Form_Cmd_ (GTW.RST.Auth_Mixin, _Cmd_) :

    active_account_required = True

    class _Form_Cmd__GET_ (_Cmd_.GET) :

        _real_name             = "GET"

        def _render_context (self, resource, request, response, ** kw) :
            pid         = int (request.req_data.get ("p", "-1"))
            try :
                account = resource.scope.pid_query (pid)
            except LookupError :
                account = getattr (response, "account", None)
            return self.__super._render_context \
                ( resource, request, response
                , account  = account
                , errors   = getattr (response, "errors",   Errors ())
                , username = getattr (response, "username", None)
                , ** kw
                )
        # end def _render_context

    GET = _Form_Cmd__GET_ # end class

    class _Form_Cmd__POST_ \
            ( _Cmd_._Cmd_Method_Mixin_
            , GTW.RST.TOP.HTTP_Method_Mixin
            , GTW.RST.Auth_Mixin.POST
            ) :

        _real_name              = "POST"

        def _skip_render (self, resource, request, response) :
            result = self.__super._skip_render (resource, request, response)
            if not result :
                resource.csrf_check (request, response)
            return result
        # end def _skip_render

    POST = _Form_Cmd__POST_ # end class

# end class _Form_Cmd_

_Ancestor = _Cmd_

class _Action_ (_Ancestor) :

    class _Action__GET_ (_Ancestor.GET) :

        ### actions are handle by GET because the links are sent to the user
        ### as email's and they should only click these links !

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
                    description = action.description
                    next        = action.handle (resource)
                    response.add_notification \
                        (GTW.Notification (_T (description)))
                    raise HTTP_Status.See_Other (next)
                except GTW.OMP.Auth.Action_Expired :
                    action.destroy      ()
                    top.scope.commit    ()
            raise HTTP_Status.Not_Found ()
        # end def _response_body

    GET = _Action__GET_ # end class

# end class _Action_

_Ancestor = _Form_Cmd_

class _Activate_ (_Ancestor) :

    page_template_name      = "account_change_password"
    active_account_required = False

    def get_title (self, account, request) :
        return _T ("Activate account for %s on website %s") \
            % (account.name, request.host)
    # end def get_title

    def _check_account (self, account, errors) :
        if account and not account.activation :
            if errors :
                errors [None].append \
                    (_T ("No activation request for this account"))
            return False
        return True
    # end def _check_account

    def _send_notification (self, response) :
        response.add_notification \
            (GTW.Notification (_T ("Activation successful.")))
    # end def _send_notification

    class _Activate__GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def _render_context (self, resource, request, response, ** kw) :
            result = self.__super._render_context \
                (resource, request, response, **kw)
            HTTP_Status = resource.top.Status
            pid         = int (request.req_data.get ("p", "-1"))
            try :
                account = resource.scope.pid_query (pid)
            except LookupError :
                ### if this called from the post, the account is set on the
                ### response cobject
                account = getattr (response, "account", None)
                if not account :
                    raise HTTP_Status.Not_Found ()
                result ["account"] = account
            else :
                if not resource._check_account (account, None) :
                    raise HTTP_Status.Forbidden ()
            return result
        # end def _render_context

    GET = _Activate__GET_ # end class

    class _Activate__POST_ (_Ancestor.POST) :

        _real_name              = "POST"

        def _response_body (self, resource, request, response) :
            debug        = getattr (resource.top, "DEBUG", False)
            req_data     = request.req_data
            top          = resource.top
            HTTP_Status  = top.Status
            self.errors  = Errors ()
            self._credentials_validation (resource, request, debug = debug)
            new_password = self.get_password \
                (request, "npassword", verify_field = "vpassword")
            account      = self.account
            resource._check_account (account, self.errors)
            if self.errors :
                response.errors   = self.errors
                response.account  = self.account
                result            = resource.GET ()._response_body \
                    (resource, request, response)
                return result
            else :
                next              = req_data.get ("next", "/")
                response.username = account.name
                account.change_password     (new_password, suspended = False)
                top.scope.commit            ()
                resource._send_notification (response)
                raise HTTP_Status.See_Other (next)
        # end def _response_body

    POST = _Activate__POST_ # end class

# end class _Activate_

_Ancestor = _Form_Cmd_

class _Change_Email_ (_Ancestor) :

    page_template_name  = "account_change_email"
    new_email_template  = "account_verify_new_email"
    old_email_template  = "account_change_email_info"
    _auth_required      = True

    class _Change_Email__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def get_email ( self, request
                      , field_name   = "nemail"
                      , verify_field = "vemail"
                      ) :
            email = self.get_required \
                (request, field_name, _T ("The Email is required."))
            if verify_field :
                verify = self.get_required \
                ( request, verify_field
                , _T ("Repeat the EMail for verification.")
                )
                if email and verify and (email != verify) :
                    self.errors [field_name].append \
                        (_T ("The Email's don't match."))
            return email
        # end def get_email

        def _response_body (self, resource, request, response) :
            debug       = getattr (resource.top, "DEBUG", False)
            req_data    = request.req_data
            top         = resource.top
            HTTP_Status = top.Status
            self.errors = Errors ()
            self._credentials_validation (resource, request, debug = debug)
            new_email   = self.get_email (request)
            if not self.errors :
                account = self.account
                next    = req_data.get ("next", "/")
                host    = request.host
                token   = account.change_email_prepare (new_email)
                link    = resource.parent.href_action  (account, token, request)
                top.scope.commit ()
                try :
                    resource.send_email \
                        ( resource.new_email_template
                        , email_to      = new_email
                        , email_subject =
                            _T ("Email confirmation for %s") % (host, )
                        , email_from    = resource.email_from
                        , link          = link
                        , NAV           = top
                        , page          = resource
                        , host          = host
                        )
                except Exception as exc :
                    self.errors [None].append (str (exc))
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
            response.errors  = self.errors
            response.account = self.account
            result = resource.GET ()._response_body \
                (resource, request, response)
            return result
        # end def _response_body

    POST = _Change_Email__POST_ # end class

# end class _Change_Email_

_Ancestor = _Activate_

class _Change_Password_ (_Ancestor) :

    active_account_required = True
    _action_kind            = _ ("Change")
    _auth_required          = True

    def get_title (self, account, request) :
        return _T ("%s Password for %s on website %s") \
            % (_T (self._action_kind), account.name, request.host)
    # end def get_title

    def _check_account (self, account, errors) :
        return True
    # end def _check_account

    def _send_notification (self, response) :
        response.add_notification \
            (GTW.Notification (_T ("The password has been changed.")))
    # end def _send_notification

# end class _Change_Password_

_Ancestor = _Form_Cmd_

class _Login_ (_Ancestor) :
    """Login page"""

    page_template_name = "login"

    class _Login__GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def _render_context (self, resource, request, response, ** kw) :
            kw.setdefault ("next", resource.sane_referrer (request))
            return self.__super._render_context \
                (resource, request, response, ** kw)
        # end def _render_context

    GET = _Login__GET_ # end class

    class _Login__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data = request.req_data
            if req_data.get ("Reset") :
                resetter = resource.parent._get_child ("request_reset_password")
                result   = resetter.POST ()._response_body \
                    (resetter, request, response)
                return result
            else :
                self.errors = Errors  ()
                debug       = getattr (resource.top, "DEBUG", False)
                username, password = self._credentials_validation \
                    (resource, request, debug = debug)
                if self.errors :
                    if password :
                        ### clear `username` in re-displayed form
                        response.username = None
                    else :
                        ### keep `username` in re-displayed form
                        response.username = username
                    response.errors   = self.errors
                    response.account  = self.account
                    result = resource.GET ()._response_body \
                        (resource, request, response)
                    return result
                else :
                    if self.account.password_change_required :
                        ### a password change is required -> redirect to
                        ### that page
                        next = resource.href_change_pass (self.account)
                    else :
                        next = req_data.get ("next", "/")
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

    GET                 = None
    _auth_required      = True

    class _Logout__POST_ (_Cmd_._Cmd_Method_Mixin_, GTW.RST.Auth_Mixin.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            response.username = None
            response.add_notification (_T ("Logout successful."))
            next = self._response_get_next (resource, request, response)
            raise resource.top.Status.See_Other (next)
        # end def _response_body

        def _response_get_next (self, resource, request, response) :
            domain     = None
            top        = resource.top
            result     = request.req_data.get ("next", request.referrer or "/")
            s, h, p    = urlparse.urlsplit (result) [:3]
            next_page  = top.resource_from_href (p)
            if not h :
                h      = urlparse.urlsplit (request.host_url).netloc
            if h == top.cc_domain or next_page == resource :
                ### need to redirect to non-cc domain
                domain = resource.s_domain or resource.domain
            if domain :
                result = "//" + domain + "/"
            elif getattr (next_page, "auth_required", False) :
                result = "/"
            return result
        # end def _response_get_next


    POST = _Logout__POST_ # end class

# end class _Logout_

_Ancestor = _Form_Cmd_

class _Make_Cert_ (_Ancestor) :

    page_template_name  = "account_make_cert"
    _auth_required      = True

    class _Make_Cert__GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def _render_context (self, resource, request, response, ** kw) :
            result = self.__super._render_context \
                (resource, request, response, **kw)
            result ["challenge"] = challenge = resource._challenge_hash \
                (request)
            request.session ["spkac_challenge"] = challenge
            return result
        # end def _render_context

    GET = _Make_Cert__GET_ # end class

    class _Make_Cert__POST_ (_Ancestor.POST) :

        _real_name              = "POST"
        _renderers              = (GTW.RST.Mime_Type.User_Cert, )

        def _response_body (self, resource, request, response) :
            from pyspkac.spkac import SPKAC
            from M2Crypto      import EVP, X509
            top          = resource.top
            HTTP_Status  = top.Status
            ca_path      = top.cert_auth_path
            if not ca_path :
                raise HTTP_Status.Not_Found ()
            try :
                ### Unicode argument to `EVP.load_key` fails [M2Crypto==0.21.1]
                cert  = X509.load_cert (Filename (".crt", ca_path).name)
                pkey  = EVP.load_key   (str (Filename (".key", ca_path).name))
            except Exception :
                raise HTTP_Status.Not_Found ()
            req_data     = request.req_data
            spkac        = req_data.get ("SPKAC", "").replace ("\n", "")
            if not spkac :
                exc = HTTP_Status.Bad_Request \
                    ( _T( "The parameter `SPKAC` is missing from the request. "
                          "Normally, the web browser should supply that "
                          "parameter automatically."
                        )

                    )
                resource.send_error_email (request, exc)
                raise exc
            challenge    = request.session.get ("spkac_challenge")
            desc         = req_data.get ("desc")
            email        = request.user.name
            cn           = "%s [%s]" % (email, desc) if desc else email
            ### Unicode arguments to `X509.new_email` fail [M2Crypto==0.21.1]
            X  = X509.new_extension
            x1 = X (b"basicConstraints", b"CA:FALSE", critical = True)
            x2 = X \
                ( b"keyUsage"
                , b"digitalSignature, keyEncipherment, keyAgreement"
                , critical = True
                )
            x3 = X (b"extendedKeyUsage", b"clientAuth, emailProtection, nsSGC")
            s  = SPKAC \
                ( spkac, challenge, x1, x2, x3
                , CN     = cn
                , Email  = email
                , O      = cert.get_subject ().O
                )
            scope  = top.scope
            CTM    = scope.Auth.Certificate
            start  = CTM.E_Type.validity.start.now ()
            finis  = start + datetime.timedelta (days = 365 * 2)
            c_obj  = CTM (email = email, validity = (start, finis), desc = desc)
            scope.commit ()
            result = c_obj.pem = s.gen_crt \
                ( pkey, cert, c_obj.pid
                , not_before = self._timestamp (start)
                , not_after  = self._timestamp (finis)
                ).as_pem ()
            response.set_header \
                ( "content-disposition", "inline"
                , filename = "%s.crt" % (email, )
                )
            scope.commit ()
            return result
        # end def _response_body

        def _timestamp (self, v) :
            ### convert from UTC to local time
            vc = v + TFL.user_config.time_zone.utcoffset (v)
            return int (time.mktime (vc.timetuple ()))
        # end def _timestamp

    POST = _Make_Cert__POST_ # end class

    def _challenge_hash (self, request) :
        scope = self.top.scope
        user  = request.user
        sig   = "%s:::%s" %     (scope.db_meta_data.dbid, user.name)
        hash  = self.hash_fct   (sig).digest ()
        return self.b64_encoded (hash, altchars = b":-")
    # end def _challenge_hash

# end class _Make_Cert_

_Ancestor = _Form_Cmd_

class _Register_ (_Ancestor) :

    page_template_name = "account_register"
    email_template     = "account_verify_new_email"

    class _Register__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data      = request.req_data
            top           = resource.top
            self.errors   = Errors ()
            username      = self.get_username (request)
            if username :
                self.get_account (resource, username)
                if self.account :
                    self.errors ["username"].append \
                        (_T ( "Account with this Email address already "
                              "registered"
                            )
                        )
            new_password  = self.get_password \
                (request, "npassword", verify_field = "vpassword")
            if not self.errors :
                next           = req_data.get ("next", "/")
                host           = request.host
                Auth           = top.scope.Auth
                account, token = Auth.Account.create_new_account \
                    (username, new_password)
                link  = resource.parent.href_action (account, token, request)
                top.scope.commit ()
                try :
                    resource.send_email \
                        ( resource.email_template
                        , email_to      = username
                        , email_subject =
                            _T ("Email confirmation for %s") % (host, )
                        , email_from    = resource.email_from
                        , link          = link
                        , NAV           = top
                        , page          = resource
                        , host          = host
                        )
                except Exception as exc :
                    self.errors [None].append (str (exc))
                else :
                    response.add_notification \
                        (_T ( "A confirmation has been sent to your email "
                              "address."
                            )
                        )
                    raise top.Status.See_Other (next)
            response.username = None
            response.errors   = self.errors
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
            req_data    = request.req_data
            top         = resource.top
            self.errors = Errors ()
            username    = self.get_username (request, "username")
            self.get_account \
                (resource, username, getattr (top, "DEBUG", False))
            if not self.account and not self.errors :
                self.errors [None].append \
                   (_T ("Account could not be found"))
            if self.errors :
                response.errors = self.errors
                result  = resource.GET ()._response_body \
                    (resource, request, response)
                return result
            else :
                Auth          = top.scope.GTW.OMP.Auth
                account       = self.account
                host          = request.host
                next          = request.referrer or "/"
                passwd, token = Auth.Account.reset_password (account)
                link = resource.parent.href_action (account, token, request)
                top.scope.commit ()
                resource.send_email \
                    ( resource.email_template
                    , email_to      = username
                    , email_subject =
                        ( _T ("Password reset for user %s on website %s")
                        % (username, host)
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

_Ancestor = _Change_Password_

class _Reset_Password_ (_Ancestor) :

    active_account_required = False
    _action_kind            = _ ("Reset")
    _auth_required          = False

# end class _Reset_Password_

_Ancestor = GTW.RST.TOP.Dir_V

class Auth (_Ancestor) :
    """Navigation directory supporting user authorization."""

    pid      = "Auth"

    _entry_type_map = dict \
        ( action                  = _Action_
        , activate                = _Activate_
        , change_email            = _Change_Email_
        , change_password         = _Change_Password_
        , login                   = _Login_
        , logout                  = _Logout_
        , make_cert               = _Make_Cert_
        , register                = _Register_
        , request_reset_password  = _Request_Reset_Password_
        , reset_password          = _Reset_Password_
        )

    @property
    @getattr_safe
    def href_activate (self) :
        return pp_join (self.abs_href, "activate")
    # end def href_activate

    @property
    @getattr_safe
    def href_login (self) :
        return pp_join (self.abs_href, "login")
    # end def href_login

    @property
    @getattr_safe
    def href_logout (self) :
        return pp_join (self.abs_href, "logout")
    # end def href_logout

    @property
    @getattr_safe
    def href_register (self) :
        return pp_join (self.abs_href, "register")
    # end def href_register

    @property
    @getattr_safe
    def href_request_reset_password (self) :
        return pp_join (self.abs_href, "request_reset_password")
    # end def href_request_reset_password

    @Once_Property
    @getattr_safe
    def _effective (self) :
        return self._get_child ("login")
    # end def _effective

    def href_action (self, obj, token, request) :
        ### `request.url_root` doesn't do the right thing for apache/mod_fcgid
        result = self._href_q \
            ( request.host_url, self.href, "action"
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

    def href_make_cert (self, obj) :
        if self.top.cert_auth_path :
            return self._href_q \
                (self.abs_href, "make_cert", p = str (obj.pid))
    # end def href_make_cert

    def href_reset_password (self) :
        return self._href_q (self.abs_href, "reset_password", p = str (obj.pid))
    # end def href_reset_password

    def _href_q (self, * args, ** kw) :
        return "%s?%s" % (pp_join (* args), urlencode (kw))
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

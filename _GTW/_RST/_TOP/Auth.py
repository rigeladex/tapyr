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
#     6-Aug-2012 (CT) Replace `_do_change_info_skip` by `skip_etag`
#    16-Aug-2012 (MG) Remove form dependecy
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.Notification
import _GTW._RST.HTTP_Method
import _GTW._RST._TOP.Dir
import _GTW._RST._TOP.Page

from   _TFL._Meta.Once_Property import Once_Property

from   _TFL.Decorator           import getattr_safe
from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pp_join
from   urllib                   import urlencode

import urlparse
import collections

class Errors (collections.defaultdict) :

    __metaclass__ = TFL.Meta.M_Class

    def __init__ (self) :
        self.__super.__init__ (list)
    # end def __init__

# end class Errors

_Ancestor = GTW.RST.TOP.Page

class _Cmd_ (_Ancestor) :

    implicit = True

# end class _Cmd_

class _Form_Cmd_ (_Cmd_) :

    skip_etag               = True
    active_account_required = True


    class _Form_Cmd__GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def _render_context (self, resource, request, response, ** kw) :
            pid         = int (request.req_data.get ("p", "-1"))
            try :
                account = resource.scope.pid_query (pid)
            except LookupError :
                account = getattr (response, "account", None)
            return self.__super._render_context \
                ( resource, request, response
                , errors  = getattr (response, "errors", Errors ())
                , account = account
                , ** kw
                )
        # end def _render_context

    GET = _Form_Cmd__GET_ # end class

    class _Form_Cmd__POST_ (GTW.RST.TOP.HTTP_Method_Mixin, GTW.RST.POST) :

        _real_name              = "POST"

        def get_account (self, resource, username, debug = False) :
            try :
                self.account = resource.account_manager.query \
                    (name = username).one ()
            except IndexError :
                self.account = None
                if debug :
                    self.errors ["username"].append \
                        ("No account with username `%s` found" % (username, ))
                ### look's like no account with this username exists
                return False
            return True
        # end def get_account

        def _authenticate (self, resource, username, password, debug = False) :
            result = False
            self.get_account (resource, username, debug)
            if password :
                result = self.account.verify_password (password)
                if not result and debug :
                    self.errors ["password"].append \
                        ( "Password is wrong:\n"
                               "  %s\n"
                               "  hash db `%s`\n"
                               "  hash in `%s`"
                            % ( password
                              , self.account.password
                              , self.account.password_hash
                                    (password, self.account.salt)
                              )
                        )
            return result
        # end def _authenticate

        def get_required (self, request, field_name, error) :
            value = request.req_data.get (field_name)
            if not value :
                self.errors [field_name].append (error)
            return value
        # end def get_required

        def get_username (self, request, field_name = "username") :
            return self.get_required \
                (request, field_name, _T ("A user name is required to login."))
        # end def get_required

        def get_password ( self, request
                         , field_name   = "password"
                         , verify_field = None
                         ) :
            password = self.get_required \
                (request, field_name, _T ("The password is required."))
            if verify_field :
                verify = self.get_required \
                ( request, verify_field
                , _T ("Repeat the password for verification.")
                )
                if password and verify and (password != verify) :
                    self.errors [field_name].append \
                        (_T ("The passwords don't match."))
            return password
        # end def get_password

        def _credetials_validation ( self
                                   , resource
                                   , request
                                   , username = "username"
                                   , password = "password"
                                   , debug    = False
                                   ) :
            username     = self.get_username (request, username)
            password     = self.get_password (request, password)
            error_add    = lambda e : self.errors [None].append (e)
            if not self._authenticate \
                   (resource, username, password, debug) :
                error_add (_T ("Username or password incorrect"))
            elif resource.active_account_required and not self.account.active :
                error_add (_T ("This account is currently inactive"))
            elif debug :
                error_add (repr (request.req_data))
        # end def _credetials_validation

    POST = _Form_Cmd__POST_ # end class

# end class _Form_Cmd_

_Ancestor = _Cmd_

class _Action_ (_Ancestor) :

    class _Action__GET_ (_Ancestor.GET) :

        ### actions are handle by GTE because the links are sent to the user
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
                except GTW.OMP.Auth.Action_Exipred :
                    action.destroy      ()
                    top.scope.commit    ()
            raise HTTP_Status.Not_Found ()
        # end def _response_body

    GET = _Action__GET_ # end class

# end class _Action_

_Ancestor = _Form_Cmd_

class _Activate_ (_Ancestor) :

    page_template_name      = "account_activate"
    active_account_required = False

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
            pid                 = int (request.req_data.get ("p", "-1"))
            ###import pdb; pdb.set_trace ()
            try :
                account = resource.scope.pid_query (pid)
            except LookupError :
                ### if this called fromthe post, the account is set on the
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
            ### import pdb; pdb.set_trace ()
            self._credetials_validation (resource, request, debug = debug)
            new_password = self.get_password \
                (request, "npassword", verify_field = "vpassword")
            account      = self.account
            resource._check_account (account, self.errors)
            if self.errors :
                response.errors  = self.errors
                response.account = self.account
                result           = resource.GET ()._response_body \
                    (resource, request, response)
                return result
            else :
                next    = req_data.get      ("next", "/")
                account.change_password     (new_password, suspended = False)
                response.username = account.name
                resource._send_notification (response)
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
            self.errors = Errors         ()
            ###import pdb; pdb.set_trace ()
            self._credetials_validation  (resource, request, debug = debug)
            new_email   = self.get_email (request)
            if not self.errors :
                account = self.account
                next    = req_data.get ("next", "/")
                host    = request.host
                token   = account.change_email_prepare (new_email)
                link    = resource.parent.href_action  (account, token, request)
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

    page_template_name      = "account_change_password"
    active_account_required = True

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
                self.errors = Errors ()
                debug       = getattr (resource.top, "DEBUG", False)
                self._credetials_validation (resource, request, debug = debug)
                if self.errors :
                    ### clear `username` in re-displayed form
                    response.username = None
                    response.errors   = self.errors
                    response.account  = self.account
                    result = resource.GET ()._response_body \
                        (resource, request, response)
                    return result
                else :
                    next = req_data.get ("next", "/")
                    if self.account.password_change_required :
                        ### a password change is required -> redirect to
                        ### that page
                        next = resource.href_change_pass (self.account)
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
            next      = request.req_data.get ("next", request.referrer or "/")
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
    email_template     = "account_verify_new_email"

    class _Register__POST_ (_Ancestor.POST) :

        _real_name             = "POST"

        def _response_body (self, resource, request, response) :
            req_data      = request.req_data
            top           = resource.top
            self.errors   = Errors            ()
            username      = self.get_username (request)
            if username :
                self.get_account              (resource, username)
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
                account, token = Auth.Account_P.create_new_account \
                    (username, new_password)
                link  = resource.parent.href_action (account, token, request)
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
                next_page     = top.resource_from_href \
                    (urlparse.urlsplit (next).path)
                passwd, token = Auth.Account_P.reset_password (account)
                link = resource.parent.href_action (account, token, request)
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
    def href_reset_password (self) :
        return pp_join (self.abs_href, "request_reset_password")
    # end def href_reset_password

    @Once_Property
    @getattr_safe
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

    @property
    @getattr_safe
    def href_activate (self) :
        return self._href_q (self.abs_href, "activate")
    # end def href_activate

    def href_change_email (self, obj) :
        return self._href_q \
            (self.abs_href, "change_email", p = str (obj.pid))
    # end def href_change_email

    def href_change_pass (self, obj) :
        return self._href_q \
            (self.abs_href, "change_password", p = str (obj.pid))
    # end def href_change_pass

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

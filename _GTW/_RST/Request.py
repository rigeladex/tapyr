# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
#    GTW.RST.Request
#
# Purpose
#    Wrap and extend wsgi-specific Request class
#
# Revision Dates
#    19-Jun-2012 (CT) Creation
#    28-Jun-2012 (CT) Add `verbose`
#     2-Jul-2012 (CT) Factor `has_option` to `GTW.Request_Data`
#    17-Jul-2012 (CT) Add property `user`
#    24-Jul-2012 (CT) Add `use_language`
#     6-Aug-2012 (CT) Add attribute `lang`
#     2-Oct-2012 (CT) Add property `brief`
#    16-Oct-2012 (CT) Add properties `ckd` and `raw`
#    16-Jan-2013 (CT) Add `ssl_authorized_user` and `ssl_client_verified`
#    26-Jan-2013 (CT) Add and use `http_server_authorized_user`
#     2-May-2013 (CT) Factor in `cookie_encoding`, `cookie`, `secure_cookie`,
#                     `_cookie_signature` from `GTW.RST.TOP.Request`
#     2-May-2013 (CT) Factor `new_secure_cookie` from `GTW.RST.Response`
#     3-May-2013 (CT) Factor `rat_secret` and add `remote_addr` to it
#     4-May-2013 (CT) Add `cookies_to_delete`, use for failing `RAT`
#     4-May-2013 (CT) Factor `apache_authorized_user`
#     5-May-2013 (CT) Fix `signature` warning of `secure_cookie`
#     5-May-2013 (CT) Factor `_auth_user_name`, turn `username` into `property`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                      import GTW
from   _TFL                      import TFL

import _GTW._RST

from   _TFL                      import I18N
from   _TFL._Meta.Once_Property  import Once_Property

import _TFL._Meta.Object

import base64
import datetime
import hmac
import logging
import time

### XXX replace home-grown code by werkzeug supplied functions
### XXX     werkzeug.utils, werkzeug.HTTP, ...

class _RST_Request_ (TFL.Meta.Object) :
    """Wrap and extend wsgi-specific Request class."""

    _real_name        = "Request"
    _resource         = None
    _user             = None

    lang              = None
    original_resource = None

    def __init__ (self, root, environ) :
        self.root     = root
        self._request = root.HTTP.Request (environ)
        self.cookies_to_delete = set ()
    # end def __init__

    def __getattr__ (self, name) :
        if name == "request" : ### XXX remove after porting of GTW.Werkzeug.Error
            return self._request
        elif name != "_request" :
            result = getattr (self._request, name)
            setattr (self, name, result)
            return result
        raise AttributeError (name)
    # end def __getattr__

    @Once_Property
    def apache_authorized_user (self) :
        return self.environ.get ("REMOTE_USER")
    # end def apache_authorized_user

    @Once_Property
    def brief (self) :
        return self.req_data.has_option ("brief")
    # end def brief

    @Once_Property
    def ckd (self) :
        req_data = self.req_data
        if "ckd" in req_data :
            return req_data.has_option ("ckd")
        elif self.method == "GET" :
            ### for `GET`, `ckd` is default
            return not req_data.has_option ("raw")
    # end def ckd

    @Once_Property
    def cookie_encoding (self) :
        return self.settings.get ("cookie_encoding", "utf-8")
    # end def cookie_encoding

    @Once_Property
    def http_server_authorized_user (self) :
        result = self.ssl_authorized_user
        if result is None :
            result = self.apache_authorized_user
        return result
    # end def http_server_authorized_user

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        return self.get_browser_locale_codes ()
    # end def locale_codes

    @Once_Property
    def rat_authorized_user (self) :
        root   = self.root
        rat    = getattr (root.SC, "RAT", None)
        result = [None]
        if rat is not None :
            def agent (self, cargo, timestamp) :
                user = None
                try :
                    pid = int (cargo)
                except Exception :
                    user = root._get_user (cargo)
                else :
                    user = root.scope.pid_query (pid)
                if user is not None :
                    try :
                        result [0] = user.name
                        return self.rat_secret (user)
                    except Exception :
                        pass
            cargo = self.secure_cookie ("RAT", agent, rat.session_ttl_s)
            if cargo is None :
                self.cookies_to_delete.add ("RAT")
            else :
                return result [0]
    # end def rat_authorized_user

    @Once_Property
    def raw (self) :
        req_data = self.req_data
        if "raw" in req_data :
            return req_data.has_option ("raw")
        elif self.method != "GET" :
            ### for all methods but `GET`, `raw` is default
            return not req_data.has_option ("ckd")
    # end def raw

    @property
    def resource (self) :
        result = self._resource
        if result is None :
            result = self.root
        return result
    # end def resource

    @resource.setter
    def resource (self, value) :
        self._resource = value
    # end def resource

    @property
    def settings (self) :
        return self.root._kw
    # end def settings

    @Once_Property
    def ssl_authorized_user (self) :
        return self.environ.get ("SSL_CLIENT_S_DN_Email")
    # end def ssl_authorized_user

    @Once_Property
    def ssl_client_verified (self) :
        return self.environ.get ("SSL_CLIENT_VERIFY") == "SUCCESS"
    # end def ssl_client_verified

    @property
    def user (self) :
        result = self._user
        if result is None and self.username :
            self._user = self.root._get_user (self.username)
        return self._user
    # end def user

    @user.setter
    def user (self, value) :
        self._user = value
    # end def user

    @property
    def username (self) :
        ### `username` is `property` not `Once_Property` to allow
        ### descendent to change redefine `username.setter` (to support `login`)
        ### `_auth_user_name` is `Once_Property` to improve performance
        return self._auth_user_name
    # end def username

    @Once_Property
    def verbose (self) :
        return self.req_data.has_option ("verbose")
    # end def verbose

    @Once_Property
    def _auth_user_name (self) :
        result = self.http_server_authorized_user
        if result is None :
            result = self.rat_authorized_user
        if result is None :
            auth   = self.authorization
            result = auth and auth.username
        return result
    # end def _auth_user_name

    def cookie (self, name) :
        return self.cookies.get (name)
    # end def cookie

    def current_time (self) :
        return time.time ()
    # end def current_time

    def get_browser_locale_codes (self) :
        """Determines the user's locale from Accept-Language header."""
        languages = self.accept_languages
        supported = getattr (self.root, "languages", set ())
        if supported :
            locales   = list (l for l, p in languages if l in supported)
            if locales :
                return locales
        return getattr (self.root, "default_locale_code", "en")
    # end def get_browser_locale_codes

    def new_secure_cookie (self, name, data, secrets = None) :
        timestamp = base64.b64encode (str (int (self.current_time ())))
        cargo     = base64.b64encode \
            (    data.encode (self.cookie_encoding)
            if   isinstance  (data, unicode)
            else data
            )
        signature = self._cookie_signature (cargo, timestamp, secrets = secrets)
        result    = "|".join ((cargo, timestamp, signature))
        return result
    # end def new_secure_cookie

    def rat_secret (self, user) :
        rip = getattr (self, "remote_addr", None)
        return (user.password, self.root.scope.db_meta_data.dbid, user.pid, rip)
    # end def rat_secret

    def secure_cookie (self, name, secret_agent = None, ttl_s = None) :
        root   = self.root
        cookie = self.cookies.get (name)
        if not cookie:
            return None
        parts  = cookie.split ("|", 2)
        if len (parts) != 3 :
            return None
        (data, timestamp, signature) = parts
        enc = self.cookie_encoding
        try:
            result = base64.b64decode (data).decode (enc)
        except Exception :
            return None
        secrets = None
        if secret_agent :
            secrets = secret_agent (self, result, timestamp)
        wanted_sig = self._cookie_signature (data, timestamp, secrets = secrets)
        if not root.HTTP.safe_str_cmp (signature, wanted_sig) :
            logging.warning ("Invalid cookie signature %r", result)
            return None
        try :
            timestamp = base64.b64decode (timestamp).decode (enc)
        except Exception :
            pass
        try :
            then = int (timestamp)
        except Exception :
            return None
        now = self.current_time ()
        ttl = ttl_s if ttl_s is not None else self.resource.session_ttl_s
        if then < (now - ttl) :
            logging.warning ("Expired cookie %r older then %s", data, ttl)
            return None
        if then > now + 180 :
            ### don't accept cookies with a timestamp more than 2 minutes in
            ### the future
            logging.warning \
                ( "Time-travelling cookie %r [%s seconds ahead]"
                , data, then - now
                )
            return None
        return result
    # end def secure_cookie

    def use_language (self, langs) :
        self.lang = langs
        I18N.use (* langs)
    # end def use_language

    def _cookie_signature (self, * parts, ** kw):
        enc     = self.cookie_encoding
        secrets = (self.settings ["cookie_salt"], kw.pop ("secrets", None))
        result  = hmac.new \
            (unicode (secrets).encode (enc), digestmod = self.root.hash_fct)
        for part in parts:
            result.update (b":::")
            result.update (part)
        return result.hexdigest ()
    # end def _cookie_signature

Request = _RST_Request_ # end class

if __name__ != "__main__" :
    GTW.RST._Export ("Request")
### __END__ GTW.RST.Request

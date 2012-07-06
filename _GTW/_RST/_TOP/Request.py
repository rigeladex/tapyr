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
#    GTW.RST.TOP.Request
#
# Purpose
#    Extend GTW.RST.Request with session handling
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _GTW.File_Session
import _GTW._RST._TOP
import _GTW._RST.Request

### XXX replace home-grown code by werkzeug supplied functions
### XXX     werkzeug.utils, werkzeug.HTTP, ...

import base64
import datetime
import hashlib
import hmac
import logging
import time

class _RST_TOP_Request_ (GTW.RST.Request) :
    """Extend GTW.RST.Request with session handling."""

    _real_name = "Request"

    @Once_Property
    def cookie_encoding (self) :
        return self.settings.get ("cookie_encoding", "utf-8")
    # end def cookie_encoding

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        codes = self.get_user_locale_codes ()
        if not codes :
            codes = self.__super.locale_codes ()
        assert codes
        return codes
    # end def locale_codes

    @Once_Property
    def session (self) :
        cookie_name = self.session_cookie_name
        S_Class     = self.settings.get  ("Session_Class", GTW.File_Session)
        sid         = self.secure_cookie (cookie_name)
        session     = S_Class (sid, self.settings, self._session_hasher)
        return session
    # end def session

    @Once_Property
    def session_cookie_name (self) :
        return self.settings.get ("session_id",  "SESSION_ID")
    # end def session_cookie_name

    @property
    def username (self) :
        return self.session.username
    # end def username

    @Once_Property
    def user_session_ttl (self) :
        result = self.settings.get ("user_session_ttl", 31 * 86400)
        if not isinstance (result, datetime.timedelta) :
            result = datetime.timedelta (seconds = result)
        return result
    # end def user_session_ttl

    @Once_Property
    def user_session_ttl_s (self) :
        ttl = self.user_session_ttl
        try :
            return ttl.total_seconds ()
        except AttributeError :
            return (ttl.days * 86400 + ttl.seconds)
    # end def user_session_ttl_s

    def cookie (self, name) :
        return self.cookies.get (name)
    # end def cookie

    def get_user_locale_codes (self) :
        supported = getattr (self.root, "languages", set ())
        result    = tuple \
            (l for l in self.session.get ("language", ()) if l in supported)
        return result
    # end def get_user_locale_codes

    def secure_cookie (self, name) :
        ### based on `tornado.web.Request.get_secure_cookie`
        cookie = self.cookies.get (name)
        if not cookie:
            return None
        parts = cookie.split ("|")
        if len (parts) != 3 :
            return None
        (data, timestamp, signature) = parts
        if not self.root.HTTP.safe_str_cmp \
                (signature, self._cookie_signature (data, timestamp)) :
            logging.warning ("Invalid cookie signature %r", data)
            return None
        if int (timestamp) < time.time () - self.user_session_ttl_s :
            logging.warning ("Expired cookie %r", data)
            return None
        try:
            return base64.b64decode (data).decode (self.cookie_encoding)
        except Exception :
            return None
    # end def secure_cookie

    def _cookie_signature (self, * parts):
        hash = hmac.new\
            (self.settings ["cookie_salt"], digestmod = hashlib.sha1)
        for part in parts:
            hash.update (part)
        return hash.hexdigest ()
    # end def _cookie_signature

    def _session_hasher (self, username) :
        hash = hashlib.sha224 (str (self._session_sig (username))).digest ()
        return base64.b64encode (hash, "~@").rstrip ("=")
    # end def _session_hasher

    def _session_sig (self, username) :
        root  = self.root
        scope = root.scope
        user  = root._get_user (username)
        return \
            ( getattr (user, "password", username)
            , scope and scope.db_meta_data.dbid or 42
            )
    # end def _session_sig

Request = _RST_TOP_Request_ # end class

if __name__ != "__main__" :
    GTW.RST.TOP._Export ("Request")
### __END__ GTW.RST.TOP.Request

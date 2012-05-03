# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW._Request_Handler_
#
# Purpose
#    Mixin on to provide common functions for all backend specific request
#    handlers
#
# Revision Dates
#    19-Jun-2010 (MG) Creation (factored from GTW.Werkzeug.Request_Handler
#                     and GTW.Tornado.Request_Handler)
#    23-Jun-2010 (MG) `s/anonymous/anonymous_account/`
#    23-Jul-2010 (MG) `add_notification` added
#     9-Aug-2010 (MG) `_NAV_Request_Handler_._handle_request` scope rollback
#                     in case of exceptions added
#    30-Nov-2010 (CT) Superfluous imports removed
#    30-Nov-2010 (CT) `_handle_request` changed to deal with `Fatal_Exceptions`
#     2-Dec-2010 (CT) `_handle_request` change fixed
#    11-Jan-2011 (CT) s/json/write_json/
#    11-Jan-2011 (CT) `json` added to provide the request's json data, if any
#    11-Jan-2011 (CT) `content-encoding` added to `json`
#    10-Mar-2011 (CT) `session_hash` added
#    11-Mar-2011 (CT) s/cookie_secret/cookie_salt/
#    11-Mar-2011 (CT) Checking of `session_hash` moved to `session`
#    11-Mar-2011 (CT) `username` and `current_user` added
#    30-Mar-2011 (CT) `** kw` added to `write_json`
#     6-Apr-2011 (CT) Properties `content_type` and `content_encoding` added
#     6-Apr-2011 (CT) `_handle_request_exception_nav` factored from descendents
#     2-May-2011 (CT) `json` changed to raise `Error_400` in case of exceptions
#     2-May-2011 (CT) `session` changed to use `self.user_session_ttl`
#                     instead of  hard-coded value (720 days)
#     3-May-2011 (CT) `user_session_ttl_s` added, `user_session_ttl` changed
#                     to return `timedelta` instance instead of seconds
#    11-May-2011 (MG) `username`: change session id on username changes
#    31-May-2011 (MG) `default_content_encoding` added
#    24-Nov-2011 (CT) Add `accept_header` and `wants_json`
#     5-Apr-2012 (CT) Remove `current_user`; move `_get_user` to `GTW.NAV`
#     3-May-2012 (CT) Change `get_browser_locale_codes` to consider
#                     `supported; `use `en`, not `en_US`, as last resort
#    ««revision-date»»···
#--

from   _GTW                       import GTW
from   _TFL                       import TFL
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.predicate             import split_hst
from   _TFL                       import I18N
from   _TFL                       import pyk

import base64
import datetime
import hashlib
import json
import sys

class _Request_Handler_ (object) :
    """Mixin for request handlers."""

    _content_type            = None
    _content_encoding        = None
    default_content_encoding = "utf-8"

    @property
    def accept_header (self) :
        return self.request.headers.get ("Accept", "")
    # end def accept_header

    @property
    def content_encoding (self) :
        if self._content_encoding is None :
            headers = self.request.headers
            ce      = headers.get ("content-encoding")
            if ce :
                self._content_encoding = ce.strip ()
            else :
                _ = self.content_type ### might load _content_encoding
        return self._content_encoding
    # end def content_encoding

    @property
    def content_type (self) :
        if self._content_type is None :
            headers   = self.request.headers
            ct, _, ce = split_hst (headers.get ("content-type", ""), ";")
            self._content_type = ct.strip ()
            if not self._content_encoding :
                h, s, t = split_hst (ce, "=")
                self._content_encoding = t.strip ()
                if not self._content_encoding :
                    if __debug__ :
                        if self.body :
                            print "Use Fallback default content encoding %s" % \
                                (self.default_content_encoding, )
                    self._content_encoding = self.default_content_encoding
        return self._content_type
    # end def content_type

    @Once_Property
    def json (self) :
        if self.content_type == "application/json" :
            try :
                return json.loads (self.body, self.content_encoding)
            except Exception as exc :
                err = self.request.Error = unicode (exc)
                raise self.PNS.Error_400 (err)
    # end def json

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        codes = self.get_user_locale_codes ()
        if not codes :
            codes = self.get_browser_locale_codes ()
        assert codes
        return codes
    # end def locale_codes

    @Once_Property
    def session (self) :
        cookie_name = self.session_cookie_name
        settings    = self.settings
        S_Class     = settings           ["Session_Class"]
        sid         = self.secure_cookie (cookie_name)
        session     = S_Class            (sid, settings, self._session_hasher)
        self._set_session_cookie         (session)
        return session
    # end def session

    @Once_Property
    def session_cookie_name (self) :
        return self.settings.get ("session_id",  "SESSION_ID")
    # end def session_cookie_name

    @Once_Property
    def settings (self) :
        return self.application.settings
    # end def settings

    @property
    def username (self) :
        return self.session.username
    # end def username

    @username.setter
    def username (self, value) :
        if value != self.username :
            self.session.username = value
            self._set_session_cookie (self.session.renew_session_id ())
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

    @Once_Property
    def wants_json (self) :
        ### XXX need to parse the accept header (quality preferences!)
        ### http://shiflett.org/blog/2011/may/the-accept-header
        return "json" in self.accept_header
    # end def wants_json

    def add_notification (self, noti) :
        notifications = self.session.notifications
        if notifications is not None :
            if not isinstance (noti, GTW.Notification) :
                noti = GTW.Notification (noti)
            notifications.append (noti)
    # end def add_notification

    def get_browser_locale_codes (self) :
        """Determines the user's locale from Accept-Language header."""
        if "Accept-Language" in self.request.headers :
            languages = self.request.headers ["Accept-Language"].split (",")
            locales   = []
            supported = self.settings.get ("languages", set ())
            for language in languages :
                parts = language.strip ().split (";")
                l = parts [0]
                if l in supported :
                    if len (parts) > 1 and parts [1].startswith ("q="):
                        try :
                            score = float (parts [1][2:])
                        except (ValueError, TypeError):
                            score = 0.0
                    else:
                        score = 1.0
                    locales.append ((l, score))
            if locales :
                locales.sort (key=lambda (l, s): s, reverse = True)
                return [l [0] for l in locales]
        return (self.settings.get ("default_locale_code", "en"), )
    # end def get_browser_locale_codes

    def get_user_locale_codes (self) :
        supported = self.settings.get ("languages", set ())
        result    = tuple \
            (l for l in self.session.get ("language", ()) if l in supported)
        return result
    # end def get_user_locale_codes

    def write_json (self, __data = None, ** kw) :
        data = dict (kw)
        if __data is not None :
            data.update (__data)
        self.set_header ("Content-Type", "text/javascript; charset=UTF-8")
        self.write      (json.dumps (data))
        return True
    # end def write_json

    def _session_hasher (self, username) :
        hash = hashlib.sha224 (str (self._session_sig (username))).digest ()
        return base64.b64encode (hash, "~@").rstrip ("=")
    # end def _session_hasher

    def _session_sig (self, username) :
        return (42, username)
    # end def _session_sig

    def _set_session_cookie (self, session) :
        cookie_name = self.session_cookie_name
        self.set_secure_cookie \
            (cookie_name, session.sid, max_age = self.user_session_ttl)
        GTW.Notification_Collection (session)
    # end def _set_session_cookie

# end class _Request_Handler_

class _NAV_Request_Handler_ (_Request_Handler_) :
    """Mixin for all request handlers using GTW.NAV"""

    @property
    def scope (self) :
        return getattr (self.nav_root, "scope", None)
    # end def scope

    def finish_request (self, scope = None) :
        self.session.save ()
        if scope :
            scope.commit  ()
    # end def finish_request

    def _handle_request (self, * args, ** kw) :
        if self.settings.get ("i18n", False) :
            I18N.use (* self.locale_codes)
        top    = self.nav_root
        scope  = getattr (top, "scope", None)
        FEs    = getattr (scope, "Fatal_Exceptions", ())
        result = (None, None)
        try :
            try :
                top.universal_view (self)
            except top.HTTP._Redirect_ as redirect :
                result = redirect, top
            self.finish_request (scope)
        except FEs :
            result = top.HTTP.Error_503 (), top
        except top.HTTP.Error_503 as exc:
            result = exc, top
        return result
    # end def _handle_request

    def _handle_request_exception_nav (self, exc) :
        top   = self.nav_root
        scope = getattr (top, "scope", None)
        if scope :
            if not isinstance (exc, top.HTTP.Status) :
                pyk.fprint \
                    ( ">>> Exception"
                    , exc
                    , "during request handling, rolling back the database"
                    , file = sys.stderr
                    )
                if __debug__ :
                    import traceback; traceback.print_exc ()
            try :
                scope.rollback ()
            except Exception :
                pass
    # end def _handle_request_exception_nav

    def _session_sig (self, username) :
        scope = self.scope
        user  = self.nav_root._get_user (username)
        return \
            ( getattr (user, "password", username)
            , scope and scope.db_meta_data.dbid
            )
    # end def _session_sig

# end class _NAV_Request_Handler_

if __name__ != "__main__" :
    GTW._Export ("_Request_Handler_", "_NAV_Request_Handler_")
### __END__ GTW._Request_Handler_

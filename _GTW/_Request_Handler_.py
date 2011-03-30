# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Martin Glueck All rights reserved
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
#    ��revision-date�����
#--

from   _GTW                       import GTW
from   _TFL                       import TFL
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL                       import I18N
from   _TFL                       import pyk

import base64
import hashlib
import json
import sys

class _Request_Handler_ (object) :
    """Mixin for request handlers."""

    @property
    def current_user (self) :
        return None
    # end def current_user

    @Once_Property
    def json (self) :
        headers = self.request.headers
        if headers.get ("content-type") == "application/json" :
            encoding = headers.get ("content-encoding")
            return json.loads (self.body, encoding)
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
        settings    = self.application.settings
        SID_Cookie  = settings.get       ("session_id",  "SESSION_ID")
        S_Class     = settings           ["Session_Class"]
        sid         = self.secure_cookie (SID_Cookie)
        session     = S_Class            (sid, settings, self._session_hasher)
        self.set_secure_cookie           (SID_Cookie, session.sid, 720)
        GTW.Notification_Collection      (session)
        return session
    # end def session

    @property
    def username (self) :
        return self.session.username
    # end def username

    @username.setter
    def username (self, value) :
        self.session.username = value
    # end def username

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
            for language in languages :
                parts = language.strip ().split (";")
                if len (parts) > 1 and parts [1].startswith ("q="):
                    try :
                        score = float (parts [1][2:])
                    except (ValueError, TypeError):
                        score = 0.0
                else:
                    score = 1.0
                locales.append ((parts [0], score))
            if locales :
                locales.sort (key=lambda (l, s): s, reverse = True)
                return [l [0] for l in locales]
        return \
            (self.application.settings.get ("default_locale_code", "en_US"), )
    # end def get_browser_locale_codes

    def get_user_locale_codes (self) :
        return self.session.get ("language")
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

# end class _Request_Handler_

class _NAV_Request_Handler_ (_Request_Handler_) :
    """Mixin for all request handlers using GTW.NAV"""

    @property
    def current_user (self) :
        return self._get_user (self.username)
    # end def current_user

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
        if self.application.settings.get ("i18n", False) :
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
        except Exception as exc :
            if scope :
                pyk.fprint \
                    ( ">>> Exception"
                    , exc
                    , "during request handling, rolling back the database"
                    , file = sys.stderr
                    )
                scope.rollback ()
            raise
        return result
    # end def _handle_request

    def _get_user (self, username) :
        top    = self.nav_root
        result = top.anonymous_account
        if username :
            try :
                result = top.account_manager.query (name = username).one ()
            except IndexError :
                pass
            except Exception as exc :
                pyk.fprint \
                    ( ">>> Exception"
                    , exc
                    , "when trying to determine the user"
                    , file = sys.stderr
                    )
        return result
    # end def _get_user

    def _session_sig (self, username) :
        scope = self.scope
        user  = self._get_user (username)
        return \
            ( getattr (user, "password", username)
            , scope and scope.db_meta_data.dbid
            )
    # end def _session_sig

# end class _NAV_Request_Handler_

if __name__ != "__main__" :
    GTW._Export ("_Request_Handler_", "_NAV_Request_Handler_")
### __END__ GTW._Request_Handler_

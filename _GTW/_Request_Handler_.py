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
#    ««revision-date»»···
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

    def add_notification (self, noti) :
        notifications = self.session.notifications
        if notifications is not None :
            if not isinstance (noti, GTW.Notification) :
                noti = GTW.Notification (noti)
            notifications.append (noti)
    # end def add_notification

    @Once_Property
    def session (self) :
        settings    = self.application.settings
        SID_Cookie  = settings.get       ("session_id", "SESSION_ID")
        secret      = settings.get       ("cookie_secret", "")
        S_Class     = settings           ["Session_Class"]
        s_hash      = self._session_hash
        sid         = self.secure_cookie (SID_Cookie)
        if sid is not None :
            session = S_Class (sid, secret)
            if session.session_hash != s_hash :
                sid = None
        if sid is None :
            session = S_Class (sid, secret)
        self.set_secure_cookie      (SID_Cookie, session.sid)
        GTW.Notification_Collection (session)
        session.session_hash = s_hash
        return session
    # end def session

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

    def write_json (self, data) :
        self.set_header ("Content-Type", "text/javascript; charset=UTF-8")
        self.write      (json.dumps (data))
        return True
    # end def write_json

    @property
    def _session_hash (self) :
        hash = hashlib.sha224 (str (self._session_sig)).digest ()
        return base64.b64encode (hash, "~@").rstrip ("=")
    # end def _session_hash

    @property
    def _session_sig (self) :
        return 42
    # end def _session_sig

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

    def get_current_user (self) :
        top      = self.nav_root
        username = self.get_secure_cookie ("username")
        result   = top.anonymous_account
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
    # end def get_current_user

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

    @property
    def _session_sig (self) :
        scope = self.scope
        user  = self.current_user
        return \
            ( getattr (user, "password", user.name)
            , scope and scope.db_meta_data.dbid
            )
    # end def _session_sig

# end class _NAV_Request_Handler_

if __name__ != "__main__" :
    GTW._Export ("_Request_Handler_", "_NAV_Request_Handler_")
### __END__ GTW._Request_Handler_

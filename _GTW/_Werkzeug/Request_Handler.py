# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Werkzeug.
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
#    GTW.Werkzeug.Request_Handler
#
# Purpose
#    A Tronado like handler for a request
#
# Revision Dates
#    20-Mar-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                           import TFL
import _TFL._Meta.Object
from   _TFL._Meta.Once_Property       import Once_Property
from   _TFL                           import I18N

from   _GTW                           import GTW
import _GTW._Werkzeug
import _GTW.Notification

from    werkzeug.contrib.securecookie import SecureCookie
from    werkzeug                      import Response, BaseRequest

import  base64
import  calendar
import  datetime
import  email.utils
import  hashlib
import  hmac
import  logging
import  time

try :
    import json
except ImportError :
    import simplejson as json

def _time_independent_equals (l, r) :
    if len (l) != len (r) :
        return False
    result = 0
    for x, y in zip (l, r) :
        result |= ord (x) ^ ord (y)
    return result == 0
# end ef _time_independent_equals

class Request_Handler (TFL.Meta.Object) :
    """Extended Request."""

    _real_name                = "Request"
    secure_cookie_exipre_time = 31 * 86400

    def __init__ (self, application, environ) :
        self.application = application
        self.request     = BaseRequest (environ)
        self.response    = Response    ()
    # end def __init__

    def clear_cookie (self, name, * args, ** kw) :
        self.response.delete_cookie (name, * args, ** kw)
    # end def clear_cookie

    def clear (self) :
        self.response.headers.clear ()
        self.response.response = []
    # end def clear

    @Once_Property
    def current_user (self) :
        return None
    # end def current_user

    def _cookie_signature (self, * parts):
        hash = hmac.new\
            ( self.application.settings ["cookie_secret"]
            , digestmod = hashlib.sha1
            )
        for part in parts:
            hash.update (part)
        return hash.hexdigest ()
    # end def _cookie_signature

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

    def finish (self, scope = None) :
        self.session.save ()
        if scope :
            scope.commit  ()
    # end def finish

    def _handle_request_exception (self, exc) :
        if isinstance (exc, GTW.Werkzeug.Status) :
            return exc (self)
        if 1 :
            import traceback
            print "*" * 79
            traceback.print_exc ()
            print "*" * 79
        raise exc
    # end def _handle_request_exception

    def json (self, data) :
        self.set_header ("Content-Type", "text/javascript; charset=UTF-8")
        self.write      (json.dumps (data))
        return True
    # end def json

    def secure_cookie (self, name) :
        ### based on the implementation of tornado.web.Request.get_secure_cookie
        data = self.request.cookies.get (name)
        if not data :
            return None
        parts = data.split ("|")
        if len (parts) != 3 :
            return None
        if not _time_independent_equals \
            (parts [2], self._cookie_signature (parts[0], parts[1])) :
            logging.warning ("Invalid cookie signature %r", data)
            return None
        timestamp = int (parts [1])
        if timestamp < time.time () - self.secure_cookie_exipre_time :
            logging.warning ("Expired cookie %r", data)
            return None
        try:
            return base64.b64decode (parts[0])
        except:
            return None
    # end def secure_cookie

    @Once_Property
    def session (self) :
        settings   = self.application.settings
        SID_Cookie = settings.get ("session_id", "SESSION_ID")
        sid        = self.secure_cookie (SID_Cookie)
        session    = settings ["Session_Class"] \
            (sid, settings.get ("cookie_secret", ""))
        self.set_secure_cookie          (SID_Cookie, session.sid)
        GTW.Notification_Collection     (session)
        return session
    # end def session

    def set_cookie ( self, key
                   , value      = ""
                   , max_age    = None
                   , expires    = None
                   , path       = "/"
                   , domain     = None
                   , secure     = None
                   , httponly   = False
                   ) :
        if isinstance (expires, datetime.datetime):
            timestamp = calendar.timegm (expires.utctimetuple ())
            expires   = email.utils.formatdate \
                (timestamp, localtime = False, usegmt = True)
        return self.response.set_cookie \
            (key, value, max_age, expires, path, domain, secure, httponly)
    # end def set_cookie

    def set_header (self, key, value) :
        if isinstance (value, datetime.datetime) :
            t     = calendar.timegm(value.utctimetuple())
            value = email.utils.formatdate (t, localtime = False, usegmt = True)
        self.response.headers [key] = value
    # end def set_header

    def set_status (self, code) :
        self.response.status_code = code
    # end def set_status

    def set_secure_cookie (self, name, data, expires_days = 30, ** kw) :
        timestamp = str (int (time.time ()))
        data      = base64.b64encode (data)
        signature = self._cookie_signature (data, timestamp)
        data      = "|".join ((data, timestamp, signature))
        expires   = ( datetime.datetime.utcnow ()
                    + datetime.timedelta       (days = expires_days)
                    )
        self.set_cookie (name, data, expires = expires, ** kw)
    # end def set_secure_cookie

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        codes = self.get_user_locale_codes ()
        if not codes :
            codes = self.get_browser_locale_codes ()
        assert codes
        return codes
    # end def locale_codes

    def write (self, data) :
        self.response.response.append (data)
    # end def write

    def __call__ (self, environ, start_response) :
        self.set_header               ("Content-Type", "text/html")
        self.response.response.append ("Hello World")
        return self.response          (environ, start_response)
    # end def __call__

# end class Request_Handler

class NAV_Request_Handler (Request_Handler) :
    """A request handler which uses GTW.NAV features."""

    def __init__ (self, application, environ, nav_root) :
        self.__super.__init__ (application, environ)
        self.nav_root = nav_root
    # end def __init__

    def __call__ (self, environ, start_response) :
        top = self.nav_root
        self.set_header ("Content-Type", "text/html")
        if self.application.settings.get ("i18n", False) :
            I18N.use         (* self.locale_codes)
        top.universal_view   (self)
        self.finish          (getattr (top, "scope", None))
        return self.response (environ, start_response)
    # end def __call__

    @Once_Property
    def current_user (self) :
        top      = self.nav_root
        username = self.secure_cookie ("username")
        result   = top.anonymous
        if username :
            try :
                result = top.account_manager.query (name = username).one ()
            except IndexError :
                pass
        return result
    # end def current_user

    def _handle_request_exception (self, exc) :
        top   = self.nav_root
        scope = getattr (top, "scope", None)
        if scope :
            scope.rollback ()
        if isinstance (exc, top.HTTP.Status) :
            return exc (self)
        raise exc
    # end def _handle_request_exception

# end class NAV_Request_Handler

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Request

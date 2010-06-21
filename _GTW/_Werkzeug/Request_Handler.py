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
#    20-Jun-2010 (MG) `GTW._Request_Handler_` factored
#    ««revision-date»»···
#--

from   _TFL                           import TFL
import _TFL._Meta.Object
from   _TFL._Meta.Once_Property       import Once_Property
from   _TFL                           import I18N

from   _GTW                           import GTW
import _GTW._Werkzeug
import _GTW._Request_Handler_
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

def _time_independent_equals (l, r) :
    if len (l) != len (r) :
        return False
    result = 0
    for x, y in zip (l, r) :
        result |= ord (x) ^ ord (y)
    return result == 0
# end ef _time_independent_equals

class Request_Handler (GTW._Request_Handler_) :
    """Extended Request."""

    __metaclass__ = TFL.Meta.M_Class

    _real_name                = "Request"
    secure_cookie_exipre_time = 31 * 86400
    cookie_encoding           = "utf-8"

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
            return base64.b64decode (parts[0]).decode (self.cookie_encoding)
        except:
            return None
    # end def secure_cookie
    get_secure_cookie = secure_cookie

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
        if isinstance (value, unicode) :
            value = value.encode (self.cookie_encoding)
        return self.response.set_cookie \
            (key, value, max_age, expires, path, domain, secure, httponly)
    # end def set_cookie

    def set_header (self, key, value) :
        if isinstance (value, datetime.datetime) :
            t     = calendar.timegm (value.utctimetuple ())
            value = email.utils.formatdate (t, localtime = False, usegmt = True)
        self.response.headers [key] = value
    # end def set_header

    def set_status (self, code) :
        self.response.status_code = code
    # end def set_status

    def set_secure_cookie (self, name, data, expires_days = 30, ** kw) :
        timestamp = str (int (time.time ()))
        if isinstance (data, unicode) :
            data  = data.encode (self.cookie_encoding)
        data      = base64.b64encode       (data)
        signature = self._cookie_signature (data, timestamp)
        data      = "|".join ((data, timestamp, signature))
        expires   = ( datetime.datetime.utcnow ()
                    + datetime.timedelta       (days = expires_days)
                    )
        self.set_cookie (name, data, expires = expires, ** kw)
    # end def set_secure_cookie

    def write (self, data) :
        self.response.response.append (data)
    # end def write

    def __call__ (self, environ, start_response) :
        self.set_header               ("Content-Type", "text/html")
        self.response.response.append ("Hello World")
        return self.response          (environ, start_response)
    # end def __call__

# end class Request_Handler

class NAV_Request_Handler (GTW._NAV_Request_Handler_, Request_Handler) :
    """A request handler which uses GTW.NAV features."""

    def __init__ (self, application, environ, nav_root) :
        self.__super.__init__ (application, environ)
        self.nav_root = nav_root
    # end def __init__

    def __call__ (self, environ, start_response) :
        self.set_header                      ("Content-Type", "text/html")
        redirect, top = self._handle_request ()
        if redirect :
            raise redirect
        return self.response (environ, start_response)
    # end def __call__

    current_user = Once_Property (GTW._NAV_Request_Handler_.get_current_user)

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

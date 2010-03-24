# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    GTW.Tornado.Request_Handler
#
# Purpose
#    Provide a base class for request handlers
#
# Revision Dates
#    12-Sep-2009 (MG) Creation
#    20-Feb-2010 (MG) Add the notification collection to the session
#    23-Feb-2010 (MG) `json` added
#    20-Mar-2010 (MG) `NAV_Request_Handler` moved in here
#    24-Mar-2010 (CT) `tornado.httpserver.HTTPRequest.url` set as alias for
#                     `uri`
#    ««revision-date»»···
#--

from   _TFL                       import TFL
from   _TFL._Meta.Once_Property   import Once_Property
import _TFL._Meta.Object
from   _TFL                       import I18N

from   _GTW                       import GTW
import _GTW.Notification
import _GTW._Tornado

import  locale
from    tornado                   import web, escape

import  tornado.httpserver
tornado.httpserver.HTTPRequest.url = TFL.Meta.Alias_Property ("uri")

class Request_Handler (web.RequestHandler, TFL.Meta.Object) :
    """Base class for a request handler"""

    @Once_Property
    def session (self) :
        settings   = self.application.settings
        SID_Cookie = settings.get ("session_id", "SESSION_ID")
        sid        = self.get_secure_cookie (SID_Cookie)
        session    = settings ["Session_Class"] \
            (sid, settings.get ("cookie_secret", ""))
        if not sid :
            self.set_secure_cookie      (SID_Cookie, session.sid)
        GTW.Notification_Collection     (session)
        return session
    # end def session

    @Once_Property
    def locale_codes (self) :
        """The locale-code for the current session."""
        codes = self.get_user_locale_codes ()
        if not codes :
            codes = self.get_browser_locale_codes ()
        assert codes
        return codes
    # end def locale_codes

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
            (self.application.settings.get ("defailt_locale_code", "en_US"), )
    # end def get_browser_locale_codes

    def get_user_locale_codes (self) :
        return self.session.get ("language")
    # end def get_user_locale_codes

    def json (self, data) :
        self.set_header ("Content-Type", "text/javascript; charset=UTF-8")
        self.write      (escape.json_encode (data))
        return True
    # end def json

# end class Request_Handler

class M_Request_Handler (Request_Handler.__class__) :
    """Metaclass for a request"""

    def __init__ (cls, name, bases, dict) :
        super (M_Request_Handler, cls).__init__ (name, bases, dict)
        for m in cls.SUPPORTED_METHODS :
            m_method_name = m.lower ()
            if not m_method_name in dict :
                setattr (cls, m_method_name, getattr (cls, cls.DEFAULT_HANDLER))
    # end def __init__

# end class M_Request_Handler

class NAV_Request_Handler (Request_Handler) :
    """Base class request handlers interacting with GTW.NAV"""

    __metaclass__   = M_Request_Handler

    DEFAULT_HANDLER = "_handle_request"

    def _finish (self, scope) :
        self.session.save ()
        if scope :
            scope.commit  ()
    # end def _finish

    def _handle_request (self, * args, ** kw) :
        if self.application.settings.get ("i18n", False) :
            I18N.use (* self.locale_codes)
        top   = GTW.NAV.Root.top
        scope = getattr (top, "scope", None)
        try :
            top.universal_view (self)
        except top.HTTP._Redirect_, redirect :
            self._finish    (scope)
            return redirect (self, top)
        self._finish (scope)
    # end def _handle_request

    def _handle_request_exception (self, exc) :
        top   = GTW.NAV.Root.top
        scope = getattr (top, "scope", None)
        if scope :
            scope.rollback ()
        if isinstance (exc, top.HTTP.Status) :
            if exc (self, top) :
                return
        self.__super._handle_request_exception (exc)
    # end def _handle_request_exception

    def get_current_user (self) :
        top      = GTW.NAV.Root.top
        username = self.get_secure_cookie ("username")
        result   = top.anonymous
        if username :
            try :
                result = top.account_manager.query (name = username).one ()
            except IndexError :
                pass
        return result
    # end def get_current_user

# end class NAV_Request_Handler

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Request_Handler

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
#    ««revision-date»»···
#--

from   _TFL                       import TFL
from   _TFL._Meta.Once_Property   import Once_Property
import _TFL._Meta.Object

import  locale

from    tornado            import web

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
            self.set_secure_cookie (SID_Cookie, session.sid)
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

# end class Request_Handler

if __name__ != "__main__" :
    from   _GTW            import GTW
    import _GTW._Tornado
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Request_Handler

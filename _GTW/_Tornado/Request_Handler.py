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
#    20-Jun-2010 (MG) `GTW._Request_Handler_` factored
#    25-Jun-2010 (MG) Changed to generate a common interface between Werkzeug
#                     and Tornado
#    ««revision-date»»···
#--

from   _TFL                       import TFL
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL                       import I18N

from   _GTW                       import GTW
import _GTW._Request_Handler_
import _GTW.Notification
import _GTW._Tornado

from    tornado                   import web, escape

import  tornado.httpserver
tornado.httpserver.HTTPRequest.url = TFL.Meta.Alias_Property ("uri")

class Request_Handler (GTW._Request_Handler_, web.RequestHandler) :
    """Base class for a request handler"""

    secure_cookie = TFL.Meta.Alias_Property ("get_secure_cookie")

# end class Request_Handler

class M_Request_Handler (TFL.Meta.M_Class, Request_Handler.__class__) :
    """Metaclass for a request"""

    def __init__ (cls, name, bases, dict) :
        super (M_Request_Handler, cls).__init__ (name, bases, dict)
        for m in cls.SUPPORTED_METHODS :
            m_method_name = m.lower ()
            if not m_method_name in dict :
                setattr (cls, m_method_name, getattr (cls, cls.DEFAULT_HANDLER))
    # end def __init__

# end class M_Request_Handler

class NAV_Request_Handler (GTW._NAV_Request_Handler_, Request_Handler) :
    """Base class request handlers interacting with GTW.NAV"""

    __metaclass__   = M_Request_Handler

    DEFAULT_HANDLER = "_handle_request"

    def __init__ (self, * args, ** kw) :
        self.nav_root = kw.pop ("nav_root")
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def _handle_request (self, * args, ** kw) :
        redirect, top = self.__super._handle_request (* args, ** kw)
        if redirect :
            return redirect (self, top)
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

# end class NAV_Request_Handler

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Request_Handler

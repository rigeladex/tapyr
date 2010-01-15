# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.NAV.
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
#    GTW.NAV.Request_Handler
#
# Purpose
#    A Request handler which interacts nicely with GTW.NAV
#
# Revision Dates
#    13-Sep-2009 (MG) Creation
#    10-Jan-2010 (MG) Moved into package `GTW.NAV`
#    ««revision-date»»···
#--

from   _GTW                    import GTW
import _GTW._NAV
import _GTW._Tornado
import _GTW._Tornado.Request_Handler

class M_Request_Handler (GTW.Tornado.Request_Handler.__class__) :
    """Metaclass for a request"""

    def __init__ (cls, name, bases, dict) :
        super (M_Request_Handler, cls).__init__ (name, bases, dict)
        for m in cls.SUPPORTED_METHODS :
            m_method_name = m.lower ()
            if not m_method_name in dict :
                setattr (cls, m_method_name, getattr (cls, cls.DEFAULT_HANDLER))
    # end def __init__

# end class M_Request_Handler

class _NAV_Request_Handler_ (GTW.Tornado.Request_Handler) :
    """Base class request handlers interacting with GTW.NAV"""

    _real_name      = "Request_Handler"
    __metaclass__   = M_Request_Handler

    DEFAULT_HANDLER = "_handle_request"

    def _handle_request (self, * args, ** kw) :
        GTW.NAV.Root.universal_view (self)
    # end def _handle_request

    def _handle_request_exception (self, exc) :
        top = GTW.NAV.Root.top
        if isinstance (exc, top.HTTP.Status) :
            if exc (self, top) :
                return
        self.__super._handle_request_exception (exc)
    # end def _handle_request_exception

Request_Handler = _NAV_Request_Handler_ # end class

if __name__ != "__main__" :
    GTW.NAV._Export ("*")
### __END__ GTW.NAV.Request_Handler

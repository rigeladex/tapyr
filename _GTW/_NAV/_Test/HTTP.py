# -*- coding: utf-8 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.NAV.Test.
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
#    GTW.NAV.Test.HTTP
#
# Purpose
#    Classes and function to simulate a HTTP request for testing purposes
#
# Revision Dates
#    19-Feb-2010 (MG) Creation
#    20-Feb-2010 (MG) Use `GTW.Memory_Session` and add a notification to the
#                     session
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object

from   _GTW                  import GTW
import _GTW.Memory_Session
import _GTW.Notification
import _GTW._NAV._Test

class Handler (TFL.Meta.Object) :
    """A fake HHTP handler."""

    session = GTW.Memory_Session ()
    GTW.Notification_Collection  (session)

    def __init__ ( self, path
                 , method  = "GET"
                 , user    = None
                 , headers = {}
                 , ** kw
                 ) :
        self.request      = Request (path, method, headers, ** kw)
        self.current_user = user
    # end def __init__

    def write (self, args, ** kw) :
        self.template, self.context = args
    # end def write

    def clear_cookie (self, name) :
        self.session.pop (name, None)
    # end def clear_cookie

    def set_secure_cookie (self, name, value) :
        self.session [name] = value
    # end def set_secure_cookie

# end class Handler

class Request (TFL.Meta.Object) :
    """A faked HHTP request used for testing purposes."""

    def __init__ (self, path, method, headers, ** arguments) :
        self.path         = path
        self.uri          = path
        self.method       = method
        self.headers      = headers
        self.arguments    = arguments
    # end def __init__

# end class Request

Request_Data = dict

class _HTTP_Exception_ (StandardError)    : pass

class _HTTP_Redirect_  (_HTTP_Exception_) : pass
class Redirect_301     (_HTTP_Redirect_)  : pass
class Redirect_302     (_HTTP_Redirect_)  : pass
class Redirect_304     (_HTTP_Redirect_)  : pass

class _HTTP_Error_     (_HTTP_Exception_) : pass
class Error_401        (_HTTP_Error_)     : pass
class Error_403        (_HTTP_Error_)     : pass
class Error_404        (_HTTP_Error_)     : pass
class Error_405        (_HTTP_Error_)     : pass
class Error_500        (_HTTP_Error_)     : pass

if __name__ != "__main__" :
    GTW.NAV.Test._Export ("*")
### __END__ GTW.NAV.Test.HTTP

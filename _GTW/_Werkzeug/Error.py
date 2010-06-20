# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
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
#    GTW.Werkzeug.Error
#
# Purpose
#    Define special error exceptions
#
# Revision Dates
#    20-Mar-2010 (MG) Creation (based on GTW.Tornado.Error)
#     6-May-2010 (MG) `Status.__init__` `* args` added
#    20-Jun-2010 (MG) `s/finish/finish_request/g`
#    ««revision-date»»···
#--

from   _GTW                 import GTW
from   _TFL                 import TFL

import _GTW._Werkzeug
import _TFL._Meta.Object
from    werkzeug            import exceptions
from    werkzeug            import Response
from    werkzeug.utils      import redirect

class M_Status (TFL.Meta.Object.__class__) :
    """Meta class for Status"""

    Table         = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.status_code is not None :
            cls.Table [cls.status_code] = cls
    # end def __init__

# end class M_Status

class Status (StandardError, TFL.Meta.Object) :
    """Base class for HTTP status exceptions"""

    __metaclass__ = M_Status

    status_code   = None

    def __init__ (self, description = "", * args) :
        self.description = description
        self.args        = args
    # end def __init__

# end class Status

class _Redirect_ (Status) :
    """Base class for all redirect's"""

    def __init__ (self, url, * args, ** kw) :
        self.url = url
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def __call__ (self, handler) :
        location = self.url
        handler.finish_request  ()
        handler.write \
            ( '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
              '<title>Redirecting...</title>\n'
              '<h1>Redirecting...</h1>\n'
              '<p>You should be redirected automatically to target URL: '
              '<a href="%s">%s</a>.  If not click the link.'
            % (location, location)
            )
        handler.set_header ("Content-Type", "text/html")
        handler.set_header ("Location",     location)
        handler.set_status (self.status_code)
        return handler.response
    # end def __call__

# end class _Redirect_

class Redirect_301 (_Redirect_) :
    """Moved Permanently."""
    status_code = 301
# end class Redirect_301

class Redirect_302 (_Redirect_) :
    """Found (moved temporarily)."""
    status_code = 302
# end class Redirect_302

class Redirect_303 (_Redirect_) :
    """See other."""
    status_code = 303
# end class Redirect_303

class Redirect_304 (_Redirect_) :
    """Not Modified."""
    status_code = 304
# end class Redirect_304

class Redirect_307 (_Redirect_) :
    """Temporary Redirect."""
    status_code = 307
# end class Redirect_307

class _Error_ (Status) :
    """Base class for all error responses."""

    def __call__ (self, handler) :
        text     = self.description
        nav_root = getattr (handler, "nav_root", None)
        if nav_root :
            handler.request.user = handler.current_user
            Templateer           = nav_root.Templateer
            template             = Templateer.get_std_template \
                (self.response.code)
            context              = Templateer.Context \
                ( exception      = self
                , page           = nav_root
                , nav_page       = nav_root
                , NAV            = nav_root
                , request        = handler.request
                )
            text = template.render (context)
        return self.response (text)
    # end def __call__

# end class _Error_

class Error_401 (_Error_) :
    """Unauthorized."""
    response = exceptions.Unauthorized
# end class Error_401

class Error_403 (_Error_) :
    """Forbidden."""
    response = exceptions.Forbidden
# end class Error_403

class Error_404 (_Error_) :
    """Not Found."""
    response    = exceptions.NotFound
# end class Error_404

class Error_405 (_Error_) :
    """Method Not Allowed."""
    response = exceptions.MethodNotAllowed
# end class Error_405

class Error_500 (_Error_) :
    """Internal Server Error."""
    response = exceptions.InternalServerError
# end class Error_500

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*", "_Redirect_")
### __END__ GTW.Werkzeug.Error

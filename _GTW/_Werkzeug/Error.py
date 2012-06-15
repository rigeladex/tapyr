# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
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
#    17-Aug-2010 (CT) `Error_503` added
#     2-Dec-2010 (CT) `_Exc_Mixin_` and `M_Error` added and used
#    31-Dec-2010 (CT) s/get_std_template/get_template/
#     5-Apr-2011 (CT) `Error_408` and `Error_409` added
#     2-May-2011 (CT) `Error_400` added
#    27-May-2011 (CT) `return_response` factored and redefined in `Error_405`
#     5-Apr-2012 (CT) Remove assignment to `handler.request.user`
#    10-May-2012 (CT) Add `__str__`
#    11-Jun-2012 (CT) Add `Error_410`, `_412`, `_415`, and `_501`
#    13-Jun-2012 (CT) Export `HTTP_Exception`
#    15-Jun-2012 (CT) Add `Error_406`
#    13-Jun-2012 (CT) Import `Response` from `werkzeug.wrappers`, not `werkzeug`
#    ««revision-date»»···
#--

from   _GTW                 import GTW
from   _TFL                 import TFL

import _GTW._Werkzeug
import _TFL._Meta.Object

from    werkzeug            import exceptions
from    werkzeug.wrappers   import Response
from    werkzeug.utils      import redirect

HTTP_Exception = exceptions.HTTPException

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

    def __str__ (self) :
        result = self.description
        if isinstance (result, unicode) :
            result = result.encode ("utf-8")
        elif not isinstance (result, str) :
            result = str (result)
        return result
    # end def __str__

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

### http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html

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

class _Exc_Mixin_ (exceptions.HTTPException) :
    "Mixin for werkzeug.exceptions classes"

    def get_body (self, environ) :
        "Returns `description` only because it contains a complete body"
        return self.description
    # end def get_body

# end class _Exc_Mixin_

class M_Error (M_Status) :
    """Meta class for Error classes"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.response is not None :
            ### Rewrite `response` to use the `description` as the whole body
            ### (it contains a complete `<html>` element)
            cls.response = type (cls.response) \
                ( cls.response.__name__
                , (_Exc_Mixin_, ) + cls.response.__bases__
                , dict (cls.response.__dict__)
                )
    # end def __init__

# end class M_Error

class _Error_ (Status) :
    """Base class for all error responses."""

    __metaclass__   = M_Error

    response        = None
    status_code     = property (lambda s : s.response.code)

    def __call__ (self, handler) :
        description = self.description
        nav_root    = getattr (handler, "nav_root", None)
        if not getattr (handler.request, "Error", None) :
            handler.request.Error = description
        if nav_root :
            Templateer            = nav_root.Templateer
            template              = Templateer.get_template (self.status_code)
            context               = Templateer.Context \
                ( exception       = self
                , fatal_exception = self if self.status_code >= 500 else None
                , page            = nav_root
                , nav_page        = nav_root
                , NAV             = nav_root
                , request         = handler.request
                )
            description = template.render (context)
        return self.return_response (description)
    # end def __call__

    def return_response (self, description) :
        ### Overriden by `Error_405`
        return self.response (description)
    # end def return_response

# end class _Error_

class Error_400 (_Error_) :
    """Bad Request."""
    response = exceptions.BadRequest
# end class Error_400

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

    response    = exceptions.MethodNotAllowed

    def __init__ (self, description = "", valid_methods = ()) :
        self.__super.__init__ (description)
        self.valid_methods = sorted (valid_methods)
    # end def __init__

    def return_response (self, description) :
        ### - werkzeug.exceptions.MethodNotAllowed has a different signature
        ###   than all other exception classes
        return self.response (self.valid_methods, description)
    # end def return_response

# end class Error_405

class Error_406 (_Error_) :
    """Not Acceptable."""
    response    = exceptions.NotAcceptable
# end class Error_406

class Error_408 (_Error_) :
    """Request Timeout."""
    response = exceptions.RequestTimeout
# end class Error_408

try :
    exceptions.Conflict
except AttributeError :
    class _Conflict_ (exceptions.HTTPException) :
        """*409* `Conflict`

           Raise to signalize a conflict.
        """

        code = 409
        description = \
            ( "<p>"
              "The request could not be completed due to a conflict with "
              "the current state of the resource. "
              "</p>"
            )

    exceptions.Conflict = _Conflict_ # end class

class Error_409 (_Error_) :
    """Conflict."""
    response = exceptions.Conflict
# end class Error_409

class Error_410 (_Error_) :
    """Gone."""
    response = exceptions.Gone
# end class Error_410

class Error_412 (_Error_) :
    """Precondition failed."""
    response = exceptions.PreconditionFailed
# end class Error_412

class Error_415 (_Error_) :
    """Unsupported media type."""
    response = exceptions.UnsupportedMediaType
# end class Error_415

class Error_500 (_Error_) :
    """Internal Server Error."""
    response = exceptions.InternalServerError
# end class Error_500

class Error_501 (_Error_) :
    """Not Implemented."""
    response = exceptions.NotImplemented
# end class Error_501

class Error_503 (_Error_) :
    """Service Unavailable."""
    response = exceptions.ServiceUnavailable
# end class Error_500

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*", "_Error_", "_Redirect_", "HTTP_Exception")
### __END__ GTW.Werkzeug.Error

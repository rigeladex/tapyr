# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Tornado.
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
#    GTW.Tornado.Error
#
# Purpose
#    Define special error exceptions
#
# Revision Dates
#    13-Jan-2010 (MG) Creation
#    14-Jan-2010 (CT) s/Templeteer/Templateer/g
#    ««revision-date»»···
#--

from   _GTW              import GTW
from   _TFL              import TFL

import _GTW._Tornado
import _TFL._Meta.Object

from    tornado.web      import HTTPError

class HTTP_Status (HTTPError, TFL.Meta.Object) :
    """Base class for HTTP status exceptions"""

    status_code = None

    def __init__ (self, * args, ** kw) :
        self.__super.__init__  (self.status_code, * args, ** kw)
    # end def __init__

# end class HTTP_Status

class _Redirect_ (HTTP_Status) :
    """Base class for all redirect's"""

    def __init__ (self, url, * args, ** kw) :
        self.url = url
        self.__super.__init__ (* args, ** kw)
    # end def __init__

    def __call__ (self, handler, nav_root = None) :
        handler.redirect (self.url, self.status_code == 301)
        return True ### exception handled
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

class Redirect_304 (_Redirect_) :
    """Not Modified."""
    status_code = 304
# end class Redirect_304

class _Error_ (HTTP_Status) :
    """Base class for all error responses."""

    template = "html/error.jnj"

    def __init__ (self, * args, ** kw) :
        self.template = kw.pop ("template", self.template)
        self.__super.__init__  (* args, ** kw)
    # end def __init__

    def __call__ (self, handler, nav_root = None) :
        if nav_root :
            template = nav_root.Templateer.get_template (self.template)
            context  = nav_root.Templateer.Context \
                ( exception = self
                , page      = nav_root
                , nav_page  = nav_root
                , NAV       = nav_root
                , request   = handler.request
                )
            if handler._headers_written :
                if not handler._finished :
                    handler.finish ()
                return
            handler.clear          ()
            handler.set_status     (self.status_code)
            handler.finish         (template.render (context))
            return True
        return False ### trigger the default error exception handling code
    # end def __call__

# end class _Error_

class Error_401 (_Error_) :
    """Unauthorized."""
    status_code = 401
# end class Error_401

class Error_403 (_Error_) :
    """Forbidden."""
    status_code = 403
# end class Error_403

class Error_404 (_Error_) :
    """Not Found."""
    status_code = 404
# end class Error_404

class Error_405 (_Error_) :
    """Method Not Allowed."""
    status_code = 405
# end class Error_405

class Error_500 (_Error_) :
    """Internal Server Error."""
    status_code = 500
# end class Error_500

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Error

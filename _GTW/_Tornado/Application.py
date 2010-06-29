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
#    GTW.Tornado.Application
#
# Purpose
#    Provide a base class for tornado applications
#
# Revision Dates
#    12-Sep-2009 (MG) Creation
#     1-Feb-2010 (MG) `__init__` added to support `media_path`
#    25-Jun-2010 (MG) Changed to generate a common interface between Werkzeug
#                     and Tornado
#    25-Jun-2010 (CT) Bug fix (s/kw/hkw/ in `handlers` loop in `__init__`)
#    28-Jun-2010 (MG) Pass the url prefix as parameter to the request handler
#    28-Jun-2010 (CT) `GTW._Application_` factored
#    29-Jun-2010 (CT) Import for all relevant modules of package added
#    ««revision-date»»···
#--

from   _TFL                import TFL
from   _GTW                import GTW

import _GTW._Application_
import _GTW.autoreload

import _GTW._Tornado.Error
import _GTW._Tornado.Request_Data
import _GTW._Tornado.Request_Handler
import _GTW._Tornado.Static_File_Handler
import _GTW._Tornado.Upload_Handler

from   tornado            import web
import tornado.httpserver
import tornado.ioloop

import _TFL.Logger

reload_logger = TFL.Logger.Create ("reload")

class _Tornado_Application_ (web.Application, GTW._Application_) :
    """Base class for Web Applications"""

    _real_name = "Application"

    def __init__ (self, * handlers, ** kw) :
        real_handlers, kw = self._init_handlers (handlers, kw)
        self.__super.__init__ (real_handlers, ** kw)
    # end def __init__

    def run_development_server (self, port = 8000, ** kw) :
        print "Start server on port %d" % (port, )
        http_server = tornado.httpserver.HTTPServer (self)
        http_server.listen                          (port)
        tornado.ioloop.IOLoop.instance ().start     ()
    # end def start_server

    def _handler_pattern (self, prefix) :
        return "(%s)/.*$" % (prefix, )
    # end def _handler_pattern

    def _init_static_handler (self, handler_spec) :
        return handler_spec
    # end def _init_static_handler

Application = _Tornado_Application_ # end class

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Application

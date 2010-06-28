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
#    ««revision-date»»···
#--

from   _TFL                import TFL
import _TFL._Meta.Object
from   _GTW                import GTW
import _GTW._Tornado.Error
import _GTW._Tornado.Static_File_Handler

from    tornado            import web
import  tornado.httpserver
import  tornado.ioloop

import  _GTW.autoreload
import  _TFL.Logger

reload_logger = TFL.Logger.Create ("reload")

class _Tornado_Application_ (web.Application, TFL.Meta.Object) :
    """Base class for Web Applications"""

    def __init__ (self, * handlers, ** kw) :
        media          = kw.pop ("media_path", None)
        static_handler = kw.pop ("static_handler", None)
        real_handlers  = []
        if static_handler :
            real_handlers.append (static_handler)
        for handler_spec in handlers :
            hkw = {}
            if len (handler_spec) > 2 :
                prefix, handler, hkw = handler_spec
            else :
                prefix, handler      = handler_spec
            real_handlers.append (("(%s)/.*$" % (prefix, ), handler, hkw))
        self.__super.__init__ (real_handlers, ** kw)
    # end def __init__

    _real_name = "Application"

    def run_development_server (self, port = 8000, ** kw) :
        print "Start server on port %d" % (port, )
        http_server = tornado.httpserver.HTTPServer (self)
        http_server.listen                          (port)
        tornado.ioloop.IOLoop.instance ().start     ()
    # end def start_server

Application = _Tornado_Application_ # end class _Tornado_Application_

as_json = dict

if __name__ != "__main__" :
    GTW.Tornado._Export ("*", "as_json")
else :
    import _GTW._Tornado.Request_Handler
    import  sys
    import  os

    app_dir   = os.path.dirname (sys.argv [0])
    media_dir = os.path.normpath \
        (os.path.join (app_dir, "..", "_NAV", "example", "media"))
    djo_dir   = os.path.normpath \
        (os.path.join (app_dir, "..", "..", "_DJO", "media"))
    class Handle_All (GTW.Tornado.Request_Handler) :

        def get (self) :
            self.write ("Hello World 2")
        # end def get

    # end class Handle_All

    auto_reload_start \
        (Application ( ((r"/", Handle_All), )
                     , static_handler = GTW.Tornado.Static_File_Handler
                         ( "media", media_dir
                         , GTW.Tornado.Static_Map ("GTW", djo_dir)
                         )
                     )
        )
### __END__ GTW.Tornado.Application

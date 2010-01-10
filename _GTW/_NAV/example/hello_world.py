# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glück. All rights reserved
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
#    GTW.NAV.example.hello_world
#
# Purpose
#    Simple hello world using the GTW.NAV and tornado frameworks
#
# Revision Dates
#    13-Sep-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                      import GTW
import _GTW._NAV.Request_Handler
import  os

import _GTW._NAV.Base
import _GTW._NAV.ReST
from    jinja2 import Environment, FileSystemLoader

ROOT_DIR      = os.path.dirname (__file__)
template_dirs = [os.path.join (ROOT_DIR, "templates")]
NAV           = GTW.NAV.Root \
    ( src_dir           = "."
    , copyright_start   = 2008
    , encoding          = "iso-8859-15"
    , input_encoding    = "iso-8859-15"
    , site_prefix       = "/"
    , site_url          = "http://localhost:8000"
    , template          = "static.html"
    , template_env      = Environment
          ( loader      = FileSystemLoader
              (template_dirs, encoding = "iso-8859-15")
          , trim_blocks = True
          )
    )
NAV.add_entries \
    ( ( dict ( name           = "index.html"
             , title          = u"Home"
             , Type           = GTW.NAV.Page_ReST_F
             )
      , dict ( name           = "test.html"
             , title          = u"Test"
             , Type           = GTW.NAV.Page_ReST_F
             )
      )
    , Dir_Type = GTW.NAV.Dir
    )

if __name__ == "__main__" :
    import _GTW._Tornado.Application

    #Tornado.auto_reload_start \
    #    ( GTW.Tornado.Application (( ((r".*", GTW.NAV.Request_Handler), ))))
    app = GTW.Tornado.Application \
        ( ((".*$", GTW.NAV.Request_Handler), )
        , debug = True
        )
    GTW.Tornado.start_server (app, 8080)
### __END__ GTW.NAV.example.hello_world

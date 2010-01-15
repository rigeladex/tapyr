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
#    14-Jan-2010 (MG) Use `TFL.CAO`
#    14-Jan-2010 (CT) `PNS_Aliases` added and `Account_P` creation enabled
#    ««revision-date»»···
#--

from   _TFL                      import TFL
from   _GTW                      import GTW
import _GTW._NAV.Request_Handler
import  os

import _GTW._NAV.Base
import _GTW._NAV.ReST
from   _JNJ.Templateer import Templateer
import _JNJ

from   _MOM            import MOM
import _GTW._OMP._Auth.Account

from   _MOM._EMS.Hash         import Manager as EMS
from   _MOM._DBW._HPS.Manager import Manager as DBW

from Redirect import Redirect, Error

### define the command lind and parse it to get the `port` from the command
### line needed for the `site_url`
import _TFL.CAO
import  sys
cmd = TFL.CAO.Cmd \
    ( opts = ( "port:I=8080?Server port"
             , "tornado_reload:B?Use the tornado reload feature"
             , "GTW_reload:B?Use the GTW reload feature"
             )
    ) (sys.argv [1:])

apt    = MOM.App_Type \
    (u"HWO", GTW, PNS_Aliases = dict (Auth = GTW.OMP.Auth)).Derived (EMS, DBW)
scope  = MOM.Scope.new (apt, None)

scope.Auth.Account_P ("user1", password = "passwd1")
scope.Auth.Account_P ("user2", password = "passwd2")

base_template_dir = os.path.dirname (_JNJ.__file__)
ROOT_DIR          = os.path.dirname (__file__)
template_dirs     = [os.path.join (ROOT_DIR, "templates"), base_template_dir]

NAV               = GTW.NAV.Root \
    ( src_dir           = "."
    , copyright_start   = 2008
    , encoding          = "iso-8859-15"
    , input_encoding    = "iso-8859-15"
    , site_prefix       = "/"
    , site_url          = "http://localhost:%d" % (cmd.port, )
    , template          = "static.jnj"
    , HTTP              = GTW.Tornado
    , Templateer        = Templateer
          ( load_path   = template_dirs
          , trim_blocks = True
          , encoding    = "iso-8859-15"
          , globals     = dict (site_base = "base.jnj")
          )
    )
NAV.add_entries \
    ( ( dict
          ( name           = "index.html"
          , title          = u"Home"
          , Type           = GTW.NAV.Page_ReST_F
          )
      , dict
          ( name           = "test.html"
          , title          = u"Test"
          , Type           = GTW.NAV.Page_ReST_F
          , login_required = True
          )
      , dict
          ( name           = "redirect_301.html"
          , title          = u"Redirect 301 (index)"
          , Type           = Redirect
          , redirect_to    = "index.html"
          , code           = 301
          )
      , dict
          ( name           = "redirect_302.html"
          , title          = u"Redirect 302 (test)"
          , Type           = Redirect
          , redirect_to    = "test.html"
          , code           = 302
          )
      )
    , Dir_Type = GTW.NAV.Dir
    )
NAV.add_entries \
    ( ( dict
          ( name           = "error_%s.html" % c
          , title          = u"Display a HTTP error %s" % c
          , Type           = Error
          , code           = c
          )
        for c in (401, 403, 404, 500)
      )
    , Dir_Type = GTW.NAV.Dir
    )
if __name__ == "__main__" :
    import _GTW._Tornado.Application
    print "Start server on port %d" % (cmd.port, )
    if cmd.GTW_reload :
        print "Use GTW autorelaod feature"
        GTW.Tornado.auto_reload_start \
            ( GTW.Tornado.Application (( ((r".*", GTW.NAV.Request_Handler), )))
            , port = cmd.port
            )
    else :
        if cmd.tornado_reload :
            print "Use Tornado buildin autorelaod feature"
        app = GTW.Tornado.Application \
            ( ((".*$", GTW.NAV.Request_Handler), )
            , cookie_secret = "sdf756!764/785'H7858&)=8766/&%$rw2?g56476W§+@"
            , debug = cmd.tornado_reload
            )
        GTW.Tornado.start_server (app, cmd.port)
### __END__ GTW.NAV.example.hello_world

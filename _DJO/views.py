# -*- coding: utf-8 -*-
# Copyright (C) 2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    DJO.views
#
# Purpose
#    Provide some standard views
#
# Revision Dates
#    15-Oct-2008 (CT) Creation
#    15-Oct-2008 (CT) `next_page` added to `logout`
#    17-Oct-2008 (CT) `_special_handler` refactored
#    17-Oct-2008 (CT) `handler_403` added
#    ««revision-date»»···
#--

from   _DJO                      import DJO
import _DJO._NAV.Base

from   django.template           import RequestContext, loader
from   django                    import http

def _special_handler (request, template_name, Response_Type = None, ** kw) :
    if Response_Type is None :
        Response_Type = http.HttpResponseNotFound
    t = loader.get_template (template_name)
    kw.setdefault ("page", DJO.NAV.Root.top)
    return Response_Type (t.render (RequestContext (request, kw)))
# end def _special_handler

def handler_403 (request, template_name = "403.html", ** kw) :
    return _special_handler \
        ( request, template_name
        , Response_Type = http.HttpResponseForbidden
        , ** kw
        )
# end def handler_403

def handler_404 (request, template_name = "404.html", ** kw) :
    return _special_handler (request, template_name, ** kw)
# end def handler_404

def handler_500 (request, template_name = "500.html", ** kw) :
    return _special_handler (request, template_name, ** kw)
# end def handler_500

def handle_500_debug (request, template_name = "500.html", ** kw) :
    import sys
    from   django.views import debug
    return debug.technical_500_response (request, * sys.exc_info ())
# end handle_500_debug

def login (request, ** kw) :
    from django.contrib.auth import views
    ### import pdb; pdb.set_trace ()
    return views.login (request, ** kw)
# end def login

def logout (request, ** kw) :
    from django.contrib.auth import views
    ### import pdb; pdb.set_trace ()
    request.user_logged_out = request.user
    return views.logout \
        (request, next_page = request.POST.get ("next"), ** kw)
# end def logout

if __name__ != "__main__":
    DJO._Export_Module ()
### __END__ DJO.views

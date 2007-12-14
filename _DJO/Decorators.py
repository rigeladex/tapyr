# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005-2007 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. office@spannberg.com
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
#    DJO.Decorators
#
# Purpose
#    Some helper functions for the url-handling
#
# Revision Dates
#    06-May-2007 (MG) Creation
#    19-May-2007 (MG) `view_url`: `url_variable` added
#    19-May-2007 (MG) `render_template` decorator added
#    18-Nov-2007 (MG) `render_template`: don't add `kw` to the result context
#                     but only the `context` key
#    14-Dec-2007 (CT) Moved into package DJO
#    ««revision-date»»···
#--

from   _DJO                      import DJO

from   django.conf               import settings
import django.conf.urls.defaults as     URL_defaults
from   django.http               import HttpResponseRedirect
from   django.shortcuts          import render_to_response
from   django.template           import RequestContext

def view_url (urls, url_name = None, prefix = "", url_variable = None, ** kw) :
    ### decorator which adds the decorated function to the url-patterns
    #### usage:
    #### @view_url ("^/foo/(.*)/$")
    #### @def _view_which_handles_this url (request, parameter_1) :
    ###     xxxx
    if url_variable is None :
        try :
            url_variable = settings.URLPATTERNS
        except AttributeError :
            url_variable = settings.URLPATTERNS = __import__ \
                (settings.ROOT_URLCONF, {}, {}, ['']).urlpatterns
    if not isinstance (urls, (list, tuple)) :
        urls = (urls, )
    def _decorator (f, url_variable = url_variable) :
        _urls = [ URL_defaults.url (u, f, kw, name = url_name or f.__name__)
                    for u in urls
                ]
        url_variable += URL_defaults.patterns (prefix, * _urls)
        return f
    # end def _decorator
    return _decorator
# end def view_url

def render_template (template, ** kw) :
    ### use this decorator as a short cut to `render_to_response`. If the
    ### decorated function returns a dict, the response is generated using
    ### the template specified (and the additional `kw` supplied will be
    ### added).
    ### If the decorated function returns a sring, a `HttpResponseRedirect`
    ### will be created with the result as the new URL.
    ###
    ### Important:
    ####  Make sure that this decorator is used BEFORE the view_url one so
    ####  that the wrapped function is passed to the view_url decorator
    def _decorator (fct) :
        def _fct_wrapper (request, * args, ** kw) :
            result = fct (request, * args, ** kw)
            if isinstance (result, dict) :
                result.update (kw.get ("context", {}))
                return render_to_response \
                    ( template, result
                    , context_instance = RequestContext (request)
                    )
            elif isinstance (result, basestring) :
                return HttpResponseRedirect (result)
            return result
        # end def _fct_wrapper
        _fct_wrapper.func_name = fct.func_name
        _fct_wrapper.__doc__   = fct.__doc__
        return _fct_wrapper
    # end def _decorator
    return _decorator
# end def render_template

if __name__ != "__main__" :
    DJO._Export ("*")
### __END__ DJO.Decorators

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    GTW.Werkzeug.Application
#
# Purpose
#    Basic application using the werkzeug WSGI utilities.
#
# Revision Dates
#    20-Mar-2010 (MG) Creation
#    24-Mar-2010 (CT) `__call__` changed to catch `GTW.Werkzeug.Status`
#                     instead of `Exception`
#    29-Apr-2010 (MG) Set `charset` of werkzeug reguest und response handlers
#     6-Mai-2010 (MG) Support for profiling added
#     6-May-2010 (MG) `url_charset` seperated from `charset` because `GET`
#                     parameters are by default `utf-8` encoded
#    25-Jun-2010 (MG) Changed to generate a common interface between Werkzeug
#                     and Tornado
#    ««revision-date»»···
#--
from   _TFL               import TFL
import _TFL._Meta.Object

from   _GTW               import GTW
import _GTW.File_Session
import _GTW._Werkzeug.Error
import _GTW._Werkzeug.Request_Handler

from    werkzeug          import ClosingIterator
from    werkzeug.wrappers import BaseRequest, BaseResponse
import  warnings
import  re

class Application (TFL.Meta.Object) :
    """A WSGI Application"""

    default_settings = dict \
        ( session_id    = "SESSION_ID"
        , cookie_secret = "salt" ### must be changed for every application
        , Session_Class = GTW.File_Session
        )

    def __init__ (self, * handlers, ** kw) :
        if "cookie_secret" not in kw :
            warnings.warn ("Using default `cookie_secret`!", UserWarning)
        static_handler          = kw.pop ("static_handler", None)
        encoding                = kw.pop ("encoding", "utf-8")
        BaseRequest.charset     = BaseResponse.charset = encoding
        BaseRequest.url_charset = "utf-8"
        self.settings           = dict (self.default_settings, ** kw)
        self.handlers           = []
        if static_handler :
            handlers = list (handlers)
            handlers.insert (0, static_handler)
        for handler_spec in handlers :
            args = ()
            if len (handler_spec) > 2 :
                prefix, handler, kw = handler_spec
            else :
                prefix, handler     = handler_spec
            self.handlers.append \
                ((re.compile ("(%s)(/.*)$" % (prefix, )), handler, kw))
        self._server_opts = kw
    # end def __init__

    def __call__ (self, environ, start_response) :
        path = environ ["PATH_INFO"]
        for pat, handler_cls, kw in self.handlers :
            match = pat.match (path)
            if match :
                sn, pi = match.groups ()
                environ ["PATH_INFO"]   = pi
                environ ["SCRIPT_NAME"] = sn
                handler = handler_cls (self, environ, ** kw)
                try :
                    return handler (environ, start_response)
                except GTW.Werkzeug.Status, exc :
                    response = handler._handle_request_exception (exc)
                    if response :
                        return response (environ, start_response)
                    raise
    # end def __call__

    def run_development_server ( self
                               , port                 = 8080
                               , host                 = "localhost"
                               , use_profiler         = False
                               , profile_log_files    = ()
                               , profile_sort_by      = ('time', 'calls')
                               , profile_restrictions = ()
                               , profile_delete_logs  = False
                               ) :
        from werkzeug import run_simple
        app = self
        use_debugger = self._server_opts.get ("debug",       False)
        use_reloader = self._server_opts.get ("auto_reload", False)
        if use_profiler :
            from werkzeug.contrib.profiler import \
                ProfilerMiddleware, MergeStream
            import os, sys
            stream       = None
            file_handles = []
            for fn in profile_log_files :
                if hasattr (fn, "write") :
                    file_handles.append (fn)
                elif fn == "stderr" :
                    file_handles.append (sys.stderr)
                else :
                    if profile_delete_logs and os.path.isfile (fn) :
                        os.unlink (fn)
                    file_handles.append (open (fn, "w"))
            if file_handles :
                stream = MergeStream (* file_handles)
            app    = ProfilerMiddleware \
                (app, stream, profile_sort_by, profile_restrictions)
            use_reloader = use_debugger = False
        run_simple \
            ( host, port, app
            , use_reloader = use_reloader
            , use_debugger = use_debugger
            )
    # end def run_development_server

# end class Application

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
else :
    import _GTW.Static_File_Map
    import _GTW._Werkzeug.Static_File_Handler
    import  os
    media_dir = os.path.join (os.path.dirname (__file__), "media")
    app = Application \
        ( ("/media", GTW.Werkzeug.Static_File_Handler, (media_dir, ))
        , ("",       GTW.Werkzeug.Request_Handler)
        , cookie_secret = "SALT"
        )
    app.run_development_server (use_debugger = True, use_reloader = True)
### __END__ GTW.Werkzeug.Application

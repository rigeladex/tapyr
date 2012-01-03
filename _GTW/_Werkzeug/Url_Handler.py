# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.Werkzeug.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.Werkzeug.Url_Handler
#
# Purpose
#    Encapsulate a handler for matching URLs
#
# Revision Dates
#     3-Jan-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _TFL._Meta.Object

class Url_Handler (TFL.Meta.Object) :
    """Encapsulate a handler for matching URLs."""

    def __init__ (self, app, pat, type, kw) :
        self.app  = app
        self.pat  = pat
        self.type = type
        self.kw   = kw
    # end def __init__

    def __call__ (self, environ, start_response, match) :
        sn, pi = match.groups ()
        environ ["PATH_INFO"]   = pi
        environ ["SCRIPT_NAME"] = sn
        handler = self.type (self.app, environ, ** self.kw)
        try :
            return handler (environ, start_response)
        except GTW.Werkzeug.Status, exc :
            response = handler._handle_request_exception (exc)
            if response :
                return response (environ, start_response)
            raise
    # end def __call__

    def match (self, path) :
        return self.pat.match (path)
    # end def match

    def matching_path (self, path) :
        match = self.pat.match (path)
        if match :
            return match.groups () [-1]
    # end def matching_path

    def __repr__ (self) :
        return repr ((self.pat, self.handler, self.kw))
    # end def __repr__

# end class Url_Handler

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Url_Handler

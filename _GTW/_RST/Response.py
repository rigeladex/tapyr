# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
#    GTW.RST.Response
#
# Purpose
#    Wrap and extend wsgi-specific Response class
#
# Revision Dates
#    20-Jun-2012 (CT) Creation
#     2-Mar-2013 (CT) Add `add_link`, change `__call__` to add link headers
#    28-Mar-2013 (CT) Add `_auto_headers` with `X-Frame-Options`
#     2-May-2013 (CT) Factor in `clear_cookie`, `set_cookie`, and
#                     `set_secure_cookie` (from GTW.RST.TOP.Response)
#     4-May-2013 (CT) Add `cookies_to_delete`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST

from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.M_Auto_Combine_Sets
import _TFL._Meta.M_Class
import _TFL._Meta.Object

class _M_Response_ (TFL.Meta.M_Auto_Combine_Sets, TFL.Meta.M_Class) :
    """Meta class for Response"""

# end class _M_Response_

class _RST_Response_ (TFL.Meta.Object) :
    """Wrap and extend wsgi-specific Response class."""

    __metaclass__     = _M_Response_

    _auto_headers     = \
        { "X-Frame-Options" : "SAMEORIGIN"
        }

    _own_vars         = \
        ("root", "_auto_headers", "_links", "_request", "_response")

    _sets_to_combine  = ("_own_vars", )

    def __init__ (self, _root, _request, * args, ** kw) :
        self.root          = _root
        self._auto_headers = dict (self._auto_headers) # allow instance changes
        self._links        = {}
        self._request      = _request
        self._response     = _root.HTTP.Response (* args, ** kw)
    # end def __init__

    def __call__ (self, * args, ** kw) :
        _response = self._response
        for c in self._request.cookies_to_delete :
            self.clear_cookie (c)
        for k, v in self._auto_headers.iteritems () :
            _response.add_header (k, v)
        for rel, (value, kw) in self._links.iteritems () :
            _response.add_header ("link", value, rel = rel, ** kw)
        return _response.__call__ (* args, ** kw)
    # end def __call__

    @property
    def resource (self) :
        return self._request.resource
    # end def resource

    def add_link (self, rel, value, ** kw) :
        self._links [rel] = value, kw
    # end def add_link

    def clear_cookie (self, name, * args, ** kw) :
        self._response.delete_cookie (name, * args, ** kw)
    # end def clear_cookie

    def set_cookie (self, key, value = "", ** kw) :
        if isinstance (value, unicode) :
            value = value.encode (self._request.cookie_encoding)
        return self._response.set_cookie (key, value, ** kw)
    # end def set_cookie

    def set_secure_cookie (self, name, data, secrets = None, ** kw) :
        cookie = self._request.new_secure_cookie (name, data, secrets)
        self.set_cookie (name, cookie, ** kw)
        return cookie
    # end def set_secure_cookie

    def __getattr__ (self, name) :
        if name not in self._own_vars :
            return getattr (self._response, name)
        raise AttributeError (name)
    # end def __getattr__

    def __setattr__ (self, name, value) :
        if name in self._own_vars :
            return self.__super.__setattr__ (name, value)
        else :
            return setattr  (self._response, name, value)
    # end def __setattr__

Response = _RST_Response_ # end class

if __name__ != "__main__" :
    GTW.RST._Export ("Response")
### __END__ GTW.RST.Response

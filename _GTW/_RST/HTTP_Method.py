# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
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
#    GTW.RST.HTTP_Method
#
# Purpose
#    Base classes for HTTP methods
#
# Revision Dates
#     8-Jun-2012 (CT) Creation
#    12-Jun-2012 (CT) Continue creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST

import _TFL._Meta.M_Class
import _TFL._Meta.Object
import _TFL.RFC2822_date

class _Meta_ (TFL.Meta.M_Class) :

    Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        name = cls.__name__
        if name != "HTTP_Method" and not name.startswith ("_") :
            cls.name = name
            if name not in cls.Table :
                cls.Table [name] = cls
    # end def __init__

# end class _Meta_

class HTTP_Method (TFL.Meta.Object) :
    """Base class for HTTP methods."""

    __metaclass__              = _Meta_

    def __call__ (self, resource, handler) :
        result = ""
        if self._do_change_info (resource, handler) :
            result = self._response (resource, handler)
            if result :
                ### XXX support other representations
                result = handler.write_json (result)
        return result
    # end def __call__

    def _do_change_info (self, resource, handler) :
        result = True
        ci     = resource.change_info
        if ci is not None :
            etag = getattr (ci, "etag", None)
            last = getattr (ci, "last_modified", None)
            if last :
                result = self._check_modified (resource, handler, last)
            if etag :
                result = self._check_etag     (resource, handler, etag)
        return result
    # end def _do_change_info

    def _response (self, resource, handler) :
        raise NotImplementedError \
            ( "%s.%s._response needs to be implemented"
            % (resource.__class__.__name__, self.__class__.__name__)
            )
    # end def _response

    def _get_date_header (self, handler, name) :
        header = handler.request.headers.get (name)
        if header is not None :
            try :
                return TFL.RFC2822.from_string (header)
            except ValueError :
                pass
    # end def _get_date_header

# end class HTTP_Method

class _HTTP_Method_R_ (HTTP_Method) :
    """Base class for HTTP methods that don't change the resource.."""

    mode                       = "r"

    def _check_etag (self, resource, handler, etag) :
        result  = True
        headers = handler.request.headers
        value   = str (etag)
        n_match = headers.get ("If-None-Match")
        if n_match is not None :
            result = etag != n_match
        handler.set_header ("ETag", value)
        return result
    # end def _check_etag

    def _check_modified (self, resource, handler, last_modified) :
        result  = True
        value   = TFL.RFC2822.as_string (last_modified)
        ims     = self._get_date_header (handler, "If-Modified-Since")
        if ims is not None :
            result = last_modified > ims
        handler.set_header ("Last-Modified", value)
        return result
    # end def _check_modified

    def _do_change_info (self, resource, handler) :
        result = self.__super._do_change_info (resource, handler)
        if not result :
            handler.set_status (304)
        return result
    # end def _do_change_info

# end class _HTTP_Method_R_

class _HTTP_Method_W_ (HTTP_Method) :
    """Base class for HTTP methods that change the resource."""

    mode                       = "w"

    def _check_etag (self, resource, handler, etag) :
        result  = True
        headers = handler.request.headers
        value   = str (etag)
        match   = headers.get ("If-Match")
        if match is not None :
            result = etag == match
        handler.set_header ("ETag", value)
        return result
    # end def _check_etag

    def _check_modified (self, resource, handler, last_modified) :
        result  = True
        value   = TFL.RFC2822.as_string (last_modified)
        ums     = self._get_date_header (handler, "If-Unmodified-Since")
        if ums is not None :
            result = last_modified == ums
        handler.set_header ("Last-Modified", value)
        return result
    # end def _check_modified

    def _do_change_info (self, resource, handler) :
        result = self.__super._do_change_info (resource, handler)
        if not result :
            handler.set_status (412)
        return result
    # end def _do_change_info

# end class _HTTP_Method_W_

class _HTTP_DELETE_ (_HTTP_Method_W_) :
    """Implement HTTP method DELETE."""

    _real_name                 = "DELETE"

DELETE = _HTTP_DELETE_ # end class

class _HTTP_HEAD_ (_HTTP_Method_R_) :
    """Implement HTTP method HEAD."""

    _real_name                 = "HEAD"

    def _response (self, resource, handler) :
        return ""
    # end def _response

HEAD = _HTTP_HEAD_ # end class

class _HTTP_GET_ (_HTTP_Method_R_) :
    """Implement HTTP method GET."""

    _real_name                 = "GET"

GET = _HTTP_GET_ # end class

class _HTTP_OPTIONS_ (_HTTP_Method_R_) :
    """Implement HTTP method OPTIONS."""

    _real_name                 = "OPTIONS"

    def __call__ (self, resource, handler) :
        methods = sorted \
            (  k for k, m in resource.SUPPORTED_METHODS.iteritems ()
            if resource.allow_method (m, handler.request)
            )
        handler.set_header ("Allow", ", ".join (methods))
        return ""
    # end def __call__

OPTIONS = _HTTP_OPTIONS_ # end class

class _HTTP_POST_ (_HTTP_Method_W_) :
    """Implement HTTP method POST."""

    _real_name                 = "POST"

POST = _HTTP_POST_ # end class

class _HTTP_PUT_ (_HTTP_Method_W_) :
    """Implement HTTP method PUT."""

    _real_name                 = "PUT"

PUT = _HTTP_PUT_ # end class

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.HTTP_Method

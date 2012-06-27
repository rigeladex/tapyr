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
#    27-Jun-2012 (CT) Fix `_check_etag` and `_check_modified`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Mime_Type

import _TFL._Meta.M_Class
import _TFL._Meta.Object
import _TFL.RFC2822_date

class _Meta_ (TFL.Meta.M_Class) :

    render_man = None
    Table      = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        name = cls.__name__
        if name != "HTTP_Method" and not name.startswith ("_") :
            cls.name = name
            if name not in cls.Table :
                cls.Table [name] = cls
        renderers = dct.get ("_renderers")
        if renderers :
            cls.render_man = GTW.RST.Mime_Type.Render_Man (renderers)
    # end def __init__

# end class _Meta_

class HTTP_Method (TFL.Meta.Object) :
    """Base class for HTTP methods."""

    __metaclass__              = _Meta_

    needs_body                 = True

    _renderers                 = (GTW.RST.Mime_Type.JSON, )

    def __call__ (self, resource, request) :
        response = resource.Response (request)
        if self._do_change_info (resource, request, response) :
            body = self._response_body (resource, request, response)
            if body is not None :
                render = self._get_renderer (resource, request, response)
                if render is not None :
                    render (request, response, body)
        return response
    # end def __call__

    def _do_change_info (self, resource, request, response) :
        result = True
        ci     = resource.change_info
        if ci is not None :
            etag = getattr (ci, "etag", None)
            last = getattr (ci, "last_modified", None)
            if last :
                result = self._check_modified \
                    (resource, request, response, last)
            if etag :
                result = result and self._check_etag \
                    (resource, request, response, etag)
        return result
    # end def _do_change_info

    def _get_renderer (self, resource, request, response) :
        result = self.render_man (self, resource, request)
        if result is None and self.needs_body :
            response.status_code = 406
            ### XXX send back list of available representations
        return result
    # end def _get_renderer

    def _response_body (self, resource, request, response) :
        raise NotImplementedError \
            ( "%s.%s._response_body needs to be implemented"
            % (resource.__class__.__name__, self.__class__.__name__)
            )
    # end def _response_body

# end class HTTP_Method

class _HTTP_Method_R_ (HTTP_Method) :
    """Base class for HTTP methods that don't change the resource.."""

    mode                       = "r"

    def _check_etag (self, resource, request, response, etag) :
        n_match = request.if_none_match
        result  = n_match is None or not n_match.contains (etag)
        response.set_etag (etag)
        return result
    # end def _check_etag

    def _check_modified (self, resource, request, response, last_modified) :
        ims    = request.if_modified_since
        result = ims is None or last_modified > ims
        response.last_modified = last_modified
        return result
    # end def _check_modified

    def _do_change_info (self, resource, request, response) :
        result = self.__super._do_change_info (resource, request, response)
        if not result :
            response.status_code = 304
        return result
    # end def _do_change_info

# end class _HTTP_Method_R_

class _HTTP_Method_W_ (HTTP_Method) :
    """Base class for HTTP methods that change the resource."""

    mode                       = "w"

    def _check_etag (self, resource, request, response, etag) :
        match  = request.if_match
        result = match is not None and match.contains (etag)
        response.set_etag (etag)
        return result
    # end def _check_etag

    def _check_modified (self, resource, request, response, last_modified) :
        ums    = request.if_unmodified_since
        result = ums is not None and last_modified == ums
        response.last_modified = last_modified
        return result
    # end def _check_modified

    def _do_change_info (self, resource, request, response) :
        result = self.__super._do_change_info (resource, request, response)
        if not result :
            response.status_code = 412
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
    needs_body                 = False

    def _response_body (self, resource, request, response) :
        return None
    # end def _response_body

HEAD = _HTTP_HEAD_ # end class

class _HTTP_GET_ (_HTTP_Method_R_) :
    """Implement HTTP method GET."""

    _real_name                 = "GET"

GET = _HTTP_GET_ # end class

class _HTTP_OPTIONS_ (_HTTP_Method_R_) :
    """Implement HTTP method OPTIONS."""

    _real_name                 = "OPTIONS"

    needs_body                 = False

    def __call__ (self, resource, request) :
        response = resource.Response (request)
        methods = sorted \
            (  k for k, m in resource.SUPPORTED_METHODS.iteritems ()
            if resource.allow_method (m, request)
            )
        response.headers ["Allow"] = ", ".join (methods)
        return response
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

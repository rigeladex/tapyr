# -*- coding: utf-8 -*-
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
#    GTW.RST.HTTP_Method
#
# Purpose
#    Base classes for HTTP methods
#
# Revision Dates
#     8-Jun-2012 (CT) Creation
#    27-Jun-2012 (CT) Fix `_HTTP_Method_R_._check_etag` and `._check_modified`
#    29-Jun-2012 (CT) Fix `_HTTP_Method_W_._check_etag` and `._check_modified`
#    29-Jun-2012 (CT) Add response header `X-last-cid`
#    13-Jul-2012 (CT) Add `_do_change_info_skip`
#    20-Jul-2012 (CT) Add `try/except` around `render` to `send_error_email`
#    23-Jul-2012 (CT) Add argument `response` to `__call__`
#    23-Jul-2012 (CT) Put `renderer` into `request`
#    31-Jul-2012 (CT) Fix `join` call in `HTTP_Method.__call__`
#     2-Aug-2012 (CT) Change `HTTP_Method.__call__` to use `response.renderer`
#     6-Aug-2012 (CT) Add `cache_control` to `_do_change_info`
#     6-Aug-2012 (CT) Change `_do_change_info` to use `resource.get_etag` and
#                     `.get_last_modified`, not `.change_info`
#     6-Aug-2012 (CT) Use `resource.skip_etag`, remove `_do_change_info_skip`
#    15-Aug-2012 (MG) Use bytes string for `X-last-cid` header
#    18-Aug-2012 (CT) Fix `_do_change_info`: apply `or` to `last`, `etag`
#    10-Sep-2012 (CT) Replace `_do_change_info` by `_skip_render`
#     2-Mar-2013 (CT) Use `response.set_header`, not `.headers [] = `
#    31-May-2013 (CT) Fix `_Meta_.__init__`: use
#                     `not name.startswith ("HTTP_Method")`, not `name !=...`
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
        if not name.startswith (("HTTP_Method", "_")) :
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

    def __call__ (self, resource, request, response) :
        if not self._skip_render (resource, request, response) :
            response.renderer = self._get_renderer (resource, request, response)
            body = self._response_body (resource, request, response)
            if body is not None and response.renderer is not None :
                try :
                    response.renderer (request, response, body)
                except Exception as exc :
                    from _TFL.Formatter import formatted
                    import traceback
                    tb = traceback.format_exc ()
                    resource.send_error_email \
                        ( request, exc
                        , "\n\n".join ((formatted (body), tb))
                        )
                    raise
        return response
    # end def __call__

    def _get_renderer (self, resource, request, response) :
        result = self.render_man (self, resource, request)
        if result is None and self.needs_body :
            self.render_man.render_acceptable \
                (self, resource, request, response)
        return result
    # end def _get_renderer

    def _response_body (self, resource, request, response) :
        raise NotImplementedError \
            ( "%s.%s._response_body needs to be implemented"
            % (resource.__class__.__name__, self.__class__.__name__)
            )
    # end def _response_body

    def _skip_render (self, resource, request, response) :
        result = False
        if not resource.skip_etag :
            etag   = resource.get_etag           (request)
            last   = resource.get_last_modified  (request)
            r_etag = self._request_etag_attr     (request)
            r_last = self._request_modified_attr (request)
            if last :
                response.last_modified = last
            if etag :
                response.set_etag (etag)
            if last or etag :
                response.cache_control.no_cache = True
            matches = []
            if last and r_last :
                matches.append (not self._check_modified (last, r_last))
            if etag and r_etag :
                matches.append (r_etag.contains (etag))
            if matches :
                result = all (matches)
        return result
    # end def _skip_render

# end class HTTP_Method

class _HTTP_Method_R_ (HTTP_Method) :
    """Base class for HTTP methods that don't change the resource.."""

    mode                       = "r"

    def _check_modified (self, last_modified, ims) :
        return last_modified > ims
    # end def _check_modified

    def _request_etag_attr (self, request) :
        return request.if_none_match
    # end def _request_etag_attr

    def _request_modified_attr (self, request) :
        return request.if_modified_since
    # end def _request_modified_attr

    def _skip_render (self, resource, request, response) :
        result = self.__super._skip_render (resource, request, response)
        ci     = resource.change_info
        if ci is not None :
            cid  = getattr (ci, "cid", None)
            if cid is not None :
                response.set_header ("X-last-cid", cid)
        if result :
            response.status_code = 304
        return result
    # end def _skip_render

# end class _HTTP_Method_R_

class _HTTP_Method_W_ (HTTP_Method) :
    """Base class for HTTP methods that change the resource."""

    mode                       = "w"

    def _check_modified (self, last_modified, ums) :
        return last_modified != ums
    # end def _check_modified

    def _request_etag_attr (self, request) :
        return request.if_match
    # end def _request_etag_attr

    def _request_modified_attr (self, request) :
        return request.if_unmodified_since
    # end def _request_modified_attr

    def _skip_render (self, resource, request, response) :
        result = self.__super._skip_render (resource, request, response)
        if result :
            response.status_code = 412
        return result
    # end def _skip_render

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

    def __call__ (self, resource, request, response) :
        methods  = sorted \
            (  k for k, m in resource.SUPPORTED_METHODS.iteritems ()
            if resource.allow_method (m, request.user)
            )
        response.set_header ("Allow", ", ".join (methods))
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

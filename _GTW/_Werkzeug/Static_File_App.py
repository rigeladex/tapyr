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
#    GTW.Werkzeug.Static_File_App
#
# Purpose
#    WSGI application serving static files
#
# Revision Dates
#    21-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW.Static_File_Map

import _GTW._Werkzeug
import _GTW._Werkzeug.Request
import _GTW._Werkzeug.Response

import _TFL._Meta.Object
import _TFL.Record

from   werkzeug            import exceptions
from   werkzeug.wsgi       import wrap_file
from   werkzeug.http       import is_resource_modified

import datetime
import mimetype
import os
import zlib

class Static_File_App (TFL.Meta.Object) :
    """WSGI application serving static files."""

    def __init__ \
            ( self, * prefix_maps
            , fallback_mimetype = "text/plain"
            , top_prefix        = ""
            , wrap              = exceptions.NotFound
            ) :
        self.prefix_maps = prefix_maps
        self.mimetype    = fallback_mimetype
        self.top_prefix  = top_prefix
        self.wrap        = wrap
    # end def __init__

    def __call__ (self, environ, start_response) :
        request   = GTW.Werkzeug.Request (environ)
        file_name = self.get_path (request.path)
        if file_name :
            result = self._file_response (environ, request, file_name)
        else :
            result = self.wrap
        return result (environ, start_response)
    # end def __call__

    def get_path (self, req_path) :
        req_path = req_path.lstrip ("/")
        for map in self.maps :
            file_name = map.get (req_path)
            if file_name :
                return file_name
    # end def get_path

    def _file_info (self, file_name) :
        stat_result = os.stat (file_name)
        mtime       = stat_result [stat.ST_MTIME]
        size        = stat_result [stat.ST_SIZE]
        fn_hash     = zlib.adler32 (file_name) & 0xffffffff
        return TFL.Record \
            ( etag  = "sf-%s-%s-%s" % (mtime, size, fn_hash)
            , mtime = datetime.fromtimestamp (mtime)
            , size  = size
            )
    # end def _file_info

    def _file_response (self, environ, request, file_name) :
        info         = self._file_info (file_name)
        has_changed  = is_resource_modified \
            (environ, info.etag, last_modified = info.mtime)
        if has_changed :
            mime_type, encoding = mimetypes.guess_type (file_name)
            response = GTW.Werkzeug.Response \
                ( wrap_file (environ, open (file_name, "rb"))
                , mimetype           = mimetype or self.mimetype
                , direct_passthrough = True
                )
            response.content_length  = info.size
            response.etag            = info.etag
            response.last_modified   = info.mtime
            if encoding :
                response.charset     = encoding
        else :
            response = GTW.Werkzeug.Response (status = 304)
        return response
    # end def _file_response

# end class Static_File_App

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Static_File_App

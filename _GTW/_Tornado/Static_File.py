# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.Tornado.
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
#    GTW.Tornado.Static_File
#
# Purpose
#    Handling of static files
#
# Revision Dates
#    20-Feb-2010 (MG) Creation (based on tornado.web.StaticFileHandler)
#    22-Feb-2010 (MG) `get` moved into `Static_File_Handler`, `get` of
#                     `Static_Map` simplified and renamed to `exists`
#    22-Feb-2010 (MG) `Static_Map` moved into `GTW.Static_File_Map`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
import _GTW._Tornado
import _GTW.Static_File_Map

from   _TFL                     import TFL
import _TFL._Meta.Object

import  os
import  stat
import  time
import  datetime
import  email
import  mimetypes
from    tornado                 import web

class _Static_File_Handler_ (web.RequestHandler) :
    """A static file handler which shpuld only be used during development to
       server static files directly form the disk.
    """

    def __init__ (self, application, request, maps) :
        super (_Static_File_Handler_, self).__init__ (application, request)
        self.maps = maps
    # end def __init__

    def head (self, path) :
        self.get (path, include_body = False)
    # end def head

    def get (self, path, include_body = True) :
        for map in self.maps :
            file_name = map.get (self, path, include_body)
            if file_name :
                return self._get (file_name, include_body)
    # end def get

    def _get (self, file_name, include_body = True) :
        # Check the If-Modified-Since, and don't send the result if the
        # content has not been modified
        stat_result = os.stat (file_name)
        modified    = datetime.datetime.fromtimestamp \
            (stat_result [stat.ST_MTIME])
        file_size   = stat_result [stat.ST_SIZE]
        ims_value   = request.headers.get ("If-Modified-Since")
        if ims_value is not None :
            date_tuple = email.utils.parsedate (ims_value)
            if_since   = datetime.datetime.fromtimestamp \
                (time.mktime (date_tuple))
            if if_since >= modified :
                handler.set_status (304)
                return

        handler.set_header ("Last-Modified",  modified)
        handler.set_header ("Content-Length", file_size)
        if "v" in request.arguments :
            handler.set_header \
                ( "Expires"
                , datetime.datetime.utcnow ()
                + datetime.timedelta       (days=365*10)
                )
            handler.set_header \
                ("Cache-Control", "max-age=" + str (86400*365*10))
        else:
            handler.set_header ("Cache-Control", "public")
        mime_type, encoding = mimetypes.guess_type (file_name)
        if mime_type :
            handler.set_header( "Content-Type", mime_type)

        if not include_body :
            return
        file = open (file_name, "rb")
        try :
            block_size = 1024 * 1024 * 1024
            for x in xrange (1 + file_size / block_size) :
                handler.write (file.read (block_size))
        finally:
            file.close()
    # end def _get

# end class _Static_File_Handler_

def Static_File_Handler (prefix, app_dir, * static_maps) :
    maps   = [GTW.Static_File_Map ("", os.path.abspath (app_dir))]
    maps.extend (static_maps)
    return ("/%s/(.*)" % (prefix, ), _Static_File_Handler_, dict (maps = maps))
# end def Static_File_Handler

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Static_File

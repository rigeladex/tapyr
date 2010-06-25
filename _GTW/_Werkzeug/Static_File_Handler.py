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
#    GTW.Werkzeug.Static_File_Handler
#
# Purpose
#    A static file handler for a werkzeug based WSGI application.
#    Should not be used in a production environment
#
# Revision Dates
#    20-Mar-2010 (MG) Creation
#    25-Jun-2010 (MG) Changed to generate a common interface between Werkzeug
#                     and Tornado
#    ««revision-date»»···
#--
from   _GTW                           import GTW
import _GTW._Werkzeug.Request_Handler
import _GTW._Werkzeug.Error
import _GTW.Static_File_Map

import  os
import  stat
import  time
import  datetime
import  email
import  mimetypes

class _Static_File_Handler_ (GTW.Werkzeug.Request_Handler) :
    """A static file handler which shpuld only be used during development to
       server static files directly form the disk.
    """

    block_size = 10 * 1024

    def __init__ (self, application, environ, maps = ()) :
        self.__super.__init__ (application, environ)
        self.maps = maps
    # end def __init__

    def __call__ (self, environ, start_response) :
        include_body = environ ["REQUEST_METHOD"] != "HEAD"
        path         = environ ["PATH_INFO"].lstrip ("/")
        for map in self.maps :
            file_name = map.get (path)
            if file_name :
                self._get (file_name, include_body)
                return self.response (environ, start_response)
        raise GTW.Werkzeug.Error_404 (path)
    # end def __call__

    def _get (self, file_name, include_body = True) :
        # Check the If-Modified-Since, and don't send the result if the
        # content has not been modified
        request     = self.request
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
                self.set_status (304)
                return

        self.set_header ("Last-Modified",  modified)
        self.set_header ("Content-Length", file_size)
        self.set_header ("Cache-Control",  "public")
        mime_type, encoding = mimetypes.guess_type (file_name)
        if mime_type :
            self.set_header ("Content-Type", mime_type)

        if include_body :
            with open (file_name, "rb") as file :
                for x in xrange (1 + file_size // self.block_size) :
                    self.write (file.read (self.block_size))
    # end def _get

# end class _Static_File_Handler_

def Static_File_Handler (prefix, media_dir, * maps) :
    maps      = list (maps)
    maps.append (GTW.Static_File_Map ("", os.path.abspath (media_dir)))
    return ("/" + prefix, _Static_File_Handler_, dict (maps = maps))
# end def Static_File_Handler

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Static_File_Handler

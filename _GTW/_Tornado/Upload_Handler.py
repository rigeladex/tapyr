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
#    GTW.Tornado.Upload_Handler
#
# Purpose
#    File upload handling
#
# Revision Dates
#    27-Jun-2010 (MG) Creation
#    ««revision-date»»···
#--
from   _GTW                          import GTW
import _GTW._Tornado.Request_Handler
import _GTW._Tornado.Request_Data
import _GTW._Upload_Handler_

class Upload_Handler ( GTW._File_Stream_Handling_
                     , GTW._Upload_Handler_
                     , GTW.Tornado.Request_Handler
                     ) :
    """File upload handler."""

    SUPPORTED_METHODS = ("POST", "PUT")

    Request_Data = GTW.Tornado.Request_Data

    def _handle_request (self, prefix) :
        path      = self.request.path
        if path.startswith (prefix) :
            path  = path [len (prefix):]
        self.path = path
        self.write (self._handle_files (self._get_file_stream))
    # end def _handle_request

# end class Upload_Handler

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Upload_Handler



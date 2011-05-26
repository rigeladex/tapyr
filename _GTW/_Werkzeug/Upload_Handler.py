# -*- coding: iso-8859-15 -*-
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
#    GTW.Werkzeug.Upload_Handler
#
# Purpose
#    File upload handling
#
# Revision Dates
#    27-Jun-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _GTW                          import GTW
import _GTW._Werkzeug.Request_Handler
import _GTW._Werkzeug.Request_Data
import _GTW._Upload_Handler_

class Upload_Request ( GTW._File_Stream_Handling_
                     , GTW.Werkzeug.Request_Handler.Request_Class
                     ) :
    """Override the way the file-stream is generated"""

# end class Upload_Request

class Upload_Handler (GTW._Upload_Handler_, GTW.Werkzeug.Request_Handler) :
    """The file upload request hanlder"""

    Request_Class = Upload_Request
    Request_Data  = GTW.Werkzeug.Request_Data

    def __call__ (self, environ, start_response) :
        self.set_header ("Content-Type", "text/html")
        self.response.response.append \
            (self._handle_files (self.request._get_file_stream))
        return self.response (environ, start_response)
    # end def __call__

# end class Upload_Handler

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Upload_Handler



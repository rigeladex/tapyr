# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package GTW.
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
#    GTW._Upload_Hanlder_
#
# Purpose
#    Base cass for file upload hanlders.
#
# Revision Dates
#    27-Jun-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                          import TFL
from   _GTW                          import GTW
import  tempfile
import  os
from    cStringIO                    import StringIO

class _File_Stream_Handling_ (object) :
    """Mixin providing the functions for creating a stream for the uploaded
       file
    """
    temp_dir = tempfile.gettempdir ()

    @TFL.Meta.Once_Property
    def temp_direcory (self) :
        result = os.path.join (self.temp_dir, os.path.dirname (self.path [1:]))
        if not os.path.isdir (result) :
            os.makedirs (result)
        return result
    # end def temp_direcory

    def _get_file_stream ( self
                         , total_content_length = 1024 * 500 + 10
                         , filename             = None
                         , content_type         = None
                         , content_length       = None
                         ) :
        if total_content_length > 1024 * 500:
            return tempfile.NamedTemporaryFile \
                ("wb+", dir = self.temp_direcory, delete = False)
        return StringIO()
    # end def _get_file_stream

# end class _File_Stream_Handling_

class _Upload_Handler_ (object) :
    """Mixin for saving the files and generating the response"""

    template = \
        """<html><head></head><body><dl>%s</dl></body>"""

    def _handle_files (self, get_file_stream) :
        result = []
        req_data      = self.Request_Data (self)
        for name, file_storage in req_data.files.iteritems () :
            file_name = getattr (file_storage.stream, "name", None)
            if file_name is None :
                stream = get_file_stream ()
                file_storage.save (stream)
                file_name = stream.name
                stream.close ()
            result.append ("<dd>%s</dd><dt>%s</dt>" % (name, file_name))
        return self.template % "".join (result)
    # end def _handle_files
# end class _Upload_Handler_

if __name__ != "__main__" :
    GTW._Export ("_File_Stream_Handling_", "_Upload_Handler_")
### __END__ GTW._Upload_Hanlder_



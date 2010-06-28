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
#    GTW.Tornado.Request_Data
#
# Purpose
#    Provide access to the request arguments and the uploaded files of a
#    tornado request handler
#
# Revision Dates
#    20-Mar-2010 (MG) Creation
#    24-Jun-2010 (MG) Signature of `__init__` changed, `files` added
#    28-Jun-2010 (MG) `stream` added
#    ««revision-date»»···
#--

from   _TFL                import TFL
import _TFL._Meta.Object
from   _GTW                import GTW
import _GTW.Request_Data
import _GTW._Tornado

class File_Storage (TFL.Meta.Object) :
    """A wrapper around an uploaded file to provide the same interface as
       werkzeug
    """

    stream = None

    def __init__ (self, ** kw) :
        self.__dict__.update (kw)
    # end def __init__

    def save (self, dst) :
        close_dst = False
        if isinstance (dst, basestring) :
            dst       = open (dst, "wb")
            close_dst = True
        try:
            dst.write (self.body)
        finally:
            if close_dst :
                dst.close ()
    # end def save

# end class File_Storage

class _Tornado_Request_Data_ (GTW.Request_Data) :

    _real_name = "Request_Data"

    def __init__ (self, handler) :
        self._request = handler.request
        self.__super.__init__ (handler.request.arguments)
    # end def __init__

    @TFL.Meta.Once_Property
    def files (self) :
        result = {}
        for name, file_list in self._request.files.iteritems () :
            assert len (file_list) == 1
            result [name] = File_Storage (** file_list [0])
        return result
    # end def files

Request_Data = _Tornado_Request_Data_ # end class

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Request_Data

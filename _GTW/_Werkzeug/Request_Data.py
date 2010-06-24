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
#    GTW.Werkzeug.Request_Data
#
# Purpose
#    A dict like object which provides access to the get and post data of a
#    werkzeug request
#
# Revision Dates
#    20-Mar-2010 (MG) Creation
#    24-Jun-2010 (MG) Signature of `__init__` changed, `files` added
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._Meta.Object

from   _GTW              import GTW
import _GTW._Werkzeug
import _GTW.Request_Data

class _Werkzeug_Request_Data_ (GTW.Request_Data) :

    def __init__ (self, handler) :
        self._request = request = handler.request
        self.__super.__init__ (dict (request.args, ** request.form))
    # end def __init__

    @TFL.Meta.Once_Property
    def files (self) :
        return self._request.files
    # end def files

Request_Data = _Werkzeug_Request_Data_ # end class

if __name__ != "__main__" :
    GTW.Werkzeug._Export ("*")
### __END__ GTW.Werkzeug.Request_Data

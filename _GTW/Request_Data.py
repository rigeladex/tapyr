# -*- coding: iso-8859-1 -*-
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
#    GTW.Request_Data
#
# Purpose
#    Wrapper around ddict like data where the values are lists but should not
#    be lists
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) Check's added to make sure te values in the original
#                     data dict contains exactly one element
#    20-Jan-2010 (MG) Support dict's which don't have lists as value's
#    29-Jan-2010 (MG) `__getitem__` and `get` fixed
#     3-Feb-2010 (MG) `iteritems` added
#    10-Feb-2010 (MG) Convert the data into unicode
#    21-Feb-2010 (MG) `pop` added
#    20-Mar-2010 (MG) Moved into `GTW` package
#    28-Jun-2010 (MG) `iterkeys` added
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._Meta.Object

from   _GTW              import GTW

class _GTW_Request_Data_ (TFL.Meta.Object) :
    """Convert the list values into no lists during access."""

    _real_name = "Request_Data"

    def __init__ (self, data) :
        self.data = data
    # end def __init__

    def _convert_element (self, value) :
        if isinstance (value, (list, tuple)) :
            assert len (value) == 1
            value = value [0]
        if value is not None and not isinstance (value, unicode) :
            return unicode (value, "utf8", "replace")
        return value
    # end def _convert_element

    def __getitem__ (self, key) :
        return self._convert_element (self.data [key])
    # end def __getitem__

    def get (self, key, default = None) :
        return self._convert_element (self.data.get (key, default))
    # end def get

    def iteritems (self) :
        for n in self.data.iterkeys () :
            yield n, self [n]
    # end def iteritems

    def iterkeys (self) :
        return self.data.iterkeys ()
    # end def iterkeys

    def pop (self, key, default = None) :
        return self._convert_element (self.data.pop (key, default))
    # end def pop

    def __contains__ (self, item) :
        return item in self.data
    # end def __contains__

    def __repr__ (self) :
        return repr (self.data)
    # end def __repr__

Request_Data = _GTW_Request_Data_ # end class

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.Request_Data

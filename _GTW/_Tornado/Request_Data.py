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
#    Wrapper around Tornado's request_data to enforce a single value per key
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
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL._Meta.Object

from   _GTW              import GTW

class Request_Data (TFL.Meta.Object) :
    """Wraps the request data from a tornado request to handle fact that
       tornado suplies all values as lists
    """

    def __init__ (self, data) :
        self.data = data
    # end def __init__

    def __getitem__ (self, key) :
        value = self.data [key]
        if isinstance (value, (list, tuple)) :
            assert len (value) == 1
            return unicode (value [0], "utf8", "replace")
        return value
    # end def __getitem__

    def get (self, key, default = None) :
        value = self.data.get (key, default)
        if isinstance (value, (list, tuple)) :
            assert len (value) == 1, value
            return unicode (value [0], "utf8", "replace")
        return value
    # end def get

    def iteritems (self) :
        for n in self.data.iterkeys () :
            yield n, self [n]
    # end def iteritems

    def pop (self, key, default = None) :
        value = self.data.pop (key, default)
        if isinstance (value, (list, tuple)) :
            assert len (value) == 1, value
            return unicode (value [0], "utf8", "replace")
        return value
    # end def pop

    def __contains__ (self, item) :
        return item in self.data
    # end def __contains__

# end class Request_Data

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Request_Data

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
#    «text»···
#
# Revision Dates
#    19-Jan-2010 (MG) Creation
#    20-Jan-2010 (MG) Check's added to make sure te values in the original
#                     data dict contains exactly one element
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
        assert len (key) == 1
        return  key [0]
    # end def __getitem__

    def get (self, key, default = None) :
        value = self.data.get (key, (default, ))
        assert len (value) == 1
        return value [0]
    # end def get

    def __contains__ (self, item) :
        return item in self.data
    # end def __contains__

# end class Request_Data

if __name__ != "__main__" :
    GTW.Tornado._Export ("*")
### __END__ GTW.Tornado.Request_Data



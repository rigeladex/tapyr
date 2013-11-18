# -*- coding: utf-8 -*-
# Copyright (C) 2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.elFinder.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.RST.TOP.elFinder.Error
#
# Purpose
#    Error handling for the jquery file browser `elfinder 2`
#    http://elfinder.org/
#
# Revision Dates
#    29-Jan-2013 (MG) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from    _GTW                       import GTW
from    _TFL._Meta.Once_Property   import Once_Property
import  _GTW._RST._TOP._elFinder

class Error (StandardError) :
    """elFinder error message"""

    def __init__ (self, code, data = None) :
        self.code = code
        self.data = data
    # end def __init__

    @Once_Property
    def json_cargo (self) :
        if self.data :
            return [self.code, self.data]
        return self.code
    # end def json_cargo

# end class Error

if __name__ != "__main__" :
    GTW.RST.TOP.elFinder._Export ("*")
### __END__ GTW.RST.TOP.elFinder.Error

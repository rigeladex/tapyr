# -*- coding: utf-8 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.CSS.
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
#    GTW.CSS._TRBL_
#
# Purpose
#    Base class for top/right/bottom/left spec
#
# Revision Dates
#    18-Jan-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._CSS
import _TFL._Meta.Object

class _TRBL0_ (TFL.Meta.Object) :
    """Base class for top/right/bottom/left spec."""

    default = None
    Type    = None

    b = property (lambda s : s.values [2])
    l = property (lambda s : s.values [3])
    r = property (lambda s : s.values [1])
    t = property (lambda s : s.values [0])

    def __init__ (self, t = None, r = None, b = None, l = None, default = None) :
        if default is None :
            default = self.default
        Type = self.Type
        self.values = tuple \
            (Type (v if v is not None else default) for v in (t, r, b, l))
    # end def __init__

    def __iter__ (self) :
        return iter (self.values)
    # end def __iter__

    def __nonzero__ (self) :
        return any (self.values)
    # end def __nonzero__

    def __str__ (self) :
        values = list (self.values)
        for h, t in ((-1, -3), (-1, -3), (0, 1)) :
            if values [h] == values [t] :
                values.pop ()
            else :
                break
        return " ".join (str (v) for v in values)
    # end def __str__

# end class _TRBL0_

class _TRBL_ (_TRBL0_) :
    """Top/right/bottom/left spec, repeated values."""

    def __init__ (self, * values) :
        assert len (values) < 5, str (values)
        l = len (values)
        if not l :
            values = (self.default, ) * 4
        elif l == 1 :
            values = values * 4
        elif l == 2 :
            values = values * 2
        elif l == 3 :
            values += (values [1], )
        self.__super.__init__ (* values)
    # end def __init__

# end class _TRBL_

if __name__ != "__main__" :
    GTW.CSS._Export ("_TRBL_", "_TRBL0_")
### __END__ GTW.CSS._TRBL_

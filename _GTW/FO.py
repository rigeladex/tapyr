# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    GTW.FO
#
# Purpose
#    Formatter for attributes of Objects
#
# Revision Dates
#    20-Jan-2010 (CT) Creation
#    10-Feb-2010 (CT) `__getattr__` changed to use `ui_display`, if any
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _TFL._Meta.Object

class FO (TFL.Meta.Object) :
    """Formatter for attributes of Objects."""

    def __init__ (self, obj, enc = None, getter = "raw_attr") :
        self.__obj    = obj
        self.__enc    = enc
        if isinstance (getter, basestring):
            self.__getter = getattr (obj, getter)
        else :
            self.__getter = lambda name : getter (obj, name)
    # end def __init__

    def __getattr__ (self, name) :
        result = None
        obj    = self.__obj
        attr   = getattr (obj.__class__, name, None)
        if attr is not None :
            ckd = getattr (obj, name, None)
            uid = getattr (ckd, "ui_display", None)
            if uid :
                result = uid
        if result is None :
            result = self.__getter (name)
        if self.__enc and isinstance (result, str) :
            result = unicode (result, self.__enc, "replace")
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class FO

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.FO

# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#    10-Feb-2010 (CT) `MOM.Entity.FO` factored
#     5-Aug-2010 (CT) `_get_nested` added to support `composite.field`
#    10-Dec-2012 (CT) Change `_get_nested` to delegate to `obj.FO`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _TFL._Meta.Object

class FO (TFL.Meta.Object) :
    """Formatter for attributes of Objects."""

    def __init__ (self, obj, enc = None) :
        self.__obj    = obj
        self.__fo     = obj.FO
        self.__enc    = enc
        self.__cache  = {}
    # end def __init__

    def _get_nested (self, name) :
        try :
            result = self.__cache [name]
        except KeyError :
            self.__cache [name] = result = unicode (getattr (self.__fo, name))
        return result
    # end def _get_nested

    def __getattr__ (self, name) :
        if "." in name :
            result = self._get_nested (name)
        else :
            result = getattr (self.__fo, name)
            if self.__enc and isinstance (result, str) :
                result = unicode (result, self.__enc, "replace")
        setattr (self, name, result)
        return result
    # end def __getattr__

# end class FO

if __name__ != "__main__" :
    GTW._Export ("*")
### __END__ GTW.FO

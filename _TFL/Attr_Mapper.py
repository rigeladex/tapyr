# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Attr_Mapper
#
# Purpose
#    Allow access to attributes of an object with different names
#
# Revision Dates
#     5-Mar-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL               import TFL
from   _TFL.predicate     import callable

import _TFL._Meta.Object

class Attr_Mapper (TFL.Meta.Object) :
    """Allow access to attributes of an object with different names"""

    def __init__ (self, ** kw) :
        self._map = kw
    # end def __init__

    def __call__ (self, obj, name) :
        mapped = self._map.get (name, name)
        if mapped is not None :
            if callable (mapped) :
                return mapped (obj)
            else :
                return getattr (obj, mapped)
        raise AttributeError (name)
    # end def __call__

# end class Attr_Mapper

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ TFL.Attr_Mapper

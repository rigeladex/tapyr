# -*- coding: utf-8 -*-
# Copyright (C) 2004-2005 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    Formatter_Scope
#
# Purpose
#    Provide a descendent of TFL.Caller.Object_Scope that returns
#    `""` instead of `None`
#
# Revision Dates
#    12-Dec-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _CAL                    import CAL
import _TFL.Caller

class Formatter_Scope (TFL.Caller.Object_Scope) :

    def __getitem__ (self, index) :
        result = self.__super.__getitem__ (index)
        if result is None :
            result = ""
        return result
    # end def __getitem__

# end class Formatter_Scope

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ Formatter_Scope



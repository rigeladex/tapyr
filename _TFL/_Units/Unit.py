# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Units.Unit
#
# Purpose
#    Model a unit
#
# Revision Dates
#     9-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units

class Unit (TFL.Meta.Object) :
    """Model a unit kind"""

    def __init__ (self, name, factor = 1.0, abbr = None) :
        self.name   = name
        self.factor = float (factor)
        self.abbr   = abbr
    # end def __init__

    def __cmp__ (self, rhs) :
        try :
            rhs = rhs.factor
        except AttributeError :
            pass
        return cmp (self.factor, rhs)
    # end def __cmp__

    def __div__ (self, rhs) :
        try :
            rhs = rhs.factor
        except AttributeError :
            pass
        return self.factor / rhs
    # end def __div__

    def __float__ (self) :
        return self.factor
    # end def __float__

    def __mul__ (self, rhs) :
        try :
            rhs = rhs.factor
        except AttributeError :
            pass
        return self.factor * rhs
    # end def __mul__

    def __pow__ (self, rhs) :
        return self.factor ** rhs
    # end def __pow__

    def __repr__ (self) :
        return "%s = %s" % (self.name, self.factor)
    # end def __repr__

# end class Unit

if __name__ != "__main__" :
    TFL.Units._Export ("Unit")
### __END__ TFL.Units.Unit

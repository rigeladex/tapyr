# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Units.Kind
#
# Purpose
#    Model a unit kind
#
# Revision Dates
#     8-Aug-2004 (CT) Creation
#    29-Sep-2006 (CT) `__add__` and `__sub__` added
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
#    ��revision-date�����
#--

from   _TFL import TFL
from   _TFL.pyk import pyk

from   _TFL._Meta.totally_ordered import totally_ordered

import _TFL._Meta.Object
import _TFL._Units.M_Kind

@totally_ordered
@pyk.adapt__div__
class Kind (TFL.Meta.BaM (TFL.Meta.Object, metaclass = TFL.Units.M_Kind)) :
    """Model a unit kind"""

    base_unit     = None ### redefine in descendents
    _units        = ()   ### redefine in descendents

    def __init__ (self, value, unit = None) :
        if unit is None :
            unit   = self.base_unit
        elif unit in self.abbrs :
            unit   = self.abbrs [unit]
        elif unit in self.units :
            unit   = self.units [unit]
        self.value = value * unit.factor
        self.unit  = unit
    # end def __init__

    def __add__ (self, rhs) :
        if isinstance (rhs, self.__class__) :
            return self.__class__ (self.value + rhs.value)
        raise TypeError \
            ( "unsupported operand type(s) for +: '%s' and '%s'"
            % (self.__class__.__name__, rhs.__class__.__name__)
            )
    # end def __add__

    def __eq__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value == rhs
    # end def __eq__

    def __lt__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value < rhs
    # end def __lt__

    def __truediv__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value / rhs
    # end def __truediv__

    def __float__ (self) :
        return self.value
    # end def __float__

    def __getattr__ (self, name) :
        if name.startswith ("as_") :
            unit_name = name [3:]
            if unit_name in self.abbrs :
                unit = self.abbrs [unit_name]
            elif unit_name in self.units :
                unit = self.units [unit_name]
            else :
                raise AttributeError (name)
            return self.value / unit.factor
        raise AttributeError (name)
    # end def __getattr__

    def __mul__ (self, rhs) :
        try :
            rhs = rhs.value
        except AttributeError :
            pass
        return self.value * rhs
    # end def __mul__

    def __repr__ (self) :
        return "%.12g" % (self.value, )
    # end def __repr__

    def __sub__ (self, rhs) :
        if isinstance (rhs, self.__class__) :
            return self.__class__ (self.value - rhs.value)
        raise TypeError \
            ( "unsupported operand type(s) for -: '%s' and '%s'"
            % (self.__class__.__name__, rhs.__class__.__name__)
            )
    # end def __sub__

# end class Kind

if __name__ != "__main__" :
    TFL.Units._Export ("Kind")
### __END__ TFL.Units.Kind

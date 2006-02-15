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
#    TFL.Units.Mass
#
# Purpose
#    Mass units
#
# Revision Dates
#     8-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind

class Mass (TFL.Units.Kind) :
    """Units of mass

       >>> Mass (1)
       1.0
       >>> Mass (1, "g")
       0.001
       >>> Mass (1, "oz")
       0.028349523125
       >>> Mass (1, "stone")
       6.35029318
       >>> Mass (1, "lb")
       0.45359237
    """

    Unit              = TFL.Units.Unit

    base_unit         = Unit ("kilogram", 1.0, "kg")
    _pound            = 0.45359237
    _units            = \
        (
        # SI prefixes
          Unit ("microgram",               0.000000001, "ug")
        , Unit ("milligram",               0.000001,    "mg")
        , Unit ("gram",                    0.001,       "g")
        , Unit ("ton",                  1000.0,         "t")
        # US customary units
        , Unit ("pound",                _pound,         "lb")
        , Unit ("grain",                _pound / 7000)
        , Unit ("drams",                _pound /  256,  "dr")
        , Unit ("ounce",                _pound /   16,  "oz")
        , Unit ("short_ton",            _pound * 2000)
        , Unit ("long_ton",             _pound * 2240)
        # Odd British unit
        , Unit ("stone",                _pound *   14)
        )

# end class Mass

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ Mass

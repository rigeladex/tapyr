# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Units.Power
#
# Purpose
#    Units of power
#
# Revision Dates
#    15-Feb-2006 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    06-Aug-2007 (CED) Future import removed again
#    ««revision-date»»···
#--



from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind

class Power (TFL.Units.Kind) :
    """Units of power

       >>> Power (1.0)
       1.0
       >>> Power (1, "kW")
       1000.0
       >>> Power (1, "hp")
       735.49875
       >>> Power (1, "cal/s")
       4.1868
    """

    Unit              = TFL.Units.Unit

    base_unit         = Unit ("watt", 1.0, "W")
    _units            = \
        ( ### see http://en.wikipedia.org/wiki/Conversion_of_units
          Unit ("calorie_per_second",         4.1868,     "cal/s")
        , Unit ("horsepower",               735.49875,    "hp")
        , Unit ("kilowatt",                1000.0,        "kW")
        )

# end class Power

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ TFL.Units.Power

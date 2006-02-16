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
#    TFL.Units.Length
#
# Purpose
#    Length units
#
# Revision Dates
#     8-Aug-2004 (CT)  Creation
#     9-Feb-2005 (CED) Some additional units added
#    15-Feb-2006 (CT)  CED's additions corrected (rounding the speed of light
#                      in the context of units is a bad thing (TM))
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind
import _TFL._Units.Prefix
import _TFL._Units.Unit

class Length (TFL.Units.Kind) :
    """Units of length.

       >>> Length (1)
       1.0
       >>> Length (1,"yd")
       0.9144
       >>> Length (1,"in")
       0.0254
       >>> Length (1,"fur")
       201.168
       >>> Length (1,"mi")
       1609.344
       >>> Length (1,"Nm")
       1852.0
    """

    Unit              = TFL.Units.Unit

    base_unit         = Unit ("meter", 1.0, "m")
    _units            = \
        ( ### see http://en.wikipedia.org/wiki/Conversion_of_units
        # SI prefixes
          Unit ("nanometer",      TFL.Units.nano,            "nm")
        , Unit ("micrometer",     TFL.Units.micro,           "um")
        , Unit ("millimeter",     TFL.Units.milli,           "mm")
        , Unit ("centimeter",     TFL.Units.centi,           "cm")
        , Unit ("decimeter",      TFL.Units.deci,            "dm")
        , Unit ("dekameter",      TFL.Units.deka,            "dam")
        , Unit ("hectometer",     TFL.Units.hecto,           "hm")
        , Unit ("kilometer",      TFL.Units.kilo,            "km")
        # US customary units
        , Unit ("mil",               2.54e-5,                "mil")
        , Unit ("inch",              0.0254,                 "in")
        , Unit ("foot",              0.3048,                 "ft")
        , Unit ("yard",              0.9144,                 "yd")
        , Unit ("rod",               5.0292,                 "rd")
        , Unit ("furlong",         201.168,                  "fur")
        , Unit ("statute_mile",   1609.344,                  "mi")
        , Unit ("nautical_mile",  1852.0,                    "Nm")
        # physics units
        , Unit ("astronomical_unit", 1.49597870691e11,       "AU")
        , Unit ("light_year",        9.4607304725808e15,     "ly")
        , Unit ("parsec",            3.0856775813e16,        "pc")
        , Unit ("angstrom",       TFL.Units.nano / 10,       "A")
        )

# end class Length

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ TFL.Units.Length

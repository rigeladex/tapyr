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
#    TFL.Units.Liquid
#
# Purpose
#    Liquid capacity units
#
# Revision Dates
#     8-Aug-2004 (CT) Creation
#    23-Jul-2007 (CED) Activated absolute_import
#    ««revision-date»»···
#--
from __future__ import absolute_import


from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind
import _TFL._Units.Volume

class Liquid (TFL.Units.Kind) :
    """Units of liquid capacity

       >>> Liquid (1)
       1.0
       >>> Liquid (1.0, "oz")
       0.029573
       >>> Liquid (1.0, "dr")
       0.003696625
       >>> Liquid (1.0, "gal")
       3.785344
       >>> Liquid (1.0, "pt")
       0.473168
    """

    Volume            = TFL.Units.Volume
    Unit              = TFL.Units.Unit

    base_unit         = Unit ("liter", 1.0, "l")
    _ounce            = 0.029573
    _units            = \
        (
        # SI prefixes
          Unit ("nanoliter",         TFL.Units.nano,  "nl")
        , Unit ("microliter",        TFL.Units.micro, "ul")
        , Unit ("milliliter",        TFL.Units.milli, "ml")
        , Unit ("centiliter",        TFL.Units.centi, "cl")
        , Unit ("deciliter",         TFL.Units.deci,  "dl")
        , Unit ("hectoliter",        TFL.Units.hecto, "hl")
        , Unit ("kiloliter",         TFL.Units.kilo,  "kl")
        , Unit ("cubic_decimeter",      1.0)
        , Unit ("cubic_meter",       1000.0)
        # US customary units
        , Unit ("ounce",             _ounce,          "oz")
        , Unit ("drop",              _ounce    / 360)
        , Unit ("drams",             _ounce    /   8, "dr")
        , Unit ("teaspoon",          _ounce    /   6, "tsp")
        , Unit ("tablespoon",        _ounce    /   2, "tb")
        , Unit ("cup",               _ounce    *   8)
        , Unit ("pint",              _ounce    *  16, "pt")
        , Unit ("quart",             _ounce    *  32, "qt")
        , Unit ("gallon",            _ounce    * 128, "gal")
        )

# end class Liquid

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ TFL.Units.Liquid

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
#    TFL.Units.Time
#
# Purpose
#    Time units
#
# Revision Dates
#     9-Feb-2005 (CED) Creation
#    15-Feb-2006 (CT)  Done right
#     8-Nov-2006 (CED) `microfortnight` added (used in VMS)
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind
import _TFL._Units.Prefix
import _TFL._Units.Unit

class Time (TFL.Units.Kind) :
    """Units of time.

       >>> Time (1)
       1.0
       >>> Time (1, "ns")
       1e-09
       >>> Time (1, "d")
       86400.0
       >>> Time (1, "wk")
       604800.0
       >>> Time (1, "wk") == Time (7, "d")
       True
    """

    Unit          = TFL.Units.Unit

    base_unit     = Unit ("second", 1.0, "s")

    _week         = 3600.0 * 24.0 * 7.0
    _units        = \
        ( ### see http://en.wikipedia.org/wiki/Conversion_of_units
        # SI prefixes
          Unit ("attosecond",      TFL.Units.atto,   "as")
        , Unit ("femtosecond",     TFL.Units.femto,  "fs")
        , Unit ("picosecond",      TFL.Units.pico,   "ps")
        , Unit ("nanosecond",      TFL.Units.nano,   "ns")
        , Unit ("microsecond",     TFL.Units.micro,  "us")
        , Unit ("millisecond",     TFL.Units.milli,  "ms")
        # Usual units
        , Unit ("jiffy",                  1 / 60.0)
        , Unit ("minute",                     60.0, "min")
        , Unit ("moment",                     90.0)
        , Unit ("hour",                     3600.0,  "h")
        , Unit ("day",               3600.0 * 24.0,  "d")
        , Unit ("week",                      _week, "wk")
        # Unusual units
        , Unit ("microfortnight",  TFL.Units.micro * 2.0 * _week)
        , Unit ("fortnight",                         2.0 * _week)
        # physics units
        , Unit ("planck_time",     1.351211818e-43)
        )

# end class Time

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ TFL.Units.Time

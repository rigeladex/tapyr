# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    Time
#
# Purpose
#    Time units
#
# Revision Dates
#     9-Feb-2005 (CED) Creation
#    ««revision-date»»···
#--
#

from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind
import _TFL._Units.Prefix
import _TFL._Units.Unit

class Time (TFL.Units.Kind) :
    """Units of time"""

    Unit          = TFL.Units.Unit

    base_unit     = Unit ("second", 1.0, "sec")
    _units        = \
        (
        # SI prefixes
          Unit ("nanosecond",      TFL.Units.nano,   "ns")
        , Unit ("microsecond",     TFL.Units.micro,  "us")
        , Unit ("millisecond",     TFL.Units.milli,  "ms")
        # Usual units
        , Unit ("minute",                     60.0, "min")
        , Unit ("hour",                     3600.0,   "h")
        , Unit ("day",               3600.0 * 24.0,   "d")
        , Unit ("week",        3600.0 * 24.0 * 7.0,   "w")
        , Unit ("fortnight",              1.2096e6,  "fn")
        )
# end class Time

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ Time



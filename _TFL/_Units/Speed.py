# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    TFL.Units.Speed
#
# Purpose
#    Units of speed
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
import _TFL._Units.Length
import _TFL._Units.Prefix
import _TFL._Units.Time
import _TFL._Units.Unit

class Speed (TFL.Units.Kind) :
    """Units of speed.

       >>> Speed (1)
       1.0
       >>> Speed (1, "kmh")
       0.277777777778
       >>> Speed (1, "c")
       299792458.0
    """

    Length        = TFL.Units.Length
    Time          = TFL.Units.Time
    Unit          = TFL.Units.Unit

    base_unit     = Unit ("meter_per_second", 1.0, "m/s")
    _units        = \
        ( ### see http://en.wikipedia.org/wiki/Conversion_of_units
        # Usual units
          Unit ("kilometer_per_hour", Length.kilometer     / Time.hour, "kmh")
        # US customary units
        , Unit ("furlong_per_fortnight", Length.furlong    / Time.fortnight)
        , Unit ("mile_per_hour",      Length.statute_mile  / Time.hour, "mph")
        , Unit ("knots",              Length.nautical_mile / Time.hour, "kn")
        # physics units
        , Unit ("speed_of_light",     2.99792458e8,  "c")
        )

# end class Speed

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ TFL.Units.Speed

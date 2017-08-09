# -*- coding: utf-8 -*-
# Copyright (C) 2007-2017 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    SKY.Location
#
# Purpose
#    Model terrestrial location of observer
#
# Revision Dates
#    14-Nov-2007 (CT) Creation
#    13-May-2016 (CT) Add `__str__`
#    29-Sep-2016 (CT) Improve support for `height`
#     9-Oct-2016 (CT) Move out from `CAL` to toplevel package
#     5-Apr-2017 (CT) Add [simple] `_Location_Arg_`
#     9-Aug-2017 (CT) Use `Angle`, not home-grown `_normalized` function
#     9-Aug-2017 (CT) Change to modern `longitude` definition (W <-> negative)
#                     + Add `longitude_meuss` for old convention
#     9-Aug-2017 (CT) Add support for time zones
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _SKY                     import SKY
from   _TFL                     import TFL
from   _TFL.pyk                 import pyk

from   _TFL.Angle               import Angle, Angle_D, Angle_R
from   _TFL.predicate           import rounded_to
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.CAO
import _TFL._Meta.Object

@pyk.adapt__str__
class Location (TFL.Meta.Object) :
    """Model terrestrial location of observer.

    `longitude` is negative for locations west of the prime meridian.
    """

    Table = {}

    def __init__ (self, latitude, longitude, name = None, height = None, tz_name = None) :
        self.latitude  = Angle (latitude)
        self.longitude = Angle (longitude)
        self.name      = name
        self.height    = 0 if height is None else height
        self.tz_name   = tz_name
        if name is not None :
            Table      = self.Table
            assert name not in Table
            Table [name] = self
            if name [0].isupper :
                setattr (Location, name, self)
    # end def __init__

    @Once_Property
    def longitude_meuss (self) :
        """Return `longitude` in old-style astronomical system (positive W of
        prime meridian).
        """
        return - self.longitude
    # end def longitude_meuss

    @Once_Property
    def tz (self) :
        """Timezone object"""
        import dateutil.tz
        result  = None
        tz_name = self.tz_name
        if tz_name is not None :
            result = dateutil.tz.gettz (tz_name)
        else :
            name   = self.name
            offset = (rounded_to (self.longitude.degrees, 15) / 15) * 3600.
            result = dateutil.tz.tzoffset (name or str (offset), offset)
        return result
    # end def tz

    def __str__ (self) :
        lon    = self.longitude
        lat    = self.latitude
        if lon.degrees > 180.0 :
            lon -= 360.0
        result = "%s %s, %s %s" % \
            ( abs (lon), "W" if lon.degrees < 0.0 else "E"
            , abs (lat), "S" if lat.degrees < 0.0 else "N"
            )
        if self.height :
            result = "%s, %2.0fm above sea level" % (result, self.height)
        if self.name :
            result = "%s [%s]" % (self.name, result)
        return result
    # end def __str__

# end class Location

Location \
    ( Angle_D (48, 14)
    , Angle_D (16, 22)
    , "Vienna"
    , 180
    , tz_name = "Europe/Vienna"
    )

Location \
    ( Angle_D (37, 51,  7)
    , - Angle_D ( 8, 47, 31)
    , "Porto Covo"
    , 25
    , tz_name = "Europe/Lisbon"
    )

class _Location_Arg_ (TFL.CAO.Str) :
    """Argument or option defining a location"""

    _real_name = "Location"

    def cook (self, value, cao = None) :
        if value :
            try :
                result = Location.Table [value]
            except KeyError :
                raw_lat, raw_lon = tuple (v.strip () for v in value.split (","))
                lat    = self._latituded  (raw_lat)
                lon    = self._longituded (raw_lon)
                result = Location (lat, lon)
            return result
    # end def cook

    def _latituded (self, value) :
        sign = -1 if value.endswith ("S") else +1
        v    = value.rstrip ("NS ")
        return float (v) * sign
    # end def _latituded

    def _longituded (self, value) :
        sign = -1 if value.endswith ("W") else +1
        v    = value.rstrip ("EW ")
        return float (v) * sign
    # end def _longituded

# end class _Location_Arg_

if __name__ != "__main__" :
    SKY._Export ("*")
### __END__ SKY.Location

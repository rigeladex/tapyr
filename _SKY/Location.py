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
#     9-Aug-2017 (CT) Add `ui_name`, `kwds` to `__init__`
#                     + Add `args` to `_Location_Arg_.cook`
#                     + Add `as_json_cargo`
#                     + Add `__new__` to use `Table [name]` if it exists
#                       * Add `normalized_lat`, `normalized_lon` to
#                         semantically normalize and ensure the latitude range
#    11-Aug-2017 (CT) Add supprt for `json_dump` (`_import_cb_json_dump`)
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

    def __new__ (cls, latitude, longitude, name = None, * args, ** kwds) :
        Table = cls.Table
        if name and name in Table :
            result = Table [name]
            lat    = cls.normalized_lat (latitude)
            if abs (result.latitude - lat) > 1e-9 :
                raise ValueError \
                    ( "Different latitude for location named %s: %s vs. %s"
                    % (name, result.latitude.degrees, lat.degrees)
                    )
            lon    = cls.normalized_lon (longitude)
            if lon > 180 :
                lon -= 360.
            if abs (result.longitude - lon) > 1e-9 :
                raise ValueError \
                    ( "Different longitude for location named %s: %s vs. %s"
                    % (name, result.longitude.degrees, lon.degrees)
                    )
        else :
            result = Table [name] = cls.__c_super.__new__ \
                (cls, latitude, longitude, name, * args, ** kwds)
            result._init_ (latitude, longitude, name, * args, ** kwds)
        return result
    # end def __new__

    def _init_ \
            ( self, latitude, longitude
            , name    = None
            , height  = None
            , tz_name = None
            , ui_name = None
            , ** kwds
            ) :
        self.latitude  = self.normalized_lat (latitude)
        self.longitude = self.normalized_lon (longitude)
        self.name      = name
        self.height    = 0 if height is None else float (height)
        self.tz_name   = tz_name
        self.ui_name   = ui_name
        self._kwds     = kwds
        self.__dict__.update (kwds)
    # end def _init_

    @classmethod
    def normalized_lat (cls, latitude) :
        result = Angle (latitude)
        if result.degrees > 270 :
            result -= 360
        if result.degrees > 90 :
            raise ValueError \
                ("Latitude must be in (-90, +90); got %s" % (latitude))
        return result
    # end def normalized_lat

    @classmethod
    def normalized_lon (cls, longitude) :
        result = Angle (longitude)
        if result.degrees > 180 :
            result -= 360.
        return result
    # end def normalized_lon

    @Once_Property
    def as_json_cargo (self) :
        result = dict \
            ( latitude  = self.latitude.degrees
            , longitude = self.longitude.degrees
            )
        for k in ("name", "height", "tz_name", "ui_name", "_kwds") :
            v = getattr (self, k, None)
            if v :
                result [k] = v
        return result
    # end def as_json_cargo

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

    @property
    def ui_name (self) :
        result = self._ui_name or self.name
        return result
    # end def ui_name

    @ui_name.setter
    def ui_name (self, value) :
        self._ui_name = value
    # end def ui_name

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
            result = "%s [%s]" % (self.ui_name, result)
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
                args   = tuple (v.strip () for v in value.split (","))
                raw_lat, raw_lon = args [:2]
                lat    = self._latituded  (raw_lat)
                lon    = self._longituded (raw_lon)
                result = Location (lat, lon, * args [2:])
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

@TFL._Add_Import_Callback ("_TFL.json_dump")
def _import_cb_json_dump (module) :
    @module.default.add_type (Location)
    def json_encode_ordinal_or_year (o) :
        return o.as_json_cargo
# end def _import_cb_json_dump

if __name__ != "__main__" :
    SKY._Export ("*")
### __END__ SKY.Location

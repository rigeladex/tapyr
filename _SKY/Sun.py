# -*- coding: utf-8 -*-
# Copyright (C) 2007-2016 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    SKY.Sun
#
# Purpose
#    Provide ephemeris of Sun
#
# References
#    J. Meeus, Astronomical Algorithms, 2nd edition, 1998, ISBN 0-943396-61-1
#
# Revision Dates
#     8-Nov-2007 (CT) Creation
#    11-Nov-2007 (CT) Creation continued
#    13-Nov-2007 (CT) Creation continued..
#    13-Nov-2007 (CT) Moved from `CAL` to `CAL.Sky`
#    13-Nov-2007 (CT) `main` added
#    14-Nov-2007 (CT) `RTS_Sun.On_Day` added (and used in `main`)
#    14-Nov-2007 (CT) `hh_mm` factored to `CAL.Time`
#     1-Jan-2008 (CT) `-day_length` and `-transit` added
#    31-Mar-2008 (CT) Doctests adapted to change of RTS to consider `dst` for
#                     local times
#    16-Jun-2013 (CT) Use `TFL.CAO`, not `TFL.Command_Line`
#    13-May-2016 (CT) Add option `-Location`, allow more than one argument
#    26-Sep-2016 (CT) Factor `CAL.Sky.Earth.Time`
#    26-Sep-2016 (CT) Adapt doc-tests to correction of `CAL.Time.microsecond`
#    27-Sep-2016 (CT) Factor `mean_obliquity_ecliptic` to `CAL.Sky.Earth.Time`
#    28-Sep-2016 (CT) Add `alt_az`
#    30-Sep-2016 (CT) Use `decl` and `ra`,
#                     not `declination` and `right_ascension`
#     9-Oct-2016 (CT) Move out from `CAL` to toplevel package
#    ««revision-date»»···
#--

from   __future__                 import print_function

from   _CAL                       import CAL
from   _SKY                       import SKY
from   _TFL                       import TFL

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.Angle                 import Angle_D, Angle_R
from   _TFL.portable_repr         import portable_repr

import _SKY.Earth
import _SKY.Location
import _SKY.RTS

import _TFL._Meta.Object
import _TFL.CAO

class Sun (TFL.Meta.Object) :
    """Model behavior of sun for a single day.

       ### Example 25.a of J. Meeus, p.165
       >>> import _CAL.Date
       >>> s = Sun (CAL.Date (1992, 10, 13))
       >>> print (portable_repr (s.time.t))
       -0.0721834360027
       >>> s.time.geometric_mean_longitude_sun
       Angle_D (201.807196507)
       >>> s.time.geometric_mean_anomaly_sun
       Angle_D (278.993966432)
       >>> print (portable_repr (s.time.eccentriticy_earth_orbit))
       0.0167116677149
       >>> s.equation_of_center
       Angle_D (-1.89732384337)
       >>> s.true_longitude
       Angle_D (199.909872663)
       >>> print (s.true_longitude)
       199°54'35.54''
       >>> print (portable_repr (s.radius_vector))
       0.997661950006
       >>> s.omega
       Angle_D (264.657131805)
       >>> s.apparent_longitude
       Angle_D (199.908941896)
       >>> print (s.apparent_longitude)
       199°54'32.19''
       >>> s.time.mean_obliquity_ecliptic
       Angle_D (23.4402297955)
       >>> print (s.time.mean_obliquity_ecliptic)
       023°26'24.83''
       >>> print (portable_repr (s.time.mean_obliquity_ecliptic.seconds))
       24.8272638004
       >>> s.time.obliquity_corrected
       Angle_D (23.4399914197)
       >>> print (portable_repr (s.ra.degrees))
       198.380825219
       >>> print (portable_repr (s.decl.degrees))
       -7.78506987319
       >>> print (portable_repr (s.equation_of_time))
       13.7110102528
    """

    ### see J. Meeus, pp. 163f.
    Table = {}

    def __new__ (cls, day) :
        Table = cls.Table
        if day in Table :
            return Table [day]
        self = TFL.Meta.Object.__new__ (cls)
        if not isinstance (day, CAL.Date_Time) :
            Table [day] = self
        self._init_ (day)
        return self
    # end def __new__

    def _init_ (self, day) :
        self.day   = day
        self.time  = time = SKY.Earth.Time (day)
        self.omega = time.longitude_ascending_node_moon
    # end def _init_

    @Once_Property
    def equation_of_center (self) :
        """Equation of center for the sun (in degrees)."""
        m1   = self.time.geometric_mean_anomaly_sun
        m2   = m1 * 2
        m3   = m1 * 3
        time = self.time
        return Angle_D \
            ( m1.sin * (1.914602 - 0.004817 * time.t - 0.000014 * time.t2)
            + m2.sin * (0.019993 - 0.000101 * time.t)
            + m3.sin * (0.000289)
            )
    # end def equation_of_center

    @Once_Property
    def true_longitude (self) :
        """True longitude of the sun (in degrees)."""
        return self.time.geometric_mean_longitude_sun + self.equation_of_center
    # end def true_longitude

    @Once_Property
    def true_anomaly (self) :
        """True anamoly of the sun (in degrees)."""
        return self.time.geometric_mean_anomaly_sun   + self.equation_of_center
    # end def true_anomaly

    @Once_Property
    def radius_vector (self) :
        """Distance of earth to the sun (in AU)."""
        ### Eq. (25.5)
        v = self.true_anomaly
        e = self.time.eccentriticy_earth_orbit
        return (1.000001018 * (1 - e * e)) / (1 + e * v.cos)
    # end def radius_vector

    @Once_Property
    def apparent_longitude (self) :
        """Apparent longitude of the sun (in degrees)."""
        return self.true_longitude - (0.00569 + 0.00478 * self.omega.sin)
    # end def apparent_longitude

    @Once_Property
    def ra (self) :
        """Apparent right ascension of the sun (in degrees)."""
        ### Eq. (25.6), for apparent position
        o      = self.time.obliquity_corrected
        l      = self.apparent_longitude
        result = Angle_R.normalized (Angle_R.atan2 (o.cos * l.sin, l.cos))
        return result
    # end def ra

    @Once_Property
    def decl (self) :
        """Apparent declination of the sun (in degrees)."""
        ### Eq. (25.7), for apparent position
        o = self.time.obliquity_corrected
        l = self.apparent_longitude
        return Angle_D.asin (o.sin * l.sin)
    # end def decl

    @Once_Property
    def equation_of_time (self) :
        """Difference between true solar time and mean solar time
           (in minutes).
        """
        ### see J. Meeus, p. 185, Eq. (28.3)
        e      = self.time.eccentriticy_earth_orbit
        l2     = self.time.geometric_mean_longitude_sun * 2
        l4     = l2 * 2
        m1     = self.time.geometric_mean_anomaly_sun
        m2     = m1 * 2
        o_half = self.time.mean_obliquity_ecliptic / 2
        y      = o_half.tan ** 2
        return Angle_R \
            (        y     * l2.sin
            - 2.00 * e     * m1.sin
            + 4.00 * e * y * m1.sin * l2.cos
            - 0.50 * y * y * l4.sin
            - 1.25 * e * e * m2.sin
            ).degrees * 4.0
    # end def equation_of_time

    def alt_az (self, lat, lon) :
        """Solar altitude and azimuth angle for location `lat`, `lon`.

           Azimuth is measured eastward from the North.
        """
        return self.ha_alt_az (lat, lon) [1:]
    # end def alt_az

    def ha_alt_az (self, lat, lon) :
        """Solar hour angle, altitude and azimuth angle for `lat`, `lon`.

           Azimuth is measured eastward from the North.
        """
        from _SKY.Earth import altitude, azimuth, hour_angle
        ra   = self.ra
        decl = self.decl
        ha   = hour_angle (self.time.sidereal_deg, lon, ra)
        alt  = altitude   (decl, ha, lat)
        az   = azimuth    (decl, ha, lat)
        return ha, alt, az
    # end def ha_alt_az

    def __add__ (self, rhs) :
        return self.__class__ (self.day + rhs)
    # end def __add__

    def __sub__ (self, rhs) :
        return self.__class__ (self.day - rhs)
    # end def __sub__

# end class Sun

class RTS_Sun (SKY.RTS) :
    """Model behavior of celestial body for a single day at a specific
       geographical position.

       >>> import _CAL.Date
       >>> s = Sun (CAL.Date (2007, 6, 13))
       >>> rts = RTS_Sun ((s - 1, s, s + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [x.time for x in (rts.rise, rts.transit, rts.set)]
       [Time (4, 53, 41, 617488), Time (12, 54, 26, 688802), Time (20, 55, 49, 329041)]
       >>> print (", ".join ("%s" % x.azimuth for x in (rts.rise, rts.set)))
       053°46'10.29'', 306°17'44.37''

       >>> s = Sun (CAL.Date (2007, 11, 13))
       >>> rts = RTS_Sun ((s - 1, s, s + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [str (x.time) for x in (rts.rise, rts.transit, rts.set)]
       ['06:57:54.736862', '11:38:47.111081', '16:19:21.794159']
       >>> [str (x.time) for x in (rts.civil_twilight_start, rts.civil_twilight_finis)]
       ['06:23:17.703592', '16:54:00.454387']
       >>> [str (x.time) for x in (rts.nautic_twilight_start, rts.nautic_twilight_finis)]
       ['05:43:05.680517', '17:34:14.366819']
       >>> [str (x.time) for x in (rts.astro_twilight_start, rts.astro_twilight_finis)]
       ['05:02:53.657442', '18:14:28.279251']
       >>> print (", ".join ("%s" % x.azimuth for x in (rts.rise, rts.set)))
       117°25'39.35'', 242°24'16.60''


       ### Tests stolen from sunriseset.py
       >>> s = Sun (CAL.Date (2002, 1, 1))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (7, 47, 23, 883358), Time (16, 52, 0, 951961))
       >>> s = Sun (CAL.Date (2002, 3, 30))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (6, 1, 45, 620799), Time (18, 39, 52, 938918))
       >>> s = Sun (CAL.Date (2002, 8, 1))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (6, 6, 41, 19043), Time (20, 38, 24, 434771))
       >>> s = Sun (CAL.Date (2004, 8, 1))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (6, 7, 14, 96321), Time (20, 37, 49, 265441))
       >>> s = Sun (CAL.Date (2000, 6, 21))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 0, 0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (6, 58, 7, 710588), Time (19, 5, 30, 247617))
       >>> s = Sun (CAL.Date (2000, 12, 21))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 0, 0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (5, 54, 30, 62686), Time (18, 2, 1, 95085))

    """

    def __init__ (self, ephs, lat, lon, h0 = Angle_D (-0.8333)) :
        self.__super.__init__ (ephs, lat, lon, h0)
        vars = self.vars
        vars ["h0"]                = Angle_D (-6.0)
        self.civil_twilight_start  = self._Event_ (self.m1, ** vars)
        self.civil_twilight_finis  = self._Event_ (self.m2, ** vars)
        vars ["h0"]                = Angle_D (-12.0)
        self.nautic_twilight_start = self._Event_ (self.m1, ** vars)
        self.nautic_twilight_finis = self._Event_ (self.m2, ** vars)
        vars ["h0"]                = Angle_D (-18.0)
        self.astro_twilight_start  = self._Event_ (self.m1, ** vars)
        self.astro_twilight_finis  = self._Event_ (self.m2, ** vars)
    # end def __init__

    @classmethod
    def On_Day (cls, date, location, h0 = Angle_D (-0.8333)) :
        s = Sun (date)
        return cls \
            ((s - 1, s, s + 1), location.latitude, location.longitude, h0)
    # end def On_Day

# end class RTS_Sun

def _main (cmd) :
    if cmd.latitude and cmd.longitude :
        location = SKY.Location \
            (cmd.latitude, cmd.longitude, cmd.Location or None)
    else :
        location = SKY.Location.Table [cmd.Location]
    print (location, "*" * 20)
    for d in cmd.argv :
        date = CAL.Date.from_string (d)
        rts  = RTS_Sun.On_Day (date, location)
        print \
            ( "Date : %s, Sunrise : %s, transit : %s, sunset : %s"
            % (date, rts.rise, rts.transit, rts.set)
            )
        if cmd.day_length :
            print ("Day length: %02d:%02d" % (rts.day_length).hh_mm)
        if cmd.transit :
            print ("Rise    azimuth : %6.2f degrees" % rts.rise.azimuth.degrees)
            print ("Transit height  : %6.2f degrees" % rts.transit.altitude.degrees)
            print ("Set     azimuth : %6.2f degrees" % rts.set.azimuth.degrees)
        if cmd.civil_twilight :
            print \
                ( "Civil  twilight starts %s, ends %s"
                % (rts.civil_twilight_start, rts.civil_twilight_finis)
                )
        if cmd.nautic_twilight :
            print \
                ( "Nautic twilight starts %s, ends %s"
                % (rts.nautic_twilight_start, rts.nautic_twilight_finis)
                )
        if cmd.astro_twilight :
            print \
                ( "Astro  twilight starts %s, ends %s"
                % (rts.astro_twilight_start, rts.astro_twilight_finis)
                )
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler       = _main
    , args          =
        ( "date:S=%s" % CAL.Date ()
        ,
        )
    , opts          =
        ( "astro_twilight:B?Show astro twilight (-18 degrees below horizon)"
        , "civil_twilight:B?Show civil twilight (-6 degrees below horizon)"
        , "day_length:B?Show length of day in hours"
        , "latitude:F?Latitude (north is positive)"
        , "Location:S=Vienna?Location of observer"
        , "longitude:F?Longitude (negative is east of Greenwich)"
        , "-nautic_twilight:B"
            "?Show time of nautic twilight (sun -12 degrees below horizon)"
        , "-transit:B?Show transit height"
        )
    )

if __name__ != "__main__":
    SKY._Export ("*")
else :
    _Command ()
### __END__ SKY.Sun

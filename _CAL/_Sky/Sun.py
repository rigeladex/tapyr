# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
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
#    CAL.Sky.Sun
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
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _TFL                     import TFL
from   _TGL                     import TGL

from   _TFL._Meta.Once_Property import Once_Property

import _CAL._Sky.Location
import _CAL._Sky.RTS
import _TFL._Meta.Object

from   _TGL.Angle     import Angle_D, Angle_R

class Sun (TFL.Meta.Object) :
    """Model behavior of sun for a single day.

       ### Example 25.a of J. Meeus, p.165
       >>> import _CAL.Date
       >>> s = Sun (CAL.Date (1992, 10, 13))
       >>> s.t
       -0.072183436002737855
       >>> s.geometric_mean_longitude
       Angle_D (201.807196507)
       >>> s.geometric_mean_anomaly
       Angle_D (278.993966432)
       >>> s.eccentriticy_earth_orbit
       0.01671166771493543
       >>> s.equation_of_center
       Angle_D (-1.89732384337)
       >>> s.true_longitude
       Angle_D (199.909872663)
       >>> print s.true_longitude
       199°54'35''
       >>> s.radius_vector
       0.99766195000562929
       >>> s.omega
       Angle_D (264.652582177)
       >>> s.apparent_longitude
       Angle_D (199.90894186)
       >>> print s.apparent_longitude
       199°54'32''
       >>> s.mean_obliquity_ecliptic
       Angle_D (23.4402297955)
       >>> print s.mean_obliquity_ecliptic
       023°26'24''
       >>> s.mean_obliquity_ecliptic.seconds
       24.827263800417541
       >>> s.obliquity_corrected
       Angle_D (23.4399912173)
       >>> s.right_ascension.degrees
       -161.61917478762672
       >>> s.declination.degrees
       -7.7850697960238602
       >>> s.equation_of_time
       13.71101025277024
    """

    ### see J. Meeus, pp. 163f.
    Table = {}

    def __new__ (cls, day) :
        Table = cls.Table
        if day in Table :
            return Table [day]
        self = Table [day] = TFL.Meta.Object.__new__ (cls)
        self._init_ (day)
        return self
    # end def __new__

    def _init_ (self, day) :
        self.day   = day
        self.t     = t = day.JC_J2000
        self.t2    = t2 = t * t
        self.t3    = t * t2
        self.omega = Angle_D (125.04 - 1934.136 * t)
    # end def _init_

    @Once_Property
    def geometric_mean_longitude (self) :
        """Geometric mean longitude of the sun (in degrees)."""
        ### Eq. (25.2)
        return Angle_D.normalized \
            (280.46646 + self.t * 36000.76983 + self.t2 * 0.0003032)
    # end def geometric_mean_longitude

    @Once_Property
    def geometric_mean_anomaly (self) :
        """Geometric mean anomaly of the sun (in degrees)."""
        ### Eq. (25.3)
        return Angle_D.normalized \
            (357.52911 + self.t * 35999.05029 - self.t2 * 0.0001537)
    # end def geometric_mean_anomaly

    @Once_Property
    def eccentriticy_earth_orbit (self) :
        """Eccentricity of earth's orbit (unitless)."""
        ### Eq. (25.4)
        return 0.016708634 - self.t * 0.000042037 - self.t2 * 0.0000001267
    # end def eccentriticy_earth_orbit

    @Once_Property
    def equation_of_center (self) :
        """Equation of center for the sun (in degrees)."""
        m1 = self.geometric_mean_anomaly
        m2 = m1 * 2
        m3 = m1 * 3
        return Angle_D \
            ( m1.sin * (1.914602 - 0.004817 * self.t - 0.000014 * self.t2)
            + m2.sin * (0.019993 - 0.000101 * self.t)
            + m3.sin * (0.000289)
            )
    # end def equation_of_center

    @Once_Property
    def true_longitude (self) :
        """True longitude of the sun (in degrees)."""
        return self.geometric_mean_longitude + self.equation_of_center
    # end def true_longitude

    @Once_Property
    def true_anomaly (self) :
        """True anamoly of the sun (in degrees)."""
        return self.geometric_mean_anomaly   + self.equation_of_center
    # end def true_anomaly

    @Once_Property
    def radius_vector (self) :
        """Distance of earth to the sun (in AU)."""
        ### Eq. (25.5)
        v = self.true_anomaly
        e = self.eccentriticy_earth_orbit
        return (1.000001018 * (1 - e * e)) / (1 + e * v.cos)
    # end def radius_vector

    @Once_Property
    def apparent_longitude (self) :
        """Apparent longitude of the sun (in degrees)."""
        return self.true_longitude - (0.00569 + 0.00478 * self.omega.sin)
    # end def apparent_longitude

    @Once_Property
    def mean_obliquity_ecliptic (self) :
        """Mean obliquity of the ecliptic (in degrees)."""
        ### see J. Meeus, p. 147, Eq. (22.2)
        return \
            ( Angle_D (23, 26, 21.448)
            - Angle_D (seconds = 46.815000) * self.t
            - Angle_D (seconds =  0.000590) * self.t2
            + Angle_D (seconds =  0.001813) * self.t3
            )
    # end def mean_obliquity_ecliptic

    @Once_Property
    def obliquity_corrected (self) :
        """Corrected obliquity of the ecliptic (in degrees)."""
        ### Eq. (25.8)
        return self.mean_obliquity_ecliptic + 0.00256 * self.omega.cos
    # end def obliquity_corrected

    @Once_Property
    def right_ascension (self) :
        """Apparent right ascension of the sun (in degrees)."""
        ### Eq. (25.6), for apparent position
        o = self.obliquity_corrected
        l = self.apparent_longitude
        return Angle_D.atan2 (o.cos * l.sin, l.cos)
    # end def right_ascension

    @Once_Property
    def declination (self) :
        """Apparent declination of the sun (in degrees)."""
        ### Eq. (25.7), for apparent position
        o = self.obliquity_corrected
        l = self.apparent_longitude
        return Angle_D.asin (o.sin * l.sin)
    # end def declination

    @Once_Property
    def equation_of_time (self) :
        """Difference between true solar time and mean solar time
           (in minutes).
        """
        ### see J. Meeus, p. 185, Eq. (28.3)
        e      = self.eccentriticy_earth_orbit
        l2     = self.geometric_mean_longitude * 2
        l4     = l2 * 2
        m1     = self.geometric_mean_anomaly
        m2     = m1 * 2
        o_half = self.mean_obliquity_ecliptic / 2
        y      = o_half.tan ** 2
        return Angle_R \
            (        y     * l2.sin
            - 2.00 * e     * m1.sin
            + 4.00 * e * y * m1.sin * l2.cos
            - 0.50 * y * y * l4.sin
            - 1.25 * e * e * m2.sin
            ).degrees * 4.0
    # end def equation_of_time

    def __add__ (self, rhs) :
        return self.__class__ (self.day + rhs)
    # end def __add__

    def __sub__ (self, rhs) :
        return self.__class__ (self.day - rhs)
    # end def __sub__

# end class Sun

class RTS_Sun (CAL.Sky.RTS) :
    """Model behavior of celestial body for a single day at a specific
       geographical position.

       >>> import _CAL.Date
       >>> s = Sun (CAL.Date (2007, 6, 13))
       >>> rts = RTS_Sun ((s - 1, s, s + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [x.time for x in (rts.rise, rts.transit, rts.set)]
       [Time (3, 53, 41, 641), Time (11, 54, 26, 712), Time (19, 55, 49, 352)]
       >>> s = Sun (CAL.Date (2007, 11, 13))
       >>> rts = RTS_Sun ((s - 1, s, s + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [str (x.time) for x in (rts.rise, rts.transit, rts.set)]
       ['06:57:54.000773', '11:38:47.000148', '16:19:21.000831']
       >>> [str (x.time) for x in (rts.civil_twilight_start, rts.civil_twilight_finis)]
       ['06:23:17.000740', '16:54:00.000491']
       >>> [str (x.time) for x in (rts.nautic_twilight_start, rts.nautic_twilight_finis)]
       ['05:43:05.000717', '17:34:14.000403']
       >>> [str (x.time) for x in (rts.astro_twilight_start, rts.astro_twilight_finis)]
       ['05:02:53.000694', '18:14:28.000316']

       ### Tests stolen from sunriseset.py
       >>> s = Sun (CAL.Date (2002, 1, 1))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (7, 47, 23, 812), Time (16, 52, 0, 881))
       >>> s = Sun (CAL.Date (2002, 3, 30))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (6, 1, 45, 552), Time (18, 39, 52, 870))
       >>> s = Sun (CAL.Date (2002, 8, 1))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (5, 6, 40, 945), Time (19, 38, 24, 361))
       >>> s = Sun (CAL.Date (2004, 8, 1))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 43.0, 79.0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (5, 7, 14, 51), Time (19, 37, 49, 220))
       >>> s = Sun (CAL.Date (2000, 6, 21))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 0, 0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (5, 58, 7, 648), Time (18, 5, 30, 185))
       >>> s = Sun (CAL.Date (2000, 12, 21))
       >>> rts = RTS_Sun ((s - 1, s, s + 1), 0, 0, -0.8333)
       >>> rts.rise.time, rts.set.time
       (Time (5, 54, 29, 994), Time (18, 2, 1, 26))
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

def command_spec (arg_array = None) :
    from   _TFL.Command_Line import Command_Line
    import _CAL.Date
    return Command_Line \
        ( arg_spec    =
            ( "date:S=%s" % CAL.Date ()
            ,
            )
        , option_spec =
            ( "astro_twilight:B?Show astro twilight (-18 degrees below horizon)"
            , "civil_twilight:B?Show civil twilight (-6 degrees below horizon)"
            , "latitude:F=48.2333333333?Latitude (north is positive)"
            , "longitude:F=-16.3333333333"
                "?Longitude (negative is east of Greenwich)"
            , "-nautic_twilight:B"
                "?Show time of nautic twilight (sun -12 degrees below horizon)"
            )
        , arg_array   = arg_array
        )
# end def command_spec

def main (cmd) :
    date = CAL.Date.from_string (cmd.date)
    rts  = RTS_Sun.On_Day (date, CAL.Sky.Location (cmd.latitude, cmd.longitude))
    print "Sunrise : %s, transit : %s, sunset : %s" % \
        (rts.rise, rts.transit, rts.set)
    if cmd.civil_twilight :
        print "Civil  twilight starts %s, ends %s" % \
            (rts.civil_twilight_start, rts.civil_twilight_finis)
    if cmd.nautic_twilight :
        print "Nautic twilight starts %s, ends %s" % \
            (rts.nautic_twilight_start, rts.nautic_twilight_finis)
    if cmd.astro_twilight :
        print "Astro  twilight starts %s, ends %s" % \
            (rts.astro_twilight_start, rts.astro_twilight_finis)
# end def main

if __name__ == "__main__":
    main (command_spec ())
else :
    CAL.Sky._Export ("*")
### __END__ CAL.Sky.Sun

"""
from _CAL._Sky.Sun import *
import _CAL.Date
s = Sun (CAL.Date (2007, 6, 13))
rts = RTS_Sun ((s - 1, s, s + 1), Angle_D (48, 14), Angle_D (-16, -20))
[str (x.time) for x in (rts.rise, rts.transit, rts.set)]
[str (x.time) for x in (rts.civil_twilight_start, rts.civil_twilight_finis)]
[str (x.time) for x in (rts.nautic_twilight_start, rts.nautic_twilight_finis)]
[str (x.time) for x in (rts.astro_twilight_start, rts.astro_twilight_finis)]
"""

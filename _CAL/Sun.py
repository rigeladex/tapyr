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
#    CAL.Sun
#
# Purpose
#    Provide time of sunrise, transit and sunset
#
# References
#    http://www.srrb.noaa.gov/highlights/sunrise/program.txt
#
# Revision Dates
#     8-Nov-2007 (CT) Creation
#    11-Nov-2007 (CT) Creation continued
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _TFL                     import TFL
from   _TGL                     import TGL

from   _TFL._Meta.Once_Property import Once_Property

import _CAL.Date_Time
import _CAL.Time
import _TFL._Meta.Object
import _TFL.Accessor
import _TGL._DRA.Interpolator

from   _TFL.Math_Func import sign
from   _TGL.Angle     import Angle_D, Angle_R

from   math import \
    ( acos
    , asin
    , atan2
    , cos
    , degrees
    , radians
    , sin
    , tan
    )
import math

class Sun_D (TFL.Meta.Object) :
    """Model behavior of sun for a single day.

       Example 25.a of J. Meeus, ISBN 0-943396-61-1, p.165
       >>> sd = Sun_D (CAL.Date (1992, 10, 13))
       >>> sd.t
       -0.072183436002737855
       >>> sd.geometric_mean_longitude
       Angle_D (201.807196507)
       >>> sd.geometric_mean_anomaly
       Angle_D (278.993966432)
       >>> sd.eccentriticy_earth_orbit
       0.01671166771493543
       >>> sd.equation_of_center
       Angle_D (-1.89732384337)
       >>> sd.true_longitude
       Angle_D (199.909872663)
       >>> print sd.true_longitude
       199°54'35''
       >>> sd.radius_vector
       0.99766195000562929
       >>> sd.omega
       Angle_D (264.652582177)
       >>> sd.apparent_longitude
       Angle_D (199.90894186)
       >>> print sd.apparent_longitude
       199°54'32''
       >>> sd.mean_obliquity_ecliptic
       Angle_D (23.4402297955)
       >>> print sd.mean_obliquity_ecliptic
       023°26'24''
       >>> sd.mean_obliquity_ecliptic.seconds
       24.827263800417541
       >>> sd.obliquity_corrected
       Angle_D (23.4399912173)
       >>> sd.right_ascension.degrees
       -161.61917478762672
       >>> sd.declination.degrees
       -7.7850697960238602
       >>> sd.equation_of_time
       13.71101025277024
    """

    ### see J. Meeus, ISBN 0-943396-61-1, pp. 163f.
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
        ### see J. Meeus, ISBN 0-943396-61-1, p. 147, Eq. (22.2)
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
        ### see J. Meeus, ISBN 0-943396-61-1, p. 185, Eq. (28.3)
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

# end class Sun_D

class Sun_P (TFL.Meta.Object) :
    """Model behavior of sun for a single day at a specific geographical
       position.
    """

    ### see J. Meeus, ISBN 0-943396-61-1, pp. 101-104

    def __init__ (self, ephs, lat, lon, h0 = Angle_D (-0.8333)) :
        self.ephs  = ephs
        self.lat   = lat   = Angle_D (getattr (lat, "degrees", lat))
        self.lon   = lon   = Angle_D (getattr (lon, "degrees", lon))
        self.h0    = h0    = Angle_D (getattr (h0,  "degrees", h0))
        self.day   = day   = ephs [0].day
        self.alpha = alpha = ephs [0].right_ascension
        self.delta = delta = ephs [0].declination
        self.sid   = sid   = Angle_D (day.sidereal_time_deg)
        self.H0    = H0    = Angle_D.acos \
            ((h0.sin - lat.sin * delta.sin) / (lat.cos * delta.cos))
        self.m0    = m0    = (float (alpha + lon - sid) / 360.) % 1.0
        self.m1    = (m0 - H0.degrees / 360.) % 1.0
        self.m2    = (m0 + H0.degrees / 360.) % 1.0
    # end def __init__

    @Once_Property
    def interpolator_a (self) :
        ephs = self.ephs
        return TGL.DRA.Interpolator_3 \
            ( (-1, ephs [0])
            , ( 0, ephs [1])
            , (+1, ephs [2])
            , y_getter = TFL.Getter [1].right_ascension.radians
            )
    # end def interpolator_a

    @Once_Property
    def interpolator_d (self) :
        ephs = self.ephs
        return TGL.DRA.Interpolator_3 \
            ( (-1, ephs [0])
            , ( 0, ephs [1])
            , (+1, ephs [2])
            , y_getter = TFL.Getter [1].declination.radians
            )
    # end def interpolator_d

    @Once_Property
    def rise_time (self) :
        return self._to_local_time (self.rise_time_ut)
    # end def rise_time

    @Once_Property
    def rise_time_ut (self) :
        m       = self.m1
        delta_m = self._delta_m (m)
        return self._to_ut (m, delta_m)
    # end def rise_time_ut

    @Once_Property
    def transit_time (self) :
        return self._to_local_time (self.transit_time_ut)
    # end def transit_time

    @Once_Property
    def transit_time_ut (self) :
        m                     = self.m0
        ha, dec, alt          = self._at_time (m)
        delta_m               = (ha.degrees - 180.) / 360.0
        self.transit_altitude = alt
        return self._to_ut (m, delta_m)
    # end def transit_time_ut

    @Once_Property
    def set_time (self) :
        return self._to_local_time (self.set_time_ut)
    # end def set_time

    @Once_Property
    def set_time_ut (self) :
        m       = self.m2
        delta_m = self._delta_m (m)
        return self._to_ut (m, delta_m)
    # end def set_time_ut

    def _at_time (self, m) :
        sid      = Angle_D.normalized (self.sid.degrees + 360.985647 * m)
        n        = m + self.day.delta_T / 86400.0
        alpha    = Angle_R (self.interpolator_a (n))
        delta    = Angle_R (self.interpolator_d (n))
        ha       = Angle_D.normalized ((sid - self.lon - alpha).degrees)
        lat      = self.lat
        altitude = Angle_R.asin \
            (lat.sin * delta.sin + lat.cos * delta.cos * ha.cos)
        return ha, delta, altitude
    # end def _at_time

    def _delta_m (self, m) :
        ha, dec, alt = self._at_time (m)
        return \
            ( (alt - self.h0).degrees % 360.0
            / (360.0 * dec.cos * self.lat.cos * ha.sin)
            )
    # end def _delta_m

    def _to_local_time (self, hours_ut) :
        lon         = self.lon.degrees
        hours_local = \
            ( hours_ut
            + ( sign (lon)
              * (CAL.Time.from_degrees (abs (lon)).seconds / 3600.0)
              )
            ) % 24.0
        return CAL.Time.from_decimal_hours (hours_local)
    # end def _to_local_time

    def _to_ut (self, m, delta_m) :
        return ((m + delta_m) * 24) % 24.0
    # end def _to_ut

# end class Sun_P

"""
from _CAL.Sun import *
sd = Sun_D (CAL.Date (2007, 11, 12))
sp = Sun_P ((sd - 1, sd, sd + 1), 48.190111, -16.26867)


from _CAL.Sun import *
from _TFL.Record import Record
d  = CAL.Date (1988, 3, 20)
sp = Sun_P \
    ( ( Record
          ( day = d - 1
          , right_ascension = Angle_D (40.68021)
          , declination     = Angle_D (18.04761)
          )
      , Record
          ( day = d
          , right_ascension = Angle_D (41.73129)
          , declination     = Angle_D (18.44092)
          )
      , Record
          ( day = d + 1
          , right_ascension = Angle_D (42.78204)
          , declination     = Angle_D (18.82742)
          )
      )
      , lat = Angle_D (42.3333)
      , lon = Angle_D (71.0833)
      , h0  = Angle_D (-0.5667)
    )
sp.rise_time_ut, sp.transit_time_ut, sp.set_time_ut
"""
### __END__ CAL.Sun

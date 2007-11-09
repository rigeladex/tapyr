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
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _CAL.Date_Time
import _TFL._Meta.Object

from   math import \
    ( asin
    , atan2
    , cos
    , degrees
    , radians
    , sin
    , tan
    )
import math

class Sun_D (TFL.Meta.Object) :
    """Model behavior of sun for a single day."""

    def __init__ (self, day) :
        self.day   = day
        self.jc    = day.JC_J2000
        self.omega = radians (125.04 - 1934.136 * self.jc)
    # end def __init__

    @Once_Property
    def geometric_mean_longitude (self) :
        """Geometric mean longitude of the sun (in degrees)."""
        t = self.jc
        result = 280.46646 + t * (36000.76983 + 0.0003032 * t)
        return result % 360
    # end def geometric_mean_longitude

    @Once_Property
    def geometric_mean_anomaly (self) :
        """Geometric mean anomaly of the sun (in degrees)."""
        t = self.jc
        return 357.52911 + t * (35999.05029 - 0.0001537 * t)
    # end def geometric_mean_anomaly

    @Once_Property
    def eccentriticy_earth_orbit (self) :
        """Eccentricity of earth's orbit (unitless)."""
        t = self.jc
        return 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    # end def eccentriticy_earth_orbit

    @Once_Property
    def equation_of_center (self) :
        """Equation of center for the sun (in degrees)."""
        m      = radians (self.geometric_mean_anomaly)
        sin_1m = sin (m)
        sin_2m = sin (m * 2)
        sin_3m = sin (m * 3)
        t      = self.jc
        return \
            ( sin_1m * (1.914602 - (0.004817 + 0.000014 * t) * t)
            + sin_2m * (0.019993 - (0.000101) * t)
            + sin_3m * (0.000289)
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
        return self.geometric_mean_anomaly + self.equation_of_center
    # end def true_anomaly

    @Once_Property
    def radius_vector (self) :
        """Distance of earth to the sun (in AU)."""
        v = self.true_anomaly
        e = self.eccentriticy_earth_orbit
        return (1.000001018 * (1 - e * e)) / (1 + e * cos (radians (v)))
    # end def radius_vector

    @Once_Property
    def apparent_longitude (self) :
        """Apparent longitude of the sun (in degrees)."""
        return self.true_longitude - 0.00569 - 0.00478 * sin (self.omega)
    # end def apparent_longitude

    @Once_Property
    def mean_obliquity_ecliptic (self) :
        """Mean obliquity of the ecliptic (in degrees)."""
        t       = self.jc
        seconds = 21.448 - t * (46.8150 + t * (0.00059 - t * 0.001813))
        return 23.0 + (26.0 + (seconds / 60.0)) / 60.0
    # end def mean_obliquity_ecliptic

    @Once_Property
    def obliquity_corrected (self) :
        """Corrected obliquity of the ecliptic (in degrees)."""
        return self.mean_obliquity_ecliptic + 0.00256 * cos (self.omega)
    # end def obliquity_corrected

    @Once_Property
    def right_ascension (self) :
        """Right ascension of the sun (in degrees)."""
        o = radians (self.obliquity_corrected)
        l = radians (self.apparent_longitude)
        return degrees (atan2 (sin (l) * cos (o), cos (l)))
    # end def right_ascension

    @Once_Property
    def declination (self) :
        """Declination of the sun (in degrees)."""
        o = radians (self.obliquity_corrected)
        l = radians (self.apparent_longitude)
        return degrees (asin (sin (o) * sin (l)))
    # end def declination

    @Once_Property
    def equation_of_time (self) :
        """Difference between true solar time and mean solar time
           (in minutes).
        """
        e      = self.eccentriticy_earth_orbit
        l      = self.geometric_mean_longitude
        m      = radians (self.geometric_mean_anomaly)
        o      = radians (self.obliquity_corrected)
        y      = tan     (o / 2)
        y     *= y
        cos_2l = cos (l * 2)
        sin_2l = sin (l * 2)
        sin_4l = sin (l * 4)
        sin_1m = sin (m)
        sin_2m = sin (m * 2)
        return degrees \
            (        y     * sin_2l
            - 2.00 * e     * sin_1m
            + 4.00 * e * y * sin_1m * cos_2l
            - 0.50 * y * y * sin_4l
            - 1.25 * e * e * sin_2m
            ) * 4.0
    # end def equation_of_time

# end class Sun_D

### __END__ CAL.Sun

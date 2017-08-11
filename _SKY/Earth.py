# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    SKY.Earth
#
# Purpose
#    Provide earth-related astronomical formulas
#
# References
#    J. Meeus, Astronomical Algorithms, 2nd edition, 1998, ISBN 0-943396-61-1
#
# Revision Dates
#    26-Sep-2016 (CT) Creation
#    27-Sep-2016 (CT) Add `altitude`, `azimuth`, and `hour_angle`
#     9-Oct-2016 (CT) Move out from `CAL` to toplevel package
#     9-Aug-2017 (CT) Use one argument `loc`, not two arguments `lat` and `lon`
#                     + Use `loc.longitude_meuss`
#    11-Aug-2017 (CT) Rename `solar_intensity` to `solar_irradiance`
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
### from   __future__  import unicode_literals ### breaks doctest

from   _CAL                       import CAL
from   _SKY                       import SKY
from   _TFL                       import TFL

import _CAL.Date_Time

import _SKY.Location

from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL.Angle                 import Angle_D, Angle_R
from   _TFL.Decorator             import Attributed
from   _TFL.portable_repr         import portable_repr

import _TFL._Meta.Object

def air_mass (altitude) :
    """Air mass coefficient due to atmospheric extinction for `altitude`.

       >>> for alt in (90, 30, 20, 15, 10, 5, 2, 0) :
       ...     print ("z = %2d° --> AM = %4.1f" % (90-alt, air_mass (alt)))
       z =  0° --> AM =  1.0
       z = 60° --> AM =  2.0
       z = 70° --> AM =  2.9
       z = 75° --> AM =  3.8
       z = 80° --> AM =  5.6
       z = 85° --> AM = 10.3
       z = 88° --> AM = 19.4
       z = 90° --> AM = 37.9

       https://en.wikipedia.org/wiki/Air_mass_(solar_energy), formula A.2
    """
    z      = Angle_D (90) - altitude
    result = 1.0 / (z.cos + 0.50572 * ((96.07995 - z.degrees) ** -1.6364))
    return result
# end def air_mass

def altitude (decl, ha, loc) :
    """Altitude of a celestial body with declination `decl` and hour angle `ha`
       for location `loc`.
    """
    ### J. Meeus, p. 93, Eq. (13.6)
    lat  = loc.latitude
    return Angle_R.asin \
        (lat.sin * decl.sin + lat.cos * decl.cos * ha.cos)
# end def altitude

def azimuth (decl, ha, loc) :
    """Azimuth of a celestial body with declination `decl` and hour angle `ha`
       for location `loc`.

       Azimuth is measured eastward from the North.
    """
    ### J. Meeus, p. 93, Eq. (13.5)
    lat      = loc.latitude
    tan_A    = \
        ( ha.sin
        / (ha.cos * lat.sin - decl.tan * lat.cos)
        )
    result   = Angle_D.normalized (Angle_R.atan (tan_A).degrees)
    corr     = 0
    if   ha < 0 and result > 180 :
        corr = Angle_D (-180) ### ha < 0 --> E of meridian
    elif ha > 0 and result < 180 :
        corr = Angle_D (+180) ### ha > 0 --> W of meridian
    result  += corr
    return Angle_D.normalized (result.degrees)
# end def azimuth

def hour_angle (sid_UT, loc, ra) :
    """Hour angle for sidereal_time `sid_UT`, location `loc`, and
       right ascension `ra`.

       `sid_UT` and `ra` must be Angle_D/Angle_R instances.
    """
    ### J. Meeus, p. 92
    lon = loc.longitude_meuss
    ha  = (sid_UT - lon - ra).degrees
    if abs (ha) >= 360.0 :
        ha = ha % 360.0
    if ha > 180.0 :
        ha -= 360.0
    elif ha < -180.0 :
        ha += 360.0
    return Angle_D (ha)
# end def hour_angle

@Attributed (in_orbit = 1353.0, in_zenith = 1040.0)
def solar_irradiance (air_mass, above_sealevel = 0) :
    """Solar irradiance for `air_mass` considering atmospheric extinction.

       air_mass == 0 : irradiance in orbit
       air_mass == 1 : irradiance for sun in zenith
       air_mass == 2 : irradiance for sun at altitude == 30°

       >>> for am in (0, 1, 1.09, 1.15, 1.41, 1.5, 2, 2.9, 3.8, 5.6, 10, 38) :
       ...     I = solar_irradiance (am)
       ...     print ("AM %5.2f @ sea level : %4.0f W/sqm" % (am, I))
       AM  0.00 @ sea level : 1353 W/sqm
       AM  1.00 @ sea level : 1040 W/sqm
       AM  1.09 @ sea level : 1020 W/sqm
       AM  1.15 @ sea level : 1010 W/sqm
       AM  1.41 @ sea level :  950 W/sqm
       AM  1.50 @ sea level :  930 W/sqm
       AM  2.00 @ sea level :  840 W/sqm
       AM  2.90 @ sea level :  710 W/sqm
       AM  3.80 @ sea level :  620 W/sqm
       AM  5.60 @ sea level :  470 W/sqm
       AM 10.00 @ sea level :  270 W/sqm
       AM 38.00 @ sea level :   20 W/sqm

       >>> for h in (45, 200, 800, 2000) :
       ...   for am in (0, 1, 1.09, 1.15, 1.41, 1.5, 2, 2.9, 3.8, 5.6, 10, 38) :
       ...     I = solar_irradiance (am, h)
       ...     print ("AM %5.2f @ %4d m : %4.0f W/sqm" % (am, h, I))
       AM  0.00 @   45 m : 1353 W/sqm
       AM  1.00 @   45 m : 1040 W/sqm
       AM  1.09 @   45 m : 1020 W/sqm
       AM  1.15 @   45 m : 1010 W/sqm
       AM  1.41 @   45 m :  950 W/sqm
       AM  1.50 @   45 m :  930 W/sqm
       AM  2.00 @   45 m :  850 W/sqm
       AM  2.90 @   45 m :  720 W/sqm
       AM  3.80 @   45 m :  620 W/sqm
       AM  5.60 @   45 m :  480 W/sqm
       AM 10.00 @   45 m :  280 W/sqm
       AM 38.00 @   45 m :   30 W/sqm
       AM  0.00 @  200 m : 1353 W/sqm
       AM  1.00 @  200 m : 1050 W/sqm
       AM  1.09 @  200 m : 1030 W/sqm
       AM  1.15 @  200 m : 1020 W/sqm
       AM  1.41 @  200 m :  960 W/sqm
       AM  1.50 @  200 m :  950 W/sqm
       AM  2.00 @  200 m :  860 W/sqm
       AM  2.90 @  200 m :  740 W/sqm
       AM  3.80 @  200 m :  640 W/sqm
       AM  5.60 @  200 m :  500 W/sqm
       AM 10.00 @  200 m :  310 W/sqm
       AM 38.00 @  200 m :   60 W/sqm
       AM  0.00 @  800 m : 1353 W/sqm
       AM  1.00 @  800 m : 1090 W/sqm
       AM  1.09 @  800 m : 1070 W/sqm
       AM  1.15 @  800 m : 1060 W/sqm
       AM  1.41 @  800 m : 1010 W/sqm
       AM  1.50 @  800 m :  990 W/sqm
       AM  2.00 @  800 m :  910 W/sqm
       AM  2.90 @  800 m :  800 W/sqm
       AM  3.80 @  800 m :  710 W/sqm
       AM  5.60 @  800 m :  590 W/sqm
       AM 10.00 @  800 m :  410 W/sqm
       AM 38.00 @  800 m :  190 W/sqm
       AM  0.00 @ 2000 m : 1353 W/sqm
       AM  1.00 @ 2000 m : 1170 W/sqm
       AM  1.09 @ 2000 m : 1150 W/sqm
       AM  1.15 @ 2000 m : 1140 W/sqm
       AM  1.41 @ 2000 m : 1100 W/sqm
       AM  1.50 @ 2000 m : 1090 W/sqm
       AM  2.00 @ 2000 m : 1020 W/sqm
       AM  2.90 @ 2000 m :  930 W/sqm
       AM  3.80 @ 2000 m :  860 W/sqm
       AM  5.60 @ 2000 m :  760 W/sqm
       AM 10.00 @ 2000 m :  610 W/sqm
       AM 38.00 @ 2000 m :  440 W/sqm

       https://en.wikipedia.org/wiki/Air_mass_(solar_energy), formulas I.1, I.2
    """
    I0 = solar_irradiance.in_orbit
    if air_mass == 0 :
        result = I0
    else :
        I0 *= 1.1
        hf  = (above_sealevel / 1000.0) / 7.1
        if above_sealevel == 0 :
            I = (I0 * (0.7 ** air_mass ** 0.678))
        else :
            I = (I0 * (((1 - hf) * 0.7 ** air_mass ** 0.678) + hf))
        result = round (I / 10.0) * 10.0
    return result
# end def solar_irradiance

class Time (TFL.Meta.Object) :
    """Model astronomical time for a single Date.

    ### Example 12.a of J. Meeus, p. 88
    >>> date = CAL.Date (1987, 4, 10)
    >>> xa   = Time (date)
    >>> print (portable_repr (xa.t))
    -0.127296372348

    >>> print (xa.mean_sidereal_time)
    13:10:46.366826
    >>> print (xa.sidereal_time)
    13:10:46.357311

    ### Example 12.b of J. Meeus, p. 89
    >>> dt  = CAL.Date_Time (1987, 4, 10, 19, 21, 0)
    >>> xb  = Time (dt)
    >>> print (portable_repr (xb.t))
    -0.127274298426

    >>> print (xb.mean_sidereal_time)
    08:34:57.089579

    """

    time = CAL.Time (0)

    def __init__ (self, date) :
        """`date` must be in UT."""
        if isinstance (date, CAL.Date_Time) :
            self.time      = date.as_time ()
        self.date          = date
        self.JC_2k         = self.t  = t  = date.JC_J2000
        self.JC_2k_squared = self.t2 = t2 = t * t
        self.JC_2k_cubed   = self.t3      = t * t2
    # end def __init__

    @Once_Property
    def eccentriticy_earth_orbit (self) :
        """Eccentricity of earth's orbit (unitless)."""
        ### Eq. (25.4)
        return 0.016708634 - self.t * 0.000042037 - self.t2 * 0.0000001267
    # end def eccentriticy_earth_orbit

    @Once_Property
    def geometric_mean_anomaly_sun (self) :
        """Geometric mean anomaly of the sun (in degrees)."""
        ### Eq. (25.3)
        return Angle_D.normalized \
            (357.52911 + self.t * 35999.05029 - self.t2 * 0.0001537)
    # end def geometric_mean_anomaly_sun

    @Once_Property
    def geometric_mean_longitude_moon (self) :
        """Geometric mean longitude of the moon (in degrees)."""
        ### see J. Meeus, p. 144;
        return Angle_D.normalized \
            (218.3165 + self.t * 481267.8813)
    # end def geometric_mean_longitude_moon

    @Once_Property
    def geometric_mean_longitude_sun (self) :
        """Geometric mean longitude of the sun (in degrees)."""
        ### see J. Meeus, p. 144; Eq. (25.2)
        return Angle_D.normalized \
            ( 280.46646
            + self.t * 36000.76983
            + self.t2 * 0.0003032
            )
    # end def geometric_mean_longitude_sun

    @Once_Property
    def longitude_ascending_node_moon (self) :
        """Longitude of the (mean) ascending node of the moon's orbit on the
           ecliptic.
        """
        ### see J. Meeus, p. 144; p.343, Eq. (47.7)
        return Angle_D \
            ( 125.04452
            - self.t  * 1934.136261
            + self.t2 * 0.0020708
            + self.t3 / 450000.0
            )
    # end def longitude_ascending_node_moon

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
    def mean_sidereal_deg (self) :
        """Mean sidereal time at `self.date` and `self.time` in degrees."""
        seconds = self.time.seconds
        if seconds == 0 :
            ### J. Meeus, eq. (12.3), p. 87
            result = 100.46061837 + 36000.770053608 * self.t
        else :
            ### J. Meeus, eq. (12.4), p. 88
            result = \
                ( 280.46061837
                + 360.98564736629 * (self.date.JD - 2451545.0)
                )
        ### J. Meeus, eq. (12.3 + 12.4), p. 87
        result += 0.000387933 * self.t2 - self.t3 / 38710000.0
        return result % 360.0
    # end def mean_sidereal_deg

    @Once_Property
    def mean_sidereal_time (self) :
        """Mean sidereal time at `self.date` and `self.time`."""
        return CAL.Time.from_degrees (self.mean_sidereal_deg)
    # end def mean_sidereal_time

    @Once_Property
    def nutation_longitude (self) :
        """Nutation in longitude (delta-phi)."""
        ### see J. Meeus, pp. 143–4
        omega  = self.longitude_ascending_node_moon
        om_2   = omega * 2
        ls_2   = self.geometric_mean_longitude_sun  * 2
        lm_2   = self.geometric_mean_longitude_moon * 2
        result = \
            ( Angle_D (seconds = -17.20) * omega.sin
            - Angle_D (seconds = - 1.32) * ls_2.sin
            - Angle_D (seconds =   0.23) * lm_2.sin
            + Angle_D (seconds =   0.21) * om_2.sin
            )
        return result
    # end def nutation_longitude

    @Once_Property
    def nutation_obliquity (self) :
        """Nutation in obliquity (delta-epsilon)."""
        ### see J. Meeus, pp. 143–4
        omega  = self.longitude_ascending_node_moon
        om_2   = omega * 2
        ls_2   = self.geometric_mean_longitude_sun  * 2
        lm_2   = self.geometric_mean_longitude_moon * 2
        result = \
            ( Angle_D (seconds =   9.20) * omega.cos
            + Angle_D (seconds =   0.57) * ls_2.cos
            + Angle_D (seconds =   0.10) * lm_2.cos
            - Angle_D (seconds =   0.09) * om_2.cos
            )
        return result
    # end def nutation_obliquity

    @Once_Property
    def obliquity_corrected (self) :
        """Corrected obliquity of the ecliptic (in degrees)."""
        ### Eq. (25.8)
        return \
            ( self.mean_obliquity_ecliptic
            + 0.00256 * self.longitude_ascending_node_moon.cos
            )
    # end def obliquity_corrected

    @Once_Property
    def sidereal_deg (self) :
        """Apparent sidereal time at `self.date` and `self.time` in degrees."""
        ### see J. Meeus, p. 95
        result = \
            ( Angle_D.normalized (self.mean_sidereal_deg)
            + (self.nutation_longitude / 15) * self.obliquity_corrected.cos
            )
        return result
    # end def sidereal_deg

    @Once_Property
    def sidereal_time (self) :
        """Apparent sidereal time at `self.date` and `self.time`."""
        return CAL.Time.from_degrees (self.sidereal_deg)
    # end def sidereal_time

# end class Time

__doc__ = r"""
Example 13.b of J. Meeus, p.95, Venus at Washington


    >>> d     = CAL.Date_Time (1987, 4, 10, 19, 21)
    >>> loc   = SKY.Location (Angle_D (38, 55, 17), - Angle_D (77,  3, 56))
    >>> ra    = Angle_D.normalized (Angle_D (23*15, 9*15, 16.641*15))
    >>> decl  = Angle_D (-6, 43, 11.61)
    >>> time  = Time (d)
    >>> ha    = hour_angle (time.sidereal_deg, loc, ra)

    >>> print (time.mean_sidereal_time)
    08:34:57.089579

    >>> print (time.nutation_longitude)
    -000°00'02.36''

    >>> print (time.obliquity_corrected, portable_repr (time.obliquity_corrected.cos))
    023°26'36.45'' 0.917453135383

    >>> print (time.sidereal_time)
    08:34:57.079969

    >>> ha
    Angle_D (64.3529401502)

    >>> Angle_D (altitude (decl, ha, loc).degrees)
    Angle_D (16.1109801199)

    >>> azimuth  (decl, ha, loc)
    Angle_D (249.12301149)

Example 22.a of J. Meeus, p.148

    >>> d     = CAL.Date_Time (1987, 4, 10)
    >>> time  = Time (d)

    >>> print (portable_repr (time.t))
    -0.127296372348

    >>> time.geometric_mean_anomaly_sun
    Angle_D (94.9805976297)

    >>> time.longitude_ascending_node_moon
    Angle_D (371.253083203)

    >>> print (time.geometric_mean_longitude_moon)
    154°39'39.90''

    >>> print (time.geometric_mean_longitude_sun)
    017°41'56.63''

    >>> print (time.nutation_longitude)
    -000°00'02.33''

    >>> print (time.nutation_obliquity)
    000°00'09.47''

    >>> print (time.mean_obliquity_ecliptic)
    023°26'27.41''

    >>> print (time.mean_obliquity_ecliptic + time.nutation_obliquity)
    023°26'36.88''

"""

if __name__ != "__main__" :
    SKY._Export_Module ()
### __END__ SKY.Earth

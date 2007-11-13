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
#    13-Nov-2007 (CT) Creation continued..
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

from   _TFL.predicate import rounded_to
from   _TGL.Angle     import Angle_D, Angle_R

class Sun_D (TFL.Meta.Object) :
    """Model behavior of sun for a single day.

       ### Example 25.a of J. Meeus, ISBN 0-943396-61-1, p.165
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

       >>> sd = Sun_D (CAL.Date (2007, 6, 13))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [x.time for x in (sp.rise, sp.transit, sp.set)]
       [Time (3, 53, 41, 641), Time (11, 54, 26, 712), Time (19, 55, 49, 352)]
       >>> sd = Sun_D (CAL.Date (2007, 11, 13))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [str (x.time) for x in (sp.rise, sp.transit, sp.set)]
       ['06:57:54.000773', '11:38:47.000148', '16:19:21.000831']
       >>> print sp.civil_twilight_start.time, sp.civil_twilight_finis.time
       06:17:42.000750 16:59:35.000743
       >>> print sp.nautic_twilight_start.time, sp.nautic_twilight_finis.time
       05:37:30.000727 17:39:49.000655
       >>> print sp.astro_twilight_start.time, sp.astro_twilight_finis.time
       04:57:18.000704 18:20:03.000568

       ### Tests stolen from sunriseset.py
       >>> sd = Sun_D (CAL.Date (2002, 1, 1))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1), 43.0, 79.0, -0.8333)
       >>> sp.rise.time, sp.set.time
       (Time (7, 47, 23, 812), Time (16, 52, 0, 881))
       >>> sd = Sun_D (CAL.Date (2002, 3, 30))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1), 43.0, 79.0, -0.8333)
       >>> sp.rise.time, sp.set.time
       (Time (6, 1, 45, 552), Time (18, 39, 52, 870))
       >>> sd = Sun_D (CAL.Date (2002, 8, 1))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1), 43.0, 79.0, -0.8333)
       >>> sp.rise.time, sp.set.time
       (Time (5, 6, 40, 945), Time (19, 38, 24, 361))
       >>> sd = Sun_D (CAL.Date (2004, 8, 1))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1), 43.0, 79.0, -0.8333)
       >>> sp.rise.time, sp.set.time
       (Time (5, 7, 14, 51), Time (19, 37, 49, 220))
       >>> sd = Sun_D (CAL.Date (2000, 6, 21))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1), 0, 0, -0.8333)
       >>> sp.rise.time, sp.set.time
       (Time (5, 58, 7, 648), Time (18, 5, 30, 185))
       >>> sd = Sun_D (CAL.Date (2000, 12, 21))
       >>> sp = Sun_P ((sd - 1, sd, sd + 1), 0, 0, -0.8333)
       >>> sp.rise.time, sp.set.time
       (Time (5, 54, 29, 994), Time (18, 2, 1, 26))

       ### Example 15.a of J. Meeus, ISBN 0-943396-61-1, pp.103-104
       >>> from _TFL.Record import Record
       >>> d  = CAL.Date (1988, 3, 20)
       >>> sp = Sun_P ( ( Record
       ...           ( day = d - 1
       ...           , right_ascension = Angle_D (40.68021)
       ...           , declination     = Angle_D (18.04761)
       ...           )
       ...       , Record
       ...           ( day = d
       ...           , right_ascension = Angle_D (41.73129)
       ...           , declination     = Angle_D (18.44092)
       ...           )
       ...       , Record
       ...           ( day = d + 1
       ...           , right_ascension = Angle_D (42.78204)
       ...           , declination     = Angle_D (18.82742)
       ...           )
       ...       )
       ...       , lat = Angle_D (42.3333)
       ...       , lon = Angle_D (71.0833)
       ...       , h0  = Angle_D (-0.5667)
       ...     )
       >>> sp.day, sp.sid
       (Date (1988, 3, 20), Angle_D (177.741535578))
       >>> [x.n for x in (sp.rise,sp.transit, sp.set)]
       [0.51881115911723963, 0.82029552154124752, 0.12177988396525549]
       >>> [x.alpha.degrees for x in (sp.rise,sp.transit, sp.set)]
       [42.276472017055596, 42.593239842037981, 41.859267859751228]
       >>> [x.delta.degrees for x in (sp.rise,sp.transit, sp.set)]
       [18.642290558106509, 18.758466152777782, 18.488352088349298]
       >>> [x.ha.degrees for x in (sp.rise, sp.transit, sp.set)]
       [-108.5688266724258, -0.054066867395242468, 108.52578574490458]
       >>> [x.altitude.degrees for x in (sp.rise,sp.transit, sp.set)]
       [-0.44595681946769256, 66.425121506118614, -0.52716315594313057]
       >>> [x.delta_m for x in (sp.rise, sp.transit, sp.set)]
       [-0.00050512499927386257, -0.00015018574276456242, 0.0001652102142790363]
       >>> [x.corrected_m for x in (sp.rise, sp.transit, sp.set)]
       [0.51765788596981754, 0.81949718765033475, 0.12129694603138638]
       >>> [x.time_ut for x in (sp.rise, sp.transit, sp.set)]
       [Time (12, 25, 25, 641), Time (19, 40, 4, 557), Time (2, 54, 40, 56)]
    """

    ### see J. Meeus, ISBN 0-943396-61-1, pp. 101-104

    h0_stars_planets = Angle_D (-0.5667)
    h0_sun           = Angle_D (-0.8333)

    class _Event_ (TFL.Meta.Object) :

        def __init__ (this, m, ** vars) :
            this.m = m
            this.__dict__.update (vars)
            this.calc            (m)
        # end def __init__

        def calc (self, m) :
            ha, dec, alt  = self._at_time       (m)
            delta_m       = self._delta_m       (ha, dec, alt)
            self.delta_m  = delta_m
            self.time_ut  = self._to_ut         (m, delta_m)
            self.time     = self._to_local_time (self.hours_ut)
        # end def calc

        def _at_time (self, m) :
            lat           = self.lat
            self.sid      = sid      = Angle_D.normalized \
                (self.sid.degrees + 360.985647 * m)
            self.n        = n        = m + self.day.delta_T / 86400.0
            self.alpha    = alpha    = Angle_R (self.self.interpolator_a (n))
            self.delta    = delta    = Angle_R (self.self.interpolator_d (n))
            self.ha       = ha       = self._hour_angle (sid, self.lon, alpha)
            self.altitude = altitude = Angle_R.asin \
                (lat.sin * delta.sin + lat.cos * delta.cos * ha.cos)
            return ha, delta, altitude
        # end def _at_time

        def _delta_m (self, ha, dec, alt) :
            return \
                ( (alt - self.h0).degrees
                / (360.0 * dec.cos * self.lat.cos * ha.sin)
                )
        # end def _delta_m

        def _hour_angle (self, sid, lon, alpha) :
            ha = (sid - lon - alpha).degrees
            if abs (ha) >= 360.0 :
                ha = ha % 360.0
            if ha > 180.0 :
                ha -= 360.0
            if ha < -180.0 :
                ha += 360.
            return Angle_D (ha)
        # end def _hour_angle

        def _to_local_time (self, hours_ut) :
            lon         = rounded_to (self.lon.degrees, 15)
            hours_local = self.hours_local = \
                ( hours_ut
                - (CAL.Time.from_degrees (lon).seconds / 3600.0)
                ) % 24.0
            return CAL.Time.from_decimal_hours (hours_local)
        # end def _to_local_time

        def _to_ut (self, m, delta_m) :
            corr_m   = self.corrected_m = m + delta_m
            hours_ut = self.hours_ut    = (corr_m * 24) % 24.0
            return CAL.Time.from_decimal_hours (hours_ut)
        # end def _to_ut

    # end class _Event_

    class _Transit_ (_Event_) :

        def _delta_m (self, ha, dec, alt) :
            return ha.degrees / 360.0
        # end def _delta_m

    # end class _Transit_

    def __init__ (self, ephs, lat, lon, h0 = h0_sun) :
        self.ephs  = ephs
        self.lat   = lat   = Angle_D (getattr (lat, "degrees", lat))
        self.lon   = lon   = Angle_D (getattr (lon, "degrees", lon))
        self.h0    = h0    = Angle_D (getattr (h0,  "degrees", h0))
        self.day   = day   = ephs [1].day
        self.alpha = alpha = ephs [1].right_ascension
        self.delta = delta = ephs [1].declination
        self.sid   = sid   = Angle_D.normalized (day.sidereal_time_deg)
        self.H0    = H0    = Angle_D.acos \
            ((h0.sin - lat.sin * delta.sin) / (lat.cos * delta.cos))
        self.m0    = m0    = ((alpha + lon - sid).degrees / 360.) % 1.0
        self.m1    = m1    = (m0 - H0.degrees             / 360.) % 1.0
        self.m2    = m2    = (m0 + H0.degrees             / 360.) % 1.0
        self.transit       = self._Transit_ (m0, ** locals ())
        self.rise          = self._Event_   (m1, ** locals ())
        self.set           = self._Event_   (m2, ** locals ())
        h0                         = Angle_D (-6.0)
        self.civil_twilight_start  = self._Event_ (m1, ** locals ())
        self.civil_twilight_finis  = self._Event_ (m2, ** locals ())
        h0                         = Angle_D (-12.0)
        self.nautic_twilight_start = self._Event_ (m1, ** locals ())
        self.nautic_twilight_finis = self._Event_ (m2, ** locals ())
        h0                         = Angle_D (-18.0)
        self.astro_twilight_start  = self._Event_ (m1, ** locals ())
        self.astro_twilight_finis  = self._Event_ (m2, ** locals ())
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

# end class Sun_P

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ CAL.Sun

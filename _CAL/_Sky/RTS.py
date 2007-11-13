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
#    CAL.RTS
#
# Purpose
#    Provide class for calculating of rising, transit and setting of
#    celestial bodies
#
# References
#    J. Meeus, Astronomical Algorithms, 2nd edition, 1998, ISBN 0-943396-61-1
#
# Revision Dates
#     8-Nov-2007 (CT) Creation
#    11-Nov-2007 (CT) Creation continued
#    13-Nov-2007 (CT) Creation continued..
#    13-Nov-2007 (CT) Moved from `CAL.Sun.Sun_P` to `CAL.Sky.RTS.RTS`
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _TFL                     import TFL
from   _TGL                     import TGL

from   _TFL._Meta.Once_Property import Once_Property

import _CAL._Sky
import _CAL.Time
import _TFL._Meta.Object
import _TFL.Accessor
import _TGL._DRA.Interpolator

from   _TFL.predicate import rounded_to
from   _TGL.Angle     import Angle_D, Angle_R

class RTS (TFL.Meta.Object) :
    """Model behavior of celestial body for a single day at a specific
       geographical position.

       >>> from _CAL._Sky.Sun import Sun
       >>> import _CAL.Date
       >>> s = Sun (CAL.Date (2007, 6, 13))
       >>> rts = RTS ((s - 1, s, s + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [x.time for x in (rts.rise, rts.transit, rts.set)]
       [Time (3, 53, 41, 641), Time (11, 54, 26, 712), Time (19, 55, 49, 352)]
       >>> s = Sun (CAL.Date (2007, 11, 13))
       >>> rts = RTS ((s - 1, s, s + 1),
       ...   Angle_D (48, 14), Angle_D (-16, -20), Angle_D (-0.8333))
       >>> [str (x.time) for x in (rts.rise, rts.transit, rts.set)]
       ['06:57:54.000773', '11:38:47.000148', '16:19:21.000831']

       ### Example 15.a of J. Meeus, pp.103-104, Venus at Boston
       >>> from _TFL.Record import Record
       >>> d  = CAL.Date (1988, 3, 20)
       >>> rts = RTS ( ( Record
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
       >>> rts.day, rts.sid
       (Date (1988, 3, 20), Angle_D (177.741535578))
       >>> [x.n for x in (rts.rise,rts.transit, rts.set)]
       [0.51881115911723963, 0.82029552154124752, 0.12177988396525549]
       >>> [x.alpha.degrees for x in (rts.rise,rts.transit, rts.set)]
       [42.276472017055596, 42.593239842037981, 41.859267859751228]
       >>> [x.delta.degrees for x in (rts.rise,rts.transit, rts.set)]
       [18.642290558106509, 18.758466152777782, 18.488352088349298]
       >>> [x.ha.degrees for x in (rts.rise, rts.transit, rts.set)]
       [-108.5688266724258, -0.054066867395242468, 108.52578574490458]
       >>> [x.altitude.degrees for x in (rts.rise,rts.transit, rts.set)]
       [-0.44595681946769256, 66.425121506118614, -0.52716315594313057]
       >>> [x.delta_m for x in (rts.rise, rts.transit, rts.set)]
       [-0.00050512499927386257, -0.00015018574276456242, 0.0001652102142790363]
       >>> [x.corrected_m for x in (rts.rise, rts.transit, rts.set)]
       [0.51765788596981754, 0.81949718765033475, 0.12129694603138638]
       >>> [x.time_ut for x in (rts.rise, rts.transit, rts.set)]
       [Time (12, 25, 25, 641), Time (19, 40, 4, 557), Time (2, 54, 40, 56)]
    """

    ### see J. Meeus, pp. 101-104

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

    def __init__ (self, ephs, lat, lon, h0 = Angle_D (-0.5667)) :
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
        self.vars  = vars  = locals ()
        self.transit       = self._Transit_ (m0, ** vars)
        self.rise          = self._Event_   (m1, ** vars)
        self.set           = self._Event_   (m2, ** vars)
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

# end class RTS

if __name__ != "__main__" :
    CAL.Sky._Export ("*")
### __END__ CAL.Sun

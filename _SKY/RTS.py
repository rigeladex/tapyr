# -*- coding: utf-8 -*-
# Copyright (C) 2007-2017 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    SKY.RTS
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
#    15-Nov-2007 (CT) `RTS._Event_.__str__` added
#    31-Mar-2008 (CT) `_to_local_time` changed to consider `dst`
#    31-Mar-2008 (CT) `azimuth` added to newly factored `_Rise_` and `_Set_`
#    17-Jul-2009 (CT) Don't display floating point values in doctest
#    25-Sep-2016 (CT) Add comment with reference o altitude formula
#    26-Sep-2016 (CT) Adapt to factored `CAL.Sky.Earth.Time`
#    26-Sep-2016 (CT) Adapt doc-tests to correction of `CAL.Time.microsecond`
#    27-Sep-2016 (CT) Factor `altitude` and `hour_angle` to `CAL.Sky.Earth`
#    27-Sep-2016 (CT) Factor `local_hour_angle` and add guard
#    30-Sep-2016 (CT) Use `decl` and `ra`, not `delta` and `alpha`,
#                     nor `declination` and `right_ascension`
#     9-Oct-2016 (CT) Adapt to move of Package_Namespace `DRA`
#     9-Oct-2016 (CT) Move out from `CAL` to toplevel package
#     9-Aug-2017 (CT) Use one argument `loc`, not two arguments `lat` and `lon`
#                     + Use `loc.longitude_meuss`
#                     + Use `loc.tz`, not home-grown code
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _SKY                     import SKY
from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

from   _SKY.Earth               import altitude, azimuth, hour_angle

import _CAL.Date_Time
import _CAL.Delta
import _CAL.Time

from   _TFL.predicate           import rounded_to
from   _TFL.Angle               import Angle, Angle_D, Angle_R

import _TFL._Meta.Object
import _TFL.Accessor
import _TFL._DRA.Interpolator

class RTS (TFL.Meta.Object) :
    """Model behavior of celestial body for a single day at a specific
       geographical position.

       ### Example 15.a of J. Meeus, pp.103-104, Venus at Boston
       >>> import _CAL.Date
       >>> from _TFL.Record import Record
       >>> d  = CAL.Date (1988, 3, 20)
       >>> rts = RTS ( ( Record
       ...           ( day  = d - 1
       ...           , time = SKY.Earth.Time (d - 1)
       ...           , ra   = Angle_D (40.68021)
       ...           , decl = Angle_D (18.04761)
       ...           )
       ...       , Record
       ...           ( day  = d
       ...           , time = SKY.Earth.Time (d)
       ...           , ra   = Angle_D (41.73129)
       ...           , decl = Angle_D (18.44092)
       ...           )
       ...       , Record
       ...           ( day  = d + 1
       ...           , time = SKY.Earth.Time (d + 1)
       ...           , ra   = Angle_D (42.78204)
       ...           , decl = Angle_D (18.82742)
       ...           )
       ...       )
       ...       , loc = SKY.Location (Angle_D (42.3333), - Angle_D (71.0833))
       ...       , h0  = Angle_D (-0.5667)
       ...     )
       >>> rts.day, rts.sid
       (Date (1988, 3, 20), Angle_D (177.741566081))
       >>> ["%5.2f" % x.n for x in (rts.rise,rts.transit, rts.set)]
       [' 0.52', ' 0.82', ' 0.12']
       >>> ["%5.2f" % x.alpha.degrees for x in (rts.rise,rts.transit, rts.set)]
       ['42.28', '42.59', '41.86']
       >>> ["%5.2f" % x.delta.degrees for x in (rts.rise,rts.transit, rts.set)]
       ['18.64', '18.76', '18.49']
       >>> ["%5.2f" % x.ha.degrees for x in (rts.rise, rts.transit, rts.set)]
       ['-108.57', '-0.05', '108.53']
       >>> ["%5.2f" % x.altitude.degrees for x in (rts.rise,rts.transit, rts.set)]
       ['-0.45', '66.43', '-0.53']
       >>> ["%8.5f" % x.delta_m for x in (rts.rise, rts.transit, rts.set)]
       ['-0.00051', '-0.00015', ' 0.00017']
       >>> ["%5.2f" % x.corrected_m for x in (rts.rise, rts.transit, rts.set)]
       [' 0.52', ' 0.82', ' 0.12']
       >>> [x.time_ut for x in (rts.rise, rts.transit, rts.set)]
       [Time (12, 25, 25, 634034), Time (19, 40, 4, 549694), Time (2, 54, 40, 48807)]

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
            ### J. Meeus, p. 103
            loc           = self.loc
            rts           = self.rts
            ### sid: sidereal time at Greenwich, in degrees,
            ###      at time `m` (expressed as fraction of a day)
            self.sid      = sid      = Angle_D.normalized \
                (rts.sid.degrees + 360.985647 * m)
            ### n: `m` corrected by difference in
            ###    Terrestrial Dynamical Time and UT
            self.n        = n        = m + self.day.delta_T / 86400.0
            self.alpha    = alpha    = Angle_R (rts.interpolator_a (n))
            self.delta    = delta    = Angle_R (rts.interpolator_d (n))
            self.ha       = ha       = hour_angle (sid,   loc, alpha)
            self.altitude = alt      = altitude   (delta, ha,  loc)
            return ha, delta, alt
        # end def _at_time

        def _delta_m (self, ha, dec, alt) :
            ### J. Meeus, p. 103
            result = \
                ( (alt - self.h0).degrees
                / (360.0 * dec.cos * self.lat.cos * ha.sin)
                )
            return result
        # end def _delta_m

        def _to_local_time (self, hours_ut) :
            dt    = CAL.Date_Time.combine (self.day, self.time_ut)
            delta = self.loc.tz.utcoffset (dt._body)
            return CAL.Time (time = (dt + delta)._body.time ())
        # end def _to_local_time

        def _to_ut (self, m, delta_m) :
            corr_m   = self.corrected_m = m + delta_m
            hours_ut = self.hours_ut    = (corr_m * 24) % 24.0
            return CAL.Time.from_decimal_hours (hours_ut)
        # end def _to_ut

        def __str__ (self) :
            return "%02d:%02d" % self.time.hh_mm
        # end def __str__

    # end class _Event_

    class _Rise_ (_Event_) :

        def calc (self, m) :
            self.__super.calc (m)
            self.azimuth  = Angle_D \
                (Angle_R.acos (self.delta.sin / self.lat.cos).degrees)
        # end def calc

    # end class _Rise_

    class _Set_ (_Event_) :

        def calc (self, m) :
            self.__super.calc (m)
            self.azimuth  = Angle_D \
                (360. - Angle_R.acos (self.delta.sin / self.lat.cos).degrees)
        # end def calc

    # end class _Set_

    class _Transit_ (_Event_) :

        def _delta_m (self, ha, dec, alt) :
            ### J. Meeus, p. 103
            return ha.degrees / 360.0
        # end def _delta_m

    # end class _Transit_

    rise = None
    set  = None

    def __init__ (self, ephs, loc, h0 = Angle_D (-0.5667)) :
        """Arguments:

           * ephs : triple of positions for UT=0:0 for (day-1, day, day+1)

           * loc  : SKY.Location instance

           * h0   : "standard" altitude, i.e., the geometric altitude of the
                    center of the body at the time of apparent rising or
                    setting

                    + 0.5667 degrees for stars and planets
                    + 0.8333 degrees for the sun

        """
        rts         = self
        self.ephs   = ephs
        self.loc    = loc
        self.lat    = lat   = loc.latitude
        self.lon    = lon   = loc.longitude_meuss
        self.h0     = h0    = Angle (h0)
        self.day    = day   = ephs [1].day
        self.alpha  = alpha = ephs [1].ra
        self.delta  = delta = ephs [1].decl
        self.time   = time  = ephs [1].time
        self.sid    = sid   = Angle_D.normalized (time.sidereal_deg)
        ### H0: local hour angle corresponding to the time of rise or set of a
        ###     celestial body. J. Meeus, eq. (15.1), p. 102
        self.H0     = H0    = self.local_hour_angle (h0, lat, delta)
        self.vars   = vars  = locals ()
        ### m0, m1, m2
        ### transit, rise, set times, on `day`, expressed as fractions of a day
        ### J. Meeus, eq. (15.2), p. 102
        self.m0     = m0    = ((alpha + lon - sid).degrees / 360.) % 1.0
        if H0 is not None :
            self.m1 = m1    = (m0 - H0.degrees             / 360.) % 1.0
            self.m2 = m2    = (m0 + H0.degrees             / 360.) % 1.0
            self.rise       = self._Rise_    (m1, ** vars)
            self.set        = self._Set_     (m2, ** vars)
        self.transit        = self._Transit_ (m0, ** vars)
    # end def __init__

    @Once_Property
    def day_length (self) :
        return self.set.time - self.rise.time
    # end def day_length

    @Once_Property
    def interpolator_a (self) :
        def gen (self) :
            ephs = self.ephs
            last = None
            for i, eph in enumerate (ephs, -1) :
                ra = eph.ra.radians
                if last is not None and ra < last :
                    ra += Angle_R.two_pi
                last = ra
                yield i, ra
        ps = tuple (gen (self))
        return TFL.DRA.Interpolator_3 (* ps)
    # end def interpolator_a

    @Once_Property
    def interpolator_d (self) :
        ephs = self.ephs
        return TFL.DRA.Interpolator_3 \
            ( (-1, ephs [0])
            , ( 0, ephs [1])
            , (+1, ephs [2])
            , y_getter = TFL.Getter [1].decl.radians
            )
    # end def interpolator_d

    def local_hour_angle (self, h0, lat, delta) :
        """Local hour angle corresponding to the time of rise or set of a
           celestial body.
        """
        ### J. Meeus, eq. (15.1), p. 102
        cos_H0 = (h0.sin - lat.sin * delta.sin) / (lat.cos * delta.cos)
        if abs (cos_H0) <= 1 :
            return Angle_D.acos (cos_H0)
    # end def local_hour_angle

# end class RTS

if __name__ != "__main__" :
    SKY._Export ("*")
### __END__ SKY.RTS

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2012 Mag. Christian Tanzer. All rights reserved
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
#    CAL.Date_Time
#
# Purpose
#    Wrapper around `datetime.datetime`
#
# Revision Dates
#    15-Oct-2004 (CT) Creation
#    17-Oct-2004 (CT) Adapted to changes in `_DTW_` and `Delta`
#    28-Dec-2005 (MG) Static method `from_ical` added
#    30-Nov-2006 (CT) `__getattr__` for `CJD`, `MJD`, `TJD`, "CJS", "MJS",
#                     and "TJS" added
#    10-Dec-2006 (CT) `from_julian` added
#    11-Dec-2006 (CT) `from_julian` corrected
#    11-Dec-2006 (CT) `__getattr__` changed to `setattr` the modified value
#    11-Nov-2007 (CT) `sidereal_time` added
#     3-Jan-2008 (CT) `time_pattern` added and `_from_string_match_kw` redefined
#     7-Jan-2008 (CT) `as_utc` added
#    31-Mar-2008 (CT) `combine` added
#    16-Jun-2010 (CT) s/print/pyk.fprint/
#    29-Mar-2012 (CT) Add support for `tzinfo`; factor `as_local`; use
#                     `CAL.Time._from_string_match_kw`
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _CAL                     import CAL

import _CAL.Date
import _CAL.Time

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL                     import pyk
from   _TFL.Regexp              import *

import datetime

class Date_Time (CAL.Date, CAL.Time) :
    """Model a (gregorian) date plus time.

       >>> from _CAL.Delta import Date_Time_Delta as Delta
       >>> d = Date_Time (2004, 10, 15, 16, 03, 14)
       >>> pyk.fprint (d)
       2004-10-15 16:03:14
       >>> d.year, d.month, d.day, d.datetime, d.week, d.weekday, d.ordinal
       (2004, 10, 15, datetime.datetime(2004, 10, 15, 16, 3, 14), 42, 4, 731869)
       >>> d.month_name
       'Oct'
       >>> d = d - Delta (3)
       >>> d.year, d.month, d.day, d.datetime, d.week, d.weekday, d.ordinal
       (2004, 10, 12, datetime.datetime(2004, 10, 12, 16, 3, 14), 42, 1, 731866)
       >>> d = d - 1
       >>> d.year, d.month, d.day, d.datetime, d.week, d.weekday, d.ordinal
       (2004, 10, 11, datetime.datetime(2004, 10, 11, 16, 3, 14), 42, 0, 731865)
       >>> d1 = d2 = Date_Time (2004, 10, 15, 16, 03, 14)
       >>> id (d1) == id (d2)
       True
       >>> d1 += 1
       >>> id (d1) == id (d2)
       False
       >>> pyk.fprint (d2 - d1)
       -1 day, 0:00:00

       >>> d = Date_Time (2006, 12, 10, 12, 26, 30)
       >>> d.TJD, d.TJS
       (14079.518402777778, 1216470390)
       >>> d
       Date_Time (2006, 12, 10, 12, 26, 30, 0)
       >>> Date_Time.from_julian (14079, kind = "TJD")
       Date_Time (2006, 12, 10, 0, 0, 0, 0)
       >>> Date_Time.from_julian (14079.518402777778, kind = "TJD")
       Date_Time (2006, 12, 10, 12, 26, 30, 0)
       >>> Date_Time.from_julian (1216470390, kind = "TJS")
       Date_Time (2006, 12, 10, 12, 26, 30, 0)

       >>> d = Date_Time (1987, 4, 10, 19, 21, 0)
       >>> d.sidereal_time
       Time (8, 34, 57, 90)

       >>> Date_Time (1988,6,19,12).JD
       2447332.0
       >>> Date_Time (1988,1,27).JD
       2447187.5
       >>> Date_Time (1999,1,1).JD
       2451179.5
       >>> Date_Time (1999,1,1,12).JD
       2451180.0
       >>> Date_Time (2000,1,1,12).JD
       2451545.0

       >>> dt = Date_Time (2008, 1, 7, 10, 16, 42, 0)
       >>> dt
       Date_Time (2008, 1, 7, 10, 16, 42, 0)
       >>> dt.as_utc ()
       Date_Time (2008, 1, 7, 9, 16, 42, 0)
       >>> dt = Date_Time (2008, 4, 7, 10, 16, 42, 0)
       >>> dt
       Date_Time (2008, 4, 7, 10, 16, 42, 0)
       >>> dt.as_utc ()
       Date_Time (2008, 4, 7, 8, 16, 42, 0)

       >>> dt = Date_Time.from_string ("2012-03-29 10:06:46 -0400")
       >>> dt
       Date_Time (2012, 3, 29, 10, 6, 46, 0)
       >>> dt.as_local ()
       Date_Time (2012, 3, 29, 16, 6, 46, 0)
       >>> dt.as_utc ()
       Date_Time (2012, 3, 29, 14, 6, 46, 0)

    """

    _Type            = datetime.datetime
    _init_arg_names  = \
        CAL.Date._init_arg_names + CAL.Time._init_arg_names
    _kind            = "datetime"
    _timetuple_slice = lambda s, tt : tt [:6] + (0, )

    mean_solar_day_over_mean_sidereal_day = 1.00273790935

    time_pattern     = Regexp \
        ( r"(?P<hour> \d{2,2})"
          r":"
          r"(?P<minute> \d{2,2})"
          r"(?: :"
            r"(?P<second> \d{2,2})"
            r"(?: \."
              r"(?P<microsecond> \d+)"
            r")?"
          r")?"
          r"(?: \s"
            r"(?P<tzinfo> [-+]\d{4,4})"
          r")?"
        , flags = re.VERBOSE | re.IGNORECASE
        )

    from _CAL.Delta import Date_Time_Delta as Delta

    def as_local (self) :
        """Return `self` converted to local time."""
        from dateutil.tz import tzlocal
        local = self
        if not local.tzinfo :
            local = self.replace (tzinfo = tzlocal ())
        return self.__class__ \
            (** {self._kind : local._body.astimezone (tzlocal ())})
    # end def as_local

    def as_utc (self) :
        """Return `self` converted to `UTC`."""
        local = self.as_local ()
        delta = self.Delta    (seconds = local._body.utcoffset ().seconds)
        return local - delta
    # end def as_utc

    @classmethod
    def combine (cls, date, time) :
        """Create a `Date_Time` object from `date` and `time` objects."""
        if isinstance (date, CAL._DTW_) :
            date = date._body
        if isinstance (time, CAL._DTW_) :
            time = time._body
        return cls (** {cls._kind : datetime.datetime.combine (date, time)})
    # end def combine

    @staticmethod
    def from_ical (ical) :
        for p_cls, tgl_cls in \
            ( (datetime.datetime,   CAL.Date_Time)
            , (datetime.date,       CAL.Date)
            , (datetime.timedelta,  CAL.Time_Delta)
            ) :
            if isinstance (ical.dt, p_cls) :
                return tgl_cls (** {tgl_cls._kind : ical.dt})
    # end def from_ical

    @classmethod
    def from_julian (cls, jd, kind = "CJD") :
        k = kind
        if kind.endswith ("S") :
            jd /= 86400.0
            k = kind [:-1] + "D"
        days          = int (jd)
        seconds       = (jd - days) * 86400
        result = super (Date_Time, cls).from_julian (days, kind = k)
        return result + CAL.Time_Delta (seconds = seconds)
    # end def from_ordinal

    @Once_Property
    def sidereal_time_deg (self) :
        """Mean sidereal time at date/time `self` in degrees
           (applies for UT only).
        """
        ### see J. Meeus, ISBN 0-943396-61-1, pp. 87-88
        ### XXX Fix this to work with arbitrary timezones
        T  = self.JC_J2000
        T2 = T  * T
        T3 = T2 * T
        return \
            ( 280.46061837
            + 360.98564736629 * (self.JD - 2451545.0)
            + 0.000387933   * T2
            - T3 / 38710000.0
            )
    # end def sidereal_time_deg

    @classmethod
    def _from_string_match_kw (cls, s, match) :
        assert match
        kw = super (Date_Time, cls)._from_string_match_kw (s, match)
        t  = s [match.end () :].lstrip ().lstrip ("T")
        if t and cls.time_pattern.match (t) :
            match = cls.time_pattern.last_match
            kw.update (CAL.Time._from_string_match_kw (t, match))
        return kw
    # end def _from_string_match_kw

    def __getattr__ (self, name) :
        result = self.__super.__getattr__ (name)
        if name in self.JD_offset :
            if name.endswith ("S") :
                result += self.seconds
            else :
                result += (self.seconds / 86400.)
            setattr (self, name, result)
        return result
    # end def __getattr__

# end class Date_Time

class Date_Time_M (CAL._Mutable_DTW_) :
    """Mutable datetime object

       >>> d1 = d2 = Date_Time_M (2004, 10, 15, 16, 03, 14)
       >>> pyk.fprint (d1, d2)
       2004-10-15 16:03:14 2004-10-15 16:03:14
       >>> id (d1) == id (d2)
       True
       >>> d1 += 1
       >>> pyk.fprint (d1, d2)
       2004-10-16 16:03:14 2004-10-16 16:03:14
       >>> id (d1) == id (d2)
       True
    """

    Class = Date_Time

# end class Date_Time_M

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ CAL.Date_Time

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2007 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _CAL                    import CAL
import _CAL.Date
import _CAL.Time

import datetime

class Date_Time (CAL.Date, CAL.Time) :
    """Model a (gregorian) date plus time.

       >>> from _CAL.Delta import Date_Time_Delta as Delta
       >>> d = Date_Time (2004, 10, 15, 16, 03, 14)
       >>> print d
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
       >>> print d2 - d1
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

    """

    _Type            = datetime.datetime
    _init_arg_names  = \
        CAL.Date._init_arg_names + CAL.Time._init_arg_names
    _kind            = "datetime"
    _timetuple_slice = lambda s, tt : tt [:6] + (0, )

    mean_solar_day_over_mean_sidereal_day = 1.00273790935

    from _CAL.Delta import Date_Time_Delta as Delta

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

    def __getattr__ (self, name) :
        result = self.__super.__getattr__ (name)
        if name in self.JD_offset :
            if name in ("CJD", "MJD", "TJD") :
                result += (self.seconds / 86400.)
            elif name in ("CJS", "MJS", "TJS") :
                result += self.seconds
            setattr (self, name, result)
        return result
    # end def __getattr__

# end class Date_Time

class Date_Time_M (CAL._Mutable_DTW_) :
    """Mutable datetime object

       >>> d1 = d2 = Date_Time_M (2004, 10, 15, 16, 03, 14)
       >>> print d1, d2
       2004-10-15 16:03:14 2004-10-15 16:03:14
       >>> id (d1) == id (d2)
       True
       >>> d1 += 1
       >>> print d1, d2
       2004-10-16 16:03:14 2004-10-16 16:03:14
       >>> id (d1) == id (d2)
       True
    """

    Class = Date_Time

# end class Date_Time_M

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ CAL.Date_Time

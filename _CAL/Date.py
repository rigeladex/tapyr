# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2011 Mag. Christian Tanzer. All rights reserved
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
#    CAL.Date
#
# Purpose
#    Wrapper around `datetime.date`
#
# Revision Dates
#    14-Oct-2004 (CT) Creation
#                     (derived from MG's CAL.Date_Time and CT's Date_Time)
#    17-Oct-2004 (CT) `__add__` and `__sub__` changed to use `Delta.dt_op`
#    17-Oct-2004 (CT) Doctest for `Month_Delta` added
#    17-Oct-2004 (CT) s/Month_Delta/MY_Delta/
#    19-Oct-2004 (CT) s/MY_Delta/Month_Delta/
#    23-Oct-2004 (CT) `_default_format` added
#    23-Oct-2004 (CT) `_new_object` redefined to handle negative values for
#                     `day`
#    26-Oct-2004 (CT) `is_weekday` added
#     2-Nov-2004 (CT) `from_string` added
#    10-Nov-2004 (CT) `from_ordinal` added
#    15-Nov-2004 (CT) `wk_ordinal` added
#     6-Jan-2005 (CT) `__main__` script added
#    01-Sep-2005 (MG) Use new decorator syntax for defining classmethod
#    30-Nov-2006 (CT) `__getattr__` changed to delegate to
#                     `__super.__getattr__`
#    30-Nov-2006 (CT) `CJD`, `MJD`, and `TJD` added
#    10-Dec-2006 (CT) `JD_offset` factored
#    10-Dec-2006 (CT) `from_julian` added
#    12-Dec-2006 (CT) `from_ordinal` changed to use `cls._kind` and
#                     `cls._Type` instead of `date` and `datetime.date`
#    12-Jan-2007 (CT) Imports fixed
#                     (import `Command_Line` and `Regexp` from _TFL)
#    11-Aug-2007 (CT) `quarter` added
#     7-Nov-2007 (CT) Use `Getter` instead of `lambda`
#     8-Nov-2007 (CT) `JD2000`, `JC_J2000`, and `julian_epoch` added
#     9-Nov-2007 (CT) Use `Once_Property` instead of `__getattr__`
#    11-Nov-2007 (CT) `sidereal_time` added
#    11-Nov-2007 (CT) `delta_T` added
#    12-Nov-2007 (CT) `JD` added, coverage of `delta_T` extended
#    23-Dec-2007 (CT) Command_Line options `-regexp` and `-xformat` added
#     3-Jan-2008 (CT) `_from_string_match_kw` factored
#     3-Jan-2008 (CT) `date_pattern` changed to make `year` mandatory
#    10-Feb-2008 (CT) `Date_Opt` added (and used for option `delta_to`)
#    15-Feb-2008 (CT) `Date_Opt` corrected (up-call to `__init__`)
#     8-May-2008 (CT) `Date_Opt` changed to use `__super`
#     4-Jan-2010 (CT) `_Date_Arg_` based on `TFL.CAO` added, `Date_Opt` removed
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _TFL                     import TFL

import _CAL._DTW_

import _TFL.Accessor
import _TFL.CAO

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Math_Func           import horner
from   _TFL.Regexp              import *

import datetime
import operator

class Date (CAL._DTW_) :
    """Model a (gregorian) date.

       >>> from _CAL.Delta import Date_Delta as Delta
       >>> d = Date (2004, 10, 14)
       >>> print d
       2004-10-14
       >>> d.year, d.month, d.day, d.date, d.week, d.weekday, d.ordinal
       (2004, 10, 14, datetime.date(2004, 10, 14), 42, 3, 731868)
       >>> d = d - Delta (3)
       >>> d.year, d.month, d.day, d.date, d.week, d.weekday, d.ordinal
       (2004, 10, 11, datetime.date(2004, 10, 11), 42, 0, 731865)
       >>> d = d - 1
       >>> d.year, d.month, d.day, d.date, d.week, d.weekday, d.ordinal
       (2004, 10, 10, datetime.date(2004, 10, 10), 41, 6, 731864)
       >>> from _CAL.Delta import Month_Delta
       >>> print d, d + Month_Delta (1)
       2004-10-10 2004-11-10
       >>> print d, d + Month_Delta (3)
       2004-10-10 2005-01-10
       >>> print d, d + Month_Delta (12)
       2004-10-10 2005-10-10
       >>> print d, d + Month_Delta (-1)
       2004-10-10 2004-09-10
       >>> print d, d + Month_Delta (-12)
       2004-10-10 2003-10-10
       >>> MD = Month_Delta
       >>> for x in (d, d + MD (3), d + MD (6), d + MD (9)):
       ...    print str (x), ":", x.quarter
       2004-10-10 : 4
       2005-01-10 : 1
       2005-04-10 : 2
       2005-07-10 : 3
       >>> d = Date (day = 1, month = 1, year = 2004)
       >>> print d, d + Month_Delta (11)
       2004-01-01 2004-12-01
       >>> d1 = Date (2004, 10, 14)
       >>> d2 = Date (2004, 10, 16)
       >>> print d1 - d2
       -2 days, 0:00:00
       >>> d = Date (day = -1, month = 1, year = 2004)
       >>> print d, d + Month_Delta (1)
       2004-01-31 2004-02-29
       >>> print d, d + Month_Delta (2)
       2004-01-31 2004-03-31
       >>> print d, d + Month_Delta (3)
       2004-01-31 2004-04-30
       >>> print d, d + Month_Delta (11)
       2004-01-31 2004-12-31
       >>> print d, d + Month_Delta (12)
       2004-01-31 2005-01-31
       >>> print d, d + Month_Delta (13)
       2004-01-31 2005-02-28
       >>> print d, d + Month_Delta (-1)
       2004-01-31 2003-12-31
       >>> print d, d + Month_Delta (-2)
       2004-01-31 2003-11-30
       >>> print d, d + Month_Delta (-3)
       2004-01-31 2003-10-31
       >>> print d, d + Month_Delta (-11)
       2004-01-31 2003-02-28
       >>> print Date.from_string ("20041102")
       2004-11-02
       >>> print Date.from_string ("2004/11/02")
       2004-11-02
       >>> print Date.from_string ("20041102")
       2004-11-02
       >>> print Date.from_string ("31.10.2004")
       2004-10-31
       >>> print Date.from_string ("31/10/2004")
       2004-10-31
       >>> print Date.from_string ("31.Oct.2004")
       2004-10-31
       >>> print Date.from_string ("Oct 5, 2004")
       2004-10-05

       >>> mjd_epoch = Date (1858, 11, 17)
       >>> tjd_epoch = Date (1968,  5, 24)
       >>> mjd_epoch.ordinal, mjd_epoch.CJD, mjd_epoch.MJD, mjd_epoch.TJD
       (678576, 2400000, 0, -40000)
       >>> tjd_epoch.ordinal, tjd_epoch.CJD, tjd_epoch.MJD, tjd_epoch.TJD
       (718576, 2440000, 40000, 0)

       >>> Date.from_julian (2400000)
       Date (1858, 11, 17)
       >>> Date.from_julian (2440000)
       Date (1968, 5, 24)
       >>> Date.from_julian (40000, kind = "MJD")
       Date (1968, 5, 24)

    """

    ### Julian date offsets to Rata Die (Jan 1, 1)
    ###     http://en.wikipedia.org/wiki/Julian_day_number
    ###     http://en.wikipedia.org/wiki/Epoch_%28astronomy%29
    JD_offset    = dict \
        ( CJD    =   1721424    ### Chronological JD (based on Jan  1, 4713 BC)
        , CJS    =   1721424
        , JD     =   1721424.5  ### Julian day (starts at noon)
        , JD2000 = -  730120.5  ### JD relative to J2000.0 (noon)
        , MJD    = -  678576    ### Modified      JD (based on Nov 17, 1858)
        , MJS    = -  678576
        , TJD    = -  718576    ### Truncated     JD (based on May 24, 1968)
        , TJS    = -  718576
        )

    months = \
        { 'jan' :  1, 'january'   :   1,  1 : "jan"
        , 'feb' :  2, 'february'  :   2,  2 : "feb"
        , 'mar' :  3, 'march'     :   3,  3 : "mar"
        , 'apr' :  4, 'april'     :   4,  4 : "apr"
        , 'may' :  5, 'may'       :   5,  5 : "may"
        , 'jun' :  6, 'june'      :   6,  6 : "jun"
        , 'jul' :  7, 'july'      :   7,  7 : "jul"
        , 'aug' :  8, 'august'    :   8,  8 : "aug"
        , 'sep' :  9, 'september' :   9,  9 : "sep"
        , 'oct' : 10, 'october'   :  10, 10 : "oct"
        , 'nov' : 11, 'november'  :  11, 11 : "nov"
        , 'dec' : 12, 'december'  :  12, 12 : "dec"
        }

    _Type            = datetime.date
    _default_format  = "%d-%m-%Y"
    _kind            = "date"
    _init_arg_names  = ("year", "month", "day")
    _timetuple_slice = lambda s, tt : tt [:3]

    date_pattern     = Multi_Regexp \
        ( r"(?P<year>  \d{4,4})"
          r"([-/]?)"
          r"(?P<month> \d{2,2})"
          r"\2"
          r"(?P<day>   \d{2,2})"
        , r"(?P<day>   \d{1,2})"
          r"([-./])"
          r"(?P<month> \d{1,2} | [a-z]{3,3})"
          r"\2"
          r"(?P<year>  \d{4,4})"
        , r"(?P<month> [a-z]{3,})"
          r"\s"
          r"(?P<day>   \d{1,2})"
          r",\s*"
          r"(?P<year>  \d{4,4})"
        , flags = re.VERBOSE | re.IGNORECASE
        )

    day              = property (TFL.Getter._body.day)
    is_weekday       = property (lambda s : s.weekday < 5)
    month            = property (TFL.Getter._body.month)
    wk_ordinal       = property (lambda s : (s.ordinal - s.weekday) // 7)
    year             = property (TFL.Getter._body.year)

    yad              = None ### set for negative `day` arguments

    from _CAL.Delta import Date_Delta as Delta

    @Once_Property
    def delta_T (self) :
        """Arithmetic difference between Terrestrial Dynamical Time and UT in
           seconds.
           >>> Date (1988).delta_T
           56.0
           >>> Date (1995).delta_T
           61.0
           >>> Date (2000).delta_T
           64.0
           >>> Date (2007).delta_T
           65.0
           >>> Date (2010).delta_T
           67.0
           >>> Date (2050).delta_T
           93.0
           >>> Date (2051).delta_T
           Traceback (most recent call last):
           ...
           ValueError: Algorithm is restricted to 1800..2050, fails for 2051
           >>> [Date (y).delta_T for y in
           ... (1800, 1802, 1822, 1830, 1990, 1972, 1950)]
           [14.0, 12.0, 10.0, 7.0, 57.0, 43.0, 27.0]
        """
        ### see http://sunearth.gsfc.nasa.gov/eclipse/SEcat5/deltat.html
        ### and http://sunearth.gsfc.nasa.gov/eclipse/SEcat5/deltatpoly.html
        ### see J. Meeus, ISBN 0-943396-61-1, p.80
        y = self.year
        t = y - 2000.
        if -19 <= t < 5 :
            return round \
                ( 63.86
                + t * ( 0.3345
                      + t * ( -0.060374
                            + t * ( 0.0017275
                                  + t * ( 0.000651814
                                        + t * 0.00002373599
                                        )
                                  )
                            )
                      )
                )
        elif -200 <= t <= -3 :
            t = (self.JD - Date (1900).JD) / 36525.
            return round \
                ( horner
                    ( t
                    , ( -1.02, 91.02, 265.90, -839.16, -1545.20
                      , 3603.62, 4385.98, -6993.23, -6090.04
                      , 6298.12, 4102.86, -2137.64, -1081.51
                      )
                    )
                )
        elif 5 <= t <= 50 :
            return round (62.92 + t * (0.32217 + t * 0.005589))
        else :
            raise ValueError, \
                "Algorithm is restricted to 1800..2050, fails for %s" % (y, )
    # end def delta_T

    @classmethod
    def from_julian (cls, jd, kind = "CJD") :
        ordinal = int (jd) - cls.JD_offset [kind]
        if kind.endswith ("S") :
            ordinal //= 86400
        return cls.from_ordinal (ordinal)
    # end def from_julian

    @classmethod
    def from_ordinal (cls, ordinal) :
        return cls (** {cls._kind : cls._Type.fromordinal (ordinal)})
    # end def from_ordinal

    @classmethod
    def from_string (cls, s) :
        match = cls.date_pattern.match (s)
        if match :
            return cls (** cls._from_string_match_kw (s, match))
        else :
            raise ValueError, s
    # end def from_string

    @Once_Property
    def JC_J2000 (self) :
        """Julian Century relative to 2000"""
        return (self.JD - 2451545.0) / 36525.0
    # end def JC_J2000

    @Once_Property
    def julian_epoch (self) :
        """Epoch based on julian years"""
        return 2000.0 + self.JD2000 / 365.25
    # end def julian_epoch

    @Once_Property
    def month_name (self) :
        return self.strftime ("%b")
    # end def month_name

    @Once_Property
    def ordinal (self) :
        """Rata Die (based on January 1, 1)"""
        return self._body.toordinal ()
    # end def ordinal

    @Once_Property
    def quarter (self) :
        return (self.month - 1) // 3 + 1
    # end def quarter

    def replace (self, ** kw) :
        if self.yad is None or "day" in kw :
            result      = self.__super.replace (** kw)
        else :
            kw ["day"]   = 1
            yad          = self.yad
            result       = self.__super.replace (** kw)
            result._body = result._body.replace \
                (day = self._day_from_end (yad, result.month, result.year))
            result.yad   = yad
        return result
    # end def replace

    @Once_Property
    def rjd (self) :
        """Relative julian day (based on January 1 of `self.year`)"""
        return self._body.timetuple ().tm_yday
    # end def rjd

    @Once_Property
    def sidereal_time (self) :
        """Mean sidereal time at 0h UT of date `self`.

           >>> d = Date (1987, 4, 10)
           >>> d.sidereal_time
           Time (13, 10, 46, 367)
        """
        import _CAL.Time
        return CAL.Time.from_degrees (self.sidereal_time_deg)
    # end def sidereal_time

    @Once_Property
    def sidereal_time_deg (self) :
        """Mean sidereal time at 0h UT of date `self` in degrees.
        """
        ### see J. Meeus, ISBN 0-943396-61-1, pp. 87-88
        T  = self.JC_J2000
        T2 = T  * T
        T3 = T2 * T
        return \
            ( 100.46061837
            + 36000.770053608 * T
            + 0.000387933     * T2
            - T3 / 38710000.0
            ) % 360.
    # end def sidereal_time_deg

    @Once_Property
    def tuple (self) :
        return self._body.timetuple ()
    # end def tuple

    @Once_Property
    def week (self) :
        return self._body.isocalendar () [1]
    # end def week

    @Once_Property
    def weekday (self) :
        return self._body.weekday ()
    # end def weekday

    def _day_from_end (self, yad, month, year) :
        from _CAL.Year import Year
        return Year (year).mmap [month].days [yad].number
    # end def _day_from_end

    @classmethod
    def _from_string_match_kw (cls, s, match) :
        assert match
        kw = {}
        for k, v in match.groupdict ().iteritems () :
            if v :
                v = v.lower ()
                if k == "month" and v in cls.months :
                    v = cls.months [v]
                else :
                    v = int (v)
                kw [k] = v
        return kw
    # end def _from_string_match_kw

    def _new_object (self, kw) :
        d = kw ["day"]
        if d < 0 :
            kw ["day"] = self._day_from_end (d, kw ["month"], kw ["year"])
            self.yad   = d
        return self.__super._new_object (kw)
    # end def _new_object

    def __getattr__ (self, name) :
        if name in self.JD_offset :
            result = self.ordinal + self.JD_offset [name]
            if name.endswith ("S") :
                result *= 86400
            setattr (self, name, result)
        else :
            result = self.__super.__getattr__ (name)
        return result
    # end def __getattr__

    def __add__ (self, rhs) :
        delta  = self._delta (rhs)
        return delta.dt_op (self, operator.add)
    # end def __add__

    def __sub__ (self, rhs) :
        delta = self._delta (rhs)
        if isinstance (delta, CAL._Delta_) :
            result = delta.dt_op (self, operator.sub)
        else :
            if hasattr (rhs, "_body") :
                rhs = rhs._body
            result = self.Delta (** {self.Delta._kind : self._body - rhs})
        return result
    # end def __sub__

# end class Date

class Date_M (CAL._Mutable_DTW_) :
    """Mutable date object

       >>> d1 = d2 = Date_M (2004, 10, 14)
       >>> print d1, d2
       2004-10-14 2004-10-14
       >>> d1 += 1
       >>> print d1, d2
       2004-10-15 2004-10-15
    """

    Class = Date

# end class Date_M

class _Date_Arg_ (TFL.CAO.Str) :
    """Argument or option with a (calendary) date value"""

    _real_name = "Date"

    def cook (self, value, cao = None) :
        if value == "now" :
            return Date ()
        if value :
            return Date.from_string (value)
    # end def cook

# end class _Date_Arg_

def _main (cmd) :
    from _TFL.Caller import Scope
    ### Usage example for `-regexp` and `-xformat`::
    ### for f in *.tex; do
    ###   VCMove $f $(python /swing/python/Date.py -regexp '(?P<prefix> .*)_(?P<date> \d{2}-[A-Za-z][a-z]{2}-\d{4}|\d{8})\.?(?P<ext> .*)' -xformat '%(date)s_%(prefix)s.%(ext)s' $f)
    ### done
    if cmd.regexp :
        regexp = Regexp (cmd.regexp, re.VERBOSE)
        if regexp.search (cmd.base_date) :
            base_date  = regexp.date
            match_dict = regexp.groupdict ()
        else :
            import sys
            print >> sys.stderr, "`%s` doesn't match for `%s`" % \
                (cmd.regexp, cmd.base_date)
            sys.exit (9)
    else :
        base_date   = cmd.base_date
        match_dict = {}
    base_date = Date.from_string (base_date)
    if cmd.offset :
        base_date += cmd.offset
    if cmd.delta_to :
        print (base_date - cmd.delta_to).days
    else :
        date = base_date.formatted (cmd.format)
        print cmd.xformat % Scope (globs = match_dict, locls = vars ())
# end def _main

_Command = TFL.CAO.Cmd \
    ( handler     = _main
    , args        =
        ( "base_date:S=%s" % Date (),)
    , opts        =
        ( TFL.CAO.Opt.Date
            ( name        = "delta_to"
            , description = "Print `base_date - delta_to`"
            )
        , "-format:S=%Y%m%d?Format for date (not used for -delta_to)"
        , "-offset:I=0?delta to `base_date` in days"
        , "-regexp:S?Use regexp to extract date from `base_date`"
        , "-xformat:S=%(date)s"
            "?Format used to format output (not used for -delta_to)"
        )
    , max_args    = 1
    )

if __name__ != "__main__" :
    CAL._Export ("*")
else :
    _Command ()
### __END__ CAL.Date

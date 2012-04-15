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
#    CAL.Delta
#
# Purpose
#    Wrapper around `datetime.timedelta`
#
# Revision Dates
#    14-Oct-2004 (CT) Creation (`Delta` just an alias for `datetime.timedelta`)
#    17-Oct-2004 (CT) `Time_Delta`, `Date_Delta`, and `Date_Time_Delta`
#                     implemented
#    17-Oct-2004 (CT) `Month_Delta` added
#    17-Oct-2004 (CT) `Month_Delta` renamed to `MY_Delta` and `years` added
#    17-Oct-2004 (CT) Getters of `Time_Delta` renamed to `h`, `m`, and `s` to
#                     allow `seconds` to return `_body.seconds` unchanged
#    19-Oct-2004 (CT) s/MY_Delta/Month_Delta/
#    23-Oct-2004 (CT) `__neg__` added
#    25-Oct-2004 (CT) `__abs__` added
#    26-Oct-2004 (CT) `__abs__` changed to return `self` for positive values
#    12-Dec-2004 (CT) `_init_arg_map` added
#     7-Nov-2007 (CT) Use `Getter` instead of `lambda`
#     1-Jan-2008 (CT) `Time_Delta.hh_mm` added
#     3-May-2011 (CT) `from_string` added
#     3-May-2011 (CT) CAO argument/option types added for `Date_Delta`,
#                     `Date_Time_Delta`, and `Time_Delta`
#    15-Apr-2012 (CT) Fix `_from_string_match_kw` (use `+=` instead of `=` in
#                     `else` of `k.startswith ("sub")`)
#    ««revision-date»»···
#--

from   _CAL                     import CAL
from   _TFL                     import TFL

import _CAL._DTW_
import _TFL.Accessor
import _TFL.CAO
import _TFL.defaultdict

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Regexp              import *

import datetime
import operator

class _Delta_ (CAL._DTW_) :
    """Root class for delta classes"""

    @classmethod
    def from_string (cls, s) :
        match = cls.delta_pattern.match (s)
        if match :
            return cls (** cls._from_string_match_kw (s, match))
        else :
            raise ValueError, s
    # end def from_string

    @classmethod
    def _from_string_match_kw (cls, s, match) :
        assert match
        kw = TFL.defaultdict (int)
        for k, v in match.groupdict ().iteritems () :
            if v :
                if k.startswith ("sub") :
                    n = k [3:]
                    f = float ("0.%s" % v)
                    if n == "days" :
                        h, m   = divmod (f * 24 * 60, 60)
                        m, s   = divmod (m * 60,      60)
                        kw ["hours"]        += int (h)
                        kw ["minutes"]      += int (m)
                        kw ["seconds"]      += int (s)
                    elif n == "hours" :
                        m, s   = divmod (int (f * 3600), 60)
                        kw ["minutes"]      += int (m)
                        kw ["seconds"]      += int (s)
                    elif n == "minutes" :
                        s, us  = divmod (int (f * 60 * 1e6), 1e6)
                        kw ["seconds"]      += int (s)
                        kw ["microseconds"] += int (us)
                    elif n == "seconds" :
                        ms, us = divmod (int (f * 1e6), 1000)
                        kw ["milliseconds"] += int (ms)
                        kw ["microseconds"] += int (us)
                    elif n == "weeks" :
                        d, h   = divmod (f * 7 * 24,  24)
                        h, m   = divmod (h * 60,      60)
                        m, s   = divmod (m * 60,      60)
                        kw ["days"]         += int (d)
                        kw ["hours"]        += int (h)
                        kw ["minutes"]      += int (m)
                        kw ["seconds"]      += int (s)
                else :
                    kw [k] += int (v)
        return kw
    # end def _from_string_match_kw

# end class _Delta_

class _DT_Delta_ (_Delta_) :
    """Root class for datetime.timedelta wrapping classes"""

    _Type            = datetime.timedelta
    _kind            = "delta"
    _timetuple_slice = lambda s, tt : (0, ) * len (s._init_arg_names)

    Zero             = datetime.timedelta (0)

    def delta_op (self, rhs, op) :
        """Return result of `op` applied to `self` and delta `rhs`"""
        result = op (self._body, rhs._body)
        return self.__class__ (** {self._kind : result})
    # end def delta_op

    def dt_op (self, dot, op) :
        """Return result of `op` applied to date/time value `dot` and delta
           `self`
        """
        result = op (dot._body, self._body)
        return dot.__class__ (** {dot._kind : result})
    # end def dt_op

    def __abs__ (self) :
        if self._body < self.Zero :
            return self.__class__ (** {self._kind : abs (self._body)})
        return self
    # end def __abs__

    def __add__ (self, rhs) :
        if isinstance (rhs, _Delta_) :
            op = self.delta_op
        else :
            op = self.dt_op
        return op (rhs, operator.add)
    # end def __add__

    def __floordiv__ (self, rhs) :
        result = self._body / rhs
        return self.__class__ (** {self._kind : result})
    # end def __floordiv__

    def __mul__ (self, rhs) :
        result = self._body * rhs
        return self.__class__ (** {self._kind : result})
    # end def __mul__

    def __neg__ (self) :
        return self.__class__ (** {self._kind : - self._body})
    # end def __neg__

    def __sub__ (self, rhs) :
        if isinstance (rhs, _Delta_) :
            op = self.delta_op
        else :
            op = self.dt_op
        return op (rhs, operator.sub)
    # end def __sub__

# end class _DT_Delta_

class Time_Delta (_DT_Delta_) :
    """Model a time delta

    >>> t = Time_Delta (3)
    >>> print t
    3:00:00
    >>> t.h, t.m, t.s, t.seconds
    (3, 0, 0, 10800)
    >>> abs (t) is t
    True
    >>> abs (t) == t
    True
    >>> t = Time_Delta (-3)
    >>> abs (t) is t
    False
    >>> abs (t) == - t
    True
    >>> hms = Time_Delta (2, 15, 42)
    >>> print hms
    2:15:42
    >>> hms.h, hms.m, hms.s, hms.seconds
    (2, 15, 42, 8142)
    >>> md = Time_Delta (minutes = 42)
    >>> print md
    0:42:00

    >>> Time_Delta.from_string("7")
    Time_Delta (7, 0, 0, 0, 0)
    >>> Time_Delta.from_string("7:42")
    Time_Delta (7, 42, 0, 0, 0)
    >>> Time_Delta.from_string("7:42:37")
    Time_Delta (7, 42, 37, 0, 0)
    >>> Time_Delta.from_string("7:42:37.25")
    Time_Delta (7, 42, 37, 250, 0)
    >>> Time_Delta.from_string("7:42:37.00025")
    Time_Delta (7, 42, 37, 0, 250)
    >>> Time_Delta.from_string ("1.5h10.25m7.125s")
    Time_Delta (1, 40, 22, 125, 0)
    >>> Time_Delta.from_string ("1.5 hours 10.25 minutes 7.125 seconds")
    Time_Delta (1, 40, 22, 125, 0)
    """

    seconds          = property (TFL.Getter._body.seconds)
    microseconds     = property (TFL.Getter._body.microseconds)
    h                = property (lambda s : (s.seconds // 3600))
    m                = property (lambda s : (s.seconds  % 3600) // 60)
    s                = property (lambda s : (s.seconds  %   60))

    _init_arg_names  = \
        ("hours", "minutes", "seconds", "milliseconds", "microseconds")
    _init_arg_map    = dict \
        ( hours      = "h"
        , minutes    = "m"
        , seconds    = "s"
        )
    _kind            = "time_delta"

    delta_pattern    = Multi_Regexp \
        ( r"^"
          r"(?P<hours> \d{1,2})"
          r"(?:"
            r": (?P<minutes> \d{1,2})"
            r"(?:"
              r": (?P<seconds> \d{1,2}) (?: \. (?P<subseconds> \d+) )?"
            r")?"
          r")?"
          r"$"
        , r"^"
          r"(?: (?P<hours> \d+) (?: \. (?P<subhours> \d+) )? \s* h(?:ours?)?)?"
          r",?\s*"
          r"(?: (?P<minutes> \d+) (?: \. (?P<subminutes> \d+) )? \s* m(?:inutes?)?)?"
          r",?\s*"
          r"(?: (?P<seconds> \d+) (?: \. (?P<subseconds> \d+) )? \s* s(?:econds?)?)?"
          r"$"
        , flags = re.VERBOSE | re.IGNORECASE
        )

    def delta_op (self, rhs, op) :
        result = self.__super.delta_op (rhs, op)
        if result._body.days :
            raise OverflowError, result
        return result
    # end def delta_op

    @Once_Property
    def hh_mm (self) :
        """Return tuple of (hour, minute) with `minute` rounded."""
        hh = self.h
        mm = self.m + (self.s + 30) // 60
        if mm >= 60 :
            mm -= 60
            hh += 1
        return (hh, mm)
    # end def hh_mm

# end class Time_Delta

class Date_Delta (_DT_Delta_) :
    """Model a date delta

    >>> d = Date_Delta (42)
    >>> print d
    42 days, 0:00:00
    >>> d.days, d.weeks
    (42, 6)
    >>> d2 = Date_Delta (5)
    >>> x = d - d2
    >>> print x
    37 days, 0:00:00
    >>> x.__class__
    <class 'Delta.Date_Delta'>
    >>> t = Time_Delta (3)
    >>> s = d + t
    >>> print s
    42 days, 3:00:00
    >>> print s.__class__
    <class 'Delta.Date_Time_Delta'>
    >>> s.days, s.h, s.m, s.s
    (42, 3, 0, 0)
    >>> d3 = Date_Delta (weeks = 2, days = 5)
    >>> print d3
    19 days, 0:00:00
    >>> print d3.days, d3.weeks
    19 2
    >>> Date_Delta.from_string ("2.5 weeks")
    Date_Delta (3, 2)
    """

    days             = property (TFL.Getter._body.days)
    weeks            = property (lambda s : s._body.days // 7)

    _init_arg_names  = ("days", "weeks")
    _kind            = "date_delta"

    delta_pattern    = Multi_Regexp \
        ( r"^"
          r"(?P<days> \d+) (?: \. (?P<subdays>  \d+) )?"
          r"$"
        , r"^"
          r"(?: (?P<weeks> \d+) (?: \. (?P<subweeks> \d+) )? \s* w(?:eeks?)?)?"
          r",?\s*"
          r"(?: (?P<days>  \d+) (?: \. (?P<subdays>  \d+) )? \s* d(?:ays?)?)?"
          r"$"
        , flags = re.VERBOSE | re.IGNORECASE
        )

    def delta_op (self, rhs, op) :
        return self._date_time_delta_maybe (self.__super.delta_op (rhs, op))
    # end def delta_op

    def _date_time_delta_maybe (self, result) :
        if result._body.seconds or result._body.microseconds :
            result = Date_Time_Delta \
                (** {Date_Time_Delta._kind : result._body})
        return result
    # end def _date_time_delta_maybe

# end class Date_Delta

class Date_Time_Delta (Date_Delta, Time_Delta) :
    """Model a date_time delta

    >>> d = Date_Time_Delta (5, 8, 3, 33)
    >>> print d
    5 days, 8:03:33
    >>> d.days, d.h, d.m, d.s
    (5, 8, 3, 33)
    >>> d2 = Date_Time_Delta (days = 2, hours = 12)
    >>> print d2
    2 days, 12:00:00
    >>> print d2.days, d2.seconds
    2 43200
    >>> print d2.weeks
    0

    >>> Date_Time_Delta.from_string ("2")
    Date_Time_Delta (2, 0, 0, 0, 0, 0, 0)
    >>> Date_Time_Delta.from_string ("2.5 weeks")
    Date_Time_Delta (3, 12, 0, 0, 0, 0, 2)
    >>> print Date_Time_Delta.from_string ("2.5 weeks")
    17 days, 12:00:00
    >>> print Date_Time_Delta.from_string ("2.5 d")
    2 days, 12:00:00
    >>> print Date_Time_Delta.from_string ("2.5 d 15.25m")
    2 days, 12:15:15
    """

    _init_arg_names = ("days", ) + Time_Delta._init_arg_names + ("weeks", )
    _kind           = "date_time_delta"

    delta_op        = _DT_Delta_.delta_op

    delta_pattern    = Multi_Regexp \
        ( r"^"
          r"(?P<days> \d+)"
          r"(?: (?: , \s*  | \s* d(?:ays?)?)"
            r"(?P<hours> \d{1,2})"
            r"(?:"
              r": (?P<minutes> \d{1,2})"
              r"(?:"
                r": (?P<seconds> \d{1,2}) (?: \. (?P<subseconds> \d+) )?"
              r")?"
            r")?"
          r")?"
          r"$"
        , r"^"
          r"(?: (?P<weeks> \d+) (?: \. (?P<subweeks> \d+) )? \s* w(?:eeks?)?)?"
          r",?\s*"
          r"(?: (?P<days>  \d+) (?: \. (?P<subdays>  \d+) )? \s* d(?:ays?)?)?"
          r",?\s*"
          r"(?: (?P<hours> \d+) (?: \. (?P<subhours> \d+) )? \s* h(?:ours?)?)?"
          r",?\s*"
          r"(?: (?P<minutes> \d+) (?: \. (?P<subminutes> \d+) )? \s* m(?:inutes?)?)?"
          r",?\s*"
          r"(?: (?P<seconds> \d+) (?: \. (?P<subseconds> \d+) )? \s* s(?:econds?)?)?"
          r"$"
        , flags = re.VERBOSE | re.IGNORECASE
        )


# end class Date_Time_Delta

class Month_Delta (_Delta_) :
    """Model month-stepping delta

       >>> print Month_Delta (1)
       +1 month
       >>> print Month_Delta (2)
       +2 months
       >>> print Month_Delta (-3)
       -3 months
       >>> print Month_Delta (years = 1)
       +1 year
       >>> print Month_Delta (years = 5)
       +5 years
       >>> print Month_Delta (3, 1)
       +3 months, +1 year
       >>> print Month_Delta (1, 2)
       +1 month, +2 years
       >>> md = Month_Delta (13)
       >>> print md
       +1 month, +1 year
       >>> print md + 1
       +2 months, +1 year
       >>> md = Month_Delta (1)
       >>> abs (md) is md
       True
       >>> print abs (md)
       +1 month
       >>> md = Month_Delta (-1)
       >>> abs (md) is md
       False
       >>> abs (md) == -md
       True
       >>> print md, abs (md)
       -1 months +1 month
    """

    def __init__ (self, months = 0, years = 0) :
        self.months = months + years * 12
    # end def __init__

    def dt_op (self, date, op) :
        """Return result of `op` applied to date(_time) value `date` and delta
           `self`
        """
        yd, m = 0, date.month + self.months
        if m == 0 :
            yd, m = -1, 12
        elif not (1 <= m <= 12) :
            yd, m = divmod (m, 12)
        return date.replace (month = m, year = date.year + yd)
    # end def dt_op

    def __abs__ (self) :
        if self.months < 0 :
            return self.__class__ (abs (self.months))
        return self
    # end def __abs__

    def __add__ (self, rhs) :
        return self.__class__ (self.months + rhs)
    # end def __add__

    def __cmp__ (self, rhs) :
        try :
            rhs = rhs.months
        except AttributeError :
            pass
        return cmp (self.months, rhs)
    # end def __cmp__

    def __hash__ (self) :
        return hash (self.months)
    # end def __hash__

    def __neg__ (self) :
        return self.__class__ (months = - self.months)
    # end def __neg__

    def __str__ (self) :
        result = []
        sign   = cmp (self.months, 0)
        years, months = divmod (abs (self.months), 12)
        if months :
            months *= sign
            result.append ("%+d month%s" % (months, ("", "s") [months != 1]))
        if years :
            years  *= sign
            result.append ("%+d year%s"  % (years,  ("", "s") [years  != 1]))
        return ", ".join (result)
    # end def __str__

    def __sub__ (self, rhs) :
        return self.__class__ (self.months - rhs)
    # end def __sub__

# end class Month_Delta

Delta = Date_Time_Delta

class _Delta_Arg_ (TFL.CAO.Str) :
    """Argument or option with a (calendary) date or time delta value"""

    def cook (self, value, cao = None) :
        return self.D_Type.from_string (value)
    # end def cook

# end class _Delta_Arg_

class _Date_Delta_Arg_ (_Delta_Arg_) :
    """Argument or option with a (calendary) date-delta value"""

    _real_name = "Date_Delta"
    D_Type     = Date_Delta

# end class _Date_Delta_Arg_

class _Date_Time_Delta_Arg_ (_Delta_Arg_) :
    """Argument or option with a (calendary) datetime-delta value"""

    _real_name = "Date_Time_Delta"
    D_Type     = Date_Time_Delta

# end class _Date_Time_Delta_Arg_

class _Time_Delta_Arg_ (_Delta_Arg_) :
    """Argument or option with a (calendary) time-delta value"""

    _real_name = "Time_Delta"
    D_Type     = Time_Delta

# end class _Time_Delta_Arg_

if __name__ != "__main__" :
    CAL._Export ("*", "_Delta_", "Delta")
### __END__ CAL.Delta

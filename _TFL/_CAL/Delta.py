# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Mag. Christian Tanzer. All rights reserved
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
#    TFL.CAL.Delta
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
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._CAL._DTW_

import datetime
import operator

class _Delta_ (TFL.CAL._DTW_) :
    """Root class for delta classes"""

# end class _Delta_

class _DT_Delta_ (_Delta_) :
    """Root class for datetime.timedelta wrapping classes"""

    _Type            = datetime.timedelta
    _kind            = "delta"
    _timetuple_slice = lambda s, tt : (0, ) * len (s._init_arg_names)

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
       >>> hms = Time_Delta (2, 15, 42)
       >>> print hms
       2:15:42
       >>> hms.h, hms.m, hms.s, hms.seconds
       (2, 15, 42, 8142)
    """

    seconds          = property (lambda s : s._body.seconds)
    microseconds     = property (lambda s : s._body.microseconds)
    h                = property (lambda s : (s.seconds // 3600))
    m                = property (lambda s : (s.seconds  % 3600) // 60)
    s                = property (lambda s : (s.seconds  %   60))

    _init_arg_names  = \
        ("hours", "minutes", "seconds", "milliseconds", "microseconds")
    _kind            = "time_delta"

    def delta_op (self, rhs, op) :
        result = self.__super.delta_op (rhs, op)
        if result._body.days :
            raise OverflowError, result
        return result
    # end def delta_op

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
    """

    days             = property (lambda s : s._body.days)
    weeks            = property (lambda s : s._body.days // 7)

    _init_arg_names  = ("days", "weeks")
    _kind            = "date_delta"

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
    """

    _init_arg_names = ("days", ) + Time_Delta._init_arg_names + ("weeks", )
    _kind           = "date_time_delta"

    delta_op        = _DT_Delta_.delta_op

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

if __name__ != "__main__" :
    TFL.CAL._Export ("*", "_Delta_", "Delta")
### __END__ TFL.CAL.Delta

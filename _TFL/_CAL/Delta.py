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
       >>> t.hours, t.minutes, t.seconds
       (3, 0, 0)
       >>> hms = Time_Delta (2,15,42)
       >>> print hms
       2:15:42
       >>> hms.hours, hms.minutes, hms.seconds
       (2, 15, 42)
    """

    seconds          = property (lambda s : s._body.seconds % 60)
    microseconds     = property (lambda s : s._body.microseconds)
    milliseconds     = property (lambda s : s._body.microseconds // 1000)
    hours            = property (lambda s : s._body.seconds // 3600)
    minutes          = property (lambda s : (s._body.seconds % 3600) // 60)

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
       >>> s.days, s.hours, s.minutes, s.seconds
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
       >>> d.days, d.hours, d.minutes, d.seconds
       (5, 8, 3, 33)
    """

    _init_arg_names = ("days", ) + Time_Delta._init_arg_names + ("weeks", )
    _kind           = "date_time_delta"

    delta_op        = _DT_Delta_.delta_op

# end class Date_Time_Delta

class Month_Delta (_Delta_) :
    """Model month-stepping delta"""

    def __init__ (self, months) :
        self.months = months
    # end def __init__

    def dt_op (self, date, op) :
        """Return result of `op` applied to date(_time) value `date` and delta
           `self`
        """
        if date.day > 28 :
            raise OverflowError, \
                ( "Cannot increase/decrease %s by %s months"
                % (date, self.months)
                )
        yd, m = divmod (date.month + self.months, 12)
        return date.replace (month = m, year = date.year + yd)
    # end def dt_op

    def __cmp__ (self, rhs) :
        return cmp (self.months, getattr (rhs, "months", rhs))
    # end def __cmp__

    def __hash__ (self) :
        return self.months
    # end def __hash__

    def __str__ (self) :
        result = "%+d month" % (self.months)
        if self.months != 1 :
            result += "s"
        return result
    # end def __str__

# end class Month_Delta

if __name__ != "__main__" :
    TFL.CAL._Export ("*", "_Delta_")
### __END__ TFL.CAL.Delta

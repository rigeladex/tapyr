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
#    TFL.CAL.Date
#
# Purpose
#    Wrapper around `datetime.date`
#
# Revision Dates
#    14-Oct-2004 (CT) Creation
#                     (derived from MG's TFL.CAL.Date_Time and CT's Date_Time)
#    17-Oct-2004 (CT) `__add__` and `__sub__` changed to use `Delta.dt_op`
#    17-Oct-2004 (CT) Doctest for `Month_Delta` added
#    17-Oct-2004 (CT) s/Month_Delta/MY_Delta/
#    19-Oct-2004 (CT) s/MY_Delta/Month_Delta/
#    23-Oct-2004 (CT) `_default_format` added
#    23-Oct-2004 (CT) `_new_object` redefined to handle negative values for
#                     `day`
#    26-Oct-2004 (CT) `is_weekday` added
#    ««revision-date»»···
#--

from   _TFL                    import TFL
import _TFL._CAL._DTW_

import datetime
import operator

class Date (TFL.CAL._DTW_) :
    """Model a (gregorian) date.

       >>> from _TFL._CAL.Delta import Date_Delta as Delta
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
       >>> from _TFL._CAL.Delta import Month_Delta
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
    """

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

    day              = property (lambda s : s._body.day)
    is_weekday       = property (lambda s : s.weekday < 5)
    month            = property (lambda s : s._body.month)
    year             = property (lambda s : s._body.year)

    yad              = None ### set for negative `day` arguments

    from _TFL._CAL.Delta import Date_Delta as Delta

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

    def _day_from_end (self, yad, month, year) :
        from _TFL._CAL.Year import Year
        return Year (year).mmap [month].days [yad].number
    # end def _day_from_end

    def _new_object (self, ** kw) :
        d = kw ["day"]
        if d < 0 :
            kw ["day"] = self._day_from_end (d, kw ["month"], kw ["year"])
            self.yad   = d
        return self.__super._new_object (** kw)
    # end def _new_object

    def __getattr__ (self, name) :
        if name == "month_name" :
            result = self.month_name = self.strftime ("%b")
        elif name == "ordinal" :
            result = self.ordinal = self._body.toordinal ()
        elif name == "rjd" :
            result = self.rjd = self._body.timetuple ().tm_yday
        elif name == "tuple" :
            result = self.tuple = self._body.timetuple ()
        elif name == "week" :
            result = self.week = self._body.isocalendar () [1]
        elif name == "weekday" :
            result = self.weekday = self._body.weekday ()
        else :
            raise AttributeError, name
        return result
    # end def __getattr__

    def __add__ (self, rhs) :
        delta  = self._delta (rhs)
        return delta.dt_op (self, operator.add)
    # end def __add__

    def __sub__ (self, rhs) :
        delta = self._delta (rhs)
        if isinstance (delta, TFL.CAL._Delta_) :
            result = delta.dt_op (self, operator.sub)
        else :
            if hasattr (rhs, "_body") :
                rhs = rhs._body
            result = self.Delta (** {self.Delta._kind : self._body - rhs})
        return result
    # end def __sub__

# end class Date

class Date_M (TFL.CAL._Mutable_DTW_) :
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

if __name__ != "__main__" :
    TFL.CAL._Export ("*")
### __END__ TFL.CAL.Date

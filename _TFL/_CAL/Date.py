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
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _TFL._CAL.Delta         import Delta
import _TFL._CAL._DTW_

import  datetime

class Date (TFL.CAL._DTW_) :
    """Model a (gregorian) date.

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
       >>> d1 = Date (2004, 10, 14)
       >>> d2 = Date (2004, 10, 16)
       >>> d1 - d2
       datetime.timedelta(-2)
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

    day_per_month   = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    _Type            = datetime.date
    _init_arg_names  = ("year", "month", "day")
    _kind            = "date"
    _timetuple_slice = lambda s, tt : tt [:3]

    year             = property (lambda s : s._body.year)
    month            = property (lambda s : s._body.month)
    day              = property (lambda s : s._body.day)

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
        result = self._body + delta
        if isinstance (delta, TFL.CAL.Delta) :
            result = self.__class__ (** {self._kind : result})
        return result
    # end def __add__

    def __sub__ (self, rhs) :
        delta  = self._delta (rhs)
        result = self._body - delta
        if isinstance (delta, TFL.CAL.Delta) :
            result = self.__class__ (** {self._kind : result})
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

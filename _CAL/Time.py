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
#    CAL.Time
#
# Purpose
#    Wrapper around `datetime.time`
#
# Revision Dates
#    15-Oct-2004 (CT) Creation
#    17-Oct-2004 (CT) `Time.Delta` defined as `Time_Delta`
#    17-Oct-2004 (CT) Adapted to renaming of accessor-functions of `Time_Delta`
#    30-Nov-2006 (CT) `__getattr__` for `seconds` added
#     7-Nov-2007 (CT) Use `Getter` instead of `lambda`
#    ««revision-date»»···
#--

from   _CAL                    import CAL
from   _TFL                    import TFL
import _CAL._DTW_
import _TFL.Accessor

import  datetime

class Time (CAL._DTW_) :
    """Model a time object.

       >>> t1 = Time (21, 35, 12)
       >>> print t1
       21:35:12
       >>> t1.hour, t1.minute, t1.second, t1.time
       (21, 35, 12, datetime.time(21, 35, 12))
       >>> t2 = Time (22, 47, 13)
       >>> print t2
       22:47:13
       >>> t1 = Time (14, 30, 0)
       >>> t2 = Time (16, 30, 0)
       >>> d  = t2 - t1
       >>> print d
       2:00:00
       >>> print t2 + d
       18:30:00
       >>> from _CAL.Delta import Time_Delta as Delta
       >>> try :
       ...     t1 + Delta (hours = 10)
       ... except OverflowError, exc :
       ...     print exc
       ...
       1 day, 0:30:00
    """

    _Type            = datetime.time
    _default_format  = "%T"
    _kind            = "time"
    _init_arg_names  = ("hour", "minute", "second", "microsecond")
    _timetuple_slice = lambda s, tt : tt [3:6] + (0, )

    hour             = property (TFL.Getter._body.hour)
    minute           = property (TFL.Getter._body.minute)
    second           = property (TFL.Getter._body.second)
    microsecond      = property (TFL.Getter._body.microsecond)

    from _CAL.Delta import Time_Delta as Delta

    def as_delta (self) :
        return self.Delta \
            ( hours = self.hour, minutes = self.minute, seconds = self.second
            , microseconds = self.microsecond
            )
    # end def as_delta

    def __getattr__ (self, name) :
        if name == "seconds" :
            result = self.hour * 3600 + self.minute * 60 + self.second
            if self.microsecond :
                result += (self.microsecond / 1000.)
            self.seconds = result
        else :
            result = self.__super.__getattr__ (name)
        return result
    # end def __getattr__

    def __add__ (self, rhs) :
        result = self.as_delta () + self._delta (rhs)
        return self.__class__ \
            (result.h, result.m, result.s, result.microseconds)
    # end def __add__

    def __sub__ (self, rhs) :
        return self.as_delta () - rhs.as_delta ()
    # end def __sub__

# end class Time

if __name__ != "__main__" :
    CAL._Export ("*")
### __END__ CAL.Time

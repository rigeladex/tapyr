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
#    TFL.CAL.Time
#
# Purpose
#    Wrapper around `datetime.time`
#
# Revision Dates
#    15-Oct-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                    import TFL
from   _TFL._CAL.Delta         import Delta
import _TFL._CAL._DTW_

import  datetime

class Time (TFL.CAL._DTW_) :
    """Model a time object.

       >>> t1 = Time (21, 35, 12)
       >>> print t1
       21:35:12
       >>> t1.hour, t1.minute, t1.second, t1.time
       (21, 35, 12, datetime.time(21, 35, 12))
       >>> t2 = Time (22, 47, 13)
       >>> print t2
       22:47:13
    """

    _Type            = datetime.time
    _init_arg_names  = ("hour", "minute", "second")
    _kind            = "time"
    _timetuple_slice = lambda s, tt : tt [3:6]

    hour             = property (lambda s: s._body.hour)
    minute           = property (lambda s: s._body.minute)
    second           = property (lambda s: s._body.second)
    microsecond      = property (lambda s: s._body.microsecond)

# end class Time

if __name__ != "__main__" :
    TFL.CAL._Export ("*")
### __END__ TFL.CAL.Time

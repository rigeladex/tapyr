# -*- coding: utf-8 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.RFC2822_date
#
# Purpose
#    Convert between `datetime` objects and strings formatted according to
#    RFC2822
#
# Revision Dates
#    12-Jun-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL        import TFL

from   email.utils import parsedate_tz
import datetime

def as_string (dt) :
    """Format datetime instance `dt` according to RFC2822.

    >>> print (as_string (datetime.datetime (2001, 11, 8, 20, 8, 47)))
    08 Nov 2001 20:08:47 -0000
    """
    result = dt.strftime ("%d %b %Y %H:%M:%S %z")
    if dt.utcoffset () is None :
        result += "-0000"
    return result
# end def as_string

def from_string (s) :
    """Convert `s` formatted according to RFC2822 into a datetime instance.

    >>> from_string ("Fri, 09 Nov 2001 01:08:47 -0000")
    datetime.datetime(2001, 11, 9, 1, 8, 47)

    >>> from_string ("Fri, 09 Nov 2001 01:08:47 -0500")
    datetime.datetime(2001, 11, 8, 20, 8, 47)

    >>> from_string ("24 Dez 2001 08:42:37 -0100")
    Traceback (most recent call last):
      ...
    ValueError: 24 Dez 2001 08:42:37 -0100

    """
    tt = parsedate_tz (s)
    if tt is not None :
        utc_offset = tt [-1]
        result     = datetime.datetime (* tt [:6])
        if utc_offset :
            result += datetime.timedelta (seconds = utc_offset)
        return result
    else :
        raise ValueError (s)
# end def from_string

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.RFC2822_date

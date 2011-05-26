# -*- coding: iso-8859-15 -*-
# Copyright (C) 2004-2007 Mag. Christian Tanzer. All rights reserved
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
#    JD
#
# Purpose
#    Compute `julian day number` for a given date
#
# Revision Dates
#     5-Jun-2004 (CT) Creation
#    11-Aug-2007 (CT) U_Test ballast removed
#    ««revision-date»»···
#--

"""A julian day number is a continuous count of days from the beginning of
the year -4712. By (astronomical) tradition, the Julian Day begins at
Greenwhich mean noon, that is, at 12h Universal Time.

see Jean Meeus, Astronomical Algorithms, 1991, 1998
"""

def JD (d, m, y) :
    """Returns Julian Day number for year `y`, month `m`, and day `d`."""
    if m <= 2 :
        y -= 1
        m += 12
    if (y, m, d) >= (1582, 10, 15) :
        a = int (y / 100)
        b = 2 - a + int (a / 4)
    else :
        b = 0
    jd = int (365.25  * (y + 4716)) + int (30.6001 * (m + 1)) + d + b - 1524.5
    return jd
# end def JD

if __name__ != "__main__" :
    from _CAL import CAL
    CAL._Export ("JD")
### __END__ JD

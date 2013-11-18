# -*- coding: utf-8 -*-
# Copyright (C) 2004-2013 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Units.Volume
#
# Purpose
#    Volume units
#
# Revision Dates
#     8-Aug-2004 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.Object
import _TFL._Units.Kind
import _TFL._Units.Length

class Volume (TFL.Units.Kind) :
    """Units of volume

       >>> Volume (1.0)
       1
       >>> Volume (1.0, "cbkm")
       1000000000
       >>> Volume (1.0, "cbin")
       1.6387064e-05
       >>> Volume (1.0, "cbft")
       0.028316846592
       >>> Volume (1.0, "cbyd")
       0.764554857984
       >>> Volume (1.0, "cbmi")
       4168181825.44
    """

    Length            = TFL.Units.Length
    Unit              = TFL.Units.Unit

    base_unit         = Unit ("cubic_meter", 1.0, "cbm")
    _units            = \
        (
        # SI prefixes
          Unit ("cubic_nanometer",  Length.nanometer    ** 3, "cbnm")
        , Unit ("cubic_micrometer", Length.micrometer   ** 3, "cbum")
        , Unit ("cubic_millimeter", Length.millimeter   ** 3, "cbmm")
        , Unit ("cubic_centimeter", Length.centimeter   ** 3, "cbcm")
        , Unit ("cubic_decimeter",  Length.decimeter    ** 3, "cbdm")
        , Unit ("cubic_dekameter",  Length.dekameter    ** 3, "cbdam")
        , Unit ("cubic_hectometer", Length.hectometer   ** 3, "cbhm")
        , Unit ("cubic_kilometer",  Length.kilometer    ** 3, "cbkm")
        # US customary units
        , Unit ("cubic_inch",       Length.inch         ** 3, "cbin")
        , Unit ("cubic_foot",       Length.foot         ** 3, "cbft")
        , Unit ("cubic_yard",       Length.yard         ** 3, "cbyd")
        , Unit ("cubic_mile",       Length.statute_mile ** 3, "cbmi")
        )

# end class Volume

if __name__ != "__main__" :
    TFL.Units._Export ("*")
### __END__ TFL.Units.Volume

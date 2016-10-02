# -*- coding: utf-8 -*-
# Copyright (C) 2007-2016 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
# ****************************************************************************
#
#++
# Name
#    CAL.Sky.Location
#
# Purpose
#    Model terrestrial location of observer
#
# Revision Dates
#    14-Nov-2007 (CT) Creation
#    13-May-2016 (CT) Add `__str__`
#    29-Sep-2016 (CT) Improve support for `height`
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
from   __future__  import unicode_literals

from   _CAL                     import CAL
from   _TFL                     import TFL
from   _TFL.pyk                 import pyk

import _CAL._Sky
import _TFL._Meta.Object

from   _TFL.Angle               import Angle_D, Angle_R

@pyk.adapt__str__
class Location (TFL.Meta.Object) :
    """Model terrestrial location of observer."""

    Table = {}

    def __init__ (self, latitude, longitude, name = None, height = None) :
        self.latitude  = self._normalized (latitude)
        self.longitude = self._normalized (longitude)
        self.name      = name
        self.height    = 0 if height is None else height
        if name is not None :
            Table      = self.Table
            assert name not in Table
            Table [name] = self
            if name [0].isupper :
                setattr (Location, name, self)
    # end def __init__

    def _normalized (self, value) :
        if isinstance (value, (list, tuple)) :
            result = Angle_D.normalized (* value)
        elif not isinstance (value, (Angle_D, Angle_R)) :
            result = Angle_D.normalized (value)
        else :
            result = value
        return result
    # end def _normalized

    def __str__ (self) :
        lon    = self.longitude
        lat    = self.latitude
        if lon.degrees > 180.0 :
            lon -= 360.0
        result = "%s %s, %s %s" % \
            ( abs (lon), "E" if lon.degrees < 0.0 else "W"
            , abs (lat), "S" if lat.degrees < 0.0 else "N"
            )
        if self.height :
            result = "%s, %2.0fm above sea level" % (result, self.height)
        if self.name :
            result = "%s [%s]" % (self.name, result)
        return result
    # end def __str__

# end class Location

Location (Angle_D (48, 14),     Angle_D (-16, -22),     "Vienna",     180)
Location (Angle_D (37, 51,  7), Angle_D (  8,  47, 31), "Porto Covo",  25)

if __name__ != "__main__" :
    CAL.Sky._Export ("*")
### __END__ Location

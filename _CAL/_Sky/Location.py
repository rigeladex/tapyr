# -*- coding: utf-8 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
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
#    ««text»»···
#
# Revision Dates
#    14-Nov-2007 (CT) Creation
#--

from   _CAL                     import CAL
from   _TFL                     import TFL

import _CAL._Sky
import _TFL._Meta.Object

from   _TFL.Angle               import Angle_D, Angle_R

class Location (TFL.Meta.Object) :
    """Model terrestrial location of observer."""

    Table = {}

    def __init__ (self, latitude, longitude, name = None, height = None) :
        self.latitude  = self._normalized (latitude)
        self.longitude = self._normalized (longitude)
        self.name      = name
        self.height    = height
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

# end class Location

Location (Angle_D (48, 14), Angle_D (-16, -22), "Vienna")

if __name__ != "__main__" :
    CAL.Sky._Export ("*")
### __END__ Location



# -*- coding: iso-8859-1 -*-
# Copyright (C) 2007 Mag. Christian Tanzer. All rights reserved
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
#    TFL.Angle
#
# Purpose
#    Model angles
#
# Revision Dates
#    12-Nov-2007 (CT) Creation
#    30-Nov-2007 (CT) Moved to TFL
#    ««revision-date»»···
#--

from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property
import _TFL._Meta.Object

import math

class _Angle_ (TFL.Meta.Object) :
    """Model an angle"""

    two_pi = 2 * math.pi

    @classmethod
    def acos (cls, x) :
        """Arc cosine of `x`."""
        return Angle_R (math.acos (x))
    # end def acos

    @classmethod
    def asin (cls, x) :
        """Arc sine of `x`."""
        return Angle_R (math.asin (x))
    # end def asin

    @classmethod
    def atan (cls, x) :
        """Arc tangent of `x`."""
        return Angle_R (math.atan (x))
    # end def atan

    @classmethod
    def atan2 (cls, y, x) :
        """Arc tangent of `y / x`."""
        return Angle_R (math.atan2 (y, x))
    # end def atan

    @Once_Property
    def cos (self) :
        """Cosine of angle."""
        return math.cos (self.radians)
    # end def cos

    @Once_Property
    def minutes (self) :
        d = self.degrees
        return int ((d - int (d)) * 60.0)
    # end def minutes

    @Once_Property
    def seconds (self) :
        d = self.degrees
        m = (d - int (d)) * 60.0
        return (m - int (m)) * 60.0
    # end def seconds

    @Once_Property
    def sin (self) :
        """Sine of angle."""
        return math.sin (self.radians)
    # end def sin

    @Once_Property
    def tan (self) :
        """Tangent of angle."""
        return math.tan (self.radians)
    # end def tan

    @Once_Property
    def tuple (self) :
        d = self.degrees
        return (int (d), self.minutes, self.seconds)
    # end def tuple

    def __add__ (self, rhs) :
        return self.__class__ (float (self) + getattr (rhs, self.name, rhs))
    # end def __add__

    def __cmp__ (self, rhs) :
        r = getattr (rhs, "degrees", rhs)
        return cmp (self.degrees, r)
    # end def __cmp__

    def __div__ (self, rhs) :
        assert not isinstance (rhs, _Angle_)
        return self.__class__ (float (self) / rhs)
    # end def __div__

    def __hash__ (self) :
        return hash (self.degrees)
    # end def __hash__

    def __mul__ (self, rhs) :
        assert not isinstance (rhs, _Angle_)
        return self.__class__ (float (self) * rhs)
    # end def __mul__

    def __repr__ (self) :
        return "%s (%s)" % (self.__class__.__name__, float (self))
    # end def __repr__

    def __str__ (self) :
        return "%3.3d°%2.2d'%2.2d''" % self.tuple
    # end def __str__

    def __sub__ (self, rhs) :
        return self.__class__ (float (self) - getattr (rhs, self.name, rhs))
    # end def __sub__

# end class _Angle_

class Angle_D (_Angle_) :
    """Model an angle specified in degrees.

       >>> print Angle_D (45)
       045°00'00''
       >>> print Angle_D (45.5)
       045°30'00''
       >>> print Angle_D (45, 20, 40)
       045°20'40''
       >>> Angle_D (45)
       Angle_D (45.0)
       >>> Angle_D (45, 30)
       Angle_D (45.5)
       >>> Angle_D (45, 30, 36)
       Angle_D (45.51)
       >>> a = Angle_D (45)
       >>> a.radians
       0.78539816339744828
       >>> a.sin, a.cos, a.tan
       (0.70710678118654746, 0.70710678118654757, 0.99999999999999989)
    """

    name = "degrees"

    def __init__ (self, degrees = 0.0, minutes = 0, seconds = 0) :
        self.degrees = d = (degrees + minutes / 60. + seconds / 3600.)
    # end def __init__

    @classmethod
    def normalized (cls, degrees) :
        return cls (degrees % 360.0)
    # end def normalized

    @Once_Property
    def radians (self) :
        return math.radians (self.degrees)
    # end def radians

    def __float__ (self) :
        return self.degrees
    # end def __float__

# end class Angle_D

class Angle_R (_Angle_) :
    """Model an angle specified in radians.

       >>> b = Angle_R (0.78539816339744828)
       >>> b.degrees
       45.0
       >>> b.sin, b.cos, b.tan
       (0.70710678118654746, 0.70710678118654757, 0.99999999999999989)
       >>> Angle_R.asin (b.sin)
       Angle_R (0.785398163397)
       >>> Angle_D.asin (b.sin)
       Angle_R (0.785398163397)
       >>> Angle_R.asin (b.sin).degrees
       44.999999999999993
    """

    name = "radians"

    def __init__ (self, radians = 0.0) :
        self.radians = radians
    # end def __init__

    @Once_Property
    def degrees (self) :
        return math.degrees (self.radians)
    # end def degrees

    def __float__ (self) :
        return self.radians
    # end def __float__

# end class Angle_R

if __name__ == "__main__" :
    TFL._Export ("*", "_Angle_")
### __END__ TFL.Angle

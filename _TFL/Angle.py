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
#    TFL.Angle
#
# Purpose
#    Model angles
#
# Revision Dates
#    12-Nov-2007 (CT) Creation
#    30-Nov-2007 (CT) Moved to TFL
#    17-Jun-2010 (CT) `__unicode__` introduced
#    23-Dec-2010 (CT) Doctest fixed (don't use `repr` of floating point numbers)
#    13-Oct-2014 (CT) Use `portable_repr`
#    16-Oct-2015 (CT) Add `__future__` imports
#    13-May-2016 (CT) Add `__abs__`, `__gt__`
#    ««revision-date»»···
#--

from   __future__  import absolute_import
from   __future__  import division
from   __future__  import print_function
### importing `unicode_literals` from `__future__` wrecks 2.7 doctest

from   _TFL                       import TFL

from   _TFL.portable_repr         import portable_repr
from   _TFL.pyk                   import pyk
from   _TFL._Meta.Once_Property   import Once_Property
from   _TFL._Meta.totally_ordered import totally_ordered

import _TFL._Meta.Object

import math

@totally_ordered
@pyk.adapt__div__
@pyk.adapt__str__
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

    def __eq__ (self, rhs) :
        r = getattr (rhs, "degrees", rhs)
        return self.degrees == r
    # end def __eq__

    def __floordiv__ (self, rhs) :
        assert not isinstance (rhs, _Angle_)
        return self.__class__ (int (self) // rhs)
    # end def __floordiv__

    def __gt__ (self, rhs) :
        r = getattr (rhs, "degrees", rhs)
        return self.degrees > r
    # end def __gt__

    def __hash__ (self) :
        return hash (self.degrees)
    # end def __hash__

    def __lt__ (self, rhs) :
        r = getattr (rhs, "degrees", rhs)
        return self.degrees < r
    # end def __lt__

    def __mul__ (self, rhs) :
        assert not isinstance (rhs, _Angle_)
        return self.__class__ (float (self) * rhs)
    # end def __mul__

    def __repr__ (self) :
        return "%s (%s)" % \
            (self.__class__.__name__, portable_repr (float (self)))
    # end def __repr__

    def __str__ (self) :
        return u"%3.3d°%2.2d'%2.2d''" % self.tuple
    # end def __str__

    def __sub__ (self, rhs) :
        return self.__class__ (float (self) - getattr (rhs, self.name, rhs))
    # end def __sub__

    def __truediv__ (self, rhs) :
        assert not isinstance (rhs, _Angle_)
        return self.__class__ (float (self) / rhs)
    # end def __truediv__

# end class _Angle_

class Angle_D (_Angle_) :
    """Model an angle specified in degrees.

       >>> print (Angle_D (45))
       045°00'00''
       >>> print (Angle_D (45.5))
       045°30'00''
       >>> print (Angle_D (45, 20, 40))
       045°20'40''
       >>> Angle_D (45)
       Angle_D (45)
       >>> Angle_D (45, 30)
       Angle_D (45.5)
       >>> Angle_D (45, 30, 36)
       Angle_D (45.51)
       >>> a = Angle_D (45)
       >>> print ("%14.12f" % a.radians)
       0.785398163397
       >>> print ("%14.12f %14.12f %14.1f" % (a.sin, a.cos, a.tan))
       0.707106781187 0.707106781187 1.0

       >>> a < 30, a > 30, a < 60, a > 60
       (False, True, True, False)

       >>> a <= 30, a >= 30, a <= 60, a >= 60
       (False, True, True, False)

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

    def __abs__ (self) :
        """Absolute value of angle"""
        return self.__class__ (abs (self.degrees))
    # end def __abs__

    def __float__ (self) :
        return self.degrees
    # end def __float__

    def __int__ (self) :
        return int (self.degrees)
    # end def __int__

# end class Angle_D

class Angle_R (_Angle_) :
    """Model an angle specified in radians.

       >>> b = Angle_R (0.78539816339744828)
       >>> b.degrees
       45.0
       >>> print ("%14.12f %14.12f %14.1f" % (b.sin, b.cos, b.tan))
       0.707106781187 0.707106781187 1.0
       >>> br = Angle_R.asin (b.sin)
       >>> print ("%s (%14.12f)" % (br.__class__.__name__, br))
       Angle_R (0.785398163397)
       >>> bd = Angle_D.asin (b.sin)
       >>> print ("%s (%14.12f)" % (bd.__class__.__name__, bd))
       Angle_R (0.785398163397)
       >>> print ("%14.1f" % Angle_R.asin (b.sin).degrees)
       45.0
    """

    name = "radians"

    def __init__ (self, radians = 0.0) :
        self.radians = radians
    # end def __init__

    @Once_Property
    def degrees (self) :
        return math.degrees (self.radians)
    # end def degrees

    def __abs__ (self) :
        """Absolute value of angle"""
        return self.__class__ (abs (self.radians))
    # end def __abs__

    def __float__ (self) :
        return self.radians
    # end def __float__

    def __int__ (self) :
        return int (self.radians)
    # end def __int__

# end class Angle_R

if __name__ == "__main__" :
    TFL._Export ("*", "_Angle_")
### __END__ TFL.Angle

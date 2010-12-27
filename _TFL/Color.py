# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Color
#
# Purpose
#    Model colors in RGB or HSL representation
#
# Revision Dates
#    26-Dec-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL                     import TFL

from   _TFL._Meta.Once_Property import Once_Property

import _TFL._Meta.Object
import _TFL.Regexp

from   collections import namedtuple

RGB_Value = namedtuple ("RGB", ("red", "green", "blue"))
HSL_Value = namedtuple ("HSL", ("hue", "saturation", "lightness"))

class Value (TFL.Meta.Object) :
    """Model an immutable color value.

       >>> white_1 = Value (rgb = (1.0, 1.0, 1.0))
       >>> white_1
       Value (rgb = (1.0, 1.0, 1.0))
       >>> white_1.rgb, white_1.hsl
       (RGB(red=1.0, green=1.0, blue=1.0), HSL(hue=0.0, saturation=0.0, lightness=1.0))

       >>> white_2 = Value (hsl = (0.0, 0.0, 1.0))
       >>> white_2
       Value (hsl = (0.0, 0.0, 1.0))
       >>> white_2.rgb, white_2.hsl
       (RGB(red=1.0, green=1.0, blue=1.0), HSL(hue=0.0, saturation=0.0, lightness=1.0))

       >>> white_1 == white_2
       True

       >>> grey50 = Value (rgb = (0.5, 0.5, 0.5))
       >>> grey50.rgb, grey50.hsl
       (RGB(red=0.5, green=0.5, blue=0.5), HSL(hue=0.0, saturation=0.0, lightness=0.5))

       >>> black = Value (rgb = (0.0, 0.0, 0.0))
       >>> black.rgb, black.hsl
       (RGB(red=0.0, green=0.0, blue=0.0), HSL(hue=0.0, saturation=0.0, lightness=0.0))

       >>> red = Value (hsl = (0.0, 1.0, 0.5))
       >>> red.rgb, red.hsl
       (RGB(red=1.0, green=0.0, blue=0.0), HSL(hue=0.0, saturation=1.0, lightness=0.5))

       >>> Value (rgb = (0.750, 0.750, 0.000)) == Value (hsl = ( 60.0, 1.000, 0.375))
       True
       >>> Value (rgb = (0.000, 0.500, 0.000)) == Value (hsl = (120.0, 1.000, 0.250))
       True
       >>> Value (rgb = (0.500, 1.000, 1.000)) == Value (hsl = (180.0, 1.000, 0.750))
       True
       >>> Value (rgb = (0.500, 0.500, 1.000)) == Value (hsl = (240.0, 1.000, 0.750))
       True
       >>> Value (rgb = (0.750, 0.250, 0.750)) == Value (hsl = (300.0, 0.500, 0.500))
       True
    """

    Table_HSL = {}
    Table_RGB = {}

    _hsl      = None
    _rgb      = None

    def __new__ (cls, rgb = None, hsl = None) :
        if rgb is None :
            result = cls.from_hsl (hsl)
        else :
            assert hsl is None
            if isinstance (rgb, HSL_Value) :
                result = cls.from_hsl (rgb)
            else :
                result = cls.from_rgb (rgb)
        return result
    # end def __new__

    @classmethod
    def clear (cls) :
        """Clear the caches `Table_HSL` and `Table_RGB`."""
        cls.Table_HSL.clear ()
        cls.Table_RGB.clear ()
    # end def clear

    @classmethod
    def from_hsl (cls, hsl) :
        assert hsl
        hsl = HSL_Value (* hsl)
        if hsl in cls.Table_HSL :
            result = cls.Table_HSL [hsl]
        else :
            result = cls.Table_HSL [hsl] = super (Value, cls).__new__ (cls)
            result._hsl = hsl
        return result
    # end def from_hsl

    @classmethod
    def from_rgb (cls, rgb) :
        assert rgb
        rgb = RGB_Value (* rgb)
        if rgb in cls.Table_RGB :
            result = cls.Table_RGB [rgb]
        else :
            result = cls.Table_RGB [rgb] = super (Value, cls).__new__ (cls)
            result._rgb = rgb
        return result
    # end def from_rgb

    @Once_Property
    def hsl (self) :
        if self._hsl is None :
            r, g, b   = rgb = self._rgb
            M  = max (rgb)
            m  = min (rgb)
            c  = M - m
            if c == 0 :
                h6 = 0
            elif M == r :
                h6 = ((g - b) / c) % 6
            elif M == g :
                h6 = ((b - r) / c) + 2
            elif M == b :
                h6 = ((r - g) / c) + 4
            else :
                raise RuntimeError ("Program should never arrive here")
            h  = h6 * 60.0
            l  = (M + m) / 2.0
            s  = c / (1.0 - abs (2.0 * l - 1.0)) if (c != 0) else 0.0
            self._hsl = hsl = HSL_Value (h, s, l)
            self.Table_HSL [hsl] = self
        return self._hsl
    # end def hsl

    @Once_Property
    def rgb (self) :
        if self._rgb is None :
            h, s, l   = self._hsl
            c  = (1.0 - abs (2.0 * l - 1.0)) * s
            h6 = h / 60.0
            x  = c * (1 - abs (h6 % 2 - 1))
            m  = l - 0.5 * c
            if h6 < 1 :
                r, g, b = c, x, 0
            elif h6 < 2 :
                r, g, b = x, c, 0
            elif h6 < 3 :
                r, g, b = 0, c, x
            elif h6 < 4 :
                r, g, b = 0, x, c
            elif h6 < 5 :
                r, g, b = x, 0, c
            elif h6 < 6 :
                r, g, b = c, 0, x
            else :
                raise ValueError ("Invalid hue: %s" % h)
            self._rgb = rgb = RGB_Value (r + m, g + m, b + m)
            self.Table_RGB [rgb] = self
        return self._rgb
    # end def rgb

    def __eq__ (self, rhs) :
        return self.rgb == getattr (rhs, "rgb", None)
    # end def __eq__

    def __hash__ (self) :
        return hash (self.rgb)
    # end def __hash__

    def __repr__ (self) :
        if self._hsl :
            name, value = "hsl", self._hsl
        else :
            name, value = "rgb", self._rgb
        return "%s (%s = (%s))" % \
            (self.__class__.__name__, name, ", ".join (str (s) for s in value))
    # end def __repr__

# end class Value

class _Color_ (TFL.Meta.Object) :
    """Base class modelling a mutable color.

       >>> c = RGB_8 (255, 0, 0)
       >>> d = c.as_RGB_X
       >>> h = d.as_HSL
       >>> print c, d, h
       rgb(255, 0, 0) #F00 hsl(0.0, 1.0, 0.5)

       >>> ca = RGB (* c.rgb, alpha = 0.25).as_RGB_8
       >>> da = ca.as_RGB_X
       >>> ha = da.as_HSL
       >>> print ca, da, ha
       rgba(255, 0, 0, 0.25) rgba(255, 0, 0, 0.25) hsla(0.0, 1.0, 0.5, 0.25)
    """

    alpha = None

    def __init__ (self, values, alpha = None) :
        if not isinstance (values, Value) :
            values = Value (** {self.name : tuple (float (v) for v in values)})
        self.value = values
        if alpha is not None :
            assert 0.0 <= alpha <= 1.0
            self.alpha = float (alpha)
    # end def __init__

    @property
    def as_HSL (self) :
        return HSL.cast (self)
    # end def as_HSL

    @property
    def as_RGB (self) :
        return RGB.cast (self)
    # end def as_RGB

    @property
    def as_RGB_8 (self) :
        return RGB_8.cast (self)
    # end def as_RGB_8

    @property
    def as_RGB_P (self) :
        return RGB_P.cast (self)
    # end def as_RGB_P

    @property
    def as_RGB_X (self) :
        return RGB_X.cast (self)
    # end def as_RGB_X

    @classmethod
    def cast (cls, v) :
        result = cls.__new__ (cls)
        result.value = v.value
        if v.alpha is not None :
            result.alpha = v.alpha
        return result
    # end def cast

    @property
    def blue (self) :
        return self.value.rgb.blue
    # end def blue

    @blue.setter
    def blue (self, value) :
        assert 0.0 <= value <= 1.0
        r, g, b = self.value.rgb
        self.value = Value (rgb = (r, g, float (value)))
    # end def blue

    @property
    def green (self) :
        return self.value.rgb.green
    # end def green

    @green.setter
    def green (self, value) :
        assert 0.0 <= value <= 1.0
        r, g, b = self.value.rgb
        self.value = Value (rgb = (r, float (value), b))
    # end def green

    @property
    def hsl (self) :
        return self.value.hsl
    # end def hsl

    @hsl.setter
    def hsl (self, value) :
        if not isinstance (value, Value) :
            value  = Value (rgb = value)
        self.value = value
    # end def hsl

    @property
    def hue (self) :
        return self.value.hsl.hue
    # end def hue

    @hue.setter
    def hue (self, value) :
        assert 0.0 <= value < 360.0
        h, s, l = self.value.hsl
        self.value = Value (hsl = (float (value), s, l))
    # end def hue

    @property
    def lightness (self) :
        return self.value.hsl.lightness
    # end def lightness

    @lightness.setter
    def lightness (self, value) :
        assert 0.0 <= value <= 1.0
        h, s, l = self.value.hsl
        self.value = Value (hsl = (h, s, float (value)))
    # end def lightness

    @property
    def red (self) :
        return self.value.rgb.red
    # end def red

    @red.setter
    def red (self, value) :
        assert 0.0 <= value <= 1.0
        r, g, b = self.value.rgb
        self.value = Value (rgb = (float (value), g, b))
    # end def red

    @property
    def rgb (self) :
        return self.value.rgb
    # end def rgb

    @rgb.setter
    def rgb (self, value) :
        if not isinstance (value, Value) :
            value  = Value (rgb = value)
        self.value = value
    # end def rgb

    @property
    def saturation (self) :
        return self.value.hsl.saturation
    # end def saturation

    @saturation.setter
    def saturation (self, value) :
        assert 0.0 <= value <= 1.0
        h, s, l = self.value.hsl
        self.value = Value (hsl = (h, float (value), l))
    # end def saturation

    def __str__ (self) :
        v = self._formatted_values ()
        if self.alpha is not None :
            return "%sa(%s, %s)" % (self.name, v, self.alpha)
        else :
            return "%s(%s)" % (self.name, v)
    # end def __str__

# end class _Color_

class HSL (_Color_) :
    """Model a color specified by hue/saturation/lightness values."""

    name = "hsl"

    def __init__ (self, hue, saturation, lightness, alpha = None) :
        assert 0.0 <= hue        <  360.0
        assert 0.0 <= saturation <= 1.0
        assert 0.0 <= lightness  <= 1.0
        self.__super.__init__ ((hue, saturation, lightness), alpha)
    # end def __init__

    def as_HSL (self) :
        return self
    # end def as_HSL

    def _formatted_values (self) :
        return "%s, %s, %s" % self.value.hsl
    # end def _formatted_values

# end class HSL

class RGB (_Color_) :
    """Model a color specified by red/green/blue values."""

    name = "rgb"

    def __init__ (self, red, green, blue, alpha = None) :
        assert 0.0 <= red   <= 1.0
        assert 0.0 <= green <= 1.0
        assert 0.0 <= blue  <= 1.0
        self.__super.__init__ ((red, green, blue), alpha)
    # end def __init__

    def as_RGB (self) :
        return self
    # end def as_RGB

    def _formatted_values (self) :
        return "%d%%, %d%%, %d%%" % \
            tuple (int (v * 100) for v in self.value.rgb)
    # end def _formatted_values

# end class RGB

class RGB_8 (RGB) :
    """Model a color specified by 8-bit values for red/green/blue."""

    def __init__ (self, red, green, blue, alpha = None) :
        self.__super.__init__ \
            ( * tuple (v / 255.0 for v in (red, green, blue))
            , alpha = alpha
            )
    # end def __init__

    def as_RGB_8 (self) :
        return self
    # end def as_RGB_8

    def _formatted_values (self) :
        return "%d, %d, %d" % tuple (int (v * 255) for v in self.value.rgb)
    # end def _formatted_values

# end class RGB_8

class RGB_P (RGB) :
    """Model a color specified by percent values for red/green/blue."""

    def __init__ (self, red, green, blue, alpha = None) :
        self.__super.__init__ \
            ( * tuple (v / 100.0 for v in (red, green, blue))
            , alpha = alpha
            )
    # end def __init__

    def as_RGB_P (self) :
        return self
    # end def as_RGB_P

# end class RGB_P

class RGB_X (RGB) :
    """Model a color specified by a hexadecimal string for RGB."""

    _pat = TFL.Regexp \
        ( r"^#"
          r"?(?P<red>[0-9a-zA-Z]{1,2})"
          r"?(?P<green>[0-9a-zA-Z]{1,2})"
          r"?(?P<blue>[0-9a-zA-Z]{1,2})"
        )

    def __init__ (self, s) :
        pat = self._pat
        if pat.match (s) :
            r, g, b = pat.red, pat.green, pat.blue
            if not (len (r) == len (g) == len (g)) :
                raise ValueError ("Colors all need same length: %s" % s)
            if len (r) == 1 :
                r, g, b = r*2, g*2, b*2
            self.__super.__init__ (tuple (int (x, 16) for x in (r, g, b)))
        else :
            raise ValueError \
                ( "Need a hexadecimal color specification like '#AABBCC', "
                  "got '%s'" % (s, )
                )
    # end def __init__

    def as_RGB_X (self) :
        return self
    # end def as_RGB_X

    def _formatted_values (self) :
        r, g, b = tuple ("%2.2X" % (x*255, ) for x in self.value.rgb)
        if all (x [0] == x [1] for x in (r, g, b)) :
            r, g, b = tuple (x [0] for x in (r, g, b))
        return "#%s%s%s" % (r, g, b)
    # end def _formatted_values

    def __str__ (self) :
        if self.alpha is None :
            return self._formatted_values ()
        else :
            return str (self.as_RGB_8)
    # end def __str__

# end class RGB_X

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Color

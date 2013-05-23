# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
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
#    27-Dec-2010 (CT) Creation continued
#    29-Dec-2010 (CT) Creation finished
#     2-Jan-2011 (CT) `__add__` and `__radd__` added
#    17-Jan-2012 (CT) Change `HSL` to be compatible with CSS
#    18-Jan-2012 (CT) Add `_Color_.__eq__` and `__hash__`
#    18-Jan-2012 (CT) Return `name`, not `"name"`, from `SVG_Color.formatted`
#    16-Apr-2012 (CT) Add `sorted` to `.iteritems`
#    31-Aug-2012 (CT) Add property `no_alpha`
#    23-May-2013 (CT) Use `TFL.Meta.BaM` for Python-3 compatibility
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
    >>> white_1.rgb, white_1.hsl
    (RGB(red=1.0, green=1.0, blue=1.0), HSL(hue=0.0, saturation=0.0, lightness=1.0))

    >>> white_2 = Value (hsl = (0.0, 0.0, 1.0))
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
        assert 0.0 <= hsl.hue        <  360.0
        assert 0.0 <= hsl.saturation <= 1.0
        assert 0.0 <= hsl.lightness  <= 1.0
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
        assert all (0.0 <= v <= 1.0 for v in rgb), str (rgb)
        if rgb in cls.Table_RGB :
            result = cls.Table_RGB [rgb]
        else :
            result = cls.Table_RGB [rgb] = super (Value, cls).__new__ (cls)
            result._rgb = rgb
        return result
    # end def from_rgb

    @Once_Property
    def hex (self) :
        r, g, b = tuple ("%2.2X" % (x*255, ) for x in self.rgb)
        return "#%s%s%s" % (r, g, b)
    # end def hex

    @Once_Property
    def hex_CSS (self) :
        r, g, b = tuple ("%2.2X" % (x*255, ) for x in self.rgb)
        if all (x [0] == x [1] for x in (r, g, b)) :
            r, g, b = tuple (x [0] for x in (r, g, b))
        return "#%s%s%s" % (r, g, b)
    # end def hex

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

class M_Color (TFL.Meta.Object.__class__) :
    """Meta class for `_Color_`."""

# end class M_Color

class _Color_ (TFL.Meta.BaM (TFL.Meta.Object, metaclass = M_Color)) :
    """Base class modelling a mutable color."""

    alpha         = None
    formatter     = None

    def __init__ (self, values, alpha = None) :
        if not isinstance (values, Value) :
            values = Value (** {self.name : tuple (float (v) for v in values)})
        self.value = values
        if alpha is not None :
            assert 0.0 <= alpha <= 1.0
            self.alpha = float (alpha)
    # end def __init__

    @classmethod
    def cast (cls, v) :
        result = cls.__new__ (cls)
        result.value = v.value
        if v.alpha is not None :
            result.alpha = v.alpha
        return result
    # end def cast

    @classmethod
    def from_value (cls, value, alpha = None) :
        result = cls.__new__ (cls)
        result.value = value
        if alpha is not None :
            result.alpha = alpha
        return result
    # end def from_value

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
    def no_alpha (self) :
        """Return a color instance without `alpha`."""
        return self if self.alpha is None else self.from_value (self.value)
    # end def no_alpha

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

    def formatted (self) :
        v = self._formatted_values ()
        if self.alpha is not None :
            return "%sa(%s, %s)" % (self.name, v, self.alpha)
        else :
            return "%s(%s)" % (self.name, v)
    # end def formatted

    def __add__ (self, rhs) :
        return str (self) + rhs
    # end def __add__

    def __radd__ (self, rhs) :
        return rhs + str (self)
    # end def __radd__

    def __eq__ (self, rhs) :
        try :
            rhs = getattr (rhs, "rgb"), getattr (rhs, "alpha")
        except AttributeError :
            return False
        else :
            return (self.rgb, self.alpha) == rhs
    # end def __eq__

    def __hash__ (self) :
        return hash (self.rgb, self.alpha)
    # end def __hash__

    def __invert__ (self) :
        return self.__class__.from_value \
            (Value (rgb = tuple (1.0 - v for v in self.rgb)), self.alpha)
    # end def __invert__

    def __mul__ (self, rhs) :
        assert 0.0 <= rhs
        return self.__class__.from_value \
            ( Value (rgb = tuple (min (v * rhs, 1.0) for v in self.rgb))
            , self.alpha
            )
    # end def __mul__

    def __str__ (self) :
        if self.formatter is not None :
            self = self.formatter.cast (self)
        return self.formatted ()
    # end def __str__

# end class _Color_

class HSL (_Color_) :
    """Model a color specified by hue/saturation/lightness values."""

    name = "hsl"

    def __init__ (self, hue, saturation, lightness, alpha = None) :
        hue = (((hue % 360.0) + 360.0) % 360.0)
        self.__super.__init__ \
            ((hue, saturation / 100.0, lightness / 100.0), alpha)
    # end def __init__

    @property
    def as_HSL (self) :
        return self
    # end def as_HSL

    def _formatted_values (self) :
        h, s, l = self.value.hsl
        return "%d, %d%%, %d%%" % (h, s * 100, l * 100)
    # end def _formatted_values

# end class HSL

class RGB (_Color_) :
    """Model a color specified by red/green/blue values."""

    name = "rgb"

    def __init__ (self, red, green, blue, alpha = None) :
        self.__super.__init__ ((red, green, blue), alpha)
    # end def __init__

    @property
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

    @property
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

    @property
    def as_RGB_P (self) :
        return self
    # end def as_RGB_P

# end class RGB_P

class RGB_X (RGB) :
    """Model a color specified by a hexadecimal string for RGB."""

    _fmt = \
        ( r"^#"
          r"(?P<red>[0-9a-zA-Z]%(q)s)"
          r"(?P<green>[0-9a-zA-Z]%(q)s)"
          r"(?P<blue>[0-9a-zA-Z]%(q)s)"
          r"$"
        )
    _pat = TFL.Multi_Regexp (_fmt % dict (q = "{2}"), _fmt % dict (q = ""))

    def __init__ (self, s, alpha = None) :
        pat = self._pat
        if pat.match (s) :
            r, g, b = pat.red, pat.green, pat.blue
            if len (r) == 1 :
                r, g, b = r*2, g*2, b*2
            self.__super.__init__ \
                ( * tuple ((int (x, 16) / 255.0) for x in (r, g, b))
                , alpha = alpha
                )
        else :
            raise ValueError \
                ( "Need a hexadecimal color specification like "
                  "'#ABCDEF' or '#ABC', got '%s' instead"
                % (s, )
                )
    # end def __init__

    @property
    def as_RGB_X (self) :
        return self
    # end def as_RGB_X

    def formatted (self) :
        if self.alpha is None :
            return self._formatted_values ()
        else :
            return self.as_RGB_8.formatted ()
    # end def formatted

    def _formatted_values (self) :
        return self.value.hex_CSS
    # end def _formatted_values

# end class RGB_X

class SVG_Color (RGB_X) :
    """Model a color named as specified by SVG 1.0 and CSS-3."""

    ### http://www.w3.org/TR/css3-color/#rgb-color
    Map = dict \
        ( aliceblue               = "#F0F8FF"
        , antiquewhite            = "#FAEBD7"
        , aqua                    = "#00FFFF"
        , aquamarine              = "#7FFFD4"
        , azure                   = "#F0FFFF"
        , beige                   = "#F5F5DC"
        , bisque                  = "#FFE4C4"
        , black                   = "#000000"
        , blanchedalmond          = "#FFEBCD"
        , blue                    = "#0000FF"
        , blueviolet              = "#8A2BE2"
        , brown                   = "#A52A2A"
        , burlywood               = "#DEB887"
        , cadetblue               = "#5F9EA0"
        , chartreuse              = "#7FFF00"
        , chocolate               = "#D2691E"
        , coral                   = "#FF7F50"
        , cornflowerblue          = "#6495ED"
        , cornsilk                = "#FFF8DC"
        , crimson                 = "#DC143C"
        , cyan                    = "#00FFFF"
        , darkblue                = "#00008B"
        , darkcyan                = "#008B8B"
        , darkgoldenrod           = "#B8860B"
        , darkgray                = "#A9A9A9"
        , darkgreen               = "#006400"
        , darkgrey                = "#A9A9A9"
        , darkkhaki               = "#BDB76B"
        , darkmagenta             = "#8B008B"
        , darkolivegreen          = "#556B2F"
        , darkorange              = "#FF8C00"
        , darkorchid              = "#9932CC"
        , darkred                 = "#8B0000"
        , darksalmon              = "#E9967A"
        , darkseagreen            = "#8FBC8F"
        , darkslateblue           = "#483D8B"
        , darkslategray           = "#2F4F4F"
        , darkslategrey           = "#2F4F4F"
        , darkturquoise           = "#00CED1"
        , darkviolet              = "#9400D3"
        , deeppink                = "#FF1493"
        , deepskyblue             = "#00BFFF"
        , dimgray                 = "#696969"
        , dimgrey                 = "#696969"
        , dodgerblue              = "#1E90FF"
        , firebrick               = "#B22222"
        , floralwhite             = "#FFFAF0"
        , forestgreen             = "#228B22"
        , fuchsia                 = "#FF00FF"
        , gainsboro               = "#DCDCDC"
        , ghostwhite              = "#F8F8FF"
        , gold                    = "#FFD700"
        , goldenrod               = "#DAA520"
        , gray                    = "#808080"
        , green                   = "#008000"
        , greenyellow             = "#ADFF2F"
        , grey                    = "#808080"
        , honeydew                = "#F0FFF0"
        , hotpink                 = "#FF69B4"
        , indianred               = "#CD5C5C"
        , indigo                  = "#4B0082"
        , ivory                   = "#FFFFF0"
        , khaki                   = "#F0E68C"
        , lavender                = "#E6E6FA"
        , lavenderblush           = "#FFF0F5"
        , lawngreen               = "#7CFC00"
        , lemonchiffon            = "#FFFACD"
        , lightblue               = "#ADD8E6"
        , lightcoral              = "#F08080"
        , lightcyan               = "#E0FFFF"
        , lightgoldenrodyellow    = "#FAFAD2"
        , lightgray               = "#D3D3D3"
        , lightgreen              = "#90EE90"
        , lightgrey               = "#D3D3D3"
        , lightpink               = "#FFB6C1"
        , lightsalmon             = "#FFA07A"
        , lightseagreen           = "#20B2AA"
        , lightskyblue            = "#87CEFA"
        , lightslategray          = "#778899"
        , lightslategrey          = "#778899"
        , lightsteelblue          = "#B0C4DE"
        , lightyellow             = "#FFFFE0"
        , lime                    = "#00FF00"
        , limegreen               = "#32CD32"
        , linen                   = "#FAF0E6"
        , magenta                 = "#FF00FF"
        , maroon                  = "#800000"
        , mediumaquamarine        = "#66CDAA"
        , mediumblue              = "#0000CD"
        , mediumorchid            = "#BA55D3"
        , mediumpurple            = "#9370DB"
        , mediumseagreen          = "#3CB371"
        , mediumslateblue         = "#7B68EE"
        , mediumspringgreen       = "#00FA9A"
        , mediumturquoise         = "#48D1CC"
        , mediumvioletred         = "#C71585"
        , midnightblue            = "#191970"
        , mintcream               = "#F5FFFA"
        , mistyrose               = "#FFE4E1"
        , moccasin                = "#FFE4B5"
        , navajowhite             = "#FFDEAD"
        , navy                    = "#000080"
        , oldlace                 = "#FDF5E6"
        , olive                   = "#808000"
        , olivedrab               = "#6B8E23"
        , orange                  = "#FFA500"
        , orangered               = "#FF4500"
        , orchid                  = "#DA70D6"
        , palegoldenrod           = "#EEE8AA"
        , palegreen               = "#98FB98"
        , paleturquoise           = "#AFEEEE"
        , palevioletred           = "#DB7093"
        , papayawhip              = "#FFEFD5"
        , peachpuff               = "#FFDAB9"
        , peru                    = "#CD853F"
        , pink                    = "#FFC0CB"
        , plum                    = "#DDA0DD"
        , powderblue              = "#B0E0E6"
        , purple                  = "#800080"
        , red                     = "#FF0000"
        , rosybrown               = "#BC8F8F"
        , royalblue               = "#4169E1"
        , saddlebrown             = "#8B4513"
        , salmon                  = "#FA8072"
        , sandybrown              = "#F4A460"
        , seagreen                = "#2E8B57"
        , seashell                = "#FFF5EE"
        , sienna                  = "#A0522D"
        , silver                  = "#C0C0C0"
        , skyblue                 = "#87CEEB"
        , slateblue               = "#6A5ACD"
        , slategray               = "#708090"
        , snow                    = "#FFFAFA"
        , springgreen             = "#00FF7F"
        , steelblue               = "#4682B4"
        , tan                     = "#D2B48C"
        , teal                    = "#008080"
        , thistle                 = "#D8BFD8"
        , tomato                  = "#FF6347"
        , turquoise               = "#40E0D0"
        , violet                  = "#EE82EE"
        , wheat                   = "#F5DEB3"
        , white                   = "#FFFFFF"
        , whitesmoke              = "#F5F5F5"
        , yellow                  = "#FFFF00"
        , yellowgreen             = "#9ACD32"
        )

    _Pam = None

    def __init__ (self, name, alpha = None) :
        key = name.lower ().replace (" ", "")
        self.__super.__init__ (self.Map [key], alpha)
    # end def __init__

    @property
    def as_RGB_X (self) :
        return RGB_X.cast (self)
    # end def as_RGB_X

    def formatted (self) :
        if self.alpha is None :
            name = self.Pam.get (self.value.hex)
            if name is not None :
                return name
            else :
                return self._formatted_values ()
        else :
            return self.as_RGB_8.formatted ()
    # end def formatted

    @property
    def Pam (self) :
        if self._Pam is None :
            self.__class__._Pam = dict \
                ((v, k) for (k, v) in sorted (self.Map.iteritems ()))
        return self._Pam
    # end def Pam

# end class SVG_Color

__all__ = tuple \
    ( k for (k, v) in globals ().iteritems ()
    if k != "_Color_" and isinstance (v, M_Color)
    )

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

Module `Color`
==========================

Classes modelling various color representations::

    >>> c = RGB_8 (255, 0, 0)
    >>> d = c.as_RGB_X
    >>> h = d.as_HSL
    >>> print c, d, h
    rgb(255, 0, 0) #F00 hsl(0, 100%, 50%)

    >>> cn = ~ c
    >>> hn = ~ h
    >>> print cn, hn
    rgb(0, 255, 255) hsl(180, 100%, 50%)

    >>> ca = RGB (* c.rgb, alpha = 0.25).as_RGB_8
    >>> da = ca.as_RGB_X
    >>> ha = da.as_HSL
    >>> print ca, da, ha
    rgba(255, 0, 0, 0.25) rgba(255, 0, 0, 0.25) hsla(0, 100%, 50%, 0.25)

    >>> b  = RGB (0, 0, 0)
    >>> hb = b.as_HSL
    >>> w  = RGB (1, 1, 1)
    >>> hw = w.as_HSL
    >>> print b, ~b, hb, ~hb
    rgb(0%, 0%, 0%) rgb(100%, 100%, 100%) hsl(0, 0%, 0%) hsl(0, 0%, 100%)
    >>> print ~w, w, ~hw, hw
    rgb(0%, 0%, 0%) rgb(100%, 100%, 100%) hsl(0, 0%, 0%) hsl(0, 0%, 100%)

    >>> print c * 0.5, w * 0.8
    rgb(127, 0, 0) rgb(80%, 80%, 80%)

    >>> _Color_.formatter = RGB_X
    >>> print b, ~b, hb, ~hb
    #000 #FFF #000 #FFF
    >>> print cn, hn
    #0FF #0FF
    >>> print ca, da, ha
    rgba(255, 0, 0, 0.25) rgba(255, 0, 0, 0.25) rgba(255, 0, 0, 0.25)

    >>> _Color_.formatter = HSL
    >>> print b, ~b, hb, ~hb
    hsl(0, 0%, 0%) hsl(0, 0%, 100%) hsl(0, 0%, 0%) hsl(0, 0%, 100%)
    >>> print cn, hn
    hsl(180, 100%, 50%) hsl(180, 100%, 50%)
    >>> print ca, da, ha
    hsla(0, 100%, 50%, 0.25) hsla(0, 100%, 50%, 0.25) hsla(0, 100%, 50%, 0.25)

    >>> _Color_.formatter = RGB_X
    >>> print SVG_Color ("Gray"), SVG_Color ("Dark red"), SVG_Color ("blue", 0.5)
    #808080 #8B0000 rgba(0, 0, 255, 0.5)

    >>> _Color_.formatter = None
    >>> print SVG_Color ("Gray"), SVG_Color ("Dark red"), SVG_Color ("blue", 0.5)
    grey darkred rgba(0, 0, 255, 0.5)

"""

if __name__ != "__main__" :
    TFL._Export_Module ()
### __END__ TFL.Color

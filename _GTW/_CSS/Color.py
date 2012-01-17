# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.CSS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.CSS.Color
#
# Purpose
#    Model a CSS color value
#
# Revision Dates
#    17-Jan-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._CSS

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property   import Once_Property

from   _TFL.Color                 import *
from   _TFL.Color                 import _Color_
from   _TFL.Regexp                import Regexp, re

class _Color_Converter_ (TFL.Meta.Object) :
    """Convert CSS color strings to the appropriate `_Color_` instance.

    >>> print (Color ("rgb(255,0,0)"))
    rgb(255, 0, 0)
    >>> print (Color ("rgb (255,0,80)"))
    rgb(255, 0, 80)
    >>> print (Color ("rgb(100%, 0%, 0%) "))
    rgb(100%, 0%, 0%)
    >>> print (Color ("rgb(100%, 0%, 25%)"))
    rgb(100%, 0%, 25%)
    >>> print (Color ("rgb(110%, 0%, -25%)"))
    rgb(100%, 0%, 0%)
    >>> print (Color ("rgba(0,0,255,0.5)"))
    rgba(0, 0, 255, 0.5)
    >>> print (Color ("rgba(100%, 50%, 0%, 0.1)"))
    rgba(100%, 50%, 0%, 0.1)
    >>> print (Color ("hsl(120, 100%, 50%)"))
    hsl(120, 100%, 50%)
    >>> print (Color ("hsl(120, 100%, 50%, 0.75)"))
    hsla(120, 100%, 50%, 0.75)
    >>> print (Color ("olive").as_RGB_X)
    #808000
    >>> print (Color ("transparent"))
    transparent

    """

    keywords      = set (("inherit", "transparent"))

    hsl_pattern   = Regexp \
        ( r"^"
        + r"hsla?\s*\("
          + r"\s* (\d{1,3})\s* "
          + r","
          + r"\s* (\d{1,3})\s*  \% \s*"
          + r","
          + r"\s* (\d{1,3})\s*  \% \s*"
          + r"(?:"
              + r","
              + r"\s* (?P<alpha> \d+ (?: \.\d*)?)\s* "
          + r")?"
        + r"\)"
        + r"$"
        , re.VERBOSE | re.IGNORECASE
        )


    rgb_8_pattern = Regexp \
        ( r"^"
        + r"rgba?\s*\("
          + r"\s* (\d{1,3})\s* "
          + r","
          + r"\s* (\d{1,3})\s* "
          + r","
          + r"\s* (\d{1,3})\s* "
          + r"(?:"
              + r","
              + r"\s* (?P<alpha> \d+ (?: \.\d*)?)\s* "
          + r")?"
        + r"\)"
        + r"$"
        , re.VERBOSE | re.IGNORECASE
        )

    rgb_p_pattern = Regexp \
        ( r"^"
        + r"rgba?\s*\("
          + r"\s* (-?\d{1,3})\s* \% \s*"
          + r","
          + r"\s* (-?\d{1,3})\s* \% \s*"
          + r","
          + r"\s* (-?\d{1,3})\s* \% \s*"
          + r"(?:"
              + r","
              + r"\s* (?P<alpha> \d+ (?: \.\d*)?)\s* "
          + r")?"
        + r"\)"
        + r"$"
        , re.VERBOSE | re.IGNORECASE
        )

    def __call__ (self, v) :
        if isinstance (v, basestring) :
            percent = lambda x : max (min (int (x), 100), 0)
            v = v.strip ()
            if v in self.keywords :
                result  = v
            elif v.startswith ("#") :
                result  = RGB_X (v)
            elif self.name_pattern.match (v) :
                result  = SVG_Color (v)
            elif self.hsl_pattern.match (v) :
                convert = (int, percent, percent)
                result  = self._convert (HSL,   convert, self.hsl_pattern)
            elif self.rgb_8_pattern.match (v) :
                result  = self._convert (RGB_8, int,     self.rgb_8_pattern)
            elif self.rgb_p_pattern.match (v) :
                result  = self._convert (RGB_P, percent, self.rgb_p_pattern)
            else :
                raise ValueError (v)
        else :
            raise ValueError (v)
        return result
    # end def __call__

    @property
    def formatter (self) :
        return _Color_.formatter
    # end def formatter

    @formatter.setter
    def formatter (self, value) :
        _Color_.formatter = value
    # end def formatter

    @Once_Property
    def name_pattern (self) :
        return Regexp \
            ( r"^"
            + "|".join (re.escape (u) for u in sorted (SVG_Color.Map))
            + r"$"
            , re.VERBOSE | re.IGNORECASE
            )
    # end def name_pattern

    def _convert (self, Type, convert, pat) :
        if not isinstance (convert, tuple) :
            convert = (convert, ) * 3
        vs    = (c (v) for c, v in zip (convert, pat.groups () [:3]))
        alpha = pat.alpha
        if alpha is not None :
            alpha = float (alpha)
        return Type (* vs, alpha = alpha)
    # end def _convert

# end class _Color_Converter_

Color = _Color_Converter_ ()

__all__ = tuple (TFL._.Color.__all__ + ("Color", ))

if __name__ != "__main__" :
    GTW.CSS._Export (* __all__)
### __END__ GTW.CSS.Color

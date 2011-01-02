# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.CSS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.CSS.Length
#
# Purpose
#    Model a CSS length value
#
# Revision Dates
#    29-Dec-2010 (CT) Creation
#     1-Jan-2011 (CT) `TRBL` added
#     1-Jan-2011 (CT) `__truediv__` and `__floordiv__` added
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division
from   __future__  import print_function, unicode_literals

from   _GTW                       import GTW
from   _TFL                       import TFL

import _GTW._CSS

import _TFL._Meta.Object

class M_Length (TFL.Meta.Object.__class__) :
    """Meta class for `Length`."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "Length" and cls.unit_name is None :
            cls.unit_name = name.lower ()
    # end def __init__

# end class M_Length

class Length (TFL.Meta.Object) :
    """Model a CSS length value.

    >>> print (Px (3))
    3px
    >>> print (Px (3) * 2)
    6px
    >>> print (Px (3) + Px (2))
    5px
    >>> print (Px (3) + In (2))
    Traceback (most recent call last):
      ...
    TypeError: Cannot add 'Px' and 'In' objects
    >>> print (Px (3) % 2)
    1px

    >>> print (Percent (100), Percent (100) / 2, Percent (100) / 3)
    100% 50.0% 33.3333333333%
    """

    __metaclass__ = M_Length

    unit_name     = None

    def __init__ (self, value = 0) :
        self.value = value
    # end def __init__

    def __add__ (self, rhs) :
        if not isinstance (rhs, self.__class__) :
            raise TypeError \
                ( "Cannot add %r and %r objects"
                % (self.__class__.__name__, rhs.__class__.__name__)
                )
        return self.__class__ (self.value + rhs.value)
    # end def __add__

    def __div__ (self, rhs) :
        if not isinstance (rhs, (int, float)) :
            raise TypeError \
                ( "Cannot divide %r and %r objects"
                % (self.__class__.__name__, rhs.__class__.__name__)
                )
        return self.__class__ (self.value / rhs)
    # end def __div__

    __truediv__ = __div__

    def __eq__ (self, rhs) :
        ru = getattr (rhs, "unit_name", None)
        if self.unit_name == ru :
            return self.value == rhs.value
        else :
            if not rhs :
                return not self
        return False
    # end def __eq__

    def __float__ (self) :
        return float (self.value)
    # end def __float__

    def __floordiv__ (self, rhs) :
        if not isinstance (rhs, (int, float)) :
            raise TypeError \
                ( "Cannot divide %r and %r objects"
                % (self.__class__.__name__, rhs.__class__.__name__)
                )
        return self.__class__ (self.value // rhs)
    # end def __floordiv__

    def __int__ (self) :
        return int (self.value)
    # end def __int__

    def __hash__ (self) :
        return (self.unit_name, self.value)
    # end def __hash__

    def __mod__ (self, rhs) :
        if not isinstance (rhs, (int, float)) :
            raise TypeError \
                ( "Cannot take remainer of %r and %r objects"
                % (self.__class__.__name__, rhs.__class__.__name__)
                )
        return self.__class__ (self.value % rhs)
    # end def __mod__

    def __mul__ (self, rhs) :
        if not isinstance (rhs, (int, float)) :
            raise TypeError \
                ( "Cannot multiply %r and %r objects"
                % (self.__class__.__name__, rhs.__class__.__name__)
                )
        return self.__class__ (self.value * rhs)
    # end def __mul__

    __rmul__ = __mul__

    def __nonzero__ (self) :
        return bool (self.value)
    # end def __nonzero__

    def __sub__ (self, rhs) :
        if not isinstance (rhs, self.__class__) :
            raise TypeError \
                ( "Cannot subtract %r and %r objects"
                % (self.__class__.__name__, rhs.__class__.__name__)
                )
        return self.__class__ (self.value - rhs.value)
    # end def __sub__

    def __str__ (self) :
        if self.value :
            return "%s%s" % (self.value, self.unit_name)
        else :
            return "0"
    # end def __str__

# end class Length

class Cm (Length) :
    """Absolute CSS length unit: centimeters."""

# end class Cm

class Em (Length) :
    """Relative CSS length unit: font size of the element."""

# end class Em

class Ex (Length) :
    """Relative CSS length unit: x-height of the element's font."""

# end class Ex

class In (Length) :
    """Absolute CSS length unit: inches."""

# end class In

class Mm (Length) :
    """Absolute CSS length unit: millimeters."""

# end class Mm

class Pc (Length) :
    """Absolute CSS length unit: picas (1 pc == 12 points)."""

# end class Pc

class Percent (Length) :
    """Relative CSS unit: percentages."""

    unit_name = "%"

    def __add__ (self, rhs) :
        if isinstance (rhs, (int, float)) :
            return self.__class__ (self.value + rhs)
        return self.__super.__add__ (rhs)
    # end def __add__

    def __sub__ (self, rhs) :
        if isinstance (rhs, (int, float)) :
            return self.__class__ (self.value - rhs)
        return self.__super.__sub__ (rhs)
    # end def __sub__

# end class Percent

class Pt (Length) :
    """Absolute CSS length unit: points (1pt == 1/72 inch)."""

# end class Pt

class Px (Length) :
    """Relative CSS length unit: size of pixel of viewing device."""

# end class Px

class TRBL (TFL.Meta.Object) :
    """Top/right/bottom/left spec

    >>> print (TRBL (0))
    0
    >>> print (TRBL (1, 2, 1, 2))
    1 2
    >>> print (TRBL (1, 2, 3, 2))
    1 2 3
    >>> print (TRBL (1, 2, 3, 4))
    1 2 3 4
    >>> print (TRBL (Px (1), Em (1)))
    1px 1em 0 0
    >>> print (TRBL (Px (1), 0, Em (1)))
    1px 0 1em
    >>> print (TRBL (Px (1), 0, Px (1)))
    1px 0
    >>> print (TRBL (t = Px (1)))
    1px 0 0
    >>> print (TRBL (r = Px (1)))
    0 1px 0 0
    >>> print (TRBL (b = Px (1)))
    0 0 1px
    >>> print (TRBL (l = Px (1)))
    0 0 0 1px
    >>> print (TRBL (default = Px(2)))
    2px
    >>> print (TRBL (t = Px (1), default = Px(2)))
    1px 2px 2px
    >>> print (TRBL (r = Px (1), default = Px(2)))
    2px 1px 2px 2px
    >>> print (TRBL (b = Px (1), default = Px(2)))
    2px 2px 1px
    >>> print (TRBL (l = Px (1), default = Px(2)))
    2px 2px 2px 1px

    """

    b = property (lambda s : s.values [2])
    l = property (lambda s : s.values [3])
    r = property (lambda s : s.values [1])
    t = property (lambda s : s.values [0])

    def __init__ (self, t = None, r = None, b = None, l = None, default = 0) :
        self.values = tuple \
            ((v if v is not None else default) for v in (t, r, b, l))
    # end def __init__

    def __nonzero__ (self) :
        return any (self.values)
    # end def __nonzero__

    def __str__ (self) :
        values = list (self.values)
        for h, t in ((-1, -3), (-1, -3), (0, 1)) :
            if values [h] == values [t] :
                values.pop ()
            else :
                break
        return " ".join (str (v) for v in values)
    # end def __str__

# end class TRBL

__all__ = tuple \
    ( k for (k, v) in globals ().iteritems () if getattr (v, "unit_name", None)
    ) + ("TRBL", )

if __name__ != "__main__" :
    GTW.CSS._Export (* __all__)
### __END__ GTW.CSS.Length

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2003 Mag. Christian Tanzer. All rights reserved
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
#    Numeric_Interval
#
# Purpose
#    Model a numeric interval
#
# Revision Dates
#    18-Nov-2003 (CT) Creation
#    ��revision-date�����
#--

from   _TFL                 import TFL
import _TFL._Meta.Object
import sys

class Numeric_Interval (TFL.Meta.Object) :
    """Class for modelling a numeric interval."""

    format = "(%s, %s)"

    def __init__ (self, lower = sys.maxint, upper = - sys.maxint) :
        self.lower = lower
        self.upper = upper
    # end def __init__

    length = property (lambda s : s.upper - s.lower)

    def after (self, other) :
        return self.lower >= other.upper
    # end def after

    def before (self, other) :
        return self.upper <= other.lower
    # end def before

    def contains (self, other) :
        return self.lower <= other.lower <= other.upper <= self.upper
    # end def contains

    def contains_point (self, point) :
        return self.lower <= point <= self.upper
    # end def contains_point

    def copy (self) :
        return self.__class__ (self.lower, self.upper)
    # end def copy

    def difference (self, other) :
        result = []
        isect  = self.intersection (other)
        if isect :
            r = self.__class__ (self.lower, isect.lower)
            if r :
                result.append (r)
            r = self.__class__ (isect.upper, self.upper)
            if r :
                result.append (r)
        return result
    # end def difference

    def intersection (self, other) :
        return self.__class__ \
            (max (self.lower, other.lower), min (self.upper, other.upper))
    # end def intersection

    def intersect (self, other) :
        self.lower = max (self.lower, other.lower)
        self.upper = min (self.upper, other.upper)
    # end def intersect

    def is_empty (self) :
        return self.lower == self.upper
    # end def is_empty

    def is_valid (self) :
        return self.lower <= self.upper
    # end def is_valid

    def overlaps (self, other) :
        return not (self.upper <= other.lower or self.lower >= other.upper)
    # end def overlaps

    def shift (self, delta) :
        self.lower += delta
        self.upper += delta
    # end def shift

    def __cmp__ (self, other) :
        try :
            return cmp ((self.lower, self.upper), (other.lower, other.upper))
        except AttributeError :
            return cmp ((self.lower, self.upper), other)
    # end def __cmp__

    def __getitem__ (self, key) :
        return (self.lower, self.upper) [key]
    # end def __getitem__

    def __nonzero__ (self) :
        return self.length > 0
    # end def __nonzero__

    def __repr__ (self) :
        return self.format % (self.lower, self.upper)
    # end def __repr__

    def __setitem__ (self, key, value) :
        setattr (self, ("lower", "upper") [key], value)
    # end def __setitem__

# end class Numeric_Interval

if __name__ != "__main__" :
    TFL._Export ("*")
### __END__ Numeric_Interval

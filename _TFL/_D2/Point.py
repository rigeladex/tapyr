# Copyright (C) 2002-2003 Mag. Christian Tanzer. All rights reserved
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
#    TFL.D2.Point
#
# Purpose
#    Classes modeling points in 2D space
#
# Revision Dates
#    24-Jun-2002 (CT) Creation
#    25-Jun-2002 (CT) Classes for relative Points renamed
#    26-Jun-2002 (CT) `R_Point_nP` added
#    22-Aug-2002 (CT) s/KeyError/IndexError/ for `__.etitem__` methods
#    24-Mar-2003 (CT) Converted to new-style class
#    24-Mar-2003 (CT) `__radd__` and `__rsub__` added
#    24-Mar-2003 (CT) `__rmul__` changed to alias of `__mul__`
#    24-Mar-2003 (CT) `__rdiv__` removed
#    ««revision-date»»···
#--

from    _TFL     import TFL
from    _TFL._D2 import D2
import  _TFL._Meta.Object
import  operator

class _Point_ (TFL.Meta.Object) :
    """Base class for points in 2D space."""

    def __getitem__ (self, index) :
        """Returns `x' for `index == 0' and `y' for `index == 1'"""
        if   index == 0 : return self.x
        elif index == 1 : return self.y
        else            : raise  IndexError, index
    # end def __getitem__

    def __len__ (self) :
        return 2
    # end def __len__

    def __str__  (self) :
        return "(%s, %s)" % (self.x, self.y)
    # end def __str__

    def __repr__ (self) :
        return "%s %s" % (self.__class__.__name__, str (self))
    # end def __repr__

    def list (self) :
        return (self.x, self.y)
    # end def list

# end class _Point_

class Point (_Point_) :
    """Model a point in rectangular, 2-dimensional space."""

    def __init__ (self, x = 0, y = 0) :
        (self.x, self.y) = (x, y)
    # end def __init__

    def shift (self, right) :
        (self.x, self.y) = (self.x + right.x, self.y + right.y)
        return self
    # end def shift

    def scale (self, right) :
        """Scale by point or number `right'"""
        try :
            (self.x, self.y) = (self.x * right.x, self.y * right.y)
        except AttributeError :
            (self.x, self.y) = (self.x * right,   self.y * right)
        return self
    # end def scale

    def __neg__ (self) :
        return self.__class__ (- self.x, - self.y)
    # end def __neg__

    def __add__  (self, right) :
        try :
            return self.__class__ (self.x + right.x, self.y + right.y)
        except AttributeError :
            return self.__class__ (self.x + right,   self.y + right)
    # end def __add__

    __radd__ = __add__

    def __sub__  (self, right) :
        try :
            return self.__class__ (self.x - right.x, self.y - right.y)
        except AttributeError :
            return self.__class__ (self.x - right,   self.y - right)
    # end def __sub__

    __rsub__ = __sub__

    def __mul__  (self, right) :
        try :
            return self.__class__ (self.x * right.x, self.y * right.y)
        except AttributeError :
            return self.__class__ (self.x * right,   self.y * right)
    # end def __mul__

    __rmul__ = __mul__

    def __div__  (self, right) :
        try :
            return self.__class__ \
                (float (self.x) / right.x, float (self.y) / right.y)
        except AttributeError :
            return self.__class__ \
                (float (self.x) / right,   float (self.y) / right)
    # end def __div__

    def __setitem__ (self, index, value) :
        """Set `x' (for `index == 0') or `y' (for `index == 1') to `value'."""
        if   index == 0 : self.x = value
        elif index == 1 : self.y = value
        else            : raise IndexError, index
    # end def __setitem__

# end class Point

class _R_Point_ (_Point_) :
    """Base class for Points positioned relative to another point."""

    def __init__ (self, offset = None, scale = None) :
        self._offset = offset or Point (0, 0)
        self._scale  = scale  or Point (1, 1)
    # end def __init__

    def __getattr__ (self, name) :
        if name == "x" :
            return (self._ref_point.x + self._offset.x) * self._scale.x
        elif name == "y" :
            return (self._ref_point.y + self._offset.y) * self._scale.y
        raise AttributeError
    # end def __getattr__

    def shift (self, right) :
        self._offset.shift (right)
        return self
    # end def shift

    def scale (self, right) :
        self._scale.scale (right)
        return self
    # end def scale

    def _reference (self) :
        raise NotImplementedError
    # end def _reference

    def __neg__ (self) :
        return self.__class__ \
            (* self._reference () + (self._offset, - self._scale))
    # end def __neg__

    def __add__  (self, right) :
        return self.__class__ \
            (* self._reference () + (self._offset + right, self._scale))
    # end def __add__

    def __sub__  (self, right) :
        return self.__class__ \
            (* self._reference () + (self._offset - right, self._scale))
    # end def __sub__

    def __mul__  (self, right) :
        return self.__class__ \
            (* self._reference () + (self._offset, self._scale * right))
    # end def __mul__

    def __rmul__ (self, left) :
        return self.__class__ \
            (* self._reference () + (self._offset, self._scale * left))
    # end def __rmul__

    def __div__  (self, right) :
        return self.__class__ \
            (* self._reference () + (self._offset, self._scale / right))
    # end def __div__

    def __rdiv__ (self, left) :
        return self.__class__ \
            (* self._reference () + (self._offset, self._scale / left))
    # end def __rdiv__

# end class _R_Point_

class R_Point_P (_R_Point_) :
    """Point positioned relative to another point.

       >>> p = Point     (5, 42)
       >>> q = R_Point_P (p, Point (3, 7))
       >>> print p, q
       (5, 42) (8, 49)
       >>> p.scale (Point (2, 0.5))
       Point (10, 21.0)
       >>> print p, q
       (10, 21.0) (13, 28.0)
       >>> q.scale (Point (3, 2))
       R_Point_P (39, 56.0)
       >>> print p, q
       (10, 21.0) (39, 56.0)
    """

    def __init__ (self, ref_point, offset = None, scale = None) :
        self._ref_point = ref_point
        self.__super.__init__ (offset, scale)
    # end def __init__

    def _reference (self) :
        return (self._ref_point, )
    # end def _reference

# end class R_Point_P

class R_Point_L (_R_Point_) :
    """Point positioned relative to a line.

       >>> l = D2.Line   (Point (0, 0), Point (20, 10))
       >>> q = R_Point_L (l, 0.5, Point (2, 2))
       >>> r = -q
       >>> print l, q, r
       ((0, 0), (20, 10)) (12.0, 7.0) (-12.0, -7.0)
       >>> l.shift (Point (5, 5))
       Line ((5, 5), (25, 15))
       >>> print l, q, r
       ((5, 5), (25, 15)) (17.0, 12.0) (-17.0, -12.0)
    """

    def __init__ (self, ref_line, shift, offset = None, scale = None) :
        self._ref_line = ref_line
        self._shift    = shift
        self.__super.__init__ (offset, scale)
    # end def __init__

    def _reference (self) :
        return self._ref_line, self._shift
    # end def _reference

    def __getattr__ (self, name) :
        if name == "_ref_point" :
            return self._ref_line.point (self._shift)
        return self.__super.__getattr__ (name)
    # end def __getattr__

# end class R_Point_L

class R_Point_R (_R_Point_) :
    """Point positioned relative to a rectangle.

       >>> r = D2.Rect   (Point (0, 10), Point (20, 0))
       >>> p = R_Point_R (r, D2.Rect.Center_Top, Point (0, 2))
       >>> print r, p
       ((0, 10), (20.0, 10.0)) (10.0, 12.0)
       >>> r.shift (Point (5.0, 5.0))
       Rect ((5.0, 15.0), (25.0, 15.0))
       >>> print r, p
       ((5.0, 15.0), (25.0, 15.0)) (15.0, 17.0)
    """

    def __init__ \
        (self, ref_rectangle, rect_point, offset = None, scale = None) :
        self._ref_rectangle = ref_rectangle
        self._rect_point    = rect_point
        self.__super.__init__ (offset, scale)
    # end def __init__

    def _reference (self) :
        return self._ref_rectangle, self._rect_point
    # end def _reference

    def __getattr__ (self, name) :
        if name == "_ref_point" :
            return self._ref_rectangle.point (self._rect_point)
        return self.__super.__getattr__ (name)
    # end def __getattr__

# end class R_Point_R

class R_Point_nP (_R_Point_) :
    """Point positioned relative to (linear combination of) n other points.

       >>> p = Point     (5, 42)
       >>> q = R_Point_P (p, Point (3, 7))
       >>> a = R_Point_nP ((p, q), (0.5, 0.5), (1.0, 0.0))
       >>> print p, q, a
       (5, 42) (8, 49) (6.5, 42.0)
       >>> b = R_Point_nP ((p, q, a), (0., 0., 1.0), (0.3, 0.4, 0.3))
       >>> print p, q, a, b
       (5, 42) (8, 49) (6.5, 42.0) (6.5, 44.8)
    """

    def __init__ \
        ( self, ref_points, x_weights, y_weights
        , offset = None, scale = None
        ) :
        if not (len (ref_points) == len (x_weights) == len (y_weights)) :
            raise ValueError, \
                ( "%s must have equal length"
                % ((ref_points, x_weights, y_weights), )
                )
        self._ref_points  = ref_points
        self._x_weights   = x_weights
        self._y_weights   = y_weights
        self.__super.__init__ (offset, scale)
    # end def __init__

    def _reference (self) :
        return (self._ref_points, self._x_weights, self._y_weights)
    # end def _reference

    def __getattr__ (self, name) :
        if name == "_ref_point" :
            return self._calc_ref_point ()
        return self.__super.__getattr__ (name)
    # end def __getattr__

    def _calc_ref_point (self) :
        return Point \
            ( reduce ( operator.add
                     , [ (p.x * w) for (p, w)
                         in zip (self._ref_points, self._x_weights)
                       ]
                     )
            , reduce ( operator.add
                     , [ (p.y * w) for (p, w)
                         in zip (self._ref_points, self._y_weights)
                       ]
                     )
            )
    # end def _calc_ref_point

# end class R_Point_nP

P  = Point
Pp = R_Point_P
Pl = R_Point_L
Pr = R_Point_R
Pn = R_Point_nP

if __name__ != "__main__" :
    D2._Export ("*", "P", "Pp", "Pl", "Pr", "Pn")

### unit-test code ############################################################

if __debug__ :

    import U_Test
    import _TFL._D2.Line
    import _TFL._D2.Rect

    def _doc_test () :
        import Point
        return U_Test.run_module_doc_tests (Point)
    # end def _doc_test

    def _test () :
        _doc_test  ()
    # end def _test

    if __name__ == "__main__" :
        _test ()
# end if __debug__

### end unit-test code ########################################################

### __END__ Point

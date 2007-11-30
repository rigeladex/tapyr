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
#    TFL.D2.Affine
#
# Purpose
#    Model affine transformations in 2D space
#
# Revision Dates
#    29-Nov-2007 (CT) Creation
#    ««revision-date»»···
#--

from    _TFL     import TFL
from    _TFL._D2 import D2
import  _TFL._Meta.Object

class Affine (TFL.Meta.Object) :
    """Affine transformation in 2D space.

       >>> t_2_4 = Affine.Trans (2, 4)
       >>> s_3_5 = Affine.Scale (3, 5)
       >>> [t_2_4 (p) for p in ((0, 0), (0, 1), (1, 0))]
       [(2, 4), (2, 5), (3, 4)]
       >>> [s_3_5 (p) for p in [(0, 0), (1, 1), (2, 4), (2, 5), (3, 4)]]
       [(0, 0), (3, 5), (6, 20), (6, 25), (9, 20)]
       >>> t_2_4 (s_3_5 ((2, 2))), s_3_5 (t_2_4 ((2, 2)))
       ((8, 14), (12, 30))
       >>> t_s = t_2_4 * s_3_5
       >>> s_t = s_3_5 * t_2_4
       >>> t_s ((2, 2)), s_t ((2, 2))
       ((8, 14), (12, 30))
    """

    @classmethod
    def Rot (cls, angle) :
        """Returns affine transformation for counter-clockwise rotation by
           `angle`.
        """
        return cls (angle.cos, - angle.sin, angle.sin, angle.cos, 0, 0)
    # end def Rot

    @classmethod
    def Scale (cls, sx, sy) :
        """Returns affine transformation for scaling by `sx`, `sy`."""
        return cls (sx, 0, 0, sy, 0, 0)
    # end def Scale

    @classmethod
    def Trans (cls, dx, dy) :
        """Returns affine transformation for translation by `dx`, `dy`."""
        return cls (1, 0, 0, 1, dx, dy)
    # end def Trans

    def __init__ (self, a, b, c, d, e, f) :
        self._matrix = ((a, b, e), (c, d, f), (0, 0, 1))
    # end def __init__

    def __call__ (self, p) :
        """Return affine transformation of point `p`."""
        xc, yc = self._matrix [:2]
        pc     = list (p) + [1]
        return \
            ( sum (u * v for (u, v) in zip (pc, xc))
            , sum (u * w for (u, w) in zip (pc, yc))
            )
    # end def __call__

    def __mul__ (self, rhs) :
        if isinstance (rhs, Affine) :
            sm = self._matrix
            rm = zip (* rhs._matrix) # transpose
            return self.__class__ \
                ( sum (u * v for (u, v) in zip (sm [0], rm [0]))
                , sum (u * v for (u, v) in zip (sm [0], rm [1]))
                , sum (u * v for (u, v) in zip (sm [1], rm [0]))
                , sum (u * v for (u, v) in zip (sm [1], rm [1]))
                , sum (u * v for (u, v) in zip (sm [0], rm [2]))
                , sum (u * v for (u, v) in zip (sm [1], rm [2]))
                )
    # end def __mul__

    ### XXX __neg__ --> Inverse matrix

    def __str__ (self) :
        (a, b, e), (c, d, f) = self._matrix [:2]
        return "(%s, %s, %s, %s, %s, %s)" % (a, b, c, d, e, f)
    # end def __str__

    def __repr__ (self) :
        return "%s %s" % (self.__class__.__name__, str (self))
    # end def __repr__

# end class Affine

if __name__ != "__main__" :
    D2._Export ("*")
### __END__ TFL.D2.Affine

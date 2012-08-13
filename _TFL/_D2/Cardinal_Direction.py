# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.D2.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.D2.Cardinal_Direction
#
# Purpose
#    Cardinal directtion in 2D space
#
# Revision Dates
#    13-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _TFL     import TFL
from   _TFL._D2 import D2

from   _TFL.Math_Func import sign

import _TFL._D2.Point

class _Cardinal_Direction_ (D2._Point_) :
    """Base class for points expressed by cardinal directions in 2D space."""

    ordinal_map =  \
        { (+1, +1) : "NE"
        , (+1, -1) : "SE"
        , (-1, -1) : "SW"
        , (-1, +1) : "NW"
        }

    def _formatted (self) :
        x, y = tuple (self)
        sx   = sign (x)
        sy   = sign (y)
        ax   = abs  (x)
        ay   = abs (y)
        if ax == ay :
            if ax :
                od = self.ordinal_map [(sx, sy)]
                result = self._formatted_dir (od, ax)
            else :
                result = "E + W"
        else :
            rs = []
            if x :
                rs.append (self._formatted_dir (("E", "W") [x < 0], ax))
            if y :
                rs.append (self._formatted_dir (("N", "S") [y < 0], ay))
            result = " + ".join (rs)
        return result
    # end def _formatted

    def _formatted_dir (self, d, v) :
        return ("%s*%s" % (d, v)) if v != 1 else d
    # end def _formatted_dir

    def __str__ (self) :
        return self._formatted ()
    # end def __str__

# end class _Cardinal_Direction_

class Cardinal_Direction (_Cardinal_Direction_, D2.Point) :
    """Cardinal direction in rectangular, 2D space.

    >>> for d in (N, E, S, W) :
    ...     print (d, tuple (d), repr (d))
    N (0, 1) Cardinal_Direction (0, 1)
    E (1, 0) Cardinal_Direction (1, 0)
    S (0, -1) Cardinal_Direction (0, -1)
    W (-1, 0) Cardinal_Direction (-1, 0)

    >>> print (E + N)
    NE

    >>> print (2*N + 2*E)
    NE*2

    >>> print (S + 5*W)
    W*5 + S

    >>> p = E*2 + N*5
    >>> q = R_Point_P (p, E*3 + N)
    >>> print ("p =", p)
    p = E*2 + N*5
    >>> print ("q =", q)
    q = E*5 + N*6

    >>> print ("p =", p.scale (Point (2, 0.5)))
    p = E*4 + N*2.5
    >>> print ("q =", q)
    q = E*7 + N*3.5

    >>> print ("q =", q.scale (Point (3, 2)))
    q = E*21 + N*7.0

    >>> import _TFL._D2.Line
    >>> l = D2.Line   (Point (0, 0), Point (20, 10))
    >>> q = R_Point_L (l, 0.5, NE * 2)
    >>> r = -q
    >>> print ("l =", l)
    l = (E + W, E*20 + N*10)
    >>> print ("q =", q)
    q = E*12.0 + N*7.0
    >>> print ("r =", r)
    r = W*12.0 + S*7.0

    >>> l.shift (Point (5, 5))
    Line (NE*5, E*25 + N*15)

    >>> print ("l =", l)
    l = (NE*5, E*25 + N*15)
    >>> print ("q =", q)
    q = E*17.0 + N*12.0
    >>> print ("r =", r)
    r = W*17.0 + S*12.0

    """

Point = Cardinal_Direction # end class

class _CD_R_Point_ (_Cardinal_Direction_, D2._R_Point_) :
    """Base class for cardinal direction Points positioned relative to
       another point.
    """

    Point = Cardinal_Direction

# end class _CD_R_Point_

def _derived (base) :
    real_name = base.__name__
    name      = "CD_" + real_name
    return base.__class__ \
        ( name, (_CD_R_Point_, base)
        , dict (_real_name = real_name)
        )
# end def _derived

R_Point_P  = Pp = _derived (D2.R_Point_P)
R_Point_L  = Pl = _derived (D2.R_Point_L)
R_Point_R  = Pr = _derived (D2.R_Point_R)
R_Point_nP = Pn = _derived (D2.R_Point_nP)

### cardinal directions
N  = North      = Cardinal_Direction ( 0, +1)
E  = East       = Cardinal_Direction (+1,  0)
S  = South      = Cardinal_Direction ( 0, -1)
W  = West       = Cardinal_Direction (-1,  0)

### ordinal directions
NE = North_East = Cardinal_Direction (+1, +1)
SE = South_East = Cardinal_Direction (+1, -1)
SW = South_West = Cardinal_Direction (-1, -1)
NW = North_West = Cardinal_Direction (-1, +1)

if __name__ != "__main__" :
    TFL.D2._Export_Module ()
    TFL.D2.CD = TFL.D2.Cardinal_Direction
### __END__ TFL.D2.Cardinal_Direction

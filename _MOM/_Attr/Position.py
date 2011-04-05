# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.Attr.
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
#    MOM.Attr.Position
#
# Purpose
#    Composite attribute type for geographical position
#
# Revision Dates
#     4-Feb-2010 (CT) Creation
#    13-Oct-2010 (CT) `example` added
#     5-Apr-2011 (MG) `distance` abd friends added
#    ««revision-date»»···
#--

from   _TFL                  import TFL
from   _MOM                  import MOM

from   _MOM._Attr            import Attr
import _MOM._Attr.Kind
from   _MOM._Attr.Type       import *

import _MOM.Entity

from   _TFL.I18N             import _, _T, _Tn

import  math

_Ancestor_Essence = MOM.An_Entity

class Position (_Ancestor_Essence) :
    """Model a geographical position."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class lat (A_Float) :
            """Latitude"""

            kind               = Attr.Necessary
            example            = u"42"
            min_value          = -90.0
            max_value          = +90.0
            ui_name            = "Latitude"

        # end class lat

        class lon (A_Float) :
            """Longitude"""

            kind               = Attr.Necessary
            example            = u"137"
            min_value          = -180.0
            max_value          = +180.0
            ui_name            = "Longitude"

        # end class lon

        class height (A_Float) :
            """Height above mean sea level"""

            kind               = Attr.Optional
            example            = u"1764"

        # end class height

    # end class _Attributes

    ### take from distance.py from thge geoip library:
    ### http://http://code.google.com/p/geopy/
    def distance (self, other, ellipsoid = "WGS-84") :
        if ellipsoid is None :
            return self.greate_circle_distance (self, other)
        return self.vincenty_distance          (self, other, ellipsoid)
    # end def distance

    # Average great-circle radius in kilometers, from Wikipedia.
    # Using a sphere with this radius results in an error of up to about 0.5%.
    EARTH_RADIUS = 6372.795

    @classmethod
    def greate_circle_distance (cls, self, other) :
        """Use spherical geometry to calculate the surface distance between
           two geodesic points. This formula can be written many different
           ways, including just the use of the spherical law of cosines or
           the haversine formula.

           The class attribute `RADIUS` indicates which radius of the earth
           to use, in kilometers. The default is to use the module constant
           `EARTH_RADIUS`, which uses the average great-circle radius.
        """

        lat1 = math.radians (self.lat)
        lng1 = math.radians (self.lon)
        lat2 = math.radians (other.lat)
        lng2 = math.radians (other.lon)

        sin_lat1, cos_lat1 = math.sin (lat1), math.cos (lat1)
        sin_lat2, cos_lat2 = math.sin (lat2), math.cos (lat2)

        delta_lng            = lng2 - lng1
        cos_d_lng, sin_d_lng = math.cos (delta_lng), math.sin (delta_lng)

        # We're correcting from floating point rounding errors on very-near
        # and exact points here
        central_angle = math.acos \
            ( min
                ( 1.0
                , sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_d_lng
                )
            )

        # From http://en.wikipedia.org/wiki/Great_circle_distance:
        #   Historically, the use of this formula was simplified by the
        #   availability of tables for the haversine function. Although this
        #   formula is accurate for most distances, it too suffers from
        #   rounding errors for the special (and somewhat unusual) case of
        #   antipodal points (on opposite ends of the sphere). A more
        #   complicated formula that is accurate for all distances is: (below)

        d = math.atan2 \
            ( math.sqrt
                ( (cos_lat2 * sin_d_lng) ** 2
                + (cos_lat1 * sin_lat2 - sin_lat1 * cos_lat2 * cos_d_lng) ** 2
                )
            , sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_d_lng
            )
        return cls.EARTH_RADIUS * d
    # end def greate_circle_distance

    # From http://www.movable-type.co.uk/scripts/LatLongVincenty.html:
    #   The most accurate and widely used globally-applicable model for the earth
    #   ellipsoid is WGS-84, used in this script. Other ellipsoids offering a
    #   better fit to the local geoid include Airy (1830) in the UK, International
    #   1924 in much of Europe, Clarke (1880) in Africa, and GRS-67 in South
    #   America. America (NAD83) and Australia (GDA) use GRS-80, functionally
    #   equivalent to the WGS-84 ellipsoid.
    ELLIPSOIDS = \
        { # model           major (km)   minor (km)     flattening
          'WGS-84'        : (6378.137,    6356.7523142,  1 / 298.257223563)
        , 'GRS-80'        : (6378.137,    6356.7523141,  1 / 298.257222101)
        , 'Airy (1830)'   : (6377.563396, 6356.256909,   1 / 299.3249646)
        , 'Intl 1924'     : (6378.388,    6356.911946,   1 / 297.0)
        , 'Clarke (1880)' : (6378.249145, 6356.51486955, 1 / 293.465)
        , 'GRS-67'        : (6378.1600,   6356.774719,   1 / 298.25)
        }
    @classmethod
    def vincenty_distance (cls, self, other, ellipsoid = "WGS-84") :
        lat1 = math.radians (self.lat)
        lng1 = math.radians (self.lon)
        lat2 = math.radians (other.lat)
        lng2 = math.radians (other.lon)

        if isinstance (ellipsoid, basestring):
            major, minor, f = cls.ELLIPSOIDS [ellipsoid]
        else:
            major, minor, f = ellipsoid

        delta_lng = lng2 - lng1
        r_lat1    = math.atan ((1 - f) * math.tan (lat1))
        r_lat2    = math.atan ((1 - f) * math.tan (lat2))

        sin_r1, cos_r1 = math.sin (r_lat1), math.cos (r_lat1)
        sin_r2, cos_r2 = math.sin (r_lat2), math.cos (r_lat2)
        lmb_lng        = delta_lng
        lmb_prime      = 2 * math.pi

        iter_limit                 = 20
        while abs (lmb_lng - lmb_prime) > 10e-12 and iter_limit > 0 :
            sin_lmb_lng, cos_lmb_lng = math.sin (lmb_lng), math.cos (lmb_lng)

            sin_sigma = math.sqrt \
                ( (cos_r2 * sin_lmb_lng) ** 2
                + (cos_r1 * sin_r2 - sin_r1 * cos_r2 * cos_lmb_lng) ** 2
                )

            if sin_sigma == 0 :
                return 0.0 # Coincident points

            cos_sigma    = sin_r1 * sin_r2 + cos_r1 * cos_r2 * cos_lmb_lng
            sigma        = math.atan2 (sin_sigma, cos_sigma)

            sin_alpha    = cos_r1 * cos_r2 * sin_lmb_lng / sin_sigma
            cos_sq_alpha = 1 - sin_alpha ** 2

            if cos_sq_alpha != 0 :
                cos2_sigma_m = \
                    cos_sigma - 2 * (sin_r1 * sin_r2 / cos_sq_alpha)
            else:
                cos2_sigma_m = 0.0 # Equatorial line

            C = f / 16. * cos_sq_alpha * (4 + f * (4 - 3 * cos_sq_alpha))

            lmb_prime = lmb_lng
            lmb_lng   = \
                ( delta_lng + (1 - C) * f * sin_alpha * (
                    sigma + C * sin_sigma * (
                        cos2_sigma_m + C * cos_sigma * (
                            -1 + 2 * cos2_sigma_m ** 2
                        )
                    )
                )
            )
            iter_limit -= 1

        if not iter_limit :
            raise ValueError ("Vincenty formula failed to converge!")

        u_sq = cos_sq_alpha * (major ** 2 - minor ** 2) / minor ** 2

        A = 1 + u_sq / 16384. * (
            4096 + u_sq * (-768 + u_sq * (320 - 175 * u_sq))
        )

        B = u_sq / 1024. * (256 + u_sq * (-128 + u_sq * (74 - 47 * u_sq)))

        delta_sigma = (
            B * sin_sigma * (
                cos2_sigma_m + B / 4. * (
                    cos_sigma * (
                        -1 + 2 * cos2_sigma_m ** 2
                    ) - B / 6. * cos2_sigma_m * (
                        -3 + 4 * sin_sigma ** 2
                    ) * (
                        -3 + 4 * cos2_sigma_m ** 2
                    )
                )
            )
        )

        s = minor * A * (sigma - delta_sigma)
        return s
    # end def vincenty_distance

# end class Position

class A_Position (_A_Composite_) :
    """Models an attribute holding a geographical position."""

    C_Type         = Position
    typ            = "Position"

# end class A_Position

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
else :
    ### simple test for the distance calculation
    class P (object) :
        def __init__ (self, lat, lon) :
            self.lat    = lat
            self.lon    = lon
        # end def __init__
    # end class P
    p1 = P (41.48696, -71.31490) ### Thames Street, Newport, RI
    p2 = P (41.50475, -81.60280) ### Cleveland, OH 44106
    print Position.greate_circle_distance (p1, p2)
    print Position.vincenty_distance      (p1, p2)
    print Position.greate_circle_distance (p2, p1)
    print Position.vincenty_distance      (p2, p1)
### __END__ MOM.Attr.Position

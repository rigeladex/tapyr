# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SRM.
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
#    GTW.OMP.SRM.Regatta
#
# Purpose
#    Model a sailing regatta for one class or handicap
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#     5-May-2010 (CT) Cached attributes added
#     5-May-2010 (CT) `perma_name` defined as `Attr.Internal` to allow queries
#     7-May-2010 (CT) `year` added
#    10-May-2010 (CT) `discards` and `races` added
#    11-May-2010 (CT) `result` added
#    31-Aug-2010 (CT) `is_team_race` added to `Regatta_C`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

from   _GTW._OMP._SRM.Attr_Type import A_Regatta_Result

import _GTW._OMP._SRM.Boat_Class
import _GTW._OMP._SRM.Regatta_Event

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Link1

class Regatta (_Ancestor_Essence) :
    """Sailing regatta for one class or handicap."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Regatta event to which this regatta belongs."""

            role_type          = GTW.OMP.SRM.Regatta_Event
            role_name          = "event"
            auto_cache         = True

        # end class left

        ### Non-primary attributes

        class discards (A_Int) :
            """Number of discardable races in regatta"""

            kind               = Attr.Optional
            default            = 0
            min_value          = 0

        # end class discards

        class name (A_String) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

        # end class name

        class perma_name (A_String) :

            kind               = Attr.Internal
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("name", )

            def computed (self, obj) :
                return TFL.Ascii.sanitized_filename (obj.name.lower ())
            # end def computed

        # end class perma_name

        class races (A_Int) :
            """Number of races sailed in regatta"""

            kind               = Attr.Optional
            default            = 0
            min_value          = 0

        # end class races

        class result (A_Regatta_Result) :
            """Information about result."""

            kind               = Attr.Optional

        # end class result

        class short_title (A_String) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("name", )

            def computed (self, obj) :
                return TFL.Ascii.sanitized_filename (obj.name)
            # end def computed

        # end class short_title

        class title (A_String) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("left", "name")

            def computed (self, obj) :
                return ", ".join ((obj.left.title, obj.name))
            # end def computed

        # end class title

        class year (A_Int) :

            kind               = Attr.Query
            auto_up_depends    = ("left", )

            def query_fct (self) :
                return Q.left.year
            # end def query_fct

        # end class year

    # end class _Attributes

# end class Regatta

_Ancestor_Essence = Regatta

class Regatta_C (_Ancestor_Essence) :
    """Regatta for a single class of sail boats."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class boat_class (A_Object) :
            """Class of boats sailing in this regatta."""

            kind               = Attr.Primary
            Class              = GTW.OMP.SRM.Boat_Class

        # end class boat_class

        class is_team_race (A_Boolean) :

            kind               = Attr.Optional
            default            = False

        # end class is_team_race

        class name (_Ancestor.name) :

            auto_up_depends    = ("boat_class", )

            def computed (self, obj) :
                return TFL.Ascii.sanitized_filename (obj.boat_class.name)
            # end def computed

        # end class name

    # end class _Attributes

# end class Regatta_C

_Ancestor_Essence = Regatta

class Regatta_H (_Ancestor_Essence) :
    """Regatta for boats in a handicap system."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class handicap (A_String) :
            """Name of handicap system used for this regatta."""

            kind               = Attr.Primary
            max_length         = 10

        # end class handicap

        class name (_Ancestor.name) :

            auto_up_depends    = ("handicap", )

            def computed (self, obj) :
                return TFL.Ascii.sanitized_filename (obj.handicap)
            # end def computed

        # end class name
    # end class _Attributes

# end class Regatta_H

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Regatta

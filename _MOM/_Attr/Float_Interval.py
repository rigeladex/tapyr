# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
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
#    MOM.Attr.Float_Interval
#
# Purpose
#    Composite attribute type for interval of float values
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   __future__            import unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

_Ancestor_Essence = MOM.An_Entity

class Float_Interval (_Ancestor_Essence) :
    """Model a interval of float values (lower, upper)."""

    ui_display_sep = " - "

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class lower (A_Float) :
            """Lower bound of interval."""

            kind               = Attr.Necessary

        # end class lower

        class upper (A_Float) :
            """Upper bound of interval."""

            kind               = Attr.Necessary

        # end class upper

        class center (A_Float) :
            """Center of interval."""

            kind               = Attr.Query
            query              = (Q.lower + Q.upper) * 0.5
            auto_up_depends    = ("lower", "upper")

        # end class center

        class length (A_Float) :
            """Length of interval."""

            kind               = Attr.Query
            query              = Q.upper - Q.lower
            auto_up_depends    = ("lower", "upper")

        # end class length

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class is_valid (Pred.Condition) :
            """The upper bound must be greater than the lower bound."""

            kind               = Pred.Object
            assertion          = "lower < upper"
            attributes         = ("lower", "upper")

        # end class is_valid

    # end class _Predicates

# end class Float_Interval

class A_Float_Interval (_A_Composite_) :
    """Models an attribute holding a interval of float values (lower, upper)"""

    P_Type         = Float_Interval
    typ            = "Float_Interval"

# end class A_Float_Interval

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export ("*")
### __END__ MOM.Attr.Float_Interval

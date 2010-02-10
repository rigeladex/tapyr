# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    MOM.Attr.Lifetime
#
# Purpose
#    Composite attribute type for (birth-date, death-date)
#
# Revision Dates
#     9-Feb-2010 (CT) Creation
#    10-Feb-2010 (CT) `A_Lifetime_N` added
#    ««revision-date»»···
#--

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _TFL.I18N             import _, _T, _Tn

_Ancestor_Essence = MOM.An_Entity

class Lifetime (_Ancestor_Essence) :
    """Model a lifetime (birth-date, death-date)."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class alive (A_Boolean) :
            """Specifies whether person, entity, or links ia currently alive"""

            kind               = Attr.Query
            auto_up_depends    = ("birth", "death")
            ### need to recompute each time `alive` is accessed
            Kind_Mixins        = (Attr.Computed, )

            def query_fct (self) :
                now = A_Date.now ()
                return \
                    ( (Q.birth <= now)
                    & ((not Q.death) or (now <= Q.death))
                    )
            # end def query_fct

        # end class alive

        class birth (A_Date) :
            """Date of birth of an person, entity, or link"""

            kind               = Attr.Required
            ui_name            = "Birth date"

        # end class birth

        class death (A_Date) :
            """Date of death of an person, entity, or link"""

            kind               = Attr.Optional
            ui_name            = "Death date"

        # end class death

        class ui_display (A_String) :
            """Display in user interface"""

            kind               = Attr.Computed

            def computed (self, obj) :
                result = [obj.raw_attr ("birth")]
                if obj.death :
                    result.append (obj.raw_attr ("death"))
                return u"-".join (result)
            # end def computed

        # end class ui_display

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class death_after_birth (Pred.Condition) :
            """The date of death must be later than the date of birth"""

            kind               = Pred.Object
            assertion          = "birth < death"
            attributes         = ("birth", "death")

        # end class death_after_birth

    # end class _Predicates

# end class Lifetime

_Ancestor_Essence = Lifetime

class Lifetime_N (_Ancestor_Essence) :
    """Model a lifetime (birth-date [default: now], death-date)."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class birth (_Ancestor.birth) :

            Kind_Mixins        = (Attr.Sticky_Mixin, )

            def computed_default (self) :
                return self.now ()
            # end def computed_default

        # end class birth

    # end class _Attributes

# end class Lifetime_N

class A_Lifetime (_A_Composite_) :
    """Models an attribute holding a (birth-date, death-date)"""

    C_Type         = Lifetime
    typ            = "Lifetime"

# end class A_Lifetime

class A_Lifetime_N (A_Lifetime) :

    C_Type         = Lifetime_N

# end class A_Lifetime_N

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Lifetime

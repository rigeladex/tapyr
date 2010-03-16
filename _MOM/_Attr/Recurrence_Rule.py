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
#    MOM.Attr.Recurrence_Rule
#
# Purpose
#    Composite attribute type for recurrence rule
#
# Revision Dates
#    10-Mar-2010 (CT) Creation
#    10-Mar-2010 (MG) `unit.C_Type` added
#    12-Mar-2010 (CT) `A_Weekday_RR_List` added and used
#    15-Mar-2010 (CT) Interface of `attr.Pickler` changed again (`attr_type`)
#    15-Mar-2010 (CT) `A_Weekday_RR._from_string_eval` redefined
#    16-Mar-2010 (CT) Bugs fixed (`__nonzero__`, `easter_offset.rrule_name`,
#                     `finish` or `count`, ...)
#    ««revision-date»»···
#--

from   _MOM.import_MOM import *
from   _MOM.import_MOM import \
     _A_Binary_String_, _A_Composite_, _A_Named_Value_, _A_Typed_List_

from   _TFL.I18N       import _, _T, _Tn

import dateutil.rrule

class A_Weekday_RR (A_Attr_Type) :
    """Weekday specification in recurrence rule."""

    typ    = "Weekday_RR"

    C_Type = dateutil.rrule.weekday
    Names  = (_("MO"), _("TU"), _("WE"), _("TH"), _("FR"), _("SA"), _("SU"))
    Table  = dict ((k, getattr (dateutil.rrule, k)) for k in Names)

    class Pickler (TFL.Meta.Object) :

        class Type (_A_Binary_String_) :
            max_length = 6
        # end class Type

        @classmethod
        def as_cargo (cls, obj, attr_kind, attr_type, value) :
            return attr_type.as_string (value)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, obj, attr_kind, attr_type, cargo) :
            return attr_type.from_string (cargo, obj)
        # end def from_cargo

    # end class Pickler

    @TFL.Meta.Class_and_Instance_Method
    def as_string (soc, value) :
        if value is not None :
            return repr (value)
        return u""
    # end def as_string

    as_code = as_string

    @TFL.Meta.Class_and_Instance_Method
    def cooked (soc, value) :
        if isinstance (value, int) :
            value = soc.Table [soc.Names [value]]
        if value is not None and not isinstance (value, soc.C_Type) :
            raise ValueError \
                (_T ("Value `%r` is not of type %s") % (value, soc.C_Type))
        return value
    # end def cooked

    def from_string (self, s, obj = None, glob = None, locl = None) :
        if s :
            return self.cooked (self._call_eval (s, self.Table, {}))
    # end def from_string

    from_code = from_string

    def _from_string_eval (self, s, obj, glob, locl) :
        return self._call_eval (s, self.Table, locl)
    # end def _from_string_eval

# end class A_Weekday_RR

class A_Weekday_RR_List (_A_Typed_List_) :
    """A list of weekday specifications in recurrence rule"""

    typ    = "Weekday_RR_List"
    C_Type = A_Weekday_RR

# end class A_Weekday_RR_List

_Ancestor_Essence = MOM.An_Entity

class Recurrence_Rule (_Ancestor_Essence) :
    """Model a recurrence rule."""

    ### http://www.ietf.org/rfc/rfc2445.txt

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class count (A_Int) :
            """Maximum number of recurrences."""

            kind               = Attr.Optional
            min_value          = 1
            rank               = -80

            rrule_name         = "count"

        # end class count

        class easter_offset (A_Int_List) :
            """Offset to Easter sunday (positive or negative, 0 means the
               Easter sunday itself).
            """

            kind               = Attr.Optional
            rank               = 100

            rrule_name         = "byeaster"

        # end class easter_offset

        class month (A_Int_List) :
            """Restrict the recurrences to the months specified (1 means
               January, ...).
            """

            kind               = Attr.Optional
            rank               = -69

            rrule_name         = "bymonth"

        # end class month

        class month_day (A_Int_List) :
            """Restrict the recurrences to the days of the month specified.
               Negative numbers count from the end of the month
               (-1 means the last day of the month).
            """

            kind               = Attr.Optional
            rank               = -70

            rrule_name         = "bymonthday"

        # end class month_day

        class period (A_Int) :
            """The interval (measured in `units`) between
               successive recurrences of an event.
            """

            kind               = Attr.Optional
            default            = 1
            min_value          = 1
            rank               = -100

            rrule_name         = "interval"

        # end class period

        class restrict_pos (A_Int_List) :
            """Restrict recurrences to the numbers given. Negative numbers
               count from the last occurrence (-1 meaning the last occurrence).
            """

            kind               = Attr.Optional
            rank               = -80

            rrule_name         = "bysetpos"

        # end class restrict_pos

        class unit (_A_Named_Value_) :
            """Unit of recurrence. `interval` is interpreted in units of
               `frequency`.
            """

            C_Type             = A_Int
            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            Table              = dict \
                (  (k, getattr (dateutil.rrule, k.upper ()))
                for k in (_("Daily"), _("Weekly"), _("Monthly"), _("Yearly"))
                )
            default            = Table ["Weekly"]
            rank               = -99

            rrule_name         = "freq"

        # end class unit

        class week (A_Int_List) :
            """Restrict the recurrences to the week numbers specified."""

            kind               = Attr.Optional

            rrule_name         = "byweekno"

        # end class week

        class week_day (A_Weekday_RR_List) :
            """Restrict the recurrences to the days of the week specified.
               (0 means monday, 6 means sunday).
            """

            kind               = Attr.Optional
            rank               = -90

            rrule_name         = "byweekday"

        # end class week_day

        class first_day_of_week (A_Int) :

            kind               = Attr.Const
            default            = dateutil.rrule.MO.weekday

            rrule_name         = "wkst"

        # end class first_day_of_week

        class year_day (A_Int_List) :
            """Restrict the recurrences to the days of the year specified.
               Negative numbers count from the end of the year
               (-1 means the last day of the year).
            """

            kind               = Attr.Optional

            rrule_name         = "byyearday"

        # end class year_day

    # end class _Attributes

    def rule (self, start = None, finish = None, cache = False) :
        kw = dict (self._rrule_attrs ())
        if finish is None and not self.count :
            kw ["count"] = 1
        return dateutil.rrule.rrule \
            (dtstart = start, until = finish, cache = cache, ** kw)
    # end def rule

    def _rrule_attrs (self) :
        for a in self.attributes.itervalues () :
            name = getattr (a, "rrule_name", None)
            if name :
                value = a.get_value (self)
                if value is not None :
                    yield name, value
    # end def _rrule_attrs

    def __nonzero__ (self) :
        return self.has_substance ()
    # end def __nonzero__

# end class Recurrence_Rule

class A_Recurrence_Rule (_A_Composite_) :
    """Models an attribute holding a recurrence rule."""

    C_Type = Recurrence_Rule
    typ    = "Recurrence_Rule"

# end class A_Recurrence_Rule

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Recurrence_Rule

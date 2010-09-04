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
#    27-Apr-2010 (CT) Default for `glob` and `locl` changed from `None` to `{}`
#     7-Jun-2010 (CT) `A_Weekday_RR.Pickler` methods guarded against `None`
#    18-Aug-2010 (CT) Attributes `dates`, `finish`, and `start` added; method
#                     `rule` removed
#    18-Aug-2010 (CT) `unit.default` changed from `Weekly` to `Daily`
#    18-Aug-2010 (CT) `Recurrence_Rule_Set` added
#    19-Aug-2010 (CT) `_Recurrence_Rule_Mixin_` added to define `ui_display`
#    19-Aug-2010 (CT) `__nonzero__` factored to `An_Entity`
#    19-Aug-2010 (CT) `count_default` added
#     2-Sep-2010 (CT) Signatures of `Pickler.as_cargo` and `.from_cargo` changed
#     4-Sep-2010 (CT) s/owner/owner.owner/ where necessary (change of
#                     _A_Composite_Collection_)
#    ««revision-date»»···
#--

from   _MOM.import_MOM import *
from   _MOM.import_MOM import \
     ( _A_Binary_String_
     , _A_Composite_, _A_Composite_Collection_
     , _A_Named_Value_
     , _A_Typed_List_
     )

from   _TFL.I18N       import _, _T, _Tn

import datetime
import dateutil.rrule

class A_Weekday_RR (A_Attr_Type) :
    """Weekday specification in recurrence rule."""

    typ    = "Weekday_RR"

    P_Type = dateutil.rrule.weekday
    Names  = (_("MO"), _("TU"), _("WE"), _("TH"), _("FR"), _("SA"), _("SU"))
    Table  = dict ((k, getattr (dateutil.rrule, k)) for k in Names)

    class Pickler (TFL.Meta.Object) :

        class Type (_A_Binary_String_) :
            max_length = 8
        # end class Type

        @classmethod
        def as_cargo (cls, attr_kind, attr_type, value) :
            if value is not None :
                return attr_type.as_string (value)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, scope, attr_kind, attr_type, cargo) :
            if cargo is not None :
                return attr_type.from_string (cargo)
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
        elif isinstance (value, basestring) :
            value = soc.Table [value]
        if value is not None and not isinstance (value, soc.P_Type) :
            raise ValueError \
                ( _T ("Value `%r` is not of type %s") % (value, soc.P_Type)
                + "\n    %s" % ", ".join (soc.Names)
                )
        return value
    # end def cooked

    def _from_string (self, s, obj, glob, locl) :
        if s :
            return self.cooked (self._call_eval (s, self.Table, {}))
    # end def _from_string

# end class A_Weekday_RR

class A_Weekday_RR_List (_A_Typed_List_) :
    """A list of weekday specifications in recurrence rule"""

    typ    = "Weekday_RR_List"
    C_Type = A_Weekday_RR

# end class A_Weekday_RR_List

_Ancestor_Essence = MOM.An_Entity

class _Recurrence_Rule_Mixin_ (_Ancestor_Essence) :
    """Mixin for classes modelling recurrence rules."""

    occurrence_format = "%Y%m%d"

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class ui_display (_Ancestor.ui_display) :

            def computed (self, obj) :
                if obj :
                    fmt = obj.occurrence_format
                    return ", ".join (o.strftime (fmt) for o in obj.occurrences)
            # end def computed

        # end class ui_display

    # end class _Attributes

# end class _Recurrence_Rule_Mixin_

_Ancestor_Essence = _Recurrence_Rule_Mixin_

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

        class finish (A_Date) :
            """Finish date of the recurrence."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Mixin, )
            rank               = -105

            rrule_name         = "until"

            def computed (self, obj) :
                owner = obj.owner
                if owner :
                    try :
                        result = obj.owner.owner_attr.finish_getter (obj)
                    except AttributeError as exc :
                        pass
                    else :
                        if isinstance (result, MOM.Date_Interval) :
                            return result.finish
            # end def computed

        # end class finish

        class first_day_of_week (A_Weekday_RR) :
            """First day of week"""

            kind               = Attr.Const
            default            = dateutil.rrule.MO.weekday

            rrule_name         = "wkst"

        # end class first_day_of_week

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

        class occurrences (A_Blob) :

            ### needs to be `Computed`, not `Auto_Cached` because result
            ### depends on `start_getter` and `finish_getter`
            kind      = Attr.Computed

            def computed (self, obj) :
                if obj :
                    kw = dict (obj._rrule_attrs ())
                    if obj.finish is None and obj.count is None :
                        dc = 1
                        if obj.owner and obj.owner.owner_attr :
                            dc = obj.owner.owner_attr.count_default
                        kw ["count"] = dc
                    return dateutil.rrule.rrule (cache = True, ** kw)
            # end def computed

        # end class occurrences

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

        class start (A_Date) :
            """Start date of the recurrence."""

            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Computed_Mixin, )
            rank               = -110

            rrule_name         = "dtstart"

            def computed (self, obj) :
                owner = obj.owner
                if owner :
                    try :
                        result = obj.owner.owner_attr.start_getter (obj)
                    except AttributeError as exc :
                        pass
                    else :
                        if isinstance (result, MOM.Date_Interval) :
                            result = result.start
                        return result
            # end def computed

        # end class start

        class unit (_A_Named_Value_) :
            """Unit of recurrence. `period` is interpreted in units of
               `unit`.
            """

            C_Type             = A_Int
            kind               = Attr.Optional
            Kind_Mixins        = (Attr.Sticky_Mixin, )
            Table              = dict \
                (  (k, getattr (dateutil.rrule, k.upper ()))
                for k in (_("Daily"), _("Weekly"), _("Monthly"), _("Yearly"))
                )
            default            = Table ["Daily"]
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

        class year_day (A_Int_List) :
            """Restrict the recurrences to the days of the year specified.
               Negative numbers count from the end of the year
               (-1 means the last day of the year).
            """

            kind               = Attr.Optional

            rrule_name         = "byyearday"

        # end class year_day

    # end class _Attributes

    def _rrule_attrs (self) :
        for a in self.attributes.itervalues () :
            name = getattr (a, "rrule_name", None)
            if name :
                value = a.get_value (self)
                if value is not None and value != [] :
                    yield name, value
    # end def _rrule_attrs

# end class Recurrence_Rule

class A_Recurrence_Rule (_A_Composite_) :
    """Models an attribute holding a recurrence rule."""

    C_Type        = Recurrence_Rule
    typ           = "Recurrence_Rule"

    start_getter  = finish_getter = TFL.Getter.owner.date
    count_default = 1

# end class A_Recurrence_Rule

class A_Recurrence_Rule_List (_A_Composite_Collection_) :
    """A list of recurrence rules."""

    typ           = "Recurrence_Rule_List"
    C_Type        = A_Recurrence_Rule

# end class A_Recurrence_Rule_List

_Ancestor_Essence = _Recurrence_Rule_Mixin_

class Recurrence_Rule_Set (_Ancestor_Essence) :
    """Model a set of recurrence rules (possibly with exceptions)."""

    ### http://labix.org/python-dateutil

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class dates (A_Date_List) :
            """Dates included in the recurrence rule set."""

            kind               = Attr.Optional
            default            = []

        # end class dates

        class date_exceptions (A_Date_List) :
            """Dates excluded from the recurrence rule set."""

            kind               = Attr.Optional
            default            = []

        # end class date_exceptions

        class occurrences (A_Blob) :

            ### needs to be `Computed`, not `Auto_Cached` because result
            ### depends on `start_getter` and `finish_getter`
            kind      = Attr.Computed

            def computed (self, obj) :
                if obj :
                    result = dateutil.rrule.rruleset (cache = True)
                    for r in obj.rules :
                        result.rrule (r.occurrences)
                    for x in obj.rule_exceptions :
                        result.exrule (x.occurrences)
                    for d in obj.dates :
                        result.rdate \
                            (datetime.datetime.fromordinal (d.toordinal ()))
                    for x in obj.date_exceptions :
                        result.exdate \
                            (datetime.datetime.fromordinal (x.toordinal ()))
                    return result
            # end def computed

        # end class occurrences

        class rules (A_Recurrence_Rule_List) :
            """Rules included in the recurrence rule set."""

            kind               = Attr.Optional
            default            = []

            start_getter       = finish_getter = \
                TFL.Getter.owner.owner.owner.date

        # end class rules

        class rule_exceptions (A_Recurrence_Rule_List) :
            """Rules excluded from the recurrence rule set."""

            kind               = Attr.Optional
            default            = []

            start_getter       = finish_getter = \
                TFL.Getter.owner.owner.owner.date
            count_default      = 365

        # end class rule_exceptions

    # end class _Attributes

# end class Recurrence_Rule_Set

class A_Recurrence_Rule_Set (_A_Composite_) :
    """Models an attribute holding a recurrence rule."""

    C_Type     = Recurrence_Rule_Set
    typ        = "Recurrence_Rule_Set"

# end class A_Recurrence_Rule_Set

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Recurrence_Rule

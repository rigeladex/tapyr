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
#    13-Oct-2010 (CT) `example` added
#    ««revision-date»»···
#--

from   _MOM.import_MOM import *
from   _MOM.import_MOM import \
     ( _A_Binary_String_
     , _A_Typed_List_
     )

from   _TFL.I18N       import _, _T, _Tn

import datetime
import dateutil.rrule

class A_Weekday_RR (A_Attr_Type) :
    """Weekday specification in recurrence rule."""

    example = u"TU"
    typ     = "Weekday_RR"

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

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Recurrence_Rule

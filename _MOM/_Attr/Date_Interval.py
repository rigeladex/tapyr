# -*- coding: iso-8859-15 -*-
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
#    MOM.Attr.Date_Interval
#
# Purpose
#    Composite attribute type for date interval (start, finish)
#
# Revision Dates
#     9-Feb-2010 (CT) Creation
#    10-Feb-2010 (CT) `A_Date_Interval_N` added
#    10-Feb-2010 (MG) `query_fct` corrected
#    24-Feb-2010 (CT) s/Lifetime/Date_Interval/; s/birth/start/; s/death/finish/
#    28-Apr-2010 (CT) `Date_Interval.days` added
#    10-May-2010 (CT) `A_Date_Interval_C` added
#     8-Sep-2011 (CT) `Date_Interval.ui_display_format` redefined
#    ««revision-date»»···
#--

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _TFL.I18N             import _, _T, _Tn

_Ancestor_Essence = MOM.An_Entity

class Date_Interval (_Ancestor_Essence) :
    """Model a date interval (start, finish)."""

    ui_display_sep = " - "

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class alive (A_Boolean) :
            """Specifies whether entity is currently alive, i.e., the current
               date lies between `start` and `finish`.
            """

            kind               = Attr.Query
            auto_up_depends    = ("start", "finish")
            ### need to recompute each time `alive` is accessed
            Kind_Mixins        = (Attr.Computed, )

            def query_fct (self) :
                now = A_Date.now ()
                return \
                    ( ((Q.start  == None) | (Q.start <= now))
                    & ((Q.finish == None) | (now <= Q.finish))
                    )
            # end def query_fct

        # end class alive

        class days (A_Int) :
            """Length of interval in days."""

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("finish", "start")

            def computed (self, obj) :
                if obj.start :
                    result = 1
                    if obj.finish :
                        result += (obj.finish - obj.start).days
                    return result
            # end def computed

        # end class days

        class finish (A_Date) :
            """Finish date of interval"""

            kind               = Attr.Optional
            rank               = 2

        # end class finish

        class start (A_Date) :
            """Start date of interval"""

            kind               = Attr.Necessary
            rank               = 1

        # end class start

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class finish_after_start (Pred.Condition) :
            """The finish date must be later than the start date"""

            kind               = Pred.Object
            assertion          = "start <= finish"
            attributes         = ("start", "finish")

        # end class finish_after_start

    # end class _Predicates

    @property
    def ui_display_format (self) :
        attrs = [self.__class__.start]
        if self.finish and self.finish != self.start :
            attrs.append (self.__class__.finish)
        return self.ui_display_sep.join ("%%(%s)s" % a.name for a in attrs)
    # end def ui_display_format

    def __nonzero__ (self) :
        return self.start is not None
    # end def __nonzero__

# end class Date_Interval

_Ancestor_Essence = Date_Interval

class Date_Interval_C (_Ancestor_Essence) :
    """Model a date_interval (start, finish [default: `start`])."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class finish (_Ancestor.finish) :

            Kind_Mixins        = (Attr.Computed_Mixin, )

            def computed (self, obj) :
                if obj and obj.start :
                    return obj.start
            # end def computed

        # end class finish

    # end class _Attributes

# end class Date_Interval_C

class Date_Interval_N (_Ancestor_Essence) :
    """Model a date_interval (start [default: now], finish)."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class start (_Ancestor.start) :

            Kind_Mixins        = (Attr.Sticky_Mixin, )

            def computed_default (self) :
                return self.now ()
            # end def computed_default

        # end class start

    # end class _Attributes

# end class Date_Interval_N

class A_Date_Interval (_A_Composite_) :
    """Models an attribute holding a date interval (start, finish)"""

    C_Type         = Date_Interval
    typ            = "Date_Interval"

# end class A_Date_Interval

class A_Date_Interval_C (A_Date_Interval) :

    C_Type         = Date_Interval_C

# end class A_Date_Interval_C

class A_Date_Interval_N (A_Date_Interval) :

    C_Type         = Date_Interval_N

# end class A_Date_Interval_N

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Lifetime

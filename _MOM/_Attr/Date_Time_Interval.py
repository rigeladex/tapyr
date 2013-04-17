# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
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
#    MOM.Attr.Date_Time_Interval
#
# Purpose
#    Composite attribute type for date interval (start, finish)
#
# Revision Dates
#    11-Jan-2013 (CT) Creation
#    25-Feb-2013 (CT) Remove `alive.auto_up_depends`
#    17-Apr-2013 (CT) Use `Computed_Set_Mixin`, not `Computed_Mixin`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _TFL.I18N             import _, _T, _Tn

_Ancestor_Essence = MOM.An_Entity

class Date_Time_Interval (_Ancestor_Essence) :
    """Model a date interval (start, finish)."""

    ui_display_sep = " - "

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class alive (A_Boolean) :
            """Specifies whether entity is currently alive, i.e., the current
               date lies between `start` and `finish`.
            """

            kind               = Attr.Query
            ### need to recompute each time `alive` is accessed
            Kind_Mixins        = (Attr.Computed, )

            def query_fct (self) :
                now = A_Date_Time.now ()
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

        class finish (A_Date_Time) :
            """Finish date of interval"""

            kind               = Attr.Optional
            example            = "2038/01/19"
            rank               = 2

        # end class finish

        class start (A_Date_Time) :
            """Start date of interval"""

            kind               = Attr.Necessary
            example            = "1970/01/01"
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

# end class Date_Time_Interval

_Ancestor_Essence = Date_Time_Interval

class Date_Time_Interval_C (_Ancestor_Essence) :
    """Model a date_interval (start, finish [default: `start`])."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class finish (_Ancestor.finish) :

            Kind_Mixins        = (Attr.Computed_Set_Mixin, )

            def computed (self, obj) :
                if obj and obj.start :
                    return obj.start
            # end def computed

        # end class finish

    # end class _Attributes

# end class Date_Time_Interval_C

class Date_Time_Interval_N (_Ancestor_Essence) :
    """Model a date_interval (start [default: now], finish)."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class start (_Ancestor.start) :

            Kind_Mixins        = (Attr.Sticky_Mixin, )
            computed_default   = A_Date_Time.now

        # end class start

    # end class _Attributes

# end class Date_Time_Interval_N

class A_Date_Time_Interval (_A_Composite_) :
    """Models an attribute holding a date interval (start, finish)"""

    P_Type         = Date_Time_Interval
    typ            = "Date_Time_Interval"

# end class A_Date_Time_Interval

class A_Date_Time_Interval_C (A_Date_Time_Interval) :

    P_Type         = Date_Time_Interval_C

# end class A_Date_Time_Interval_C

class A_Date_Time_Interval_N (A_Date_Time_Interval) :

    P_Type         = Date_Time_Interval_N

# end class A_Date_Time_Interval_N

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Date_Interval

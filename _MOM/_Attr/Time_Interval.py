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
#    MOM.Attr.Time_Interval
#
# Purpose
#    Composite attribute type for time interval (start, finish)
#
# Revision Dates
#     8-Mar-2010 (CT) Creation
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM       import *
from   _MOM.import_MOM       import _A_Composite_

from   _TFL.I18N             import _, _T, _Tn

_Ancestor_Essence = MOM.An_Entity

class Time_Interval (_Ancestor_Essence) :
    """Model a time interval (start, finish)"""

    ui_display_sep = " - "

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class start (A_Time) :
            """Start time of interval"""

            kind               = Attr.Necessary
            rank               = 1

        # end class start

        class finish (A_Time) :
            """Finish time of interval"""

            kind               = Attr.Optional
            rank               = 2

        # end class finish

    # end class _Attributes

    class _Predicates (_Ancestor_Essence._Predicates) :

        _Ancestor = _Ancestor_Essence._Predicates

        class finish_after_start (Pred.Condition) :
            """The finish time must be later than the start time"""

            kind               = Pred.Object
            assertion          = "start < finish"
            attributes         = ("start", "finish")

        # end class finish_after_start

    # end class _Predicates

    def __nonzero__ (self) :
        return self.start is not None
    # end def __nonzero__

# end class Time_Interval

class A_Time_Interval (_A_Composite_) :
    """Models an attribute holding a time interval (start, finish)"""

    P_Type         = Time_Interval
    typ            = "Time_Interval"

# end class A_Time_Interval

__all__ = tuple \
    (  k for (k, v) in globals ().iteritems ()
    if isinstance (v, MOM.Meta.M_Attr_Type)
    )

if __name__ != "__main__" :
    MOM.Attr._Export (* __all__)
### __END__ MOM.Attr.Time_Interval

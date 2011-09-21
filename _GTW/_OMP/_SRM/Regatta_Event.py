# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.SRM.Regatta_Event
#
# Purpose
#    Model a sailing regatta event for one or more classes/handicaps
#
# Revision Dates
#    15-Apr-2010 (CT) Creation
#     5-May-2010 (CT) `perma_name` changed from `Cache` to `Internal` to
#                     allow use in queries
#    11-May-2010 (CT) `club` added
#    23-Nov-2010 (CT) `ui_date` changed to avoid display of `start == finish`
#    14-Dec-2010 (CT) `year` changed from `Internal` to `Cached`
#     8-Sep-2011 (CT) `completer` added to `name`, `club` and `desc`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM._Attr.Date_Interval import *

import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn
import _TFL.Ascii

_Ancestor_Essence = GTW.OMP.SRM.Object

class Regatta_Event (_Ancestor_Essence) :
    """Sailing regatta event for one or more classes/handicaps."""

    ui_display_sep        = " "

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class name (A_String) :
            """Name of the regatta event."""

            kind               = Attr.Primary
            max_length         = 64
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class name

        class date (A_Date_Interval_C) :
            """`start` and `finish` date of regatta"""

            kind               = Attr.Primary

            completer          = Attr.C_Completer_Spec (Attr.Selector.primary)

        # end class date

        ### Non-primary attributes

        class club (A_String) :
            """Club organizing the regatta event."""

            kind               = Attr.Optional
            max_length         = 8
            completer          = Attr.Completer_Spec  (1)

        # end class club

        class desc (A_String) :
            """Short description of the regatta."""

            kind               = Attr.Optional
            max_length         = 160
            completer          = Attr.Completer_Spec  (1)

        # end class desc

        class perma_name (A_String) :
            """Name used for perma-link."""

            kind               = Attr.Internal
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("name", )

            def computed (self, obj) :
                return TFL.Ascii.sanitized_filename (obj.name.lower ())
            # end def computed

        # end class perma_name

        class short_title (A_String) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("name", )

            def computed (self, obj) :
                return obj.name
            # end def computed

        # end class title

        class title (A_String) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("date", "name", "desc")

            def computed (self, obj) :
                return " ".join ((obj.desc or obj.name, obj.ui_date))
            # end def computed

        # end class title

        class ui_date (A_String) :

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("date", )
            date_format        = "%d.%m.%Y"

            def computed (self, obj) :
                date_format   = self.date_format
                start, finish = obj.date.start, obj.date.finish
                result        = []
                if finish is not None and finish.month == start.month :
                    if finish != start :
                        result.append (start.strftime  ("%d."))
                else :
                    result.append (start.strftime  (date_format))
                if finish is not None :
                    result.append (finish.strftime (date_format))
                return "--".join (result)
            # end def computed

        # end class ui_date

        class year (A_Int) :
            """Year in which the regatta happens."""

            kind               = Attr.Cached
            Kind_Mixins        = (Attr.Computed_Set_Mixin, )
            auto_up_depends    = ("date", )

            def computed (self, obj) :
                if obj.date and obj.date.start :
                    return obj.date.start.year
            # end def computed

        # end class year

    # end class _Attributes

# end class Regatta_Event

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Regatta_Event

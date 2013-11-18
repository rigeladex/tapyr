# -*- coding: utf-8 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.EVT.
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
#    GTW.OMP.EVT.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    15-Mar-2010 (CT) Creation
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     8-Nov-2011 (CT) `Calendar` added
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Remove `Form_args`,
#                     i.e., stuff related to non-AFS forms
#    24-Feb-2012 (CT) Remove `Event_occurs` (too electric by far)
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Calendar            = dict \
        ( ETM           = "GTW.OMP.EVT.Calendar"
        )
    Event               = dict \
        ( ETM           = "GTW.OMP.EVT.Event"
        , list_display  = ("left", "date", "time", "calendar")
        , sort_key      = TFL.Sorted_By
            ("-date.start", "-time.start", "left")
        )

# end class Admin

from   _GTW._AFS._MOM import Spec
import _GTW._OMP._EVT.Event
import _GTW._OMP._EVT.Recurrence_Spec

GTW.OMP.EVT.Event.GTW.afs_spec           = Spec.Entity \
    ( include_links =
        ( Spec.Entity_Link ("recurrence", include_links = ("rules", ))
        ,
        )
    )

GTW.OMP.EVT.Recurrence_Spec.GTW.afs_spec = Spec.Entity \
    (include_links = ("rules", ))

if __name__ != "__main__" :
    GTW.OMP.EVT._Export_Module ()
### __END__ GTW.OMP.EVT.Nav

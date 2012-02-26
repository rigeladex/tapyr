# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.SWP.
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
#    GTW.OMP.SWP.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    16-Feb-2010 (MG) Creation (based on GTW.OMP.PAP.Nav)
#    24-Feb-2010 (CT) Creation continued
#    11-Mar-2010 (MG) Special widget's used for event date/time
#    23-Mar-2010 (CT) `Gallery` and `Picture` added
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#     7-Nov-2011 (CT) Remove boilerplate from `afs_spec` for Entity_Link `clips`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Remove `Form_args`, `*_completer`,
#                     i.e., stuff related to non-AFS forms
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Clip_X               = dict \
        ( ETM            = "GTW.OMP.SWP.Clip_X"
        , list_display   =
            ( "ui_display", "short_title", "date", "creator", "format"
            , "last_changed"
            )
        , sort_key       = TFL.Sorted_By ("-date.start", "-prio", "perma_name")
        )

    Gallery              = dict \
        ( ETM            = "GTW.OMP.SWP.Gallery"
        , sort_key       = TFL.Sorted_By ("-date.start", "perma_name")
        )

    Page                 = dict \
        ( ETM            = "GTW.OMP.SWP.Page"
        , list_display   =
            ( "ui_display", "short_title", "date", "creator", "format"
            , "last_changed"
            )
        , sort_key       = TFL.Sorted_By ("-date.start", "-prio", "perma_name")
        )

    Picture              = dict \
        ( ETM            = "GTW.OMP.SWP.Picture"
        , sort_key       = TFL.Sorted_By \
            ("-left.date.start", "left.perma_name", "number")
        )

# end class Admin

from   _GTW._AFS._MOM import Spec
import _GTW._OMP._SWP.Page

GTW.OMP.SWP.Page.GTW.afs_spec = Spec.Entity \
    ( include_links =
        ( "creator"
        , Spec.Entity_Link
            ( "events"
            , include_links =
                ( Spec.Entity_Link ("recurrence", include_links = ("rules", ))
                ,
                )
            )
        , "clips"
        )
    )

if __name__ != "__main__" :
    GTW.OMP.SWP._Export_Module ()
### __END__ GTW.OMP.SWP.Nav

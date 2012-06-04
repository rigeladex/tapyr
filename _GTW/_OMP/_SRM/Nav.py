# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package  GTW.OMP.SRM.
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
#     GTW.OMP.SRM.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    19-Apr-2010 (CT) Creation
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#    31-Aug-2010 (CT) `Team` and `Team_has_Boat_in_Regatta` added
#     6-Sep-2010 (CT) `Boat_in_Regatta` adapted to change of `race_results`
#     7-Sep-2011 (CT) `Sailor` added
#    23-Sep-2011 (CT) `Club` added
#     7-Oct-2011 (CT) `GTW.OMP.SRM.Boat_in_Regatta.GTW.afs_spec` added
#    14-Nov-2011 (CT) Correct `Boat_in_Regatta.sort-key`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    24-Jan-2012 (CT) Add `_crew` to `GTW.OMP.SRM.Boat_in_Regatta.GTW.afs_spec`
#    24-Jan-2012 (CT) Remove `Form_args`, `regatta_completer`,
#                     i.e., stuff related to non-AFS forms
#     1-Feb-2012 (CT) Add `Extra` "AF_BiR" to `Form_Cache`
#     2-Feb-2012 (CT) Add `attr_spec` parameters to `AF_BiR`
#    27-Feb-2012 (CT) Add `GTW.OMP.SRM.Club.GTW.afs_kw` (`collapsed = False`)
#     4-Jun-2012 (CT) Rename `handicap` to `boat_class`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

from   _TFL.I18N                import _

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Boat               = dict \
        ( ETM          = "GTW.OMP.SRM.Boat"
        , sort_key     = TFL.Sorted_By ("left.name", "nation", "sail_number")
        )
    Boat_Class         = dict \
        ( ETM          = "GTW.OMP.SRM.Boat_Class"
        , sort_key     = TFL.Sorted_By ("name")
        )
    Boat_in_Regatta    = dict \
        ( ETM          = "GTW.OMP.SRM.Boat_in_Regatta"
        , sort_key     = TFL.Sorted_By
            ( "-regatta.event.date.start"
            , "skipper.person.last_name"
            , "skipper.person.first_name"
            )
        )
    Club               = dict \
        ( ETM          = "GTW.OMP.SRM.Club"
        )
    Page               = dict \
        ( ETM          = "GTW.OMP.SRM.Page"
        , sort_key     = TFL.Sorted_By ("-date.start", "perma_name")
        , list_display =
            ( "ui_display", "creator", "date", "format", "last_changed")
        )

    Regatta_C          = dict \
        ( ETM          = "GTW.OMP.SRM.Regatta_C"
        , sort_key     = TFL.Sorted_By ("-event.date.start", "boat_class.name")
        , list_display = ("event", "boat_class", "kind")
        )

    Regatta_H          = dict \
        ( ETM          = "GTW.OMP.SRM.Regatta_H"
        , sort_key     = TFL.Sorted_By ("-event.date.start", "boat_class.name")
        , list_display = ("event", "boat_class", "kind")
        )

    Regatta_Event      = dict \
        ( ETM          = "GTW.OMP.SRM.Regatta_Event"
        , sort_key     = TFL.Sorted_By ("-date.start", "name")
        , list_display = ( "name", "date", "desc")
        )

    Sailor             = dict \
        ( ETM          = "GTW.OMP.SRM.Sailor"
        )

    Team               = dict \
        ( ETM          = "GTW.OMP.SRM.Team"
        , sort_key     = TFL.Sorted_By
            ( "-regatta.event.date.start"
            , "name"
            )
        , list_display = ("regatta", "name", "club", "leader")
        )

    Team_has_Boat_in_Regatta = dict \
        ( ETM          = "GTW.OMP.SRM.Team_has_Boat_in_Regatta"
        , list_display = ("team", "boat.boat")
        )

# end class Admin

from   _GTW._AFS._MOM            import Spec
from   _GTW._AFS._MOM.Form_Cache import Extra, Form_Cache

import _GTW._OMP._SRM.Boat_in_Regatta

GTW.OMP.SRM.Club.GTW.afs_kw = dict (collapsed  = False)
GTW.OMP.SRM.Boat_in_Regatta.GTW.afs_spec = Spec.Entity \
    (include_links = ("_crew", "race_results", ))

Form_Cache.add \
    ( Extra
        ( "AF_BiR"
        , dict
            ( name = "GTW.OMP.SRM.Boat_in_Regatta"
            , spec = Spec.Entity
                ( attr_spec     = dict
                    ( right     = dict (prefilled  = True)
                    , place     = dict (show_in_ui = False)
                    , points    = dict (show_in_ui = False)
                    )
                , include_links = ("_crew", )
                )
            )
        )
    )

if __name__ != "__main__" :
     GTW.OMP.SRM._Export_Module ()
### __END__  GTW.OMP.SRM.Nav

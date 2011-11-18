# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin
import _GTW._Form._MOM.Javascript

from   _GTW._Form._MOM.Inline_Description      import \
    ( Link_Inline_Description       as LID
    , Attribute_Inline_Description  as AID
    , Collection_Inline_Description as CID
    )
from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )
from  _GTW._Form.Widget_Spec    import Widget_Spec as WS

from   _TFL.I18N                import _

primary  = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    regatta_completer = GTW.Form.MOM.Javascript.Completer \
        ( fields    =
            ("date", "name")
        , triggers  = dict
            ( date = dict (min_chars = 4)
            , name = dict (min_chars = 1)
            )
        , name      = "Regatta_Event"
        )

    ### XXX ...

    Boat = dict \
        ( ETM       = "GTW.OMP.SRM.Boat"
        , sort_key  = TFL.Sorted_By ("left.name", "nation", "sail_number")
        )
    Boat_Class = dict \
        ( ETM       = "GTW.OMP.SRM.Boat_Class"
        , sort_key  = TFL.Sorted_By ("name")
        )
    Boat_in_Regatta = dict \
        ( ETM       = "GTW.OMP.SRM.Boat_in_Regatta"
        , Form_args =
            ( FGD ()
            , LID
                ( "GTW.OMP.SRM.Race_Result"
                , FGD ()
                )
            )
        , sort_key  = TFL.Sorted_By
            ( "-regatta.event.date.start"
            , "skipper.person.last_name"
            , "skipper.person.first_name"
            )
        )
    Club = dict \
        ( ETM       = "GTW.OMP.SRM.Club"
        )
    Page          = dict \
        ( ETM       = "GTW.OMP.SRM.Page"
        , sort_key  = TFL.Sorted_By ("year", "perma_name")
        , Form_args =
            ( FGD
                ( AID
                    ( "event"
                    , FGD
                        ( primary
                        , render_mode = "table"
                        , css_class   = "inline-instance"
                        )
                    , completer = regatta_completer
                    )
                , "perma_name", "desc"
                , "date"
                , "creator"
                , "format"
                , "text"
                )
            ,
            )
        , list_display   =
            ( "ui_display", "creator", "date", "format", "last_changed")
        )

    Regatta_C       = dict \
        ( ETM       = "GTW.OMP.SRM.Regatta_C"
        , sort_key  = TFL.Sorted_By ("-event.date.start", "boat_class.name")
        , Form_args =
            ( FGD
                ( AID
                    ( "event"
                    , FGD
                        ( primary
                        , render_mode = "table"
                        , css_class   = "inline-instance"
                        )
                    , completer = regatta_completer
                    )
                , WF ()
                )
            ,
            )
        , list_display   = ("event", "boat_class", "kind")
        )

    Regatta_H       = dict \
        ( ETM       = "GTW.OMP.SRM.Regatta_H"
        , sort_key  = TFL.Sorted_By ("-event.date.start", "handicap")
        , Form_args =
            ( FGD
                ( AID
                    ( "event"
                    , FGD
                        ( primary
                        , render_mode = "table"
                        , css_class   = "inline-instance"
                        )
                    , completer = regatta_completer
                    )
                , WF ()
                )
            ,
            )
        , list_display   = ("event", "handicap", "kind")
        )

    Regatta_Event = dict \
        ( ETM       = "GTW.OMP.SRM.Regatta_Event"
        , sort_key  = TFL.Sorted_By ("-date.start", "name")
        , Form_args =
            ( FGD ("name", "date", "desc", "club", WF ())
            ,
            )
        , list_display   = ( "name", "date", "desc")
        )

    Sailor          = dict \
        ( ETM       = "GTW.OMP.SRM.Sailor"
        )

    Team            = dict \
        ( ETM       = "GTW.OMP.SRM.Team"
        , sort_key  = TFL.Sorted_By ("-regatta.event.date.start", "name")
        , list_display   = ("regatta", "name", "club", "leader")
        )

    Team_has_Boat_in_Regatta = dict \
        ( ETM       = "GTW.OMP.SRM.Team_has_Boat_in_Regatta"
        , list_display   = ("team", "boat.boat")
        )

# end class Admin

from   _GTW._AFS._MOM import Spec
import _GTW._OMP._SRM.Boat_in_Regatta

GTW.OMP.SRM.Boat_in_Regatta.GTW.afs_spec = Spec.Entity \
    (include_links = ("race_results", ))

if __name__ != "__main__" :
     GTW.OMP.SRM._Export_Module ()
### __END__  GTW.OMP.SRM.Nav

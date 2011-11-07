# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _TFL                     import TFL
from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin
import _GTW._Form._MOM.Javascript
import _GTW._OMP._PAP.Nav

from   _GTW._Form._MOM.Inline_Description      import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
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

    creator_completer = GTW.OMP.PAP.Nav.Admin.person_completer

    Clip_X          = dict \
        ( ETM       = "GTW.OMP.SWP.Clip_X"
        , Form_args =
            ( FGD
                ( primary, "title"
                , AID
                    ( "date"
                    , FGD (render_mode = "table")
                    , legend = _("Publication and expiration date")
                    )
                , "format", "text", "link_to"
                )
            ,
            )
        , list_display   =
            ( "ui_display", "short_title", "date", "creator", "format"
            , "last_changed"
            )
        , sort_key       = TFL.Sorted_By ("-date.start", "-prio", "perma_name")
        )

    Gallery         = dict \
        ( ETM       = "GTW.OMP.SWP.Gallery"
        , Form_args =
            ( FGD
                ( primary, "short_title", "title", "directory"
                , AID
                    ( "date"
                    , FGD (render_mode = "table")
                    , legend        = _("Publication and expiration date")
                    )
                 ### XXX put LID for Entity_created_by_Person here
#                , AID
#                    ( "creator"
#                    , FGD
#                        ( primary
#                        , render_mode = "table"
#                        , css_class   = "inline-instance"
#                        )
#                    , completer      = creator_completer
#                    , legend         = _("Photographer")
#                    )
                )
            ,
            )
        , sort_key       = TFL.Sorted_By ("-date.start", "perma_name")
        )

    Page            = dict \
        ( ETM       = "GTW.OMP.SWP.Page"
        , Form_args =
            ( FGD
                ( primary, "short_title", "title"
                , AID
                    ( "date"
                    , FGD (render_mode = "table")
                    , legend = _("Publication and expiration date")
                    )
                 ### XXX put LID for Entity_created_by_Person here
#                , AID
#                    ( "creator"
#                    , FGD ( primary
#                          , render_mode = "table"
#                          , css_class = "inline-instance"
#                          )
#                    , completer = creator_completer
#                    , legend = _("Creator of the contents of the web page")
#                    )
                , "head_line", "format", "text"
                )
            , LID
                ( "GTW.OMP.EVT.Event"
                , FGD
                    ( AID ( "date"
                          , render_mode = "table"
                          , legend      = _("Date interval of event")
                          , title       = _("Date interval")
                          )
                    , AID ( "time"
                          , render_mode = "table"
                          , legend      = _("Time interval of event")
                          , title       = _("Time interval")
                          )
                    , "detail"
                    , legend    = _("Events associated to page")
                    , render_mode = "div_seq"
                    , title     = _("Events")
                    )
                , LID
                    ( "GTW.OMP.EVT.Recurrence_Spec"
                    , FGD (render_mode = "div_seq")
                    , legend = _("Recurrence rule")
                    )
                )
            , LID
                ( "GTW.OMP.SWP.Clip_O"
                , FGD
                    ( "abstract"
                    #, widget = "html/form.jnj, fg_div_seq"
                    , AID
                        ( "date_x"
                        , render_mode = "table"
                        , legend      = _("Date interval of news clip")
                        , title       = _("Date interval")
                        )
                    , legend    = _("News clip for page")
                    , title     = _("Clip")
                    )
                )
            , FGD ()
            )
        , list_display   =
            ( "ui_display", "short_title", "date", "creator", "format"
            , "last_changed"
            )
        , sort_key       = TFL.Sorted_By ("-date.start", "-prio", "perma_name")
        )

    Picture         = dict \
        ( ETM       = "GTW.OMP.SWP.Picture"
        , Form_args =
            ( FGD
                ( AID
                    ( "gallery"
                    , FGD (primary, render_mode = "table")
                    , legend        = _("Gallery")
                    )
                , "number"
                , AID
                    ( "photo"
                    , FGD (render_mode = "table")
                    , legend        = _("Photo")
                    )
                , AID
                    ( "thumb"
                    , FGD (render_mode = "table")
                    , legend        = _("Thumbnail")
                    )
                )
            ,
            )
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

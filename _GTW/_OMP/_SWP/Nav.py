# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   _TFL                   import TFL
from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin
import _GTW._Form._MOM.Javascript

from   _GTW._Form._MOM.Inline_Description      import \
    ( Link_Inline_Description      as LID
    , Attribute_Inline_Description as AID
    )
from   _GTW._Form._MOM.Field_Group_Description import \
    ( Field_Group_Description as FGD
    , Field_Prefixer          as FP
    , Wildcard_Field          as WF
    )
from  _GTW._Form.Widget_Spec  import Widget_Spec as WS

from   _TFL.I18N                import _

primary = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Page            = dict \
        ( ETM       = "GTW.OMP.SWP.Page"
        , Type      = GTW.NAV.E_Type.Admin
        , Form_args =
            ( FGD
                ( "perma_name", "short_title", "title", "head_line"
                , "format", "text"
                )
            , AID
                ( "date"
                , FGD (widget = "html/form.jnj, fg_tr")
                , legend = _("Publication and expiration date")
                )
            , AID
                ( "author"
                , FGD ( primary
                      , widget    = "html/form.jnj, fg_tr"
                      , css_class = "inline-instance"
                      )
                , completer = GTW.Form.MOM.Javascript.Completer
                    ( fields    =
                        ("last_name", "first_name", "middle_name", "title")
                    , triggers  = dict
                        ( last_name  = dict (min_chars = 2)
                        , first_name = dict (min_chars = 2)
                        )
                    , name      = "Author_Info"
                    )
                , legend = _("Author of web page")
                )
            , LID
                ( "GTW.OMP.EVT.Event"
                , AID ( "date"
                      , widget = WS
                          ( AID.widget
                          , inline_table_th =
                              "html/form.jnj, inline_table_aid_sep_th"
                          , inline_table_td =
                              "html/form.jnj, inline_table_aid_sep_td"
                          )
                      )
                , AID ( "time"
                      , widget = WS
                          ( AID.widget
                          , inline_table_th =
                              "html/form.jnj, inline_table_aid_sep_th"
                          , inline_table_td =
                              "html/form.jnj, inline_table_aid_sep_td"
                          )
                      )
                , AID
                    ( "recurrence"
                    , FGD ()
                    , legend = _("Recurrence rule")
                    )
                , legend    = _("Events")
                , title     = _("Events")
                )
            , FGD ()
            )
        , list_display   =
            ("ui_display", "short_title", "date", "author", "format")
        , sort_key       = TFL.Sorted_By \
            ("-prio", "-date.start", "-date.finish", "perma_name")
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.SWP._Export_Module ()
### __END__ GTW.OMP.SWP.Nav

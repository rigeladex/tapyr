# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2011 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

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

primary = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    Calendar        = dict \
        ( ETM       = "GTW.OMP.EVT.Calendar"
        )
    Event           = dict \
        ( ETM       = "GTW.OMP.EVT.Event"
        , Form_args =
            ( FGD
                ( "object", "date", "time", "detail", "short_title"
                )
            , LID
                ( "GTW.OMP.EVT.Recurrence_Spec"
                , CID
                    ( "rules"
                    , legend = _("Recurrence rules")
                    , popup  = False
                    )
                , CID
                    ( "rule_exceptions"
                    , legend = _("Recurrence exceptions")
                    , popup  = False
                    )
                , FGD
                    ( "dates", "date_exceptions"
                    )
                , legend = _("Recurrence rule set")
                )
            )
        )

    Event_occurs    = dict \
        ( ETM       = "GTW.OMP.EVT.Event_occurs"
        , Form_args =
            ( FGD
                ( AID ("event", FGD ("object"))
                , "date"
                , "time"
                )
            ,
            )
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

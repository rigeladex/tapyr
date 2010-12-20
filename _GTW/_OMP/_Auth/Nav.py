# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.Auth.
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
#    GTW.OMP.Auth.Nav
#
# Purpose
#    Provide configuration for GTW.NAV.E_Type.Admin entries
#
# Revision Dates
#    26-Feb-2010 (CT) Creation
#    30-Apr-2010 (MG) Adapted to new form's
#     2-May-2010 (MG) Simplified
#     6-May-2010 (MG) Switch to render mode rendering
#    ««revision-date»»···
#--

from   _TFL.I18N                import _
from   _GTW                     import GTW

import _GTW._NAV._E_Type.Admin
from   _GTW._NAV.Permission     import Is_Superuser
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

primary = WF ("primary")

class Admin (object) :
    """Provide configuration for GTW.NAV.E_Type.Admin entries"""

    group_completer  =GTW.Form.MOM.Javascript.Completer \
        ( fields    = "name"
        , triggers  = dict (name = dict (min_chars = 1))
        , name      = "Group_Completer"
        )

    Account          = dict \
        ( ETM        = "GTW.OMP.Auth.Account_P"
        , Type       = GTW.NAV.E_Type.Admin
        , Form_args  =
            ( FGD ()
            , LID
                ( "GTW.OMP.Auth.Account_in_Group"
                , FGD ("group")
                , field_attrs = dict
                    (group = dict (completer = group_completer))
                , legend    = _("Groups")
                , title     = _("Groups")
                )
            )
        , permission = Is_Superuser ()
        )

    Group            = dict \
        ( ETM        = "GTW.OMP.Auth.Group"
        , Type       = GTW.NAV.E_Type.Admin
        , permission = Is_Superuser ()
        )

    Account_in_Group = dict \
        ( ETM        = "GTW.OMP.Auth.Account_in_Group"
        , Type       = GTW.NAV.E_Type.Admin
        , permission = Is_Superuser ()
        )

# end class Admin

if __name__ != "__main__" :
    GTW.OMP.Auth._Export_Module ()
### __END__ GTW.OMP.Auth.Nav

# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.SWP.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.SWP.Referral
#
# Purpose
#    A resource referring to another resource
#
# Revision Dates
#    28-Jan-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM.import_MOM          import *

from   _GTW                     import GTW

import _GTW._OMP._SWP.Object_PN

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SWP.Object_PN

class Referral (_Ancestor_Essence) :
    """A resource referring to another resource."""

    ui_display_sep        = "/"

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class parent_url (A_Url_L) :
            """URL of parent resource."""

            kind               = Attr.Primary
            rank               = -10

        # end class parent_url

        ### Non-primary attributes

        class download (A_Boolean) :
            """Mark `target_url` as download URL."""

            kind               = Attr.Optional
            raw_default        = "no"

        # end class download

        class target_url (A_Url) :
            """URL of target resource."""

            kind               = Attr.Required

        # end class target_url

    # end class _Attributes

# end class Referral

if __name__ != "__main__" :
    GTW.OMP.SWP._Export ("*")
### __END__ GTW.OMP.SWP.Referral

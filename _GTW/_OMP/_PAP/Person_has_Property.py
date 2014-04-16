# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.Person_has_Property
#
# Purpose
#    Add `my_person` to links between `Person` and `Property`
#
# Revision Dates
#    16-Apr-2014 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM.import_MOM        import *

from   _GTW._OMP._PAP.Subject_has_Property   import Subject_has_Property

def _add_my_person (auto_kw) :
    class my_person (A_Id_Entity) :
        """Person this %(right.role_name)s is attached to."""

        kind                = Attr.Query
        P_Type              = "PAP.Person"
        query               = Q.left
        hidden              = True

    # end class my_person
    auto_kw ["extra_attributes"].update (my_person = my_person)
# end def _add_my_person

_kw = Subject_has_Property.auto_derive_np_kw ["Person", "left"]

_kw ["_update_auto_kw"].update \
    ( my_person  = _add_my_person
    )

### __END__ GTW.OMP.PAP.Person_has_Property

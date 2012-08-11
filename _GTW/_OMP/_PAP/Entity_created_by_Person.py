# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.Entity_created_by_Person
#
# Purpose
#    Model created-by association for all kinds of entities
#
# Revision Dates
#    13-Oct-2010 (CT) Creation
#    14-Oct-2010 (CT) `Init_Only_Mixin` added to `_Attributes`
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#    11-Aug-2012 (CT) Add `refuse_links`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Entity
from   _GTW._OMP._PAP.Person  import Person

_Ancestor_Essence = MOM.Link2

class Entity_created_by_Person (PAP.Entity, _Ancestor_Essence) :
    """Created-By association for all kinds of entities"""

    refuse_links = set \
        (( "GTW.OMP.PAP.Entity_created_by_Person"
         , "PAP.Entity_created_by_Person"
        ))

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor   = _Ancestor_Essence._Attributes

        Kind_Mixins = (Attr.Init_Only_Mixin, )

        ### Primary attributes

        class left (_Ancestor.left) :
            """Entity created by `person`."""

            role_type          = MOM.Id_Entity
            role_name          = "entity"
            max_links          = 1

        # end class left

        class right (_Ancestor.right) :
            """Person that created the `entity`."""

            role_type          = Person
            role_name          = "creator"
            auto_cache         = True

        # end class right

        ### Non-primary attributes

        class date (A_Date_Time) :
            """Creation date/time."""

            kind               = Attr.Internal
            computed_default   = A_Date_Time.now

        # end class date

    # end class _Attributes

# end class Entity_created_by_Person

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Entity_created_by_Person

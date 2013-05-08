# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# #*** <License> ************************************************************#
# This module is part of the package MOM.
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
#    MOM.Id_Entity_has_Tag
#
# Purpose
#    Tagging of Id-Entities
#
# Revision Dates
#    29-Jan-2013 (MG) Creation
#    15-May-2013 (CT) Rename `auto_cache` to `auto_rev_ref`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from    _MOM.import_MOM        import *
from    _GTW                   import GTW
import  _GTW._OMP._PAP.Entity

_Ancestor_Essence = MOM.Object

class Tag (_Ancestor_Essence) :
    """Models a tag"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """The name of the tag"""

            kind               = Attr.Primary
            ignore_case        = True
            max_length         = 30

        # end class name

        class description (A_Text) :
            """Description for the tag"""

            kind               = Attr.Optional

        # end class description

    # end class _Attributes

# end class Tag

_Ancestor_Essence = MOM.Link2

class Id_Entity_has_Tag (_Ancestor_Essence) :
    """Taging associationfor all kind of entities"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Entity which has the tag"""

            role_type          = MOM.Id_Entity
            role_name          = "entity"

        # end class left

        class right (_Ancestor.right) :
            """The tag"""

            role_type          = Tag
            role_name          = "tag"
            auto_rev_ref       = True

        # end class right

        class entity_type_name (A_String) :
            """Cache the type name of the entity to allow filtering on
               database level
            """

            kind               = Attr.Internal
            max_length         = 60
            auto_up_depends    = ("right", )

            def computed (self, obj) :
                return str (obj.left.type_name)
            # end def computed

        # end class entity_type_name

    # end class _Attributes

# end class Id_Entity_has_Tag

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.Id_Entity_has_Tag

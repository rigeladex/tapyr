# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Person_has_Phone
#
# Purpose
#    Model the link between a person and a phone number
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#     3-Feb-2010 (CT) `_Person_has_Property_` factored
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

import _GTW._OMP._PAP.Entity
from   _GTW._OMP._PAP._Person_has_Property_  import _Person_has_Property_
from   _GTW._OMP._PAP.Phone                  import Phone

_Ancestor_Essence = _Person_has_Property_

class Person_has_Phone (_Ancestor_Essence) :
    """Model the link between a person and a phone number"""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class right (_Ancestor.right) :

            role_type     = Phone
            ui_name       = _("Phone")
            auto_cache    = True

        # end class right

        class extension (A_Int) :
            """Extension number used in PBX"""

            kind            = Attr.Optional
            min_value       = 0
            max_value       = 99999
            ui_name         = _("Extension")

        # end class extension

    # end class _Attributes

# end class Person_has_Phone

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Person_has_Phone

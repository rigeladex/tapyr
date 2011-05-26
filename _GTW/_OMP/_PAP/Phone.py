# -*- coding: iso-8859-15 -*-
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
#    GTW.OMP.PAP.Phone
#
# Purpose
#    Model a phone number
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#     3-Feb-2010 (MG) `extension`  removed
#    28-Feb-2010 (CT) Use `A_Numeric_String` instead of `A_Int` and
#                     `A_Decimal` for `country_code`, `area_code`, and `number`
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP

import _GTW._OMP._PAP.Entity

_Ancestor_Essence = MOM.Object

class _PAP_Phone_ (PAP.Entity, _Ancestor_Essence) :
    """Model a phone number"""

    _real_name     = "Phone"

    ui_display_sep = "/"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class country_code (A_Numeric_String) :
            """International country code of phone number (without prefix)"""

            kind           = Attr.Primary
            max_length     = 3
            check          = ("value != '0'", )
            rank           = 1

        # end class country_code

        class area_code (A_Numeric_String) :
            """National area code of phone number (without prefix)"""

            kind           = Attr.Primary
            max_length     = 5
            check          = ("value != '0'", )
            rank           = 2

        # end class area_code

        class number (A_Numeric_String) :
            """Phone number proper (without country code, area code, extension)"""

            kind           = Attr.Primary
            max_length     = 14
            check          = ("value != '0'", )
            rank           = 3

        # end class number

        class desc (A_String) :
            """Short description of the phone number"""

            kind           = Attr.Optional
            max_length     = 20
            ui_name        = "Description"

        # end class desc

    # end class _Attributes

Phone = _PAP_Phone_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Phone

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
#    GTW.OMP.PAP.Phone
#
# Purpose
#    Model a phone number
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

import _GTW._OMP._PAP.Entity

_Ancestor_Essence = MOM.Object

class _PAP_Phone_ (PAP.Entity, _Ancestor_Essence) :
    """Model a phone number"""

    _real_name = "Phone"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class country_code (A_Int) :
            """International country code of phone number (without prefix)"""

            kind           = Attr.Primary
            rank           = 1
            ui_name        = _("Country code")

            min_value      = 1
            max_value      = 999

        # end class country_code

        class area_code (A_Int) :
            """National area code of phone number (without prefix)"""

            kind           = Attr.Primary
            rank           = 2
            ui_name        = _("Area code")

            min_value      = 1

        # end class area_code

        class subscriber_number (A_Decimal) :
            """Phone number proper (without country code, area code, extension)"""

            kind           = Attr.Primary
            rank           = 3
            ui_name        = _("Number")

            min_value      = 100
            max_digits     = 14
            decimal_places = 0

        # end class subscriber_number

        class extension (A_Int) : ### Move into Link!
            """Extension number used in PBX"""

            kind            = Attr.Primary
            rank            = 4
            min_value       = 0

        # end class extension

        class desc (A_String) :
            """Short description of the phone number"""

            kind           = Attr.Optional
            max_length     = 20
            ui_name        = _("Description")

        # end class desc

    # end class _Attributes

Phone = _PAP_Phone_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Phone

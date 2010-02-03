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
#    GTW.OMP.PAP.Address
#
# Purpose
#    Model a (postal) address
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

class _PAP_Address_ (PAP.Entity, _Ancestor_Essence) :
    """Model a (postal) address."""

    _real_name = "Address"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class street (A_String) :
            """Street (or place) and house number"""

            kind           = Attr.Primary
            max_length     = 80
            rank           = 1
            ui_name        = _("Street")

        # end class street

        class zip (A_String) :
            """Zip code of address"""

            kind           = Attr.Primary
            max_length     = 6
            rank           = 2
            ui_name        = _("Zip code")

        # end class zip

        class city (A_String) :
            """City, town, or village"""

            kind           = Attr.Primary
            max_length     = 30
            rank           = 3
            ui_name        = _("City")

        # end class city

        class country (A_String) :

            kind           = Attr.Primary
            max_length     = 40
            rank           = 4
            ui_name        = _("Country")

        # end class country

        class region (A_String) :
            """State or province or region"""

            default        = u""
            kind           = Attr.Primary_Optional
            max_length     = 40
            rank           = 5
            ui_name        = _("Region")

        # end class region

        class desc (A_String) :
            """Short description of the address"""

            kind           = Attr.Optional
            max_length     = 20
            ui_name        = _("Description")

        # end class desc

        class lat (A_Float) :
            """Latitude"""

            kind           = Attr.Optional
            check          = ("-90.0 <= value <= 90.0", )
            ui_name        = _("Latitude")

        # end class lat

        class lon (A_Float) :
            """Longitude"""

            kind           = Attr.Optional
            check          = ("-180.0 <= value <= 180.0", )
            ui_name        = _("Longitude")

        # end class lon

    # end class _Attributes

    def components (self) :
        result = [self.street, ", ".join ((self.zip, self.city))]
        if self.region :
            result.append (self.region)
        result.append (self.country)
        return result
    # end def components

Address = _PAP_Address_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Address

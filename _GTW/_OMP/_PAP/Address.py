# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer All rights reserved
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
#     4-Feb-2010 (CT) Composite `position` instead of `lat` and `lon`
#    22-Feb-2010 (CT) `ignore_case` set for primary attributes
#    23-Mar-2011 (CT) `region` made `Optional`, not `Primary_Optional`
#     7-Sep-2011 (CT) `completer` specifications for primary attributes added
#    18-Nov-2011 (CT) Import `unicode_literals` from `__future__`
#     8-Aug-2012 (CT) Add `example`
#    ««revision-date»»···
#--

from   __future__            import unicode_literals

from   _MOM.import_MOM        import *
from   _MOM._Attr.Position    import *

from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
import _GTW._OMP._PAP.Entity

_Ancestor_Essence = PAP.Object

class _PAP_Address_ (_Ancestor_Essence) :
    """Model a (postal) address."""

    _real_name = "Address"

    class _Attributes (_Ancestor_Essence._Attributes) :

        ### Primary attributes

        class street (A_String) :
            """Street (or place) and house number"""

            kind           = Attr.Primary
            example        = "Mystery Lane 42"
            ignore_case    = True
            max_length     = 60
            rank           = 1

            completer      = Attr.Completer_Spec  (3, Attr.Selector.primary)

        # end class street

        class zip (A_String) :
            """Zip code of address"""

            kind           = Attr.Primary
            example        = "9876"
            ignore_case    = True
            max_length     = 6
            rank           = 2
            ui_name        = "Zip code"

            completer      = Attr.Completer_Spec  \
                (1, Attr.Selector.Primary_Followers ())

        # end class zip

        class city (A_String) :
            """City, town, or village"""

            kind           = Attr.Primary
            example        = "Middletown"
            ignore_case    = True
            max_length     = 30
            rank           = 3

            completer      = Attr.Completer_Spec  \
                (1, Attr.Selector.Primary_Followers ())

        # end class city

        class country (A_String) :
            "Country"

            kind           = Attr.Primary
            example        = "Land of the Brave"
            ignore_case    = True
            max_length     = 20
            rank           = 4

            completer      = Attr.Completer_Spec  \
                (1, Attr.Selector.Primary_Followers ())

        # end class country

        ### Non-primary attributes

        class region (A_String) :
            """State or province or region"""

            kind           = Attr.Optional
            ignore_case    = True
            max_length     = 20
            rank           = 5

        # end class region

        class desc (A_String) :
            """Short description of the address"""

            kind           = Attr.Optional
            max_length     = 20
            ui_name        = "Description"

            completer      = Attr.Completer_Spec  (1)

        # end class desc

        class position (A_Position) :
            """Geographical position"""

            kind           = Attr.Optional

        # end class position

    # end class _Attributes

    def components (self) :
        result = [self.FO.street, ", ".join ((self.FO.zip, self.FO.city))]
        if self.region :
            result.append (self.FO.region)
        result.append (self.FO.country)
        return result
    # end def components

Address = _PAP_Address_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Address

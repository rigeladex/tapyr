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
#    GTW.OMP.PAP.Person
#
# Purpose
#    Model a Person
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#    29-Jan-2010 (CT) `middle_name` added
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP
from   _TFL.I18N              import _

import _GTW._OMP._PAP.Entity

_Ancestor_Essence = MOM.Object

class _PAP_Person_ (PAP.Entity, _Ancestor_Essence) :
    """Model a person."""

    _real_name = "Person"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class last_name (A_String) :
            """Last name of person"""

            kind           = Attr.Primary
            max_length     = 48
            rank           = 1
            ui_name        = _("Last name")

        # end class last_name

        class first_name (A_String) :
            """First name of person"""

            kind           = Attr.Primary
            max_length     = 32
            rank           = 2
            ui_name        = _("First name")

        # end class first_name

        class middle_name (A_String) :
            """Middle name of person"""

            kind           = Attr.Primary_Optional
            default        = ""
            rank           = 1
            ui_name        = _("Middle name")

        # end class middle_name

        class title (A_String) :
            """Academic title."""

            kind           = Attr.Primary_Optional
            max_length     = 20
            rank           = 2
            ui_name        = _("Academic title")

        # end class title

        class birth_date (A_Date) :
            """Date of birth"""

            kind           = Attr.Optional
            ui_name        = _("Date of birth")

        # end class birth_date

        ### class sex (A_Sex) : ...

    # end class _Attributes

Person = _PAP_Person_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Person

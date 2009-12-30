# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
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
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

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

        # end class last_name

        class first_name (A_String) :
            """First name of person"""

            kind           = Attr.Primary
            max_length     = 32
            rank           = 2

        # end class first_name

        class title (A_String) :
            """Academic title."""

            kind           = Attr.Optional
            max_length     = 20

        # end class title

        class birth_date (A_Date) :
            """Date of birth"""

            kind           = Attr.Optional

        # end class birth_date

        ### class sex (A_Sex) : ...

    # end class _Attributes

Person = _PAP_Person_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Person

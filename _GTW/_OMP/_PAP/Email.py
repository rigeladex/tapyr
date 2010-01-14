# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Email
#
# Purpose
#    Model an email address
#
# Revision Dates
#    30-Dec-2009 (CT) Creation
#    14-Jan-2010 (CT) `ui_name` added to some attributes
#    ««revision-date»»···
#--

from   _MOM.import_MOM        import *
from   _GTW                   import GTW

import _GTW._OMP._PAP.Entity

_Ancestor_Essence = MOM.Object

class _PAP_Email_ (PAP.Entity, _Ancestor_Essence) :
    """Model an email address"""

    _real_name = "Email"

    class _Attributes (_Ancestor_Essence._Attributes) :

        class address (A_String) :
            """Email address (including domain)"""

            kind           = Attr.Primary
            max_length     = 80
            rank           = 1
            ui_name        = _("Email address")

        # end class address

        class desc (A_String) :
            """Short description of the email address"""

            kind           = Attr.Optional
            max_length     = 20
            ui_name        = _("Description")

        # end class desc

    # end class _Attributes

Email = _PAP_Email_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Email

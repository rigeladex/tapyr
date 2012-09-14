# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.PAP.
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
#    GTW.OMP.PAP.Property
#
# Purpose
#    Model a property of a subject, e.g., phone number, email, ...
#
# Revision Dates
#    12-Sep-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM             import *
from   _MOM._Attr.Date_Interval    import *

from   _GTW._OMP._PAP.Attr_Type    import *

from   _GTW                        import GTW
from   _GTW._OMP._PAP              import PAP
from   _TFL.I18N                   import _

import _GTW._OMP._PAP.Entity

_Ancestor_Essence = PAP.Object

class _PAP_Property_ (_Ancestor_Essence) :
    """Property of a subject, e.g., a person or a company."""

    _real_name  = "Property"

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class desc (A_String) :
            """Short description of the %(ui_name.lower ())s"""

            kind               = Attr.Optional
            example            = _("Office")
            max_length         = 20
            ui_name            = _("Description")

            completer          = Attr.Completer_Spec  (1)

        # end class desc

    # end class _Attributes

Property = _PAP_Property_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Property

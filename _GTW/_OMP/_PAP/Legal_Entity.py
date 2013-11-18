# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Legal_Entity
#
# Purpose
#    Model a legal entity that isn't a natural person
#
# Revision Dates
#     4-Mar-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM             import *
from   _GTW._OMP._PAP.Attr_Type    import *

from   _GTW                        import GTW
from   _GTW._OMP._PAP              import PAP
from   _TFL.I18N                   import _

import _GTW._OMP._PAP.Subject

_Ancestor_Essence = PAP.Subject

class _PAP_Legal_Entity_ (_Ancestor_Essence) :
    """Model a legal entity that isn't a natural person."""

    _real_name  = "Legal_Entity"

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class name (A_String) :
            """Name of %(type_base_name.lower ())s."""

            kind               = Attr.Primary
            max_length         = 64
            ignore_case        = True
            completer          = Attr.Completer_Spec  (2, Attr.Selector.primary)

        # end class name

        class short_name (A_String) :
            """Short name of %(type_base_name.lower ())s."""

            kind               = Attr.Optional
            max_length         = 12
            ignore_case        = True
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class short_name

    # end class _Attributes

Legal_Entity = _PAP_Legal_Entity_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Legal_Entity

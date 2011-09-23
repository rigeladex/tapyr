# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This modify is part of the package GTW.OMP.SRM.
#
# This modify is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This modify is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this modify. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.OMP.SRM.Club
#
# Purpose
#    Model a sailing club
#
# Revision Dates
#    23-Sep-2011 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _MOM.import_MOM          import *

import _GTW._OMP._SRM.Entity

from   _TFL.I18N                import _, _T, _Tn

_Ancestor_Essence = GTW.OMP.SRM.Object

class Club (_Ancestor_Essence) :
    """A sailing club."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class name (A_String) :
            """Short name of the sailing club."""

            kind               = Attr.Primary
            example            = "RORC"
            ignore_case        = True
            max_length         = 8
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class name

        ### Non-primary attributes

        class long_name (A_String) :
            """Long name of the sailing club."""

            kind               = Attr.Optional
            example            = "Royal Ocean Racing Club"
            max_length         = 64

        # end class long_name

    # end class _Attributes

# end class Club

if __name__ != "__main__" :
    GTW.OMP.SRM._Export ("*")
### __END__ GTW.OMP.SRM.Club

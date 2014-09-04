# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Subject
#
# Purpose
#    Model a legal subject, i.e., person or company
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    19-Mar-2012 (CT) Add `is_partial = True` to `Subject`
#     4-Sep-2014 (CT) Add query attribute `my_group`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM             import *
from   _MOM._Attr.Date_Interval    import *

from   _GTW._OMP._PAP.Attr_Type    import *

from   _GTW                        import GTW
from   _GTW._OMP._PAP              import PAP
from   _TFL.I18N                   import _

import _GTW._OMP._PAP.Entity

_Ancestor_Essence = PAP.Object

class _PAP_Subject_ (_Ancestor_Essence) :
    """Model a legal subject, i.e., a person or company."""

    _real_name  = "Subject"

    is_partial  = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        class lifetime (A_Date_Interval) :
            """Date of birth [`start`] (and death [`finish`])"""

            kind           = Attr.Optional

        # end class lifetime

        class my_group (A_Id_Entity) :
            """Just an alias to be allow polymorphic queries using `my_group`.

               For instance, if a E_Type has an attribute `owner` with P_Type
               `PAP.Subject`, a query like::

                   Q.owner == g

               where `g` is an instance of `PAP.Group` will work, but would
               fail without the `my_group` defined here as `Q.NIL`.
            """

            kind               = Attr.Query
            P_Type             = "PAP.Group"
            query              = Q.NIL
            hidden             = True

        # end class my_group

        class my_person (A_Id_Entity) :
            """Just an alias to be allow polymorphic queries using `my_person`.

               For instance, if a E_Type has an attribute `owner` with P_Type
               `PAP.Subject`, a query like::

                   Q.owner == p

               where `p` is an instance of `PAP.Person` will work, but would
               fail without the `my_person` defined here as `Q.NIL`.
            """

            kind               = Attr.Query
            P_Type             = "PAP.Person"
            query              = Q.NIL
            hidden             = True

        # end class my_person

    # end class _Attributes

Subject = _PAP_Subject_ # end class

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Subject

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
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
#    GTW.OMP.PAP.Attr_Type
#
# Purpose
#    Define attribute types for package GTW.OMP.PAP
#
# Revision Dates
#     4-Jun-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _MOM.import_MOM          import *
from   _MOM.import_MOM          import _A_Named_Object_

import _GTW._OMP._PAP

from   _TFL.I18N                import _, _T, _Tn

class A_Sex (_A_Named_Object_) :
    """Sex of a person."""

    typ       = "Sex"
    Table     = \
        { u"F"  : _(u"Female")
        , u"M"  : _(u"Male")
        }

# end class A_Sex

if __name__ != "__main__" :
    GTW.OMP.PAP._Export ("*")
### __END__ GTW.OMP.PAP.Attr_Type

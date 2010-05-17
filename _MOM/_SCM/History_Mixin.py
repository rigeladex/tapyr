# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.SCM.History_Mixin
#
# Purpose
#    History mixin for MOM Scope change management
#
# Revision Dates
#     7-Oct-2009 (CT) Creation (factored from TOM.SCM.History_Mixin)
#    17-Dec-2009 (CT) `add_change` added
#    ««revision-date»»···
#--

from   _MOM          import MOM
from   _TFL          import TFL

import _MOM._SCM

import _TFL._Meta.Object

class History_Mixin (TFL.Meta.Object) :

    change_count = 0

    def __init__ (self) :
        self.history      = []
    # end def __init__

    def add_change (self, change) :
        self.history.append (change)
    # end def add_change

    def __nonzero__ (self) :
        return bool (self.change_count or self.history)
    # end def __nonzero__

# end class History_Mixin

if __name__ != "__main__" :
    MOM.SCM._Export ("*")
### __END__ MOM.SCM.History_Mixin

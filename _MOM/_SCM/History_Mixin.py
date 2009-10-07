# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2009 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.cluster
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
#    MOM.SCM.History_Mixin
#
# Purpose
#    History mixin for MOM Scope change management
#
# Revision Dates
#     7-Oct-2009 (CT) Creation (factored from TOM.SCM.Change)
#    ««revision-date»»···
#--

from   _MOM          import MOM
from   _TFL          import TFL

import _MOM._SCM

import _TFL._Meta.Object

class History_Mixin (TFL.Meta.Object) :

    def __init__ (self) :
        self.change_count = 0
        self.history      = []
    # end def __init__

    def __nonzero__ (self) :
        return bool (self.change_count or self.history)
    # end def __nonzero__

# end class History_Mixin

if __name__ != "__main__" :
    MOM.SCM._Export ("*")
### __END__ MOM.SCM.History_Mixin

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.MOM.
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
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.MOM.Compiler
#
# Purpose
#    Compile AFS Forms for MOM entities
#
# Revision Dates
#     8-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS._MOM

import _TFL._Meta.Object

class _Base_ (TFL.Meta.Object) :
    """Base class for MOM-AFS compiler."""

# end class _Base_

class Entity (_Base_) :
    """Compile a AFS form element for a MOM Entity."""

    def __init__ (self) :
        pass ### XXX
    # end def __init__

# end class Entity

if __name__ != "__main__" :
    GTW.AFS.MOM._Export ("*")
### __END__ GTW.AFS.MOM.Compiler

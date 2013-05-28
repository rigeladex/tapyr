# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package TFL.UI.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this module; if not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    TFL.UI.Change_Counter
#
# Purpose
#    Change counter to track changes in object model
#
# Revision Dates
#    28-May-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _TFL           import TFL
import _TFL._UI.Mixin

class Change_Counter (TFL.UI.Mixin) :
    """Change counter to track changes in object model and in UI widgets"""

    def __init__ (self, scxope = None) :
        self.scope  = scope
        self._count = 0
    # end def __init__

    def inc (self) :
        self._count += 1
    # end def inc

    def __iadd__ (self, rhs) :
        self._count += rhs
    # end def __iadd__

    def __int__ (self) :
        result = self._count
        if self.scope is not None :
            result += self.scope.changes
        return result
    # end def __int__

# end class TFL.UI.Change_Counter

if __name__ != "__main__" :
    TFL.UI._Export ("*")
### __END__ TFL.UI.Change_Counter

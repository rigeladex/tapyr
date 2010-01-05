# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer. All rights reserved
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
#    MOM.Pred.Err_and_Warn_List
#
# Purpose
#    Encapsules lists of error and warning objects
#
# Revision Dates
#     1-Oct-2009 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Pred

import _TFL._Meta.Object

class Err_and_Warn_List (TFL.Meta.Object) :

    def __init__ (self, errors, warnings) :
        self.errors   = errors
        self.warnings = warnings
    # end def __init__

    def extend (self, other) :
        self.errors.extend   (other.errors)
        self.warnings.extend (other.warnings)
    # end def extend

    def __len__ (self) :
        return len (self.errors)
    # end def __len__

    def __nonzero__ (self) :
        return bool (self.errors)
    # end def __nonzero__

    def __iter__ (self) :
        return iter (self.errors)
    # end def __iter__

# end class Err_and_Warn_List

if __name__ != "__main__" :
    MOM.Pred._Export ("*")
### __END__ MOM.Pred.Err_and_Warn_List

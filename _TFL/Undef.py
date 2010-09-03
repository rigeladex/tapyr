# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package TFL.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public License
# icense along with this module; if not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    TFL.Undef
#
# Purpose
#    Provide a class for defining undefined objects with nice repr
#
# Revision Dates
#     3-Sep-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _TFL               import TFL

class Undef (object) :
    """Undefined object."""

    def __init__ (self, name = None) :
        self.name = name
    # end def __init__

    def __repr__ (self) :
        names = [self.__class__.__name__]
        if self.name :
            names.append (self.name)
        return "<%s>" % "/".join (names)
    # end def __repr__

# end class Undef

if __name__ != "__main__" :
    TFL._Export ("Undef")
### __END__ TFL.Undef

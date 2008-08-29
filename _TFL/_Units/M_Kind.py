# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2008 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    TFL.Units.M_Kind
#
# Purpose
#    Meta class for TFL.Units.Kind
#
# Revision Dates
#     9-Aug-2004 (CT) Creation
#    29-Aug-2008 (CT) s/super(...)/__m_super/
#    ««revision-date»»···
#--

from   _TFL import TFL
import _TFL._Meta.M_Class
import _TFL._Units.Unit

class M_Kind (TFL.Meta.M_Class) :
    """Meta class for TFL.Units.Kind"""

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        cls.abbrs = abbrs = {}
        cls.units = units = {}
        for u in (cls.base_unit, ) + tuple (cls._units) :
            if u :
                units [u.name] = abbrs [u.abbr] = u
                setattr (cls, u.name, u)
    # end def __init__

# end class M_Kind

if __name__ != "__main__" :
    TFL.Units._Export ("M_Kind")
### __END__ TFL.Units.M_Kind

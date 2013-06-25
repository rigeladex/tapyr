# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.Prop.
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
#    MOM.Prop.Kind
#
# Purpose
#    Base class for attribute and predicate kinds
#
# Revision Dates
#    24-Sep-2009 (CT) Creation
#    12-Sep-2012 (CT) Add `__init__` argument `e_type`
#    25-Jun-2013 (CT) Use `__mro__`, not `mro ()`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Meta.M_Prop_Kind
import _MOM._Prop

import _TFL._Meta.M_Class

class _Prop_Kind_ (property) :
    """Base class for attribute and predicate kinds."""

    __metaclass__ = MOM.Meta.M_Prop_Kind
    _real_name    = "Kind"

    def __init__ (self, prop, e_type) :
        self.prop    = prop
        self.name    = prop.name
        self.__doc__ = prop.description
    # end def __init__

    def __getattr__ (self, name) :
        if not name.startswith ("_") :
            return getattr (self.prop, name)
        raise AttributeError \
            ("%s [%s: %s]" % (name, self, self.__class__.__mro__))
    # end def __getattr__

Kind = _Prop_Kind_ # end class

if __name__ != "__main__" :
    MOM.Prop._Export ("*")
### __END__ MOM.Prop.Kind

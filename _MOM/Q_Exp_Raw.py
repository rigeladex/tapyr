# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.
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
#    MOM.Q_Exp_Raw
#
# Purpose
#    Extend TFL.Q_Exp to support query expressions for raw values
#
# Revision Dates
#    19-Jul-2011 (CT) Creation
#    19-Jul-2011 (MG) `_name` converted to `Once_Property`
#    13-Sep-2011 (CT) All Q_Exp internal classes renamed to `_«name»_`
#     8-Jul-2013 (CT) Derive `_RAW_DESC_` from `object`, not `property`
#    19-Jul-2013 (CT) Derive `Raw_Attr_Query` from `Attr_Query`;
#                     set `Q_Exp.Base.RAW` to `Raw_Attr_Query ()`;
#                     remove `_RAW_` and `_RAW_DESC_` (nice simplification)
#    30-Aug-2013 (CT) Remove `SET`
#    ««revision-date»»···
#--

from   __future__               import unicode_literals

from   _MOM                     import MOM
from   _TFL                     import TFL
from   _TFL._Meta.Once_Property import Once_Property

import _MOM.Entity
import _TFL.Q_Exp

class Raw_Attr_Query (TFL.Attr_Query) :
    """Syntactic sugar for creating Filter objects based on raw attribute
       queries.
    """

    def __getattr__ (self, name) :
        return self._Get_Raw_ (self, name)
    # end def __getattr__

# end class Raw_Attr_Query

TFL.Q_Exp.Base.RAW = Raw_Attr_Query ()

@TFL.Add_New_Method (Raw_Attr_Query)
class _Get_Raw_ (TFL.Q_Exp._Get_) :
    """Query getter for raw values."""

    def __init__ (self, Q, postfix, prefix = "") :
        self.Q        = Q
        self._postfix = postfix
        self._prefix  = prefix
    # end def __init__

    def _getter (self, obj) :
        if self._prefix :
            obj = getattr (TFL.Getter, self._prefix) (obj)
        key = self._postfix
        if hasattr (obj, "raw_attr") and key in obj.attributes :
            return obj.raw_attr (key)
        else :
            result = getattr (obj, key)
            if isinstance (obj, MOM.Entity) :
                result = unicode (result)
            return result
    # end def _getter

    @Once_Property
    def _name (self) :
        if self._prefix :
            return ".".join ((self._prefix, self._postfix))
        return self._postfix
    # end def _name

    def __getattr__ (self, name) :
        return self.__class__ (self.Q, name, self._name)
    # end def __getattr__

    def __repr__ (self) :
        return "Q.RAW.%s" % (self._name, )
    # end def __repr__

# end class _Get_Raw_

if __name__ != "__main__" :
    MOM._Export_Module ()
### __END__ MOM.Q_Exp_Raw

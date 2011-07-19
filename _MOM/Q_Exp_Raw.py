# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   __future__               import unicode_literals

from   _MOM                     import MOM
from   _TFL                     import TFL
from   _TFL._Meta.Once_Property import Once_Property

import _MOM.Entity
import _TFL.Q_Exp

class _RAW_ (TFL.Meta.Object) :
    """Query generator for raw value queries."""

    def __init__ (self, Q) :
        self.Q = Q
    # end def __init__

    def __getattr__ (self, name) :
        return self.Get_Raw (self.Q, name)
    # end def __getattr__

# end class _RAW_

class _RAW_DESC_ (property) :

    def __get__ (self, obj, cls) :
        if obj is None :
            return self
        return _RAW_ (obj)
    # end def __get__

# end class _RAW_DESC_

TFL.Q_Exp.Base.RAW = _RAW_DESC_ ()

@TFL.Add_New_Method (_RAW_)
class Get_Raw (TFL.Q_Exp.Get) :
    """Query getter for raw values."""

    def __init__ (self, Q, postfix, prefix = "") :
        self.Q        = Q
        self._postfix = postfix
        self._prefix  = prefix
    # end def __init__

    def SET (self, obj, value) :
        if self._prefix :
            obj = getattr (TFL.Getter, self._prefix) (obj)
        obj.set_raw (** { self._postfix : value })
    # end def SET

    def _getter (self, obj) :
        if self._prefix :
            obj = getattr (TFL.Getter, self._prefix) (obj)
        key = self._postfix
        if key in obj.attributes :
            return obj.raw_attr (key)
        else :
            return unicode (getattr (obj, key))
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

# end class Get_Raw

### __END__ MOM.Q_Exp_Raw

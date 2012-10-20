# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.
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
#    GTW.RST.R_Map
#
# Purpose
#    Resource map
#
# Revision Dates
#    18-Oct-2012 (CT) Creation
#    20-Oct-2012 (CT) Add and use `_find_missing`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL
import _TFL._Meta.Object

class _M_R_Map_ (TFL.Meta.Object.__class__) :
    """Meta class for resource maps"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        cls.add_properties (* dct.get ("_prop_names", ()))
    # end def __init__

    def add_properties (cls, * names) :
        for name in names :
            cls.add_property (name)
    # end def add_properties

    def add_property (cls, name) :
        _name = "_" + name
        def _get (self) :
            result = getattr (self, _name)
            if result is None and self._find_missing is not None :
                result = self._find_missing (name)
            return result
        def _set (self, value) :
            setattr (self, _name, value)
        def _del (self) :
            setattr (self, _name, None)
        setattr (cls, name, property (_get, _set, _del))
        setattr (cls, _name, None)
    # end def add_property

# end class _M_R_Map_

class R_Map (TFL.Meta.Object) :
    """Resource map"""

    __metaclass__ = _M_R_Map_

    _find_missing = None
    _prop_names   = ()

    def __repr__ (self) :
        name  = self.__class__.__name__
        attrs = sorted \
            ((k.strip ("_"), v) for k, v in sorted (self.__dict__.iteritems ()))
        return "%s (%s)" % \
            (name, ", ".join (("%s = %s" % (k, v)) for k, v in attrs))
    # end def __repr__

# end class R_Map

if __name__ != "__main__" :
    GTW.RST._Export ("*")
### __END__ GTW.RST.R_Map

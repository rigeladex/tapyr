# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Graph.
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
#    MOM.Graph.Spec
#
# Purpose
#    Specification of MOM Graphs
#
# Revision Dates
#    16-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM._Graph

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class _Entity_ (TFL.Meta.Object) :
    """Specification of an essential entity as part of a Graph."""

    def __init__ (self, name = None) :
        self._name = name
        self._kw   = {}
    # end def __init__

    def __call__ (self, graph = None, ** kw) :
        if graph is not None :
            if kw :
                raise TypeError ("Can't pass both keyword args and `graph`")
            e_type = graph [self._name]
            return e_type (** self._kw)
        elif self._kw  :
            raise TypeError ("Can't call with keyword args twice")
        else :
            self._kw = kw
    # end def __call__

    def __getattr__ (self, name) :
        full_name = ".".join ((self._name, name)) if self._name else name
        return self.__class__ (full_name)
    # end def __getattr__

# end class _Entity_

class Graph (TFL.Meta.Object) :
    """Specification of a graph describing (part of) a MOM-based object model."""

    def __init__ (self, app_type, * entities) :
        self.app_type = app_type
        self.map      = {}
        self.add (* entities)
    # end def __init__

    def add (self, * entities) :
        for e_spec in entities :
            e_spec (self)
    # end def add

    def __contains__ (self, item) :
        return item in self.map
    # end def __contains__

    def __getitem__ (self, key) :
        try :
            result = self.map      [key]
        except KeyError :
            e_type = self.app_type [key]
            result = self.map      [key] = e_type.Graph_Type (self)
        return result
    # end def __getitem__

    def __len__ (self) :
        return len (self.map)
    # end def __len__

# end class Graph

if __name__ != "__main__" :
    MOM.Graph._Export_Module ()
### __END__ MOM.Graph.Spec

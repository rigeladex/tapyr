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
#    26-Aug-2012 (CT) Change `setup_links` to use `sorted`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM._Graph

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Accessor

class _E_Type_ (TFL.Meta.Object) :
    """Specification of an essential entity as part of a Graph."""

    anchor = None

    def __init__ (self, name = None) :
        self._name = name
        self._args = ()
        self._kw   = {}
    # end def __init__

    def __call__ (self, * args, ** kw) :
        if self._args or self._kw  :
            raise TypeError ("Can't call with args/kw twice")
        else :
            self._args = args
            self._kw   = kw
        return self
    # end def __call__

    def instantiate (self, graph, anchor = None, offset = None) :
        e_type = graph    [self._name]
        kw     = dict     (self._kw)
        if e_type.anchor is None :
            if anchor is not None :
                kw.setdefault ("anchor", anchor)
            if offset is not None :
                kw.setdefault ("offset", offset)
        result = e_type   (** kw)
        return result
    # end def instantiate

    def __getattr__ (self, name) :
        full_name = ".".join ((self._name, name)) if self._name else name
        return self.__class__ (full_name)
    # end def __getattr__

    def __str__ (self) :
        return "<E.%s %s>" % (self._name, sorted (self._kw.iteritems ()))
    # end def __str__

# end class _E_Type_

ET = _E_Type_ ()

class Graph (TFL.Meta.Object) :
    """Specification of a graph describing (part of) a MOM-based object model."""

    def __init__ (self, app_type, * entities) :
        self.app_type = app_type
        self.cid      = 0
        self.node_map = {}
        self.add (* entities)
    # end def __init__

    def add (self, * entities) :
        i = len (self.node_map)
        for e_spec in entities :
            e_spec.instantiate (self)
        for e in self.nodes () [i:] :
            e.auto_add_roles ()
    # end def add

    def nodes (self, sort_key = TFL.Getter.index) :
        return sorted (self.node_map.itervalues (), key = sort_key)
    # end def nodes

    def setup_links (self) :
        sort_key = TFL.Sorted_By ("slack", "type_name")
        for n in sorted (self.node_map.itervalues (), key = sort_key) :
            n.setup_links ()
    # end def setup_links

    def __contains__ (self, item) :
        return item in self.node_map
    # end def __contains__

    def __getitem__ (self, key) :
        try :
            result = self.node_map [key]
        except KeyError :
            e_type = self.app_type [key]
            result = self.node_map [key] = e_type.Graph_Type (self, e_type)
        return result
    # end def __getitem__

    def __len__ (self) :
        return len (self.node_map)
    # end def __len__

# end class Graph

if __name__ != "__main__" :
    MOM.Graph._Export_Module ()
### __END__ MOM.Graph.Spec

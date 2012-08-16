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
#    MOM.Graph.Entity
#
# Purpose
#    Model MOM entities as displayed in a MOM.Graph
#
# Revision Dates
#    16-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM               import MOM
from   _TFL               import TFL

import _MOM.import_MOM
import _MOM._Graph

import _TFL.Decorator
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class Entity (TFL.Meta.Object) :

    def __init__ (self, graph) :
        self.graph = graph
    # end def __init__

    def __call__ (self, ** kw) :
        ### XXX
        return self
    # end def __call__
# end class Entity

@TFL.Add_To_Class ("Graph_Type", MOM.Object)
class Object (Entity) :
    """Model display of a MOM.Object in a MOM graph"""
# end class Object

@TFL.Add_To_Class ("Graph_Type", MOM.Link1)
class Link1 (Entity) :
    """Model display of a MOM.Link1 in a MOM graph"""
# end class Link1

@TFL.Add_To_Class ("Graph_Type", MOM.Link2)
class Link2 (Entity) :
    """Model display of a MOM.Link2 in a MOM graph"""
# end class Link2

@TFL.Add_To_Class ("Graph_Type", MOM.Link3)
class Link3 (Entity) :
    """Model display of a MOM.Link3 in a MOM graph"""
# end class Link3

if __name__ != "__main__" :
    MOM.Graph._Export ("*")
### __END__ MOM.Graph.Entity

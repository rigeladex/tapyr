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
#    MOM.Graph.Relation
#
# Purpose
#    Model relations between MOM entities as displayed in a MOM.Graph
#
# Revision Dates
#    18-Aug-2012 (CT) Creation
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM                   import MOM
from   _TFL                   import TFL

import _MOM.import_MOM
import _MOM._Graph

from   _TFL._D2               import Cardinal_Direction as CD

import _TFL.Decorator
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

class _Relation_ (TFL.Meta.Object) :
    """Base class for relations between MOM entities."""

    @TFL.Meta.Once_Property
    def kind (self) :
        return self.__class__.__name__
    # end def kind

# end class _Relation_

class Attr (_Relation_) :
    """Model an attribute relation between MOM entities."""

    def __init__ (self, attr, source, target) :
        self.attr   = attr
        self.name   = attr.name
        self.source = source
        self.target = target
    # end def __init__

    def __repr__ (self) :
        return "<Graph.Relation.%s %s.%s -> %s>" % \
            (self.kind, self.source.type_name, self.name, self.target.type_name)
    # end def __repr__

# end class Attr

class Is_A (_Relation_) :
    """Model an inheritance relation between MOM entities."""

    name = "IS_A"

    def __init__ (self, source, target) :
        self.source = source
        self.target = target
    # end def __init__

    def __repr__ (self) :
        return "<Graph.Relation %s IS A %s>" % \
            (self.source.type_name, self.target.type_name)
    # end def __repr__

# end class IS_A

class Role (Attr) :
    """Model a link role relation between MOM entities."""
# end class Role

def new (rel, source, target) :
    """Return a Relation instance for `rel`, `source`, `target`."""
    if isinstance (rel, basestring) :
        if rel.startswith ("IS_A") :
            return Is_A (source, target)
        else :
            raise ValueError ("Don't understand relation %s" % (rel, ))
    else :
        T = Role if rel.is_link_role else Attr
        return T (rel, source, target)
# end def new

if __name__ != "__main__" :
    MOM.Graph._Export_Module ()
### __END__ MOM.Graph.Relation

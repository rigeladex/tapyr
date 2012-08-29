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
#    21-Aug-2012 (CT) Add `info` and `label`
#    22-Aug-2012 (CT) Add `delta`, `reverse`, `set_connector`
#    26-Aug-2012 (CT) Add `add_guides`
#    29-Aug-2012 (CT) Add `desc` and `title`
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

class _Reverse_ (TFL.Meta.Object) :
    """Reverse relation"""

    is_reverse        = True
    reverse           = None

    def __init__ (self, relation) :
        self.reverse = relation
    # end def __init__

    @TFL.Meta.Once_Property
    def delta (self) :
        return - self.reverse.delta
    # end def delta

    @property
    def other_connector (self) :
        return self.reverse.source_connector
    # end def other_connector

    @property
    def ref (self) :
        return self.target
    # end def pos

    def set_connector (self, side, offset) :
        assert self.reverse.target_connector is None
        self.reverse.target_connector = (side, offset)
    # end def set_connector

    def __getattr__ (self, name) :
        return getattr (self.reverse, name)
    # end def __getattr__

    def __repr__ (self) :
        return "<Graph.Reverse_Relation.%s %s.%s <- %s>" % \
            (self.kind, self.source.type_name, self.name, self.target.type_name)
    # end def __repr__

# end class _Reverse_

class _Relation_ (TFL.Meta.Object) :
    """Base class for relations between MOM entities."""

    guides            = None
    info              = None
    is_reverse        = False
    source_connector  = None
    target_connector  = None

    def __init__ (self, source, target) :
        self.source   = source
        self.target   = target
    # end def __init__

    @TFL.Meta.Once_Property
    def delta (self) :
        return self.source.pos - self.target.pos
    # end def delta

    @TFL.Meta.Once_Property
    def kind (self) :
        return self.__class__.__name__
    # end def kind

    @TFL.Meta.Once_Property
    def label (self) :
        return self.name
    # end def label

    @property
    def other_connector (self) :
        return self.target_connector
    # end def other_connector

    @property
    def ref (self) :
        return self.source
    # end def pos

    @TFL.Meta.Once_Property
    def reverse (self) :
        return _Reverse_ (self)
    # end def reverse

    def add_guides (self) :
        if self.source_connector and self.target_connector :
            src_c, trg_c = self.source_connector [0], self.target_connector [0]
            dim    = src_c.dim
            delta  = self.delta
            dd     = getattr (delta, dim)
            guides = self.guides = []
            add    = guides.append
            if src_c.is_opposite (trg_c) :
                if getattr (delta, src_c.other_dim) != 0 :
                    p2_a = CD.Point (** {dim : 1})
                    p2_b = CD.Point (* reversed (p2_a))
                    off  = src_c.guide_offset (1)
                    add ((CD.Point (1, 1), CD.Point (0, 0), off))
                    add ((p2_a,            p2_b,            off))
            else :
                p2_a = src_c.guide_point (0)
                p2_b = CD.Point (* reversed (p2_a))
                add ((p2_a, p2_b))
    # end def add_guides

    def set_connector (self, side, offset) :
        assert self.source_connector is None
        self.source_connector = (side, offset)
    # end def set_connector

# end class _Relation_

class Attr (_Relation_) :
    """Model an attribute relation between MOM entities."""

    def __init__ (self, attr, source, target) :
        self.attr   = attr
        self.name   = attr.name
        self.__super.__init__ (source, target)
    # end def __init__

    @TFL.Meta.Once_Property
    def desc (self) :
        return self.attr.description
    # end def desc

    @TFL.Meta.Once_Property
    def info (self) :
        result = self.attr.kind
        if result :
            return "[%s]" % (result, )
    # end def info

    @TFL.Meta.Once_Property
    def rid (self) :
        return "%s.%s:%s" % \
            (self.source.type_name, self.name, self.target.type_name)
    # end def rid

    @TFL.Meta.Once_Property
    def title (self) :
        return "%s attribute %s" % (self.source.type_name, self.name)
    # end def title

    def __repr__ (self) :
        return "<Graph.Relation.%s %s.%s -> %s>" % \
            (self.kind, self.source.type_name, self.name, self.target.type_name)
    # end def __repr__

# end class Attr

class Is_A (_Relation_) :
    """Model an inheritance relation between MOM entities."""

    name = "IS_A"

    @TFL.Meta.Once_Property
    def desc (self) :
        return "%s is derived from %s" % \
            (self.source.type_name, self.target.type_name)
    # end def desc

    @TFL.Meta.Once_Property
    def rid (self) :
        return "%s:is_a:%s" % (self.source.type_name, self.target.type_name)
    # end def rid

    @TFL.Meta.Once_Property
    def title (self) :
        return "%s is-a %s" % (self.source.type_name, self.target.type_name)
    # end def desc

    def __repr__ (self) :
        return "<Graph.Relation %s IS A %s>" % \
            (self.source.type_name, self.target.type_name)
    # end def __repr__

# end class Is_A

class Role (Attr) :
    """Model a link role relation between MOM entities."""

    @TFL.Meta.Once_Property
    def info (self) :
        result = self.attr.max_links
        if result and result > 0 :
            return "0 .. %s" % (result, )
    # end def info

    @TFL.Meta.Once_Property
    def label (self) :
        return self.attr.generic_role_name
    # end def label

    @TFL.Meta.Once_Property
    def rid (self) :
        return "%s.%s:%s" % \
            (self.source.type_name, self.attr.role_name, self.target.type_name)
    # end def rid

    @TFL.Meta.Once_Property
    def title (self) :
        return "%s role %s" % (self.source.type_name, self.attr.role_name)
    # end def title

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

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

from   _MOM                   import MOM
from   _TFL                   import TFL

import _MOM.import_MOM
import _MOM._Graph.Relation

from   _TFL._D2               import Cardinal_Direction as CD
from   _TFL.Regexp            import Regexp, re

import _TFL.Decorator
import _TFL._Meta.Object
import _TFL._Meta.Once_Property

_word_sep = Regexp("([^A-Za-z0-9])")

class Entity (TFL.Meta.Object) :

    attr       = None

    _anchor    = None
    _label     = None
    _offset    = None
    _pos       = None
    _sync_cid  = -1

    @property
    def anchor (self) :
        return self._anchor
    # end def anchor

    @anchor.setter
    def anchor (self, value) :
        if self._anchor is not None and value is not None :
            raise TypeError \
                ( "%s cannot have multiple anchors: %s <-> %s"
                % (self.type_name, self._anchor, value)
                )
        self.graph.cid +=1
        self._anchor = value
    # end def anchor

    @property
    def label (self) :
        result = self._label
        if result is None :
            result = self._label = self.type_name
        return result
    # end def label

    @TFL.Meta.Once_Property
    def label_parts (self) :
        def _gen (label) :
            parts = _word_sep.split (label)
            yield parts [0]
            it = iter (parts [1:])
            while True :
                try :
                    s = it.next ()
                    p = it.next ()
                except StopIteration :
                    break
                yield s + p
        label = self.label
        if label.startswith ("_") :
            return (label, )
        else :
            return tuple (_gen (label))
    # end def label_parts

    @property
    def offset (self) :
        result = self._offset
        if result is None :
            anchor = self.anchor
            if anchor is not None :
                pass ### XXX calculate automatic offset
        return result
    # end def offset

    @offset.setter
    def offset (self, value) :
        if value != self._offset :
            self.graph.cid +=1
            self._offset = value
    # end def offset

    @property
    def pos (self) :
        result = self._pos
        if result is None or self._sync_cid != self.graph.cid :
            self._sync_cid = self.graph.cid
            anchor = self.anchor
            if anchor is not None :
                result = CD.Pp    (anchor.pos, self.offset)
            else :
                result = CD.Point (* (self.offset or ()))
            self._pos = result
        return result
    # end def pos

    @TFL.Meta.Once_Property
    def type_name (self) :
        return self.e_type.type_name
    # end def type_name

    def __init__ (self, graph, e_type) :
        self.graph      = graph
        self.e_type     = e_type
        self.index      = len (graph.node_map)
        self.rel_map    = {}
        self.is_a_count = 0
    # end def __init__

    def __call__ (self, * args, ** kw) :
        self.pop_to_self (kw, "anchor", "offset")
        self.pop_to_self (kw, "label", prefix = "_")
        anchor = self.anchor
        graph  = self.graph
        e_type = self.e_type
        for a in args :
            self._add (a)
        for k, v in sorted (kw.iteritems ()) :
            if k == "IS_A" :
                rel = "IS_A_%d" % self.is_a_count
                self.is_a_count += 1
                self._add (v, rel)
            else :
                try :
                    attr = getattr (e_type, k)
                except AttributeError :
                    off  = CD.Point.from_name (k)
                    self._add (v, offset = off)
                else :
                    if attr.E_Type :
                        if isinstance (v, CD._Cardinal_Direction_) :
                            e = graph [attr.E_Type.type_name]
                            self._add (e, attr, offset = v)
                        else :
                            self._add (v, attr)
                    else :
                        raise TypeError \
                            ("Unknown kw argument: %s = %r" % (k, v))
        return self
    # end def __call__

    def auto_add_roles (self) :
        graph   = self.graph
        e_type  = self.e_type
        rel_map = self.rel_map
        for role in e_type.Roles :
            if role.name not in rel_map :
                e = graph [role.E_Type.type_name]
                self._add (e, role, auto = True)
    # end def auto_add_roles

    def instantiate (self, graph, anchor = None, offset = None) :
        if graph != self.graph :
            raise ValueError ("Non-matching graph")
        kw = {}
        if anchor is not None :
            kw ["anchor"] = anchor
        if offset is not None :
            kw ["offset"] = offset
        return self (** kw)
    # end def instantiate

    def _add (self, et, rel = None, ** kw) :
        auto = kw.pop ("auto", False)
        ikw  = dict (kw)
        if not (auto or et.anchor)  :
            ikw ["anchor"] = self
        result = et.instantiate (self.graph, ** ikw)
        rtn    = result.type_name
        if rel is None and rtn in self.e_type.role_map :
            rel = self.e_type.Roles [self.e_type.role_map [rtn]]
        if rel is not None :
            self.rel_map [getattr (rel, "name", rel)] = \
                MOM.Graph.Relation.new (rel, self, result)
        return result
    # end def _add

    def __repr__ (self) :
        return "%s @ %s" % (self, self.pos)
    # end def __repr__

    def __str__ (self) :
        result = "<Graph.%-6s %s>" % (self.__class__.__name__, self.type_name)
        return result
    # end def __str__

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

    @property
    def label (self) :
        result = self._label
        if result is None :
            e_type = self.e_type
            label  = e_type.type_base_name
            l_tbn  = e_type.left.E_Type.type_base_name
            if label.startswith (l_tbn) :
                label = label [len (l_tbn):]
            r_tbn  = e_type.right.E_Type.type_base_name
            if label.endswith (r_tbn) :
                label = label [:- len (r_tbn)]
            if label == e_type.type_base_name :
                label = e_type.type_name
            result = self._label = label
        return result
    # end def label

# end class Link2

@TFL.Add_To_Class ("Graph_Type", MOM.Link3)
class Link3 (Entity) :
    """Model display of a MOM.Link3 in a MOM graph"""
# end class Link3

if __name__ != "__main__" :
    MOM.Graph._Export ("*")
### __END__ MOM.Graph.Entity

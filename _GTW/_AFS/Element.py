# -*- coding: iso-8859-1 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.AFS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    GTW.AFS.Element
#
# Purpose
#    Model elements of AJAX-enhanced forms
#
# Revision Dates
#     6-Feb-2011 (CT) Creation
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import json

class _Element_ (TFL.Meta.Object) :
    """Base class for AFS element classes."""

    children = ()
    id_sep   = "."
    max_cid  = 0
    _id      = None

    def __init__ (self, ** kw) :
        children  = kw.pop ("children", None)
        id        = kw.pop ("id",       None)
        if children is not None :
            self.children = list (children)
        if id is not None :
            self.id = id
        self.kw = kw
    # end def __init__

    @property
    def id (self) :
        return self._id
    # end def id

    @id.setter
    def id (self, value) :
        if self._id is not None :
            raise TypeError \
                ("Cannot change id from `%s` to `%s`" % (self._id, value))
        self._id = value
    # end def id

    @Once_Property
    def as_json (self) :
        return json.dumps (self.as_json_cargo)
    # end def as_json

    @Once_Property
    def as_json_cargo (self) :
        result = dict (self.kw, type = self.__class__.__name__)
        if self.children :
            result ["children"] = [c.as_json_cargo for c in self.children]
        result ["$id"] = self.id
        return result
    # end def as_json_cargo

    def child_id (self, id, sep, id_map) :
        if id :
            result = sep.join ((id, str (self.max_cid + 1)))
            self.max_cid += 1
            if result in id_map :
                raise KeyError ("Duplicate id %s" % result)
            return result
    # end def child_id

    def copy (self, ** kw) :
        ckw      = dict (self.kw, ** kw)
        children = [c.copy () for c in self.children] if self.children else None
        return self.__class__ (children = children, ** ckw)
    # end def copy

    def _id_children (self, id, children, id_map) :
        sep = self.id_sep
        for c in children :
            c.id  = cid  = self.child_id (id, sep, id_map)
            id_map [cid] = c
            c._id_children (c.id, c.children, id_map)
    # end def _id_children

    def __getattr__ (self, name) :
        try :
            return self.kw [name]
        except KeyError :
            raise AttributeError (name)
    # end def __getattr__

    def __str__ (self) :
        n = getattr (self, "name", None) or getattr (self, "type_name", None)
        if n :
            return "<%s %s %r>" % (self.__class__.__name__, self.id, n)
        else :
            return "<%s %s>"    % (self.__class__.__name__, self.id)
    # end def __str__

# end class _Element_

class Entity (_Element_) :
    """Model a sub-form for a single entity."""

    id_sep = ":"

    def __init__ (self, type_name, ** kw) :
        self.__super.__init__ (type_name = type_name, ** kw)
    # end def __init__

# end class Entity

class Entity_List (_Element_) :
    """Model a sub-form for a list of entities.

       Because the number of elements varies from context to context, an
       instance of `Entity_List` has a `proto` entity defining the structure
       of the children. Children can be added as necessary, but won't be
       registered in the form's `id_map`.
    """

    id_sep  = "::"
    max_cid = -1

    def __init__ (self, type_name, proto, ** kw) :
        self.proto = proto
        self.__super.__init__ (type_name = type_name, ** kw)
    # end def __init__

    def add_child (self) :
        cs     = self.children
        id     = self.child_id   (self.id, self.id_sep, {})
        result = self.proto.copy (id = id)
        if id :
            result._id_children  (id, result.children, {})
        cs.append (result)
        return result
    # end def add_child

    def _id_children (self, id, children, id_map) :
        self.__super._id_children (id, [self.proto], id_map)
        self.__super._id_children (id, children,     {})
    # end def _id_children

# end class Entity_List

class Field (_Element_) :
    """Model a field of an AJAX-enhanced form."""

    def __init__ (self, name, ** kw) :
        self.__super.__init__ (name = name, ** kw)
    # end def __init__

# end class Field

class Field_Composite (Field) :
    """Model a composite field of a AJAX-enhanced form."""

# end class Field_Composite

class Fieldset (_Element_) :
    """Model a set of fields of an AJAX-enhanced form."""

    id_sep = ":"

# end class Fieldset

class Form (_Element_) :
    """Model a AJAX-enhanced form."""

    Table  = {}
    id_sep = ":"

    def __init__ (self, id, children, ** kw) :
        Table = self.Table
        if kw.pop ("REGISTER", True) :
            if id in Table :
                raise KeyError ("Duplicate form id %s" % id)
            else :
                Table [id] = self
        self.id_map = {}
        self.__super.__init__ (id = id, children = children, ** kw)
        self._id_children     (id, children, self.id_map)
    # end def __init__

    @Once_Property
    def dynamic_children_p (self) :
        s = Entity_List.id_sep
        return any ((s in id) for id in self.id_map)
    # end def dynamic_children_p

    def copy (self, ** kw) :
        if "id" not in kw :
            kw = dict (kw, id = self.id, REGISTER = False)
        return self.__super.copy (** kw)
    # end def copy

# end class Form

__doc__ = """
Usage example::

    >>> import pprint
    >>> f = Form ( "F"
    ...     , children =
    ...         [ Entity
    ...             ( type_name = "PAP.Person"
    ...             , children  =
    ...                 [ Fieldset
    ...                     ( name     = "primary"
    ...                     , children =
    ...                         [ Field (name  = "last_name")
    ...                         , Field (name  = "first_name")
    ...                         ]
    ...                     )
    ...                 , Field_Composite
    ...                     ( name     = "lifetime"
    ...                     , children =
    ...                         [ Field (name = "start")
    ...                         , Field (name = "finish")
    ...                         ]
    ...                     )
    ...                 ]
    ...             )
    ...         , Entity
    ...             ( type_name = "SRM.Boat_Type"
    ...             , children  =
    ...                 [ Field (name = "name")
    ...                 ]
    ...             )
    ...         ]
    ...     )
    >>> pprint.pprint (f.as_json_cargo)
    {'$id': 'F',
     'children': [{'$id': 'F:1',
                    'children': [{'$id': 'F:1:1',
                                   'children': [{'$id': 'F:1:1:1',
                                                  'name': 'last_name',
                                                  'type': 'Field'},
                                                 {'$id': 'F:1:1:2',
                                                  'name': 'first_name',
                                                  'type': 'Field'}],
                                   'name': 'primary',
                                   'type': 'Fieldset'},
                                  {'$id': 'F:1:2',
                                   'children': [{'$id': 'F:1:2.1',
                                                  'name': 'start',
                                                  'type': 'Field'},
                                                 {'$id': 'F:1:2.2',
                                                  'name': 'finish',
                                                  'type': 'Field'}],
                                   'name': 'lifetime',
                                   'type': 'Field_Composite'}],
                    'type': 'Entity',
                    'type_name': 'PAP.Person'},
                   {'$id': 'F:2',
                    'children': [{'$id': 'F:2:1',
                                   'name': 'name',
                                   'type': 'Field'}],
                    'type': 'Entity',
                    'type_name': 'SRM.Boat_Type'}],
     'type': 'Form'}
    >>> f.as_json
    '{"$id": "F", "type": "Form", "children": [{"$id": "F:1", "type_name": "PAP.Person", "type": "Entity", "children": [{"$id": "F:1:1", "type": "Fieldset", "name": "primary", "children": [{"$id": "F:1:1:1", "type": "Field", "name": "last_name"}, {"$id": "F:1:1:2", "type": "Field", "name": "first_name"}]}, {"$id": "F:1:2", "type": "Field_Composite", "name": "lifetime", "children": [{"$id": "F:1:2.1", "type": "Field", "name": "start"}, {"$id": "F:1:2.2", "type": "Field", "name": "finish"}]}]}, {"$id": "F:2", "type_name": "SRM.Boat_Type", "type": "Entity", "children": [{"$id": "F:2:1", "type": "Field", "name": "name"}]}]}'
    >>> sorted (f.id_map)
    ['F:1', 'F:1:1', 'F:1:1:1', 'F:1:1:2', 'F:1:2', 'F:1:2.1', 'F:1:2.2', 'F:2', 'F:2:1']
    >>> [str (f.id_map [id]) for id in sorted (f.id_map)]
    ["<Entity F:1 'PAP.Person'>", "<Fieldset F:1:1 'primary'>", "<Field F:1:1:1 'last_name'>", "<Field F:1:1:2 'first_name'>", "<Field_Composite F:1:2 'lifetime'>", "<Field F:1:2.1 'start'>", "<Field F:1:2.2 'finish'>", "<Entity F:2 'SRM.Boat_Type'>", "<Field F:2:1 'name'>"]

"""

if __name__ != "__main__" :
    GTW.AFS._Export ("*")
### __END__ GTW.AFS.Element

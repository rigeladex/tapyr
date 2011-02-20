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
#     7-Feb-2011 (CT) Creation continued
#     8-Feb-2011 (CT) Creation continued..
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.predicate           import split_hst, rsplit_hst

import json

class _Element_ (TFL.Meta.Object) :
    """Base class for AFS element classes."""

    children = ()
    id_sep   = "."
    list_sep = "::"
    root_sep = "-"
    max_cid  = 0
    _id      = None

    def __init__ (self, ** kw) :
        self.pop_to_self  (kw, "id", "id_sep")
        children = kw.pop ("children", None)
        if children is not None :
            self.children = list (children)
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

    def _formatted (self, level = 0) :
        result = ["%s%s" % (" " * level, self)]
        level += 1
        result.extend (c._formatted (level) for c in self.children)
        return "\n".join (result)
    # end def _formatted

    def _id_children (self, id, children, id_map) :
        sep = self.id_sep
        for c in children :
            c.id  = cid  = self.child_id (id, sep, id_map)
            _, _, lid    = rsplit_hst (cid, self.root_sep)
            id_map [lid] = c
            c._id_children (cid, c.children, id_map)
    # end def _id_children

    def __getattr__ (self, name) :
        try :
            return self.kw [name]
        except KeyError :
            raise AttributeError (name)
    # end def __getattr__

    def __repr__ (self) :
        return self._formatted ()
    # end def __repr__

    def __str__ (self) :
        n = getattr (self, "name", None) or getattr (self, "type_name", None)
        if n :
            return "<%s %s %r>" % (self.__class__.__name__, self.id, n)
        else :
            return "<%s %s>"    % (self.__class__.__name__, self.id)
    # end def __str__

# end class _Element_

class _Element_List_ (_Element_) :
    """Base class for AFS classes modelling a list of elements."""

    def __init__ (self, ** kw) :
        self.id_map = {}
        self.__super.__init__ (** kw)
    # end def __init__

    def __getitem__ (self, key) :
        r, _, k = split_hst (key, self.root_sep)
        h, _, t = split_hst (k,   self.list_sep)
        try :
            result = self.id_map [h]
            if t :
                if self.root_sep in t :
                    result = result [t]
                elif t == "0" : ### Access to prototype
                    result = result.proto
                else :
                    raise KeyError
        except (AttributeError, KeyError) :
            raise KeyError (key)
        return result
    # end def __getitem__

# end class _Element_List_

class Entity (_Element_) :
    """Model a sub-form for a single entity."""

    id_sep = ":"

    def __init__ (self, type_name, ** kw) :
        self.__super.__init__ (type_name = type_name, ** kw)
    # end def __init__

# end class Entity

class Entity_Link (Entity) :
    """Model a sub-form for a link to entity in containing sub-form."""

# end class Entity_Link

class Entity_List (_Element_List_) :
    """Model a sub-form for a list of entities.

       Because the number of elements varies from context to context, an
       instance of `Entity_List` has a `proto` entity defining the structure
       of the children. Children can be added as necessary, but won't be
       registered in the form's `id_map`.
    """

    id_sep  = _Element_List_.list_sep
    max_cid = -1

    def __init__ (self, proto, ** kw) :
        self.proto   = proto
        proto.id_sep = self.root_sep
        self.__super.__init__ (** kw)
    # end def __init__

    def add_child (self) :
        if self.children is self.__class__.children :
            self.children = []
        cs     = self.children
        result = self.proto.copy ()
        self._id_child_or_proto  (self.id, result, {})
        cs.append (result)
        return result
    # end def add_child

    def copy (self, ** kw) :
        return self.__super.copy (proto = self.proto.copy (), ** kw)
    # end def copy

    def _formatted (self, level = 0) :
        result = [self.__super._formatted (level)]
        if not self.children :
            result.append (self.proto._formatted (level + 1))
        return "\n".join (result)
    # end def _formatted

    def _id_children (self, id, children, id_map) :
        self._id_child_or_proto   (id, self.proto, self.id_map)
        self.__super._id_children (id, children,   {})
    # end def _id_children

    def _id_child_or_proto (self, id, cop, id_map) :
        cop.id = cid = self.child_id (id, self.id_sep, id_map)
        if cid :
            cop._id_children (cid, cop.children, id_map)
    # end def _id_child_or_proto

    def __str__ (self) :
        n = getattr (self, "name", None) or getattr (self, "type_name", None)
        p = str (self.proto)
        if n :
            return "<%s %s %r %s>" % (self.__class__.__name__, self.id, n, p)
        else :
            return "<%s %s %s>"    % (self.__class__.__name__, self.id, p)
    # end def __str__

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

class Form (_Element_List_) :
    """Model a AJAX-enhanced form."""

    id_sep = _Element_List_.root_sep
    Table  = {}

    def __init__ (self, id, children, ** kw) :
        Table = self.Table
        if kw.pop ("REGISTER", True) :
            if id in Table :
                raise KeyError ("Duplicate form id %s" % id)
            else :
                Table [id] = self
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
    ...                 , Entity_List
    ...                     ( proto     = Entity
    ...                         ( type_name = "PAP.Person_has_Email"
    ...                         , children  =
    ...                             [ Field (name = "desc")
    ...                             , Entity
    ...                                 ( type_name = "PAP.Email"
    ...                                 , children  = [Field (name = "address")]
    ...                                 )
    ...                             ]
    ...                         )
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
     'children': [{'$id': 'F-1',
                    'children': [{'$id': 'F-1:1',
                                   'children': [{'$id': 'F-1:1:1',
                                                  'name': 'last_name',
                                                  'type': 'Field'},
                                                 {'$id': 'F-1:1:2',
                                                  'name': 'first_name',
                                                  'type': 'Field'}],
                                   'name': 'primary',
                                   'type': 'Fieldset'},
                                  {'$id': 'F-1:2',
                                   'children': [{'$id': 'F-1:2.1',
                                                  'name': 'start',
                                                  'type': 'Field'},
                                                 {'$id': 'F-1:2.2',
                                                  'name': 'finish',
                                                  'type': 'Field'}],
                                   'name': 'lifetime',
                                   'type': 'Field_Composite'},
                                  {'$id': 'F-1:3', 'type': 'Entity_List'}],
                    'type': 'Entity',
                    'type_name': 'PAP.Person'},
                   {'$id': 'F-2',
                    'children': [{'$id': 'F-2:1',
                                   'name': 'name',
                                   'type': 'Field'}],
                    'type': 'Entity',
                    'type_name': 'SRM.Boat_Type'}],
     'type': 'Form'}
    >>> f.as_json
    '{"$id": "F", "type": "Form", "children": [{"$id": "F-1", "type_name": "PAP.Person", "type": "Entity", "children": [{"$id": "F-1:1", "type": "Fieldset", "name": "primary", "children": [{"$id": "F-1:1:1", "type": "Field", "name": "last_name"}, {"$id": "F-1:1:2", "type": "Field", "name": "first_name"}]}, {"$id": "F-1:2", "type": "Field_Composite", "name": "lifetime", "children": [{"$id": "F-1:2.1", "type": "Field", "name": "start"}, {"$id": "F-1:2.2", "type": "Field", "name": "finish"}]}, {"$id": "F-1:3", "type": "Entity_List"}]}, {"$id": "F-2", "type_name": "SRM.Boat_Type", "type": "Entity", "children": [{"$id": "F-2:1", "type": "Field", "name": "name"}]}]}'
    >>> sorted (f.id_map)
    ['1', '1:1', '1:1:1', '1:1:2', '1:2', '1:2.1', '1:2.2', '1:3', '2', '2:1']
    >>> [str (f.id_map [id]) for id in sorted (f.id_map)]
    ["<Entity F-1 'PAP.Person'>", "<Fieldset F-1:1 'primary'>", "<Field F-1:1:1 'last_name'>", "<Field F-1:1:2 'first_name'>", "<Field_Composite F-1:2 'lifetime'>", "<Field F-1:2.1 'start'>", "<Field F-1:2.2 'finish'>", '<Entity_List F-1:3>', "<Entity F-2 'SRM.Boat_Type'>", "<Field F-2:1 'name'>"]

    >>> print f ["F-1:2.1"]
    <Field F-1:2.1 'start'>
    >>> print f ["F-1:3"]
    <Entity_List F-1:3>
    >>> print f ["F-1:3::0"]
    <Entity F-1:3::0 'PAP.Person_has_Email'>
    >>> print f ["F-1:3::0-1"]
    <Field F-1:3::0-1 'desc'>
    >>> fel = f ["F-1:3"]
    >>> print fel.proto
    <Entity F-1:3::0 'PAP.Person_has_Email'>
    >>> sorted (fel.id_map)
    ['1', '2', '2:1']
    >>> [str (fel.id_map [id]) for id in sorted (fel.id_map)]
    ["<Field F-1:3::0-1 'desc'>", "<Entity F-1:3::0-2 'PAP.Email'>", "<Field F-1:3::0-2:1 'address'>"]

    >>> g = f.copy ()
    >>> gel = g ["F-1:3"]
    >>> sorted (gel.id_map)
    ['1', '2', '2:1']
    >>> print gel.add_child ()
    <Entity F-1:3::1 'PAP.Person_has_Email'>
    >>> print gel.add_child ()
    <Entity F-1:3::2 'PAP.Person_has_Email'>
    >>> sorted (gel.id_map)
    ['1', '2', '2:1']
    >>> pprint.pprint (g.as_json_cargo)
    {'$id': 'F',
     'children': [{'$id': 'F-1',
                   'children': [{'$id': 'F-1:1',
                                 'children': [{'$id': 'F-1:1:1',
                                               'name': 'last_name',
                                               'type': 'Field'},
                                              {'$id': 'F-1:1:2',
                                               'name': 'first_name',
                                               'type': 'Field'}],
                                 'name': 'primary',
                                 'type': 'Fieldset'},
                                {'$id': 'F-1:2',
                                 'children': [{'$id': 'F-1:2.1',
                                               'name': 'start',
                                               'type': 'Field'},
                                              {'$id': 'F-1:2.2',
                                               'name': 'finish',
                                               'type': 'Field'}],
                                 'name': 'lifetime',
                                 'type': 'Field_Composite'},
                                {'$id': 'F-1:3',
                                 'children': [{'$id': 'F-1:3::1',
                                               'children': [{'$id': 'F-1:3::1:1',
                                                             'name': 'desc',
                                                             'type': 'Field'},
                                                            {'$id': 'F-1:3::1:2',
                                                             'children': [{'$id': 'F-1:3::1:2:1',
                                                                           'name': 'address',
                                                                           'type': 'Field'}],
                                                             'type': 'Entity',
                                                             'type_name': 'PAP.Email'}],
                                               'type': 'Entity',
                                               'type_name': 'PAP.Person_has_Email'},
                                              {'$id': 'F-1:3::2',
                                               'children': [{'$id': 'F-1:3::2:1',
                                                             'name': 'desc',
                                                             'type': 'Field'},
                                                            {'$id': 'F-1:3::2:2',
                                                             'children': [{'$id': 'F-1:3::2:2:1',
                                                                           'name': 'address',
                                                                           'type': 'Field'}],
                                                             'type': 'Entity',
                                                             'type_name': 'PAP.Email'}],
                                               'type': 'Entity',
                                               'type_name': 'PAP.Person_has_Email'}],
                                 'type': 'Entity_List'}],
                   'type': 'Entity',
                   'type_name': 'PAP.Person'},
                  {'$id': 'F-2',
                   'children': [{'$id': 'F-2:1',
                                 'name': 'name',
                                 'type': 'Field'}],
                   'type': 'Entity',
                   'type_name': 'SRM.Boat_Type'}],
     'type': 'Form'}
    >>> print g.as_json
    {"$id": "F", "type": "Form", "children": [{"$id": "F-1", "type_name": "PAP.Person", "type": "Entity", "children": [{"$id": "F-1:1", "type": "Fieldset", "name": "primary", "children": [{"$id": "F-1:1:1", "type": "Field", "name": "last_name"}, {"$id": "F-1:1:2", "type": "Field", "name": "first_name"}]}, {"$id": "F-1:2", "type": "Field_Composite", "name": "lifetime", "children": [{"$id": "F-1:2.1", "type": "Field", "name": "start"}, {"$id": "F-1:2.2", "type": "Field", "name": "finish"}]}, {"$id": "F-1:3", "type": "Entity_List", "children": [{"$id": "F-1:3::1", "type_name": "PAP.Person_has_Email", "type": "Entity", "children": [{"$id": "F-1:3::1:1", "type": "Field", "name": "desc"}, {"$id": "F-1:3::1:2", "type_name": "PAP.Email", "type": "Entity", "children": [{"$id": "F-1:3::1:2:1", "type": "Field", "name": "address"}]}]}, {"$id": "F-1:3::2", "type_name": "PAP.Person_has_Email", "type": "Entity", "children": [{"$id": "F-1:3::2:1", "type": "Field", "name": "desc"}, {"$id": "F-1:3::2:2", "type_name": "PAP.Email", "type": "Entity", "children": [{"$id": "F-1:3::2:2:1", "type": "Field", "name": "address"}]}]}]}]}, {"$id": "F-2", "type_name": "SRM.Boat_Type", "type": "Entity", "children": [{"$id": "F-2:1", "type": "Field", "name": "name"}]}]}
    >>> print g ["F-1:3::0-1"]
    <Field F-1:3::0-1 'desc'>
    >>> print g ["F-1:3::1-1"]
    <Field F-1:3::0-1 'desc'>
    >>> print g ["F-1:3::2-1"]
    <Field F-1:3::0-1 'desc'>
    >>> print g ["F-1:3::42-1"]
    <Field F-1:3::0-1 'desc'>
    >>> tuple (str (c) for c in gel.children)
    ("<Entity F-1:3::1 'PAP.Person_has_Email'>", "<Entity F-1:3::2 'PAP.Person_has_Email'>")

"""

if __name__ != "__main__" :
    GTW.AFS._Export ("*")
### __END__ GTW.AFS.Element

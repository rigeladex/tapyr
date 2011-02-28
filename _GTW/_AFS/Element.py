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
#    22-Feb-2011 (CT) `Form.__init__` changed to `copy` children with `.id`
#    23-Feb-2011 (CT) `Form.__call__` and `Fieldset.__call__` added
#    23-Feb-2011 (CT) `Field.__init__` changed to `pop_to_self` of
#                     `description` and `explanation` from `kw`
#    23-Feb-2011 (CT) `Entity_List.clone` added
#    24-Feb-2011 (CT) `Field_Entity` added
#    25-Feb-2011 (CT) `Form.__call__` changed to return `GTW.AFS.Instance.Form`
#                     instead of data `dict`
#    25-Feb-2011 (CT) `_call_iter` factored from `__call__`, `child_ids` added
#    25-Feb-2011 (CT) Handling of `id_map` changed (only `Form` instance has
#                     one, use full `id` as key, put in Entity_List.children)
#    27-Feb-2011 (CT) `id` setting changed (0-based, `Entity_List.proto` gets
#                     `p` instead of `0`)
#    27-Feb-2011 (CT) `__call__` revamped (each __call__ now creates a
#                     GTW.AFS.Instance object), `_data` added
#    27-Feb-2011 (CT) `as_json` moved to `GTW.AFS.Instance`, `as_json_cargo`
#                     changed to not include `children`
#    27-Feb-2011 (CT) `Entity_List.new_child` factored
#    28-Feb-2011 (CT) `needs_value` added
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS.Instance

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.predicate           import split_hst, rsplit_hst

import json

class _Element_ (TFL.Meta.Object) :
    """Base class for AFS element classes."""

    children    = ()
    id_sep      = "."
    list_sep    = "::"
    needs_value = False
    root_sep    = "-"
    _id         = None

    def __init__ (self, ** kw) :
        self.pop_to_self  (kw, "id", "id_sep")
        children = kw.pop ("children", None)
        if children is not None :
            self.children = list (children)
        self.kw = kw
    # end def __init__

    def __call__ (self, * args, ** kw) :
        result = GTW.AFS.Instance \
            ( self
            , children = list (self._call_iter (* args, ** kw))
            , ** self._data (* args, ** kw)
            )
        ### XXX compute and set csrf tokens for result
        return result
    # end def __call__

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
    def as_json_cargo (self) :
        result         = dict (self.kw, type = self.__class__.__name__)
        result ["$id"] = self.id
        return result
    # end def as_json_cargo

    def copy (self, ** kw) :
        ckw      = dict (self.kw, ** kw)
        children = [c.copy () for c in self.children] if self.children else None
        return self.__class__ (children = children, ** ckw)
    # end def copy

    def _call_iter (self, * args, ** kw) :
        for c in self.children :
            yield c (* args, ** kw)
    # end def _call_iter

    def _data (self, * args, ** kw) :
        return {"value" : {}}
    # end def _data

    def _formatted (self, level = 0) :
        result = ["%s%s" % (" " * level, self)]
        level += 1
        result.extend (c._formatted (level) for c in self.children)
        return "\n".join (result)
    # end def _formatted

    def _id_children (self, id, children, id_map) :
        sep = self.id_sep
        for i, c in enumerate (children) :
            c_id = c._set_id (self, i)
            if c_id in id_map :
                raise KeyError \
                    ("Duplicate id %s: %s vs. %s" % (c_id, c, id_map [c_id]))
            id_map [c_id] = c
            c._id_children (c_id, c.children, id_map)
    # end def _id_children

    def _set_id (self, parent, i) :
        self.id = result = parent.id_sep.join ((parent.id, str (i)))
        return result
    # end def _set_id

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
        infos = ["%s" % self.id]
        for k in "name", "type_name" :
            n = getattr (self, k, None)
            if n is not None :
                v = "%r" % n
                if infos [-1] != v :
                    infos.append (v)
        return "<%s %s>" % (self.__class__.__name__, " ".join (infos))
    # end def __str__

# end class _Element_

class _Element_List_ (_Element_) :
    """Base class for AFS classes modelling a list of elements."""

    def __getitem__ (self, key) :
        try :
            return self.id_map [key]
        except KeyError :
            h, _, t = split_hst (key, self.list_sep)
            i, _, u = split_hst (t,   self.root_sep)
            p = self.list_sep.join \
                ((h, self.root_sep.join (("p", u)) if u else "p"))
            try :
                return self.id_map [p]
            except KeyError :
                raise KeyError (key)
    # end def __getitem__

# end class _Element_List_

class Entity (_Element_) :
    """Model a sub-form for a single entity."""

    id_sep      = ":"
    needs_value = True

    def __init__ (self, type_name, ** kw) :
        self.__super.__init__ (type_name = type_name, ** kw)
    # end def __init__

# end class Entity

class Entity_Link (Entity) :
    """Model a sub-form for a link to entity in containing sub-form."""

# end class Entity_Link

class Entity_List (_Element_List_) :
    """Model a sub-form for a list of entities."""

    id_sep  = _Element_List_.list_sep

    def __init__ (self, proto, ** kw) :
        self.proto   = proto
        proto.id_sep = self.root_sep
        self.__super.__init__ (** kw)
    # end def __init__

    def add_child (self) :
        if self.children is self.__class__.children :
            self.children = []
        cs     = self.children
        result = self.new_child (len (cs), self.id_map)
        cs.append (result)
        return result
    # end def add_child

    def copy (self, ** kw) :
        return self.__super.copy (proto = self.proto.copy (), ** kw)
    # end def copy

    def new_child (self, i, id_map) :
        result = self.proto.copy ()
        result.id_sep = self.root_sep
        if self.id :
            self._id_child_or_proto (result, i, id_map)
        return result
    # end def new_child

    def _formatted (self, level = 0) :
        result = [self.__super._formatted (level)]
        if not self.children :
            result.append (self.proto._formatted (level + 1))
        return "\n".join (result)
    # end def _formatted

    def _id_children (self, id, children, id_map) :
        self.id_map = id_map
        self._id_child_or_proto   (self.proto, "p",      id_map)
        self.__super._id_children (id,         children, id_map)
    # end def _id_children

    def _id_child_or_proto (self, cop, i, id_map) :
        cop._set_id      (self, i)
        cop._id_children (cop.id, cop.children, id_map)
        id_map [cop.id] = cop
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

    needs_value = True

    def __init__ (self, name, ** kw) :
        self.pop_to_self      (kw, "description", "explanation")
        self.__super.__init__ (name = name, ** kw)
    # end def __init__

# end class Field

class Field_Composite (Field) :
    """Model a composite field of a AJAX-enhanced form."""

# end class Field_Composite

class Field_Entity (Entity, Field) :
    """Model an entity-holding field of a AJAX-enhanced form."""

# end class Field_Entity

class Fieldset (_Element_) :
    """Model a set of fields of an AJAX-enhanced form."""

    id_sep = ":"

# end class Fieldset

class Form (_Element_List_) :
    """Model a AJAX-enhanced form."""

    id_sep      = _Element_List_.root_sep
    needs_value = True
    Table       = {}

    def __init__ (self, id, children, ** kw) :
        self.id_map = {}
        Table = self.Table
        if kw.pop ("REGISTER", True) :
            if id in Table :
                raise KeyError ("Duplicate form id %s" % id)
            else :
                Table [id] = self
        children = tuple \
            ((c.copy () if c.id is not None else c) for c in children)
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

    def _call_body (self, * args, ** kw) :
        data = self.__super.__call__ (* args, ** kw)
        return GTW.AFS.Instance.Form (self, data)
    # end def _call_body

    def _call_iter (self, * args, ** kw) :
        assert len (args) == len (self.children), repr (self)
        for a, c in zip (args, self.children) :
            yield c (a, ** kw)
    # end def _call_iter

# end class Form

__doc__ = """
Usage example::

    >>> from _TFL.Formatter import Formatter
    >>> formatted = Formatter (width = 160)
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
    >>> print repr (f)
    <Form F>
     <Entity F-0 'PAP.Person'>
      <Fieldset F-0:0 'primary'>
       <Field F-0:0:0 'last_name'>
       <Field F-0:0:1 'first_name'>
      <Field_Composite F-0:1 'lifetime'>
       <Field F-0:1.0 'start'>
       <Field F-0:1.1 'finish'>
      <Entity_List F-0:2 <Entity F-0:2::p 'PAP.Person_has_Email'>>
       <Entity F-0:2::p 'PAP.Person_has_Email'>
        <Field F-0:2::p-0 'desc'>
        <Entity F-0:2::p-1 'PAP.Email'>
         <Field F-0:2::p-1:0 'address'>
     <Entity F-1 'SRM.Boat_Type'>
      <Field F-1:0 'name'>
    >>> sorted (f.id_map)
    ['F-0', 'F-0:0', 'F-0:0:0', 'F-0:0:1', 'F-0:1', 'F-0:1.0', 'F-0:1.1', 'F-0:2', 'F-0:2::p', 'F-0:2::p-0', 'F-0:2::p-1', 'F-0:2::p-1:0', 'F-1', 'F-1:0']
    >>> [str (f.id_map [id]) for id in sorted (f.id_map)]
    ["<Entity F-0 'PAP.Person'>", "<Fieldset F-0:0 'primary'>", "<Field F-0:0:0 'last_name'>", "<Field F-0:0:1 'first_name'>", "<Field_Composite F-0:1 'lifetime'>", "<Field F-0:1.0 'start'>", "<Field F-0:1.1 'finish'>", "<Entity_List F-0:2 <Entity F-0:2::p 'PAP.Person_has_Email'>>", "<Entity F-0:2::p 'PAP.Person_has_Email'>", "<Field F-0:2::p-0 'desc'>", "<Entity F-0:2::p-1 'PAP.Email'>", "<Field F-0:2::p-1:0 'address'>", "<Entity F-1 'SRM.Boat_Type'>", "<Field F-1:0 'name'>"]

    >>> print f ["F-0:1.0"]
    <Field F-0:1.0 'start'>
    >>> print f ["F-0:2"]
    <Entity_List F-0:2 <Entity F-0:2::p 'PAP.Person_has_Email'>>
    >>> print f ["F-0:2::p"]
    <Entity F-0:2::p 'PAP.Person_has_Email'>
    >>> print f ["F-0:2::p-0"]
    <Field F-0:2::p-0 'desc'>
    >>> print f ["F-0:2::p-0"]
    <Field F-0:2::p-0 'desc'>
    >>> print f ["F-0:2::1-0"]
    <Field F-0:2::p-0 'desc'>
    >>> fel = f ["F-0:2"]
    >>> print fel.proto
    <Entity F-0:2::p 'PAP.Person_has_Email'>

    >>> g = f.copy ()
    >>> gel = g ["F-0:2"]
    >>> print gel.add_child ()
    <Entity F-0:2::0 'PAP.Person_has_Email'>
    >>> print gel.add_child ()
    <Entity F-0:2::1 'PAP.Person_has_Email'>
    >>> print repr (g)
    <Form F>
     <Entity F-0 'PAP.Person'>
      <Fieldset F-0:0 'primary'>
       <Field F-0:0:0 'last_name'>
       <Field F-0:0:1 'first_name'>
      <Field_Composite F-0:1 'lifetime'>
       <Field F-0:1.0 'start'>
       <Field F-0:1.1 'finish'>
      <Entity_List F-0:2 <Entity F-0:2::p 'PAP.Person_has_Email'>>
       <Entity F-0:2::0 'PAP.Person_has_Email'>
        <Field F-0:2::0-0 'desc'>
        <Entity F-0:2::0-1 'PAP.Email'>
         <Field F-0:2::0-1:0 'address'>
       <Entity F-0:2::1 'PAP.Person_has_Email'>
        <Field F-0:2::1-0 'desc'>
        <Entity F-0:2::1-1 'PAP.Email'>
         <Field F-0:2::1-1:0 'address'>
     <Entity F-1 'SRM.Boat_Type'>
      <Field F-1:0 'name'>
    >>> sorted (g.id_map)
    ['F-0', 'F-0:0', 'F-0:0:0', 'F-0:0:1', 'F-0:1', 'F-0:1.0', 'F-0:1.1', 'F-0:2', 'F-0:2::0', 'F-0:2::0-0', 'F-0:2::0-1', 'F-0:2::0-1:0', 'F-0:2::1', 'F-0:2::1-0', 'F-0:2::1-1', 'F-0:2::1-1:0', 'F-0:2::p', 'F-0:2::p-0', 'F-0:2::p-1', 'F-0:2::p-1:0', 'F-1', 'F-1:0']
    >>> print g ["F-0:2::p-0"]
    <Field F-0:2::p-0 'desc'>
    >>> print g ["F-0:2::0-0"]
    <Field F-0:2::0-0 'desc'>
    >>> print g ["F-0:2::1-0"]
    <Field F-0:2::1-0 'desc'>
    >>> print g ["F-0:2::42-0"]
    <Field F-0:2::p-0 'desc'>
    >>> tuple (str (c) for c in gel.children)
    ("<Entity F-0:2::0 'PAP.Person_has_Email'>", "<Entity F-0:2::1 'PAP.Person_has_Email'>")

"""

if __name__ != "__main__" :
    GTW.AFS._Export_Module ()
### __END__ GTW.AFS.Element

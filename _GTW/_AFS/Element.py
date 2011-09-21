# -*- coding: iso-8859-15 -*-
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
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
#     1-Mar-2011 (CT) `M_Form` added
#     1-Mar-2011 (CT) s/_data/_value/
#     2-Mar-2011 (CT) `prefilled`, `_value_sig`, and `sid` added
#     6-Mar-2011 (CT) `Entity.form_hash` factored
#     6-Mar-2011 (CT) `_value_sig` changed to use `instance.id` instead of
#                     `self.id` (needed for dynamic children of Entity_List)
#     8-Mar-2011 (CT) `_value` simplified (`needs_value` moved to
#                     `_Element_.__call__`)
#     9-Mar-2011 (CT) `_update_sid` factored
#    15-Mar-2011 (CT) Guard against names starting with `__` added to
#                     `__getattr__`
#    15-Mar-2011 (CT) `Form.Load` and `Form.Store` added
#    17-Mar-2011 (CT) `_instance_kw` added
#    17-Mar-2011 (CT) `Field.input_widget` added
#    18-Mar-2011 (CT) `_Element_.renderer` and `.widget` added
#    20-Mar-2011 (CT) `css_class` added
#    21-Mar-2011 (CT) Call of `_value` moved to `_instance_kw`
#    22-Mar-2011 (CT) `het_c` and `het_h` added
#    23-Mar-2011 (CT) `_pop_to_self` factored and used in `copy`, too
#    29-Mar-2011 (CT) `changeable` and `readonly` added
#    29-Mar-2011 (CT) `Field._value_sig` changed to include `prefilled`
#    30-Mar-2011 (CT) `display` and `instantiated` added
#    30-Mar-2011 (CT) `Form.__getitem__` changed to allow nested Entity_Lists
#    31-Mar-2011 (CT) `Entity_List` changed to redefine `.instantiated`
#     1-Apr-2011 (CT) `_Element_.instantiated` changed to honor `child_id`
#     4-Apr-2011 (CT) s/child_id/new_id_suffix/
#    13-Apr-2011 (CT) `_pop_in_call` added
#    19-May-2011 (CT) `Form.__getitem__` changed to use `_list_element_pat`
#                     instead of `split_hst` to massage `key` (allow recursion)
#    31-May-2011 (MG) `form_hash`: `str` calls added to convert unicode
#                     `_sid` and `_session_secret` values to strings
#     1-Jun-2011 (CT) `form_hash` changed to apply `str` to unicode-values only
#    10-Jun-2011 (MG) `Group` added
#     1-Aug-2011 (CT) `Field_Composite.het_c` and `Fieldset.het_c` changed
#                     from `section` to `div`
#    16-Sep-2011 (CT) `anchor_id` (and `_anchor_children`) added
#    20-Sep-2011 (CT) `completer` added to `as_json_cargo` and
#                     `_anchor_children`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._AFS.Instance
import _GTW._Form.Widget_Spec

import _TFL._Meta.Object
import _TFL._Meta.M_Auto_Combine_Lists
from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.predicate           import split_hst
from   _TFL.pyk                 import pickle
from   _TFL.Regexp              import Regexp, re

import json

class _M_Element_ (TFL.Meta.M_Auto_Combine_Lists, TFL.Meta.Object.__class__) :
    """Meta class for `_Element_`"""

# end class _M_Element_

class M_Form (_M_Element_) :
    """Meta class for `Form`."""

    def __getitem__ (cls, key) :
        id, _, t = split_hst (key, cls.id_sep)
        return cls.Table [id]
    # end def __getitem__

# end class M_Form

class _Element_ (TFL.Meta.Object) :
    """Base class for AFS element classes."""

    __metaclass__ = _M_Element_

    children      = ()
    completer     = None
    het_c         = "div" ### HTML element type to be used for the container
    het_h         = "h2"  ### HTML element type to be used for the heading
    id_sep        = "."
    id_suffix_pat = Regexp (r"\d+$")
    init          = ""
    list_sep      = "::"
    needs_value   = False
    prefilled     = False
    rank          = 0
    readonly      = False
    renderer      = None
    root_sep      = "-"
    widget        = None
    _css_class    = None
    _id           = None
    _pop_in_call  = ("allow_new", "collapsed")
    _pop_to_self  = \
        ( "completer", "css_class", "description", "explanation"
        , "id", "id_sep", "needs_value", "prefilled", "readonly"
        , "renderer", "required", "ui_name", "widget"
        )
    _lists_to_combine   = ("_pop_to_self", "_pop_in_call")

    def __init__ (self, ** kw) :
        self.pop_to_self  (kw, * self._pop_to_self)
        children = kw.pop ("children", None)
        if children is not None :
            self.children = list (children)
        self.kw = kw
    # end def __init__

    def __call__ (self, * args, ** kw) :
        ikw = self._instance_kw (* args, ** kw)
        for k in self._pop_in_call :
            kw.pop (k, None)
        result = GTW.AFS.Instance \
            ( self
            , children = list (self._call_iter (* args, ** kw))
            , ** ikw
            )
        return result
    # end def __call__

    @property
    def anchor_id (self) :
        try :
            d = self.kw ["an$"]
        except KeyError :
            pass
        else :
            return self.id [:- d]
    # end def anchor_id

    @anchor_id.setter
    def anchor_id (self, anchor_id) :
        if self.id.startswith (anchor_id) :
            d = len (self.id) - len (anchor_id)
            self.kw ["an$"] = d
    # end def anchor_id

    @property
    def as_json_cargo (self) :
        result = dict (self.kw, type = self.__class__.__name__)
        if hasattr (self.completer, "as_json_cargo") :
            result ["completer"] = self.completer.as_json_cargo
        result ["$id"] = self.id
        return result
    # end def as_json_cargo

    @property
    def css_class (self) :
        return " ".join (c for c in self._css_classes () if c)
    # end def css_class

    @css_class.setter
    def css_class (self, value) :
        self._css_class = value
    # end def css_class

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

    def copy (self, ** kw) :
        ckw      = dict \
            ( (k, getattr (self, k))
            for k in self._pop_to_self if k in self.__dict__
            )
        ckw.update (self.kw, ** kw)
        children = [c.copy () for c in self.children] if self.children else None
        return self.__class__ (children = children, ** ckw)
    # end def copy

    def display (self, instance) :
        return instance._display
    # end def display

    def instantiated (self, id, * args, ** kw) :
        new_id_suffix = kw.pop ("new_id_suffix", None)
        this          = self
        if new_id_suffix :
            id = self.id_suffix_pat.sub (new_id_suffix, id)
        if self.id != id :
            this = self.copy  (id = id)
            this._id_children (id, this.children, {})
        return this (* args, ** kw)
    # end def instantiated

    def transitive_iter (self) :
        yield self
        for c in self.children :
            for x in c.transitive_iter () :
                yield x
    # end def transitive_iter

    def _anchor_children (self, anchor = None) :
        for c in self.children :
            c._anchor_children (anchor)
    # end def _anchor_children

    def _call_iter (self, * args, ** kw) :
        for c in self.children :
            yield c (* args, ** kw)
    # end def _call_iter

    def _css_classes (self) :
        return (self._css_class, self.__class__.__name__)
    # end def _css_classes

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

    def _instance_kw (self, * args, ** kw) :
        result = dict (kw)
        if self.needs_value :
            result ["value"] = self._value (* args, ** kw)
        return result
    # end def _instance_kw

    @property
    def _name (self) :
        for k in "name", "type_name" :
            try :
                return self.kw [k]
            except KeyError :
                pass
    # end def _name

    def _set_id (self, parent, i) :
        self.id = result = parent.id_sep.join ((parent.id, str (i)))
        return result
    # end def _set_id

    def _value (self, * args, ** kw) :
        p = self.prefilled or kw.get ("prefilled")
        return {"prefilled" : True} if p else {}
    # end def _value

    def _value_sig (self, instance) :
        pass
    # end def _value_sig

    def __getattr__ (self, name) :
        if not name.startswith ("__") :
            try :
                return self.kw [name]
            except KeyError :
                pass
        raise AttributeError (name)
    # end def __getattr__

    def __repr__ (self) :
        return self._formatted ()
    # end def __repr__

    def __str__ (self) :
        infos = ["%s" % self.id]
        for k in "name", "type_name" :
            n = self.kw.get (k)
            if n is not None :
                v = "%r" % n
                if infos [-1] != v :
                    infos.append (v)
        return "<%s %s>" % (self.__class__.__name__, " ".join (infos))
    # end def __str__

# end class _Element_

class _Anchor_MI_ (_Element_) :

    def _anchor_children (self, anchor = None) :
        self.__super._anchor_children (anchor = self)
    # end def _anchor_children

# end class _Anchor_MI_

class _Field_MI_ (_Element_) :

    def _anchor_children (self, anchor = None) :
        if anchor is not None :
            self.anchor_id = anchor.id
            ac = anchor.completer
            sc = self.completer
            if hasattr (sc, "entity_p") and hasattr (ac, "derived") :
                self.completer = ac.derived (sc)
        self.__super._anchor_children (anchor)
    # end def _anchor_children

# end class _Field_MI_

class _Element_List_ (_Element_) :
    """Base class for AFS classes modelling a list of elements."""

    het_c       = "section" ### HTML element type to be used for the container
    het_h       = "h1"      ### HTML element type to be used for the heading

# end class _Element_List_

class Entity (_Anchor_MI_, _Element_) :
    """Model a sub-form for a single entity."""

    het_c       = "section" ### HTML element type to be used for the container
    het_h       = "h1"      ### HTML element type to be used for the heading
    id_sep      = ":"
    needs_value = True
    renderer    = "afs_div_seq"

    def __init__ (self, type_name, ** kw) :
        self.__super.__init__ (type_name = type_name, ** kw)
    # end def __init__

    def __call__ (self, * args, ** kw) :
        result = self.__super.__call__ (* args, ** kw)
        self._update_sid (result, ** kw)
        return result
    # end def __call__

    def apply (self, * args, ** kw) :
        raise NotImplementedError \
            ("%s must implement method apply" % (self.__class__, ))
    # end def apply

    def form_hash (self, value, ** kw) :
        _sid = kw.get ("_sid", 0)
        _session_secret = kw.get ("_session_secret")
        if isinstance (_sid, unicode) :
            _sid = str (_sid)
        if isinstance (_session_secret, unicode) :
            _session_secret = str (_session_secret)
        sig = value.sig = value.form_sig \
            (self._value_sig_t (value), _sid, _session_secret)
        result = value.form_hash (sig)
        return result
    # end def form_hash

    def _update_sid (self, result, ** kw) :
        result.value.update (sid = self.form_hash (result, ** kw))
    # end def _update_sid

    def _value_sig_t (self, instance) :
        return (str (instance.id), self.type_name, instance.init)
    # end def _value_sig_t

# end class Entity

class Entity_Link (_Field_MI_, Entity) :
    """Model a sub-form for a link to entity in containing sub-form."""

    rank = 100

    def display (self, instance) :
        return "; ".join (c.display for c in instance.children if c.display)
    # end def display

# end class Entity_Link

class Entity_List (_Element_List_) :
    """Model a sub-form for a list of entities."""

    id_sep   = _Element_List_.list_sep
    renderer = "afs_div_seq"

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

    def instantiated (self, id, * args, ** kw) :
        new_id_suffix = kw.pop ("new_id_suffix")
        child         = self.new_child (new_id_suffix, {})
        return child (* args, ** kw)
    # end def instantiated

    def new_child (self, i, id_map) :
        result = self.proto.copy ()
        result.id_sep = self.root_sep
        if self.id :
            self._id_child_or_proto (result, i, id_map)
        result._anchor_children (self.anchor_id)
        return result
    # end def new_child

    def transitive_iter (self) :
        for x in self.__super.transitive_iter () :
            yield x
        if not self.children :
            for x in self.proto.transitive_iter () :
                yield x
    # end def transitive_iter

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

class _Field_ (_Element_) :
    """Base class for AFS field classes."""

    needs_value   = True

    input_widget  = GTW.Form.Widget_Spec ("html/AFS/input.jnj, string")
    _pop_to_self  = ("changeable", "choices", "input_widget")

    def __init__ (self, name, ** kw) :
        self.__super.__init__ (name = name, ** kw)
    # end def __init__

# end class Field

class Field (_Field_MI_, _Field_) :
    """Model a field of an AJAX-enhanced form."""

    def _css_classes (self) :
        return (self._css_class, )
    # end def _css_classes

    def _value_sig (self, instance) :
        result = (str (instance.id), self.name, instance.init)
        if getattr (instance, "prefilled", False) :
            result = (result, True)
        return result
    # end def _value_sig

# end class Field

class Field_Composite (_Field_MI_, _Anchor_MI_, _Field_) :
    """Model a composite field of a AJAX-enhanced form."""

    het_c       = "div"     ### HTML element type to be used for the container
    het_h       = "h2"      ### HTML element type to be used for the heading
    renderer    = "afs_div_seq"

    def _value_sig (self, instance) :
        return (str (instance.id), self.name, instance.form_sig ())
    # end def _value_sig

# end class Field_Composite

class Field_Entity (_Field_MI_, Entity, _Field_) :
    """Model an entity-holding field of a AJAX-enhanced form."""

    het_h       = "h2"      ### HTML element type to be used for the heading

    def _value_sig (self, instance) :
        return (str (instance.id), self.name)
    # end def _value_sig

# end class Field_Entity

class Fieldset (_Element_) :
    """Model a set of fields of an AJAX-enhanced form."""

    het_c       = "div"     ### HTML element type to be used for the container
    het_h       = "h2"      ### HTML element type to be used for the heading
    id_sep      = ":"
    renderer    = "afs_div_seq"

    def display (self, instance) :
        return "; ".join (c.display for c in instance.children if c.display)
    # end def display

    def _css_classes (self) :
        return self.__super._css_classes () + (self.name.capitalize (), )
    # end def _css_classes

    def _value_sig (self, instance) :
        return instance.form_sig ()
    # end def _value_sig

# end class Fieldset

class Form (_Element_List_) :
    """Model a AJAX-enhanced form."""

    __metaclass__ = M_Form

    het_c         = "section" ### HTML element type to be used for the container
    het_h         = "h1"      ### HTML element type to be used for the heading
    id_sep        = _Element_List_.root_sep
    needs_value   = True
    renderer      = "afs_div_seq"
    Table         = {}

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
        self._anchor_children ()
    # end def __init__

    @Once_Property
    def dynamic_children_p (self) :
        s = Entity_List.id_sep
        return any ((s in id) for id in self.id_map)
    # end def dynamic_children_p

    @Once_Property
    def _list_element_pat (self) :
        return Regexp \
            ( "".join
                ( ( re.escape (self.list_sep)
                  , r"\d+"
                  , r"(?:"
                  ,   re.escape (self.root_sep)
                  ,   r"(?P<tail>.*)"
                  , r")?"
                  )
                )
            )
    # end def _list_element_pat

    def copy (self, ** kw) :
        if "id" not in kw :
            kw = dict (kw, id = self.id, REGISTER = False)
        return self.__super.copy (** kw)
    # end def copy

    def _call_iter (self, * args, ** kw) :
        assert len (args) == len (self.children), repr (self)
        for a, c in zip (args, self.children) :
            yield c (a, ** kw)
    # end def _call_iter

    def _css_classes (self) :
        return self.__super._css_classes () + ("AFS", )
    # end def _css_classes

    def _value (self, * args, ** kw) :
        result = self.__super._value (* args, ** kw)
        result.update (sid = kw.get ("_sid", 0))
        return result
    # end def _value

    def __getitem__ (self, key) :
        if key == self.id :
            return self
        try :
            return self.id_map [key]
        except KeyError :
            l_sep = self.list_sep
            l_pat = self._list_element_pat
            if l_pat.search (key) :
                r_sep = self.root_sep
                head  = key [:l_pat.start ()]
                tail  = "p"
                if l_pat.tail :
                    tail = r_sep.join ((tail, l_pat.tail))
                p_key = l_sep.join ((head, tail))
                return self [p_key]
            else :
                raise
    # end def __getitem__

    @classmethod
    def Load (cls, pickle_path) :
        """Load `Table` from `pickle_path`."""
        with open (pickle_path, "rb") as file :
            try :
                table = pickle.load (file)
            except pickle.PickleError as exc :
                raise EnvironmentError (str (exc))
        table.update (cls.Table)
        ### We want to set `Table` for `GTW.AFS.Element.Form`, not for a
        ### possible descedent class
        GTW.AFS.Element.Form.Table = table
    # end def Load

    @classmethod
    def Store (cls, pickle_path) :
        """Store `Table` as pickle in `pickle_path`."""
        with open (pickle_path, "wb") as file :
            try :
                pickle.dump (cls.Table, file, pickle.HIGHEST_PROTOCOL)
            except pickle.PickleError as exc :
                raise EnvironmentError (str (exc))
    # end def Store

# end class Form

class Group (Fieldset) :
    """Group elements of a form"""

# end class Group

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
     <Entity F-0 u'PAP.Person'>
      <Fieldset F-0:0 u'primary'>
       <Field F-0:0:0 u'last_name'>
       <Field F-0:0:1 u'first_name'>
      <Field_Composite F-0:1 u'lifetime'>
       <Field F-0:1.0 u'start'>
       <Field F-0:1.1 u'finish'>
      <Entity_List F-0:2 <Entity F-0:2::p u'PAP.Person_has_Email'>>
       <Entity F-0:2::p u'PAP.Person_has_Email'>
        <Field F-0:2::p-0 u'desc'>
        <Entity F-0:2::p-1 u'PAP.Email'>
         <Field F-0:2::p-1:0 u'address'>
     <Entity F-1 u'SRM.Boat_Type'>
      <Field F-1:0 u'name'>
    >>> sorted (f.id_map)
    [u'F-0', u'F-0:0', u'F-0:0:0', u'F-0:0:1', u'F-0:1', u'F-0:1.0', u'F-0:1.1', u'F-0:2', u'F-0:2::p', u'F-0:2::p-0', u'F-0:2::p-1', u'F-0:2::p-1:0', u'F-1', u'F-1:0']
    >>> [str (f.id_map [id]) for id in sorted (f.id_map)]
    ["<Entity F-0 u'PAP.Person'>", "<Fieldset F-0:0 u'primary'>", "<Field F-0:0:0 u'last_name'>", "<Field F-0:0:1 u'first_name'>", "<Field_Composite F-0:1 u'lifetime'>", "<Field F-0:1.0 u'start'>", "<Field F-0:1.1 u'finish'>", "<Entity_List F-0:2 <Entity F-0:2::p u'PAP.Person_has_Email'>>", "<Entity F-0:2::p u'PAP.Person_has_Email'>", "<Field F-0:2::p-0 u'desc'>", "<Entity F-0:2::p-1 u'PAP.Email'>", "<Field F-0:2::p-1:0 u'address'>", "<Entity F-1 u'SRM.Boat_Type'>", "<Field F-1:0 u'name'>"]

    >>> print f ["F-0:1.0"]
    <Field F-0:1.0 u'start'>
    >>> print f ["F-0:2"]
    <Entity_List F-0:2 <Entity F-0:2::p u'PAP.Person_has_Email'>>
    >>> print f ["F-0:2::p"]
    <Entity F-0:2::p u'PAP.Person_has_Email'>
    >>> print f ["F-0:2::p-0"]
    <Field F-0:2::p-0 u'desc'>
    >>> print f ["F-0:2::p-0"]
    <Field F-0:2::p-0 u'desc'>
    >>> print f ["F-0:2::1-0"]
    <Field F-0:2::p-0 u'desc'>
    >>> fel = f ["F-0:2"]
    >>> print fel.proto
    <Entity F-0:2::p u'PAP.Person_has_Email'>

    >>> g = f.copy ()
    >>> gel = g ["F-0:2"]
    >>> print gel.add_child ()
    <Entity F-0:2::0 u'PAP.Person_has_Email'>
    >>> print gel.add_child ()
    <Entity F-0:2::1 u'PAP.Person_has_Email'>
    >>> print repr (g)
    <Form F>
     <Entity F-0 u'PAP.Person'>
      <Fieldset F-0:0 u'primary'>
       <Field F-0:0:0 u'last_name'>
       <Field F-0:0:1 u'first_name'>
      <Field_Composite F-0:1 u'lifetime'>
       <Field F-0:1.0 u'start'>
       <Field F-0:1.1 u'finish'>
      <Entity_List F-0:2 <Entity F-0:2::p u'PAP.Person_has_Email'>>
       <Entity F-0:2::0 u'PAP.Person_has_Email'>
        <Field F-0:2::0-0 u'desc'>
        <Entity F-0:2::0-1 u'PAP.Email'>
         <Field F-0:2::0-1:0 u'address'>
       <Entity F-0:2::1 u'PAP.Person_has_Email'>
        <Field F-0:2::1-0 u'desc'>
        <Entity F-0:2::1-1 u'PAP.Email'>
         <Field F-0:2::1-1:0 u'address'>
     <Entity F-1 u'SRM.Boat_Type'>
      <Field F-1:0 u'name'>
    >>> sorted (g.id_map)
    [u'F-0', u'F-0:0', u'F-0:0:0', u'F-0:0:1', u'F-0:1', u'F-0:1.0', u'F-0:1.1', u'F-0:2', u'F-0:2::0', u'F-0:2::0-0', u'F-0:2::0-1', u'F-0:2::0-1:0', u'F-0:2::1', u'F-0:2::1-0', u'F-0:2::1-1', u'F-0:2::1-1:0', u'F-0:2::p', u'F-0:2::p-0', u'F-0:2::p-1', u'F-0:2::p-1:0', u'F-1', u'F-1:0']
    >>> print g ["F-0:2::p-0"]
    <Field F-0:2::p-0 u'desc'>
    >>> print g ["F-0:2::0-0"]
    <Field F-0:2::0-0 u'desc'>
    >>> print g ["F-0:2::1-0"]
    <Field F-0:2::1-0 u'desc'>
    >>> print g ["F-0:2::42-0"]
    <Field F-0:2::p-0 u'desc'>
    >>> tuple (str (c) for c in gel.children)
    ("<Entity F-0:2::0 u'PAP.Person_has_Email'>", "<Entity F-0:2::1 u'PAP.Person_has_Email'>")

    >>> print Form ["F"]
    <Form F>
    >>> print Form ["F-0:2::0"]
    <Form F>
    >>> print f ["F"]
    <Form F>

"""

if __name__ != "__main__" :
    GTW.AFS._Export_Module ()
### __END__ GTW.AFS.Element

# -*- coding: utf-8 -*-
# Copyright (C) 2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.MF3.
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
#    GTW.MF3.Element
#
# Purpose
#    Model elements of MOM Forms
#
# Revision Dates
#    24-Apr-2014 (CT) Creation
#     2-May-2014 (CT) Remove `changeable`;
#                     replaced by `attr.kind.change_forbidden`
#     2-May-2014 (CT) Use `readonly`, not `prefilled`, in
#                     `Field_Entity.__call__`
#     2-May-2014 (CT) Honor `skip` in `elements_transitive`,
#                     `field_elements`, `template_elements`
#     3-May-2014 (CT) Change `_Field_.required` to honor `parent.required`
#     7-May-2014 (CT) Add `MAT.A_Int.mf3_input_widget`
#     7-May-2014 (CT) Add and use `GTW.MF3.Completer`
#     8-May-2014 (CT) Factor `_new_element`, `_Auto_Element`
#     8-May-2014 (CT) Add `attr_map`, `__getitem__` to `_Field_Composite_Mixin_`
#     8-May-2014 (CT) Add `completer_elems`
#     9-May-2014 (CT) Factor `check_sigs`
#    16-May-2014 (CT) Redefine `Field_Entity.collapsed`
#     4-Jun-2014 (CT) Split `id` into `bare_id` and `index`
#     4-Jun-2014 (CT) Add and use `_pop_to_self_`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

import _GTW._MF3.Completer

from   _MOM.import_MOM          import Q

import _MOM._Attr.Selector
import _MOM._Attr.Type

from   _TFL._Meta.M_Class       import BaM
from   _TFL.predicate           import filtered_join
from   _TFL.pyk                 import pyk

import _TFL._Meta.Object
import _TFL._Meta.M_Auto_Combine_Lists
import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.Undef

from   itertools                import chain as ichain

import hashlib
import hmac
import json
import logging

MAT                                     = MOM.Attr
MAT.A_Attr_Type.mf3_input_widget        = "mf3_input, string"
MAT.A_Boolean.mf3_input_widget          = "mf3_input, boolean"
MAT.A_Confirmation.mf3_input_widget     = "mf3_input, boolean"
MAT.A_Date.mf3_input_widget             = "mf3_input, date"
MAT.A_Date_Time.mf3_input_widget        = "mf3_input, datetime"
MAT.A_Email.mf3_input_widget            = "mf3_input, email"
MAT.A_Enum.mf3_input_widget             = "mf3_input, named_object"
MAT.A_Int.mf3_input_widget              = "mf3_input, integer"
MAT.A_Numeric_String.mf3_input_widget   = "mf3_input, number"
MAT.A_Text.mf3_input_widget             = "mf3_input, text"
MAT.A_Url.mf3_input_widget              = "mf3_input, url"
MAT._A_Id_Entity_.mf3_input_widget      = "mf3_input, id_entity"
MAT._A_Named_Object_.mf3_input_widget   = "mf3_input, named_object"
MAT._A_Named_Value_.mf3_input_widget    = "mf3_input, named_value"
MAT._A_Number_.mf3_input_widget         = "mf3_input, number"
MAT.A_Attr_Type.mf3_template_macro      = None
MAT.A_Confirmation.mf3_template_macro   = "Field__Confirmation"
MAT.A_Attr_Type.mf3_template_module     = None
MAT.A_Date_Interval.mf3_template_module = "mf3_h_cols"

class _M_Element_ (TFL.Meta.M_Auto_Combine_Lists, TFL.Meta.Object.__class__) :
    """Meta class for `_Element_`"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        ### get real name (necessary, if `_real_name` was used in class def)
        name = cls.__name__
        if not name.startswith ("_") :
            if "template_macro" not in dct :
                cls.template_macro = name
            root = cls.m_root
            if getattr (root, "_Element_Map", None) :
                cls._update_element_map (root)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        result._update_element_map (result.root)
        return result
    # end def __call__

    @property
    def fq_id (cls) :
        return cls.bare_id
    # end def fq_id

    ### `m_root` cannot be a `Once_Property` because inheritance
    @property
    def m_root (cls) :
        parent = cls.parent
        return cls if parent is None else parent.m_root
    # end def m_root

    def __repr__ (cls) :
        if cls.bare_id :
            return "<class %s %s>" % (cls.__name__, cls.bare_id)
        return cls.__m_super.__repr__ ()
    # end def __repr__

# end class _M_Element_

class M_Entity (_M_Element_) :
    """Meta class for `_Entity_`."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.parent is None :
            ### delay construction of `cls._Element_Map` until first call
            ### of `__getitem__`
            ### * `id` of elements is set later by `_add_auto_attributes`
            cls._Element_Map = None
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = cls.__new__ (cls, * args, ** kw)
        result._Element_Map = {}
        result.__init__ (* args, ** kw)
        return result
    # end def __call__

    @property
    def __Element_Map (cls) :
        result = cls._Element_Map
        if result is None :
            result = cls._Element_Map = {}
            if cls.parent is None :
                for e in cls.elements_transitive () :
                    if e is not cls :
                        e._update_element_map (cls)
        return result
    # end def _Element_Map

    def __getitem__ (cls, key) :
        return cls.__Element_Map [key]
    # end def __getitem__

# end class M_Entity

class M_Field (_M_Element_) :
    """Meta class for `Field`."""

# end class M_Field

class _Base_ (TFL.Meta.Object) :
    """Base class of element classes."""

    bare_id             = None
    completer           = None
    elements            = ()
    id                  = TFL.Meta.Alias_Meta_and_Class_Attribute ("fq_id")
    id_sep              = "."
    name                = None
    parent              = None
    q_name              = None
    skip                = False
    template_module     = "mf3"
    ui_rank             = 0
    undef               = TFL.Undef ("value")

    _commit_errors      = ()
    _conflicts          = 0
    _element_ids        = ("id", )
    _index              = None
    _lists_to_combine   = ("_element_ids", "_pop_to_self", "_pop_to_self_")
    _pop_to_self        = ("parent", "template_macro", "template_module")
    _pop_to_self_       = ("index", )
    _required           = False
    _submitted_value    = undef
    _submission_errors  = ()

    def __init__ (self, ** kw) :
        pass
    # end def __init__

    @TFL.Meta.Once_Property
    def commit_errors (self) :
        return list \
            ( ichain
                ( self._commit_errors
                , * (e.commit_errors for e in self.elements)
                )
            )
    # end def submission_errors

    @TFL.Meta.Once_Property
    def conflicts (self) :
        return sum ((e.conflicts for e in self.elements), self._conflicts)
    # end def conflicts

    @TFL.Meta.Once_Property
    def errors (self) :
        return self.submission_errors + self.commit_errors
    # end def errors

    @TFL.Meta.Once_Property
    def fq_id (self) :
        return filtered_join ("", [self.bare_id, self.index])
    # end def fq_id

    @TFL.Meta.Once_Property
    def index (self) :
        return filtered_join \
            ("", [self.parent and self.parent.index, self._index])
    # end def index

    @TFL.Meta.Once_Property
    def root (self) :
        parent = self.parent
        return self if parent is None else parent.root
    # end def root

    @TFL.Meta.Once_Property
    def submission_errors (self) :
        return list \
            ( ichain
                ( self._submission_errors
                , * (e.submission_errors for e in self.elements)
                )
            )
    # end def submission_errors

    @property
    def submitted_value (self) :
        return self._submitted_value
    # end def submitted_value

    @TFL.Meta.Once_Property
    def template_elements (self) :
        return sorted \
            ((e for e in self.elements if not e.skip), key = Q.ui_rank)
    # end def template_elements

    @TFL.Meta.Class_and_Instance_Method
    def elements_transitive (soc) :
        if not soc.skip :
            yield soc
            for e in soc.elements :
                if not e.skip :
                    for et in e.elements_transitive () :
                        yield et
    # end def elements_transitive

    def submitted_value_transitive (self) :
        return dict (self._submitted_value_iter ())
    # end def submitted_value_transitive

    @TFL.Meta.Class_and_Instance_Method
    def template_module_iter (soc) :
        for e in soc.elements_transitive () :
            tm = e.template_module
            if tm :
                yield tm
    # end def template_module_iter

    def _my_cargo (self, cargo) :
        return cargo ["field_values"].get (self.id, {})
    # end def _my_cargo

    @TFL.Meta.Class_and_Instance_Method
    def _update_element_map (soc, root) :
        if root is not soc :
            Map = root._Element_Map
            for k in soc._element_ids :
                key = getattr (soc, k, None)
                if key :
                    Map [key] = soc
    # end def _update_element_map

    def _submitted_value_iter (self) :
        undef = self.undef
        for e in self.elements :
            v = e.submitted_value
            if v is not undef :
                yield e.name, v
    # end def _submitted_value_iter

    def __iter__ (self) :
        for e in self.elements :
            if not e.skip :
                yield e
    # end def __iter__

    def __repr__ (self) :
        return "<%s %s>" % (self.__class__.__name__, self.id)
    # end def __repr__

# end class _Base_

class _Element_ (BaM (_Base_, metaclass = _M_Element_)) :
    """Base class for MF3 element classes."""

    id_essence        = TFL.Meta.Alias_Property ("essence")

    def __init__ (self, essence = None, ** kw) :
        self.__super.__init__ (essence = essence, ** kw)
        self.pop_to_self      (kw, * self._pop_to_self)
        self.pop_to_self      (kw, * self._pop_to_self_, prefix = "_")
        elements      = self.__class__.elements
        self.essence  = essence
        self.elements = list (self._new_element (e, ** kw) for e in elements)
    # end def __init__

    @TFL.Meta.Once_Property
    def field_elements (self) :
        def _gen (self) :
            for e in self.elements :
                if isinstance (e, Field_Composite) and not e.skip :
                    for f in e.field_elements :
                        yield f
                elif isinstance (e, _Field_) :
                    yield e
        return tuple (e for e in _gen (self) if not e.skip)
    # end def field_elements

    @classmethod
    def _add_auto_attributes (cls, E_Type, ** kw) :
        kw.pop ("parent", None)
        cls.elements = tuple \
            (   cls._Auto_Element (ak, E_Type, ** kw)
            for ak in cls.attr_selector (E_Type)
            )
    # end def _add_auto_attributes

    @classmethod
    def _Auto_Element (cls, ak, E_Type, ** kw) :
        return ak.MF3_Element.Auto (ak, E_Type, parent = cls, ** kw)
    # end def _Auto_Element

    def _new_element (self, e, ** kw) :
        return e (self.essence, parent = self, ** kw)
    # end def _new_element

    @TFL.Meta.Class_and_Instance_Method
    def _new_id (soc, essence) :
        parent = soc.parent
        return parent.id_sep.join ((parent.bare_id, soc._own_id (essence)))
    # end def _new_id

# end class _Element_

class _Entity_Mixin_ (_Base_) :
    """Mixin for Entity elements"""

    attr_selector       = MOM.Attr.Selector.List \
        (MOM.Attr.Selector.primary, MOM.Attr.Selector.required)
    render_groups       = ()
    _pop_to_self        = ("attr_selector", "render_groups")

    def __call__ (self, scope, cargo) :
        essence = self.essence
        errors  = self._submission_errors = []
        r_errs  = 0
        handler = self._create_from_submission if essence is None \
            else  self._change_from_submission
        try :
            for e in self.elements :
                e (scope, cargo)
                if e.attr.kind.is_required :
                    r_errs += len (e.submission_errors)
            svs = self.submitted_value
            if svs and not (self.conflicts or r_errs) :
                handler (scope, svs)
        except MOM.Error.Error as exc :
            if not errors :
                errors.append (exc)
    # end def __call__

    @TFL.Meta.Once_Property
    def entity_as_json_cargo (self) :
        return dict \
            ( ((f.r_name, f.field_as_json_cargo) for f in self.field_elements)
            , ** { "$sid" : self.root.sig_hash (self.sig) }
            )
    # end def entity_as_json_cargo

    @TFL.Meta.Once_Property
    def sig (self) :
        return tuple (f.sig for f in self.field_elements)
    # end def sig

    def fields_as_json_cargo (self) :
        return ((f.id, f.field_as_json_cargo) for f in self.field_elements)
    # end def fields_as_json_cargo

    def _change_from_submission (self, scope, svs) :
        on_error = self._submission_errors.append
        try :
            self.essence.set_raw (on_error = on_error, ** svs)
        except MOM.Error.Error as exc :
            on_error (exc)
        except Exception as exc :
            logging.exception \
                ( "Exception from `set_raw` for %r with %s"
                % (self.essence, sorted (svs.iteritems ()))
                )
            on_error (exc)
    # end def _change_from_submission

    def _create_from_submission (self, scope, svs) :
        ETM = scope [self.E_Type.type_name]
        return self._create_instance (ETM, svs)
    # end def _create_from_submission

    def _create_instance (self, ETM, svs) :
        error = None
        on_error = self._submission_errors.append
        try :
            try :
                rqas      = ETM.raw_query_attrs (svs, svs)
                matches   = ETM.query (* rqas)
            except Exception as exc :
                logging.exception \
                    ( "Exception from "
                      "`ETM.query (* ETM.raw_query_attrs (svs, svs))` "
                      "for ETM = %s, svs = %s"
                    % (ETM.type_name, sorted (svs.iteritems ()), )
                    )
                on_error (exc)
                count     = 0
            else :
                count     = matches.count ()
            if not count :
                result    = ETM (on_error = on_error, raw = True, ** svs)
            else :
                error     = None
                try :
                    epks  = ETM.E_Type.epkified (** svs)
                except MOM.Error.Required_Missing as exc :
                    error = exc
                except Exception :
                    pass
                if error is None :
                    if count == 1 :
                        result = matches.one ()
                    else :
                        error = MOM.Error.Ambiguous_Epk \
                            ( ETM.E_Type, (), svs, count
                            , * matches.limit (3).all ()
                            )
                if error is not None :
                    on_error (error)
        except MOM.Error.Invariants as exc :
            if not exc.any_required_empty :
                on_error (exc)
        else :
            self.essence = self._submitted_value = result
            return result
    # end def _create_instance

    def __iter__ (self) :
        result = self.render_groups or self.elements
        return iter (result)
    # end def __iter__

# end class _Entity_Mixin_

class _Field_ (BaM (_Element_, metaclass = M_Field)) :
    """Base class for MF3 field classes."""

    collapsed               = False
    default                 = _Base_.undef
    prefilled               = False
    template_module         = None

    _attr_prop_map          = dict \
        ( ( (k, k) for k in
            ( "css_align",   "css_class"
            , "description", "explanation", "ui_description"
            , "ui_name",     "ui_rank"
            )
          )
        , allow_new         = "ui_allow_new"
        , choices           = "Choices"
        , input_widget      = "mf3_input_widget"
        , label             = "ui_name"
        , _required         = "is_required"
        , settable          = "is_settable"
        , template_macro    = "mf3_template_macro"
        , template_module   = "mf3_template_module"
        )

    _edit                   = _Base_.undef
    _element_ids            = ("q_name", )
    _init                   = _Base_.undef
    _pop_to_self            = \
        ( "allow_new",        "changeable"
        , "css_align",        "css_class",        "default"
        , "description",      "edit",             "explanation"
        , "init",             "input_widget",     "label"
        , "prefilled",        "skip",             "settable"
        , "template_module",  "template_macro"
        )
    _pop_to_self_           = ("collapsed", "required")
    _q_name                 = None

    def __init__ (self, essence = None, ** kw) :
        q_name      = self.q_name
        attr_spec   = kw.get ("attr_spec", {}).get (q_name, {})
        akw         = dict (attr_spec, ** kw)
        self.__super.__init__ (essence, ** akw)
    # end def __init__

    @classmethod
    def Auto (cls, ak, E_Type, ** kw) :
        name   = q_name = ak.name
        parent = kw.get ("parent")
        if cls.attr_selector is not None :
            E_Type = E_Type.attr_prop (name).E_Type
        def _gen_attr (cls, ak) :
            for k, n in cls._attr_prop_map.items () :
                v = getattr (ak, n, None)
                if not (v is None and getattr (cls, k, None)) :
                    yield k, v
        akw    = dict  (_gen_attr (cls, ak), ** kw)
        if parent :
            q_name = ".".join ((parent.q_name, name)) if parent.q_name else name
            attr_spec = akw.get ("attr_spec", {}).get (q_name, {})
            akw.update (attr_spec)
        akw.setdefault ("attr_selector", cls.attr_selector)
        result = cls.New \
            ( name
            , E_Type        = E_Type
            , attr          = ak.attr
            , name          = name
            , _q_name       = q_name
            , ** akw
            )
        if parent :
            result.bare_id = result._new_id (E_Type)
        if cls.attr_selector is not None :
            result._add_auto_attributes (E_Type, ** kw)
        return result
    # end def Auto

    @TFL.Meta.Once_Property
    def completer (self) :
        a_completer = self.attr.completer
        if a_completer is not None and not (self.readonly or self.skip) :
            return a_completer.MF3 (self)
    # end def completer

    @TFL.Meta.Once_Property
    def Entity (self) :
        result = self.parent
        while isinstance (result, Field_Composite) :
            result = result.parent
        return result
    # end def Entity

    @property
    def edit (self) :
        result = self._edit
        if result is self.undef :
            result = self._edit = self.init
        return result
    # end def edit

    @edit.setter
    def edit (self, value) :
        self._edit = value
    # end def edit

    @property
    def init (self) :
        if self.id_essence is None and self.default is not self.undef :
            result = self.default
        else :
            result = self._init
            if result is self.undef :
                result = self._init = self.attr.kind.get_raw (self.essence)
            else :
                ### XXX TBD: what to do about cooked values here ???
                pass
        return result
    # end def init

    @init.setter
    def init (self, value) :
        self._init = value
    # end def init

    @TFL.Meta.Class_Property
    @TFL.Meta.Class_and_Instance_Method
    def q_name (soc) :
        result = soc._q_name
        if result is None :
            parent = soc.parent
            result = soc.name
            if parent.q_name :
                result = soc._q_name = ".".join ((parent.q_name, result))
        return result
    # end def q_name

    @TFL.Meta.Once_Property
    def r_name (self) :
        """Name relative to `self.Entity`"""
        e_q_name = self.Entity.q_name
        result   = self.q_name
        if e_q_name :
            result = result [len (e_q_name) + 1:]
        return result
    # end def r_name

    @property
    def readonly (self) :
        return any \
            ( ( not self.settable
              , self.prefilled
              , self.id_essence is not None
                and self.attr.kind.change_forbidden (self.essence)
              )
            )
    # end def readonly

    @property
    def required (self) :
        return self.parent.required and self._required
    # end def required

    @property
    def sig (self) :
        return (self.name, self.readonly)
    # end def sig

    @TFL.Meta.Class_and_Instance_Method
    def _own_id (soc, essence) :
        return soc.name
    # end def _own_id

# end class _Field_

class _Field_Composite_Mixin_ (_Element_) :
    """Mixin for Field_Composite and Field_Entity"""

    def __init__ (self, essence = None, ** kw) :
        ref = getattr (essence, self.name) if essence is not None else None
        self.__super.__init__ (ref, ** kw)
    # end def __init__

    @TFL.Meta.Once_Property
    def attr_map (self) :
        result = {}
        for e in self.elements :
            result [e.attr.name] = e
        return result
    # end def attr_map

    @property
    def submitted_value (self) :
        return self.submitted_value_transitive () or self.undef
    # end def submitted_value

    @property
    def ui_display (self) :
        result = self.essence.ui_display if self.id_essence else None
        return result
    # end def ui_display

    def get (self, key, default = None) :
        return self.attr_map.get (key, default)
    # end def get

    def __getitem__ (self, key) :
        return self.attr_map [key]
    # end def __getitem__

# end class _Field_Composite_Mixin_

class Entity (BaM (_Entity_Mixin_, _Element_, metaclass = M_Entity)) :
    """Form comprising a single essential entity."""

    attr_selector       = MOM.Attr.Selector.editable
    id_sep              = ":"
    required            = True
    sid                 = 0
    session_secret      = "some-secret"

    _hash_fct           = hashlib.sha224
    _pop_to_self        = ("_hash_fct", "sid", "session_secret")

    def __init__ (self, scope, essence = None, ** kw) :
        self.completer_map = {}
        self.scope         = scope
        self.__super.__init__ (essence, ** kw)
    # end def __init__

    def __call__ (self, scope, cargo) :
        self.check_sigs       (cargo)
        self.__super.__call__ (scope, cargo)
        return self
    # end def __call__

    @classmethod
    def Auto (cls, E_Type, ** kw) :
        E_Type = E_Type.E_Type ### necessary if E_Type_Manager is passed in
        parent = kw.get ("parent")
        cls._set_id (E_Type, kw)
        result = cls.New \
            ( E_Type.type_name.replace (".", "__")
            , E_Type        = E_Type
            , attr_selector = kw.pop ("attr_selector", cls.attr_selector)
            , ** kw
            )
        if parent is None and "template_macro" not in kw :
            result.template_macro = "Entity_Form"
        result._add_auto_attributes (E_Type, ** kw)
        return result
    # end def Auto

    @TFL.Meta.Once_Property
    def as_json (self) :
        cargo = self.as_json_cargo
        return json.dumps (cargo, sort_keys = True)
    # end def as_json

    @TFL.Meta.Once_Property
    def as_json_cargo (self) :
        def _gen (self, elems) :
            for e in elems :
                for k, v in e.fields_as_json_cargo () :
                    yield k, v
        elems    = tuple (self.elements_transitive ())
        sig_hash =  self.root.sig_hash
        result   = dict \
            ( cargo         = dict
                ( field_values  = dict (_gen (self, self.entity_elements))
                , sid           = self.sid
                , sigs          = dict
                    (  (e.id, sig_hash (e.sig))
                    for e in self.entity_elements
                    )
                )
            , checkers      = {} ### XXX
            , completers    = dict
                (  (e.completer.id, e.completer.as_json_cargo)
                for e in elems if e.completer
                )
            )
        errors = self.errors
        if errors :
            result ["errors"] = MOM.Error.as_json_cargo (* errors)
        return result
    # end def as_json_cargo

    @TFL.Meta.Once_Property
    def Entity (self) :
        return self
    # end def Entity

    @TFL.Meta.Once_Property
    def entity_elements (self) :
        def _gen (self) :
            for e in self.elements_transitive () :
                if isinstance (e, _Entity_Mixin_) and e.field_elements :
                    yield e
        return tuple (_gen (self))
    # end def entity_elements

    @property
    def submitted_value (self) :
        return self.submitted_value_transitive ()
    # end def submitted_value

    @property
    def ui_display (self) :
        if self.essence :
            return self.essence.ui_display
    # end def ui_display

    def check_sigs (self, cargo) :
        cargo_sigs = cargo.get ("sigs", {})
        for e in self.entity_elements :
            sh = self.sig_hash (e.sig)
            ch = cargo_sigs.get (e.id)
            if sh != ch :
                ### XXX TBD ???
                print \
                    ( "Sig mismatch for %s:\n    expected %s,\n    got %s"
                    % (e, sh, ch)
                    )
    # end def check_sigs

    def get (self, key, default = None) :
        return self._Element_Map.get (key, default)
    # end def get

    def sig_hash (self, sig) :
        dbid   = self.scope.db_meta_data.dbid
        salt   = pyk.encoded (self.session_secret)
        result = hmac.new (salt, digestmod = self._hash_fct)
        for s in (self.id, sig, self.E_Type.db_sig, dbid) :
            result.update (pyk.encoded (s))
        return result.hexdigest ()
    # end def sig_hash

    @TFL.Meta.Class_and_Instance_Method
    def _own_id (soc, E_Type) :
        return str (E_Type.i_rank)
    # end def _own_id

    @TFL.Meta.Class_and_Instance_Method
    def _set_id (soc, E_Type, kw) :
        parent     = kw.get ("parent")
        postfix    = kw.pop ("id_postfix", None) or soc._own_id (E_Type)
        if parent is None :
            prefix = kw.pop ("id_prefix", "MF")
            id     = "%s-%s" % (prefix, postfix)
        else :
            id     = parent.id_sep.join ((parent.bare_id, postfix))
        kw ["bare_id"] = id
    # end def _new_id

    def __getitem__ (self, key) :
        return self._Element_Map [key]
    # end def __getitem__

# end class Entity

@TFL.Add_To_Class ("MF3_Element", MAT.A_Attr_Type)
class Field (_Field_) :
    """Field comprising a single atomic attribute."""

    asyn                = _Base_.undef
    attr_selector       = None

    def __call__ (self, scope, cargo) :
        my_cargo  = self._my_cargo (cargo)
        if my_cargo :
            ak    = self.attr.kind
            undef = self.undef
            edit  = my_cargo.get ("edit", undef)
            if edit is not undef :
                if self.id_essence :
                    init = my_cargo.get ("init", ak.get_raw (None))
                    asyn = ak.get_raw (self.essence)
                    if init != asyn :
                        self.conflicts += 1
                        self.asyn       = asyn
                        ### XXX add MOM.Error.?Async_Conflict?...
                        ###     to essence._submission_errors
                else :
                    init = my_cargo.get ("init")
                if edit != init :
                    self._submitted_value = edit
    # end def __call__

    @TFL.Meta.Once_Property
    def completer_elems (self) :
        return (self, )
    # end def completer_elems

    @property
    def cooked (self) :
        attr = self.attr
        kind = attr.kind
        if self.id_essence :
            return kind.get_value   (self.essence)
        else :
            return attr.from_string (self.edit)
    # end def edit

    @TFL.Meta.Once_Property
    def field_as_json_cargo (self) :
        init   = self.init
        edit   = self.edit
        asyn   = self.asyn
        asyn_p = asyn is not self.undef
        if self.id_essence is None and not asyn_p :
            init = None
        result = {}
        if asyn_p or init :
            result ["init"] = init
        if asyn_p or (edit and init != edit) :
            result ["edit"] = edit
        if asyn_p :
            result ["conflict"] = asyn
        return result
    # end def field_as_json_cargo

    @property
    def ui_display (self) :
        if self.id_essence :
            return getattr (self.essence.FO, self.name)
    # end def ui_display

# end class Field

@TFL.Add_To_Class ("MF3_Element", MAT._A_Composite_)
class Field_Composite (_Field_Composite_Mixin_, _Field_) :
    """Field comprising a composite attribute."""

    attr_selector       = MOM.Attr.Selector.editable

    def __call__ (self, scope, cargo) :
        self._submission_errors = []
        for e in self.elements :
            e (scope, cargo)
    # end def __call__

    @TFL.Meta.Once_Property
    def completer_elems (self) :
        return self.elements
    # end def completer_elems

    @property
    def cooked (self) :
        return self.essence if self.id_essence is not None else ()
    # end def edit

    @property
    def edit (self) :
        return ""
    # end def edit

    @property
    def id_essence (self) :
        """Return essence of parent/ancestor element that is an Id_Entity."""
        return self.Entity.essence
    # end def id_essence

    @property
    def init (self) :
        return ""
    # end def init

# end class Field_Composite

@TFL.Add_To_Class ("MF3_Element", MAT._A_Id_Entity_)
class Field_Entity (_Field_Composite_Mixin_, _Entity_Mixin_, _Field_) :
    """Field comprising an attribute referring to another essential Entity."""

    _collapsed          = _Base_.undef
    _essence            = None
    _submitted_value_tp = False

    def __call__ (self, scope, cargo) :
        _essence = self._essence
        my_cargo = self._my_cargo (cargo)
        undef    = self.undef
        value    = undef
        if my_cargo :
            if self.readonly :
                self._submitted_value = my_cargo.get ("init", {}).get ("pid")
            else :
                edit = my_cargo.get ("edit", {})
                if not edit :
                    edit = my_cargo.get ("init", {})
                pid  = edit.get ("pid")
                if pid is not None :
                    if _essence is None or pid != _essence.pid :
                        value = scope.pid_query (pid)
                        self._submitted_value = value
                    else :
                        ### XXX
                        ### will change linked objects inline
                        ### that's not always what the doctor ordered !!!
                        with self.LET (_submitted_value_tp = True) :
                            self.__super.__call__ (scope, cargo)
                else :
                    self.__super.__call__ (scope, cargo)
    # end def __call__

    @property
    def collapsed (self) :
        result = self._collapsed
        if result is self.undef :
            result = self.essence is not None
        return result
    # end def collapsed

    @TFL.Meta.Once_Property
    def completer_elems (self) :
        if self.allow_new and self.attr.completer and not self.readonly :
            def _gen (self) :
                attr_map = self.attr_map
                for a in self.E_Type.primary :
                    e = attr_map.get (a.name)
                    if e is not None and not e.skip :
                        yield e
            return tuple (_gen (self))
        else :
            return (self, )
    # end def completer_elems

    @property
    def cooked (self) :
        return self.essence
    # end def cooked

    @property
    def essence (self) :
        result = self._essence
        if result is None :
            result = self.default
            if result is self.undef :
                result = None
            else :
                ### XXX TBD: what to do about raw values here ???
                pass
        return result
    # end def essence

    @essence.setter
    def essence (self, value) :
        if self._essence != None :
            raise TypeError \
                ( "%s already has value %s; cannot change to %"
                % (self, self.essence.ui_display, value)
                )
        self._essence = value
    # end def essence

    @TFL.Meta.Once_Property
    def field_as_json_cargo (self) :
        essence = self.essence
        if essence is None :
            value  = {}
        else :
            value  = dict \
                ( cid     = essence.last_cid
                , display = essence.ui_display
                , pid     = essence.pid
                )
        result = dict (init = value)
        return result
    # end def field_as_json_cargo

    @property
    def init (self) :
        essence = self.essence
        result  = "" if essence is None else essence.pid
        return result
    # end def init

    @init.setter
    def init (self, value) :
        self.essence = value
    # end def init

    @property
    def submitted_value (self) :
        result = self._submitted_value
        undef  = self.undef
        if result is undef and \
               (self._essence is None or self._submitted_value_tp) :
            result = self.submitted_value_transitive () or undef
        return result
    # end def submitted_value

    def fields_as_json_cargo (self) :
        result = self.__super.fields_as_json_cargo () if self.allow_new else ()
        if self.essence is not None :
            result = ichain (((self.id, self.field_as_json_cargo), ), result)
        return result
    # end def fields_as_json_cargo

    def _new_element (self, e, ** kw) :
        kw ["skip"] = kw.get ("skip") or not self.allow_new
        return self.__super._new_element (e, ** kw)
    # end def _new_element

# end class Field_Entity

if __name__ != "__main__" :
    GTW.MF3._Export_Module ()
### __END__ GTW.MF3.Element

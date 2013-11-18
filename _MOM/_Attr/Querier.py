# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Attr.
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
#    MOM.Attr.Querier
#
# Purpose
#    Model queries for MOM attributes
#
# Revision Dates
#     4-Dec-2011 (CT) Creation (factored from MOM.Attr.Filter)
#     4-Dec-2011 (CT) Change signature of `_Filter_.__init__` to `(querier)`
#     4-Dec-2011 (CT) Add `_full_name`
#     4-Dec-2011 (CT) Add `choices` to `_as_template_elem_inv`
#     7-Dec-2011 (CT) Add `E_Type`
#    12-Dec-2011 (CT) Add `Class`, remove `deep`
#    13-Dec-2011 (CT) Add `Atoms`, `Unwrapped`, and `Unwrapped_Atoms`
#    13-Dec-2011 (CT) Add `QC` and `QR`
#    16-Dec-2011 (CT) Add `IN`
#    20-Dec-2011 (CT) Use `.sig_attr` instead of home-grown code
#    20-Dec-2011 (CT) Factor `_Container_`, derive `E_Type` from it
#    20-Dec-2011 (CT) Add `Children_Transitive`, `E_Type.As_Json`
#    22-Dec-2011 (CT) s/Children/Attrs/
#    22-Dec-2011 (CT) Add `_attr_selector` to `_Type_` and use it in
#                     `_Container_._attrs`
#    22-Dec-2011 (CT) Add `E_Type.Select`
#     5-Oct-2012 (CT) Guard `_Container_._attrs` against missing `E_Type`
#    10-Oct-2012 (CT) Change `_Type_._cooker` to apply `from_string` to strings
#     7-Mar-2013 (CT) Add `_string_q_name`, `_string_attr_name`,`_string_cooker`
#     7-Mar-2013 (CT) Redefine `Raw.Table` to include `EQS` and `NES`
#    19-Mar-2013 (CT) Refactor `Attrs_Transitive` (and `_attrs_transitive`)
#    19-Mar-2013 (CT) Add argument `seen_etypes` to `_attrs_transitive` to
#                     break E_Type cycles
#    19-Mar-2013 (CT) Protect `As_Json_Cargo`, `As_Template_Elem` against cycles
#    19-Mar-2013 (CT) Protect `Atoms`, `Unwrapped_Atoms`
#    19-Mar-2013 (CT) Pass a copy of `seen_etypes` to recursive calls
#                     (otherwise, a sibling can mask a E_Type)
#    20-Mar-2013 (CT) Add and use `_recursion_limit = 2` to limit E_Type cycles
#    20-Mar-2013 (CT) Add `E_Type.As_Template_Elem`
#    21-Mar-2013 (CT) Factor `_do_recurse`
#                     * consider `has_identity` and `polymorphic_epk`
#    21-Mar-2013 (CT) Check `_do_recurse` once for `self` in `_as_json_cargo`,
#                     `_as_template_elem`; not for each element of `.Attrs`
#    21-Mar-2013 (CT) Redefine `Id_Entity._as_json_cargo_inv`
#                     * add `children_np`
#    22-Mar-2013 (CT) Add `default_child` to `Id_Entity._as_json_cargo_inv`,
#                     factor `E_Types_CNP`, add `E_Types_AQ`
#    22-Mar-2013 (CT) Move `_polymorphic` check out of `_do_recurse`
#    28-Mar-2013 (CT) Redefine `Id_Entity._as_json_cargo`, `._as_template_elem`
#                     to include `._as_...` for each of the `children_np`
#    28-Mar-2013 (CT) Redefine `_Id_Entity_NP_._as_json_cargo_inv`, and
#                     `._as_json_cargo`
#     2-Apr-2013 (CT) Redefine `Id_Entity._as_template_elem_inv` to add
#                     `type_name`
#     3-Apr-2013 (CT) Add `ui_type_name` to `Id_Entity._as_template_elem`
#    11-Apr-2013 (CT) Redefine `_Id_Entity_NP_._ui_name_T` to add `[type_name]`
#    11-Apr-2013 (CT) Include `children_np` in `Sig_Map`
#    18-Apr-2013 (CT) Change `E_Types_CNP` to use
#                     `selectable_e_types_unique_epk`, not `children_np`
#     3-Jun-2013 (CT) Get attribute descriptors from `E_Type.attributes`
#     5-Jun-2013 (CT) Use `Selector.ui_attr`, not `.all`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

from   _MOM._Attr            import Filter

import _TFL._Meta.Object

from   _TFL.Decorator        import getattr_safe
from   _TFL.I18N             import _, _T, _Tn
from   _TFL.defaultdict      import defaultdict_int as ETC
from   _TFL.predicate        import filtered_join, split_hst, uniq

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

id_sep = "__"
op_sep = "___"
ui_sep = "/"

class _Base_ (TFL.Meta.Object) :

    _recursion_limit = 2

    @property    ### depends on currently selected language (I18N/L10N)
    @getattr_safe###
    def As_Json_Cargo (self) :
        return self._as_json_cargo (ETC ())
    # end def As_Json_Cargo

    @property    ### depends on currently selected language (I18N/L10N)
    @getattr_safe###
    def As_Template_Elem (self) :
        return self._as_template_elem (ETC ())
    # end def As_Template_Elem

    @TFL.Meta.Once_Property
    @getattr_safe
    def Atoms (self) :
        return tuple (self._atoms (ETC ()))
    # end def Atoms

    @TFL.Meta.Once_Property
    @getattr_safe
    def Attrs_Transitive (self) :
        return tuple (self._attrs_transitive (ETC ()))
    # end def Attrs_Transitive

    @TFL.Meta.Once_Property
    @getattr_safe
    def Unwrapped_Atoms (self) :
        return tuple (self._unwrapped_atoms (ETC ()))
    # end def Unwrapped_Atoms

    @TFL.Meta.Once_Property
    @getattr_safe
    def _polymorphic (self) :
        cet = self.E_Type
        result = False
        if cet is not None and cet.has_identity :
            result = cet.polymorphic_epk
        return result
    # end def _polymorphic

    def _as_json_cargo (self, seen_etypes) :
        return dict (self._as_json_cargo_inv, ui_name = self._attr.ui_name_T)
    # end def _as_json_cargo

    def _as_template_elem (self, seen_etypes) :
        result = dict (self._as_template_elem_inv, ui_name = self._ui_name_T)
        return TFL.Record (** result)
    # end def _as_template_elem

    def _sig_map_transitive (self, seen_etypes) :
        return {}
    # end def _sig_map_transitive

# end class _Base_

class _Container_ (_Base_) :

    @TFL.Meta.Once_Property
    @getattr_safe
    def Attrs (self) :
        return tuple (getattr (self, c.name) for c in self._attrs)
    # end def Attrs

    @TFL.Meta.Once_Property
    @getattr_safe
    def _attrs (self) :
        ET = self.E_Type
        if ET is not None :
            return self._attr_selector (self.E_Type)
        else :
            return ()
    # end def _attrs

    def _as_json_cargo (self, seen_etypes) :
        seen_etypes [self.E_Type] += 1
        result = self.__super._as_json_cargo (seen_etypes)
        if self._do_recurse (self, self._recursion_limit, seen_etypes) :
            if not self._polymorphic :
                attrs = list \
                    (c._as_json_cargo (ETC (seen_etypes)) for c in self.Attrs)
                if attrs :
                    result ["attrs"] = attrs
        return result
    # end def _as_json_cargo

    def _as_template_elem (self, seen_etypes) :
        seen_etypes [self.E_Type] += 1
        result = self.__super._as_template_elem (seen_etypes)
        if self._do_recurse (self, self._recursion_limit, seen_etypes) :
            if not self._polymorphic :
                attrs = list \
                    (   c._as_template_elem (ETC (seen_etypes))
                    for c in self.Attrs
                    )
                if attrs :
                    result ["attrs"] = attrs
        return result
    # end def _as_template_elem

    def _atoms (self, seen_etypes) :
        seen_etypes [self.E_Type] += 1
        rc = self._recursion_limit
        for c in self.Attrs :
            if self._do_recurse (c, rc, seen_etypes) and not c._polymorphic :
                for ct in c._atoms (ETC (seen_etypes)):
                    yield ct
    # end def _atoms

    def _attrs_transitive (self, seen_etypes) :
        seen_etypes [self.E_Type] += 1
        rc = self._recursion_limit
        for c in self.Attrs :
            if self._do_recurse (c, rc, seen_etypes) and not c._polymorphic :
                for ct in c._attrs_transitive (ETC (seen_etypes)):
                    yield ct
            else :
                yield c
    # end def _attrs_transitive

    def _do_recurse (self, c, rc, seen_etypes) :
        cet    = c.E_Type
        result = True
        if cet is not None :
            if cet.has_identity :
                result = seen_etypes [cet] <= rc
            seen_etypes [cet] += 1
        return result
    # end def _do_recurse

    def _sig_map_transitive (self, seen_etypes) :
        seen_etypes [self.E_Type] += 1
        result = self.__super._sig_map_transitive (seen_etypes)
        rc = self._recursion_limit
        for c in self.Attrs :
            if self._do_recurse (c, rc, seen_etypes) :
                result.update (c._sig_map_transitive (seen_etypes))
        return result
    # end def _sig_map_transitive

    def _unwrapped_atoms (self, seen_etypes) :
        seen_etypes [self.E_Type] += 1
        rc = self._recursion_limit
        for c in self.Attrs :
            if self._do_recurse (c, rc, seen_etypes) and not c._polymorphic :
                for ct in c.Unwrapped.Atoms :
                    yield ct
    # end def _unwrapped_atoms

# end class _Container_

class _M_Type_ (TFL.Meta.Object.__class__) :
    """Meta class for Type classes."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        cls.Op_Map  = dict  (cls.Table, ** cls._Table)
        cls.Op_Keys = tuple (sorted (cls.Table))
        if cls.Op_Keys and cls.Op_Keys not in cls.Signatures :
            cls.Signatures [cls.Op_Keys] = len (cls.Signatures)
    # end def __init__

    def __str__ (cls) :
        return "<Attr.Type.Querier %s %s>" % (cls.__name__, cls.Op_Keys)
    # end def __str__

# end class _M_Type_

class _Type_ (_Base_) :
    """Base class for Type classes.

       A Type class provides all filters for a set of Attr.Type classes.
    """

    __metaclass__ = _M_Type_

    Base_Op_Table = Filter._Filter_.Base_Op_Table

    Class         = None
    Signatures    = {}

    ### `Table` maps the filter operations that can sensibly be selected in a UI
    Table   = dict \
        ( EQ                 = Filter.Equal
        , GE                 = Filter.Greater_Equal
        , GT                 = Filter.Greater_Than
        , IN                 = Filter.In
        , LE                 = Filter.Less_Equal
        , LT                 = Filter.Less_Than
        , NE                 = Filter.Not_Equal
        )
    ### `_Table` maps additonal filter operations that don't make sense in a UI
    _Table  = dict \
        ( AC                 = Filter.Auto_Complete
        )

    def __init__ (self, attr, outer = None) :
        self._attr  = attr
        self._outer = outer
        self._attr_selector = outer and outer._attr_selector
    # end def __init__

    @TFL.Meta.Once_Property
    @getattr_safe
    def Attrs (self) :
        return ()
    # end def Attrs

    @TFL.Meta.Once_Property
    @getattr_safe
    def E_Type (self) :
        return self._attr.E_Type
    # end def E_Type

    @TFL.Meta.Once_Property
    @getattr_safe
    def QC (self, ) :
        return getattr (Filter.Q, self._q_name)
    # end def QC

    @TFL.Meta.Once_Property
    @getattr_safe
    def QR (self, ) :
        return getattr (Filter.Q, self._q_name_raw)
    # end def QR

    @TFL.Meta.Once_Property
    @getattr_safe
    def Sig_Key (self) :
        if self.Op_Keys :
            return self.Signatures [self.Op_Keys]
    # end def Sig_Key

    @TFL.Meta.Once_Property
    @getattr_safe
    def Unwrapped (self) :
        result = self
        if self._outer :
            result = self.__class__ (self._attr)
        return result
    # end def Unwrapped

    @TFL.Meta.Once_Property
    @getattr_safe
    def _as_json_cargo_inv (self) :
        attr     = self._attr
        Class    = self.Class
        Sig_Key  = self.Sig_Key
        result   = dict (name = attr.name)
        if Class :
            result ["Class"]    = Class
        if Sig_Key is not None :
            result ["sig_key"]  = Sig_Key
        return result
    # end def _as_json_cargo_inv

    @TFL.Meta.Once_Property
    @getattr_safe
    def _as_template_elem_inv (self) :
        attr     = self._attr
        result   = dict \
            ( self._as_json_cargo_inv
            , attr        = attr
            , id          = self._id
            , full_name   = self._full_name
            )
        if attr.Choices :
            result ["choices"] = attr.Choices
        return result
    # end def _as_template_elem_inv

    @TFL.Meta.Once_Property
    @getattr_safe
    def _attr_name (self) :
        return self._attr.name
    # end def _attr_name

    @property
    @getattr_safe
    def _attr_selector (self) :
        return getattr (self, "__attr_selector", None) or MOM.Attr.Selector.sig
    # end def _attr_selector

    @_attr_selector.setter
    @getattr_safe
    def _attr_selector (self, value) :
        if value is None :
            value = MOM.Attr.Selector.sig
        elif not (  value is MOM.Attr.Selector.ui_attr
                 or isinstance (value, MOM.Attr.Selector.Kind)
                 ) :
            value = MOM.Attr.Selector.sig
        setattr (self, "__attr_selector", value)
    # end def _attr_selector

    @TFL.Meta.Once_Property
    @getattr_safe
    def _full_name (self) :
        outer = self._outer
        return filtered_join (".", (outer and outer._q_name, self._attr.name))
    # end def _full_name

    @TFL.Meta.Once_Property
    @getattr_safe
    def _id (self) :
        outer = self._outer
        return filtered_join (id_sep, (outer and outer._id, self._attr.name))
    # end def _id

    @TFL.Meta.Once_Property
    @getattr_safe
    def _q_name (self) :
        outer = self._outer
        return filtered_join (".", (outer and outer._q_name, self._attr_name))
    # end def _q_name

    @TFL.Meta.Once_Property
    @getattr_safe
    def _q_name_raw (self) :
        outer = self._outer
        return filtered_join \
            (".", (outer and outer._q_name, self._attr.raw_name))
    # end def _q_name_raw

    @property    ### depends on currently selected language (I18N/L10N)
    @getattr_safe###
    def _ui_name_T (self) :
        outer = self._outer
        return filtered_join \
            (ui_sep, (outer and outer._ui_name_T, self._attr.ui_name_T))
    # end def _ui_name_T

    def Wrapped (self, outer) :
        assert not self._outer
        return self.__class__ (self._attr, outer)
    # end def Wrapped

    def _atoms (self, seen_etypes) :
        yield self
    # end def _atoms

    def _attrs_transitive (self, seen_etypes) :
        yield self
    # end def _attrs_transitive

    def _cooker (self, value) :
        attr = self._attr
        if isinstance (value, basestring) :
            return attr.from_string (value, None, {}, {})
        else :
            return attr.cooked (value)
    # end def _cooker

    def _sig_map_transitive (self, seen_etypes) :
        result  = self.__super._sig_map_transitive (seen_etypes)
        op_keys = self.Op_Keys
        if op_keys :
            result [self.Signatures [op_keys]] = op_keys
        return result
    # end def _sig_map_transitive

    def _unwrapped_atoms (self, seen_etypes) :
        yield self.Unwrapped
    # end def _unwrapped_atoms

    def __getattr__ (self, name) :
        try :
            result_type = self.Op_Map [name]
        except KeyError :
            raise AttributeError (name)
        else :
            result = result_type (self)
            setattr (self, name, result)
            return result
    # end def __getattr__

    def __repr__ (self) :
        return str (self)
    # end def __repr__

    def __str__ (self) :
        return "<%s.AQ [Attr.Type.Querier %s]>" % \
            (self._q_name, self.__class__.__name__)
    # end def __str__

# end class _Type_

class _Composite_ (_Container_, _Type_) :

    def _attrs_transitive (self, seen_etypes) :
        yield self
        for c in self.__super._attrs_transitive (seen_etypes) :
            yield c
    # end def _attrs_transitive

    def __getattr__ (self, name) :
        try :
            result = self.__super.__getattr__ (name)
        except AttributeError :
            head, _, tail = split_hst (name, ".")
            try :
                result = self.E_Type.attributes [head].AQ.Wrapped (self)
                setattr (self, head, result)
                if tail :
                    result = getattr (Filter.Q, tail) (result)
            except LookupError :
                raise AttributeError (name)
        return result
    # end def __getattr__

# end class _Composite_

class Boolean (_Type_) :

    Table  = dict \
        ( EQ                 = Filter.Equal
        )

# end class Boolean

class Ckd (_Type_) :

    pass

# end class Ckd

class Composite (_Composite_) :

    Table  = dict ()
    _Table = dict \
        ( AC                 = Filter.Composite_Auto_Complete
        , EQ                 = Filter.Composite_Equal
        , GE                 = Filter.Composite_Greater_Equal
        , GT                 = Filter.Composite_Greater_Than
        , IN                 = Filter.Composite_In
        , LE                 = Filter.Composite_Less_Equal
        , LT                 = Filter.Composite_Less_Than
        , NE                 = Filter.Composite_Not_Equal
        )

# end class Composite

class Date (_Type_) :

    Table  = dict \
        ( EQ                 = Filter.Date_Equal
        , GE                 = Filter.Date_Greater_Equal
        , GT                 = Filter.Date_Greater_Than
        , IN                 = Filter.Date_In
        , LE                 = Filter.Date_Less_Equal
        , LT                 = Filter.Date_Less_Than
        , NE                 = Filter.Date_Not_Equal
        )
    _Table = dict \
        ( AC                 = Filter.Date_Auto_Complete
        )

# end class Date

class Id_Entity (_Composite_) :

    Class  = "Entity"
    Table  = dict \
        ( EQ                 = Filter.Id_Entity_Equal
        , IN                 = Filter.Id_Entity_In
        , NE                 = Filter.Id_Entity_Not_Equal
        )
    _Table = dict \
        ( AC                 = Filter.Id_Entity_Auto_Complete
        , GE                 = Filter.Id_Entity_Greater_Equal
        , GT                 = Filter.Id_Entity_Greater_Than
        , LE                 = Filter.Id_Entity_Less_Equal
        , LT                 = Filter.Id_Entity_Less_Than
        )

    @TFL.Meta.Once_Property
    @getattr_safe
    def E_Types_AQ (self) :
        E_Types_CNP = self.E_Types_CNP
        if E_Types_CNP :
            return dict \
                (   (k, _Id_Entity_NP_ (ET, self._attr))
                for (k, ET) in E_Types_CNP.iteritems ()
                )
    # end def E_Types_AQ

    @TFL.Meta.Once_Property
    @getattr_safe
    def E_Types_CNP (self) :
        ET  = self.E_Type
        apt = ET.app_type
        cnp = self._attr.selectable_e_types_unique_epk
        if ET.polymorphic_epk and cnp :
            return dict ((str (c), apt.entity_type (c)) for c in cnp)
    # end def E_Types_CNP

    @TFL.Meta.Once_Property
    @getattr_safe
    def _as_json_cargo_inv (self) :
        result = self.__super._as_json_cargo_inv
        ET     = self.E_Type
        if self.E_Types_CNP :
            if ET.default_child :
                result ["default_child"] = ET.default_child
        return result
    # end def _as_json_cargo_inv

    @TFL.Meta.Once_Property
    @getattr_safe
    def _as_template_elem_inv (self) :
        result = self.__super._as_template_elem_inv
        result ["type_name"] = self.E_Type.type_name
        return result
    # end def _as_template_elem_inv

    def _as_json_cargo (self, seen_etypes) :
        result = self.__super._as_json_cargo (seen_etypes)
        E_Types_CNP = self.E_Types_CNP
        if E_Types_CNP :
            result ["children_np"] = list \
                (   self [etn]._as_json_cargo (seen_etypes)
                for etn in sorted (E_Types_CNP)
                )
        return result
    # end def _as_json_cargo

    def _as_template_elem (self, seen_etypes) :
        result = self.__super._as_template_elem (seen_etypes)
        result ["ui_type_name"] = _T (self.E_Type.ui_name)
        E_Types_CNP = self.E_Types_CNP
        if E_Types_CNP :
            result ["children_np"] = list \
                (   self [etn]._as_template_elem (seen_etypes)
                for etn in sorted (E_Types_CNP)
                )
        return result
    # end def _as_template_elem

    def _sig_map_transitive (self, seen_etypes) :
        result     = self.__super._sig_map_transitive (seen_etypes)
        E_Types_AQ = self.E_Types_AQ
        if E_Types_AQ :
            for aq in E_Types_AQ.itervalues () :
                result.update (aq._sig_map_transitive (seen_etypes))
        return result
    # end def _sig_map_transitive

    def __getitem__ (self, key) :
        E_Types_AQ = self.E_Types_AQ
        if E_Types_AQ :
            return E_Types_AQ [key]
    # end def __getitem__

# end class Id_Entity

class _Id_Entity_NP_ (Id_Entity) :

    def __init__ (self, ET, attr, outer = None) :
        self._E_Type = ET
        self.__super.__init__ (attr, outer = outer)
    # end def __init__

    @property
    def E_Type (self) :
        return self._E_Type
    # end def E_Type

    @TFL.Meta.Once_Property
    @getattr_safe
    def Unwrapped (self) :
        result = self
        if self._outer :
            result = self.__class__ (self._E_Type, self._attr)
        return result
    # end def Unwrapped

    @TFL.Meta.Once_Property
    @getattr_safe
    def _as_json_cargo_inv (self) :
        result = self.__super._as_json_cargo_inv
        result ["type_name"] = self.E_Type.type_name
        return result
    # end def _as_json_cargo_inv

    @property    ### depends on currently selected language (I18N/L10N)
    @getattr_safe###
    def _ui_name_T (self) :
        return "%s[%s]" % ((self.__super._ui_name_T), _T (self.E_Type.ui_name))
    # end def _ui_name_T

    def Wrapped (self, outer) :
        assert not self._outer
        return self.__class__ (self._E_Type, self._attr, outer)
    # end def Wrapped

    def _as_json_cargo (self, seen_etypes) :
        result = self.__super._as_json_cargo (seen_etypes)
        result ["ui_type_name"] = _T (self.E_Type.ui_name)
        return result
    # end def _as_json_cargo

# end class _Id_Entity_NP_

class String (_Type_) :

    Table  = dict \
        ( _Type_.Table
        , CONTAINS           = Filter.Contains
        , ENDSWITH           = Filter.Ends_With
        , STARTSWITH         = Filter.Starts_With
        )
    _Table = dict \
        ( AC                 = Filter.Auto_Complete_S
        )

    @TFL.Meta.Once_Property
    @getattr_safe
    def _string_attr_name (self) :
        return self._attr_name
    # end def _string_attr_name

    @TFL.Meta.Once_Property
    @getattr_safe
    def _string_cooker (self) :
        return self._cooker
    # end def _string_cooker

    @TFL.Meta.Once_Property
    @getattr_safe
    def _string_q_name (self) :
        return self._q_name
    # end def _string_cooker

# end class String

class Raw (String) :

    Table  = dict \
        ( String.Table
        , EQS                = Filter.Equal_S
        , NES                = Filter.Not_Equal_S
        )

    @TFL.Meta.Once_Property
    @getattr_safe
    def _string_attr_name (self) :
        return self._attr.raw_name
    # end def _string_attr_name

    @TFL.Meta.Once_Property
    @getattr_safe
    def _string_cooker (self) :
        return unicode
    # end def _string_cooker

    @TFL.Meta.Once_Property
    @getattr_safe
    def _string_q_name (self) :
        return self._q_name_raw
    # end def _string_cooker

# end class Raw

class E_Type (_Container_) :
    """Query object for `E_Type` returning an essential attribute's `AQ`"""

    _id = _q_name = _ui_name_T = None

    def __init__ (self, E_Type, _attr_selector = None) :
        self.E_Type = E_Type
        self._attr_selector = _attr_selector
    # end def __init__

    def Select (self, _attr_selector) :
        return self.__class__ (self.E_Type, _attr_selector)
    # end def Select

    @property
    def As_Json (self) :
        import json
        return json.dumps (self.As_Json_Cargo, sort_keys = True)
    # end def as_json

    @property    ### depends on currently selected language (I18N/L10N)
    @getattr_safe###
    def As_Json_Cargo (self) :
        filters = [f.As_Json_Cargo for f in self.Attrs]
        return dict \
            ( filters   = filters
            , name_sep  = id_sep
            , op_map    = self.Op_Map
            , op_sep    = op_sep
            , sig_map   = self.Sig_Map
            , ui_sep    = ui_sep
            )
    # end def As_Json_Cargo

    @property    ### depends on currently selected language (I18N/L10N)
    @getattr_safe###
    def As_Template_Elem (self) :
        return [f.As_Template_Elem for f in self.Attrs]
    # end def As_Template_Elem

    @property
    def Op_Map (self) :
        result = {}
        for k, v in _Type_.Base_Op_Table.iteritems () :
            sym = _T (v.op_sym)
            result [k] = dict \
                ( desc  = _T (v.desc)
                , sym   = sym
                )
        return result
    # end def Op_Map

    @TFL.Meta.Once_Property
    def Sig_Map (self) :
        result      = {}
        seen_etypes = ETC ()
        for c in self.Attrs :
            result.update (c._sig_map_transitive (seen_etypes))
        return result
    # end def Sig_Map

    @property
    def _attr_selector (self) :
        return getattr (self, "__attr_selector")
    # end def _attr_selector

    @_attr_selector.setter
    def _attr_selector (self, value) :
        setattr (self, "__attr_selector", value or MOM.Attr.Selector.ui_attr)
    # end def _attr_selector

    def __getattr__ (self, name) :
        head, _, tail = split_hst (name, ".")
        try :
            result = self.E_Type.attributes [head].AQ.Wrapped (self)
            setattr (self, head, result)
            if tail :
                result = getattr (Filter.Q, tail) (result)
        except LookupError :
            raise AttributeError (name)
        return result
    # end def __getattr__

    def __repr__ (self) :
        return "<Attr.Type.Querier.%s for %s>" % \
            (self.__class__.__name__, self.E_Type.type_name)
    # end def __repr__

    def __str__ (self) :
        return "<%s.AQ>" % (self.E_Type.type_name, )
    # end def __str__

# end class E_Type

if __name__ != "__main__" :
    MOM.Attr._Export_Module ()
### __END__ MOM.Attr.Querier

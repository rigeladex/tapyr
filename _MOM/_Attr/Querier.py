# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
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
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

from   _MOM._Attr            import Filter

import _TFL._Meta.Object

from   _TFL.I18N             import _, _T, _Tn
from   _TFL.predicate        import filtered_join, split_hst, uniq

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

id_sep = "__"
op_sep = "___"
ui_sep = "/"

class _Container_ (TFL.Meta.Object) :

    @TFL.Meta.Once_Property
    def Atoms (self) :
        return tuple (a for c in self.Attrs for a in c.Atoms)
    # end def Atoms

    @TFL.Meta.Once_Property
    def Attrs (self) :
        return tuple (getattr (self, c.name) for c in self._attrs)
    # end def Attrs

    @TFL.Meta.Once_Property
    def Unwrapped_Atoms (self) :
        return tuple (a for c in self.Attrs for a in c.Unwrapped.Atoms)
    # end def Unwrapped_Atoms

    @TFL.Meta.Once_Property
    def _attrs (self) :
        return self._attr_selector (self.E_Type)
    # end def _attrs

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

class _Type_ (TFL.Meta.Object) :
    """Base class for Type classes.

       A Type class provides all filters for a set of Attr.Type classes.
    """

    __metaclass__ = _M_Type_

    Base_Op_Table = Filter._Filter_.Base_Op_Table

    Class         = None
    Signatures    = {}

    ### `Table` maps the operations that can sensibly be selected in a UI
    Table   = dict \
        ( EQ                 = Filter.Equal
        , GE                 = Filter.Greater_Equal
        , GT                 = Filter.Greater_Than
        , IN                 = Filter.In
        , LE                 = Filter.Less_Equal
        , LT                 = Filter.Less_Than
        , NE                 = Filter.Not_Equal
        )
    ### `_Table` maps additonal operations that don't make sense in a UI
    _Table  = dict \
        ( AC                 = Filter.Auto_Complete
        )

    def __init__ (self, attr, outer = None) :
        self._attr  = attr
        self._outer = outer
        self._attr_selector = outer and outer._attr_selector
    # end def __init__

    @property    ### depends on currently selected language (I18N/L10N)
    def As_Json_Cargo (self) :
        Attrs = self.Attrs
        result   = dict \
            ( self._as_json_cargo_inv
            , ui_name  = self._attr.ui_name_T
            )
        if Attrs :
            result ["attrs"] = [c.As_Json_Cargo for c in Attrs]
        return result
    # end def As_Json_Cargo

    @property    ### depends on currently selected language (I18N/L10N)
    def As_Template_Elem (self) :
        Attrs = self.Attrs
        result   = dict \
            ( self._as_template_elem_inv
            , ui_name  = self._ui_name_T
            )
        if Attrs :
            result ["attrs"] = [c.As_Template_Elem for c in Attrs]
        return TFL.Record (** result)
    # end def As_Template_Elem

    @TFL.Meta.Once_Property
    def Atoms (self) :
        return (self, )
    # end def Atoms

    @TFL.Meta.Once_Property
    def Attrs (self) :
        return ()
    # end def Attrs

    @TFL.Meta.Once_Property
    def Attrs_Transitive (self) :
        return tuple (self._attrs_transitive ())
    # end def Attrs_Transitive

    @TFL.Meta.Once_Property
    def E_Type (self) :
        return self._attr.E_Type
    # end def E_Type

    @TFL.Meta.Once_Property
    def QC (self, ) :
        return getattr (Filter.Q, self._q_name)
    # end def QC

    @TFL.Meta.Once_Property
    def QR (self, ) :
        return getattr (Filter.Q, self._q_name_raw)
    # end def QR

    @TFL.Meta.Once_Property
    def Sig_Key (self) :
        if self.Op_Keys :
            return self.Signatures [self.Op_Keys]
    # end def Sig_Key

    @TFL.Meta.Once_Property
    def Unwrapped (self) :
        result = self
        if self._outer :
            result = self.__class__ (self._attr)
        return result
    # end def Unwrapped

    @TFL.Meta.Once_Property
    def Unwrapped_Atoms (self) :
        return (self.Unwrapped, )
    # end def Unwrapped_Atoms

    @TFL.Meta.Once_Property
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
    def _attr_name (self) :
        return self._attr.name
    # end def _attr_name

    @property
    def _attr_selector (self) :
        return getattr (self, "__attr_selector", None) or MOM.Attr.Selector.sig
    # end def _attr_selector

    @_attr_selector.setter
    def _attr_selector (self, value) :
        if value is None :
            value = MOM.Attr.Selector.sig
        elif not (  value is MOM.Attr.Selector.all
                 or isinstance (value, MOM.Attr.Selector.Kind)
                 ) :
            value = MOM.Attr.Selector.sig
        setattr (self, "__attr_selector", value)
    # end def _attr_selector

    @TFL.Meta.Once_Property
    def _cooker (self) :
        return self._attr.cooked
    # end def _cooker

    @TFL.Meta.Once_Property
    def _full_name (self) :
        outer = self._outer
        return filtered_join (".", (outer and outer._q_name, self._attr.name))
    # end def _full_name

    @TFL.Meta.Once_Property
    def _id (self) :
        outer = self._outer
        return filtered_join (id_sep, (outer and outer._id, self._attr.name))
    # end def _id

    @TFL.Meta.Once_Property
    def _q_name (self) :
        outer = self._outer
        return filtered_join (".", (outer and outer._q_name, self._attr_name))
    # end def _q_name

    @TFL.Meta.Once_Property
    def _q_name_raw (self) :
        outer = self._outer
        return filtered_join \
            (".", (outer and outer._q_name, self._attr.raw_name))
    # end def _q_name_raw

    @property    ### depends on currently selected language (I18N/L10N)
    def _ui_name_T (self) :
        outer = self._outer
        return filtered_join \
            (ui_sep, (outer and outer._ui_name_T, self._attr.ui_name_T))
    # end def _ui_name_T

    def Wrapped (self, outer) :
        assert not self._outer
        return self.__class__ (self._attr, outer)
    # end def Wrapped

    def _attrs_transitive (self) :
        yield self
        for c in self.Attrs :
            for ct in c.Attrs_Transitive :
                yield ct
    # end def _attrs_transitive

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

    def __getattr__ (self, name) :
        try :
            result = self.__super.__getattr__ (name)
        except AttributeError :
            head, _, tail = split_hst (name, ".")
            try :
                result = getattr (self._attr.E_Type, head).AQ.Wrapped (self)
                setattr (self, head, result)
                if tail :
                    result = getattr (result, tail)
            except AttributeError :
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

# end class Id_Entity

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

# end class String

class Raw (String) :

    @TFL.Meta.Once_Property
    def _attr_name (self) :
        return self._attr.raw_name
    # end def _attr_name

    @TFL.Meta.Once_Property
    def _cooker (self) :
        return unicode
    # end def _cooker

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

    @property
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

    @TFL.Meta.Once_Property
    def Attrs_Transitive (self) :
        return tuple (ct for c in self.Attrs for ct in c.Attrs_Transitive)
    # end def Attrs_Transitive

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
        result = {}
        Signatures = _Type_.Signatures
        for f in uniq (f.Op_Keys for f in self.Attrs_Transitive) :
            if f :
                result [Signatures [f]] = f
        return result
    # end def Sig_Map

    @property
    def _attr_selector (self) :
        return getattr (self, "__attr_selector")
    # end def _attr_selector

    @_attr_selector.setter
    def _attr_selector (self, value) :
        setattr (self, "__attr_selector", value or MOM.Attr.Selector.all)
    # end def _attr_selector

    def __getattr__ (self, name) :
        head, _, tail = split_hst (name, ".")
        result = getattr (self.E_Type, head).AQ.Wrapped (self)
        setattr (self, head, result)
        if tail :
            result = getattr (Filter.Q, tail) (result)
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

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
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

from   _MOM._Attr            import Filter

import _TFL._Meta.Object

from   _TFL.predicate        import filtered_join, split_hst

import _TFL._Meta.Object
import _TFL._Meta.Once_Property

id_sep = "__"
ui_sep = "/"

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

    deep          = False
    Signatures    = {}

    ### `Table` maps the operations that can sensibly be selected in a UI
    Table   = dict \
        ( EQ                 = Filter.Equal
        , GE                 = Filter.Greater_Equal
        , GT                 = Filter.Greater_Than
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
    # end def __init__

    @property    ### depends on currently selected language (I18N/L10N)
    def as_json_cargo (self) :
        Children = self.Children
        result   = dict \
            ( self._as_json_cargo_inv
            , ui_name  = self._attr.ui_name_T
            )
        if Children :
            result ["children"] = [c.as_json_cargo for c in Children]
        return result
    # end def as_json_cargo

    @property    ### depends on currently selected language (I18N/L10N)
    def as_template_elem (self) :
        Children = self.Children
        result   = dict \
            ( self._as_template_elem_inv
            , ui_name  = self._ui_name_T
            )
        if Children :
            result ["children"] = [c.as_template_elem for c in Children]
        return TFL.Record (** result)
    # end def as_template_elem

    @TFL.Meta.Once_Property
    def Children (self) :
        return ()
    # end def Children

    @TFL.Meta.Once_Property
    def Sig_Key (self) :
        if self.Op_Keys :
            return self.Signatures [self.Op_Keys]
    # end def Sig_Key

    @TFL.Meta.Once_Property
    def _as_json_cargo_inv (self) :
        attr     = self._attr
        deep     = self.deep
        Sig_Key  = self.Sig_Key
        result   = dict (name = attr.name)
        if deep :
            result ["deep"]     = deep
        if Sig_Key is not None :
            result ["sig_key"]  = Sig_Key
        return result
    # end def _as_json_cargo_inv

    @TFL.Meta.Once_Property
    def _as_template_elem_inv (self) :
        result   = dict \
            ( self._as_json_cargo_inv
            , attr        = self._attr
            , id          = self._id
            , full_name   = self._full_name
            )
        return result
    # end def _as_template_elem_inv

    @TFL.Meta.Once_Property
    def _attr_name (self) :
        return self._attr.name
    # end def _attr_name

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

    @property    ### depends on currently selected language (I18N/L10N)
    def _ui_name_T (self) :
        outer = self._outer
        return filtered_join \
            (ui_sep, (outer and outer._ui_name_T, self._attr.ui_name_T))
    # end def _ui_name_T

    def Inner (self, outer) :
        assert not self._outer
        return self.__class__ (self._attr, outer)
    # end def Inner

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

    def __str__ (self) :
        return "<%s.Q [Attr.Type.Querier %s]>" % \
            (self._q_name, self.__class__.__name__)
    # end def __str__

# end class _Type_

class Boolean (_Type_) :

    Table  = dict \
        ( EQ                 = Filter.Equal
        )

# end class Boolean

class Ckd (_Type_) :

    pass

# end class Ckd

class _Composite_ (_Type_) :

    @TFL.Meta.Once_Property
    def Children (self) :
        return tuple \
            (getattr (self, c.name) for c in self._inner_attrs)
    # end def Children

    def __getattr__ (self, name) :
        try :
            result = self.__super.__getattr__ (name)
        except AttributeError :
            head, _, tail = split_hst (name, ".")
            try :
                result = getattr (self._attr.E_Type, head).Q.Inner (self)
                setattr (self, head, result)
                if tail :
                    result = getattr (result, tail)
            except AttributeError :
                raise AttributeError (name)
        return result
    # end def __getattr__

# end class _Composite_

class Composite (_Composite_) :

    Table  = dict ()
    _Table = dict \
        ( AC                 = Filter.Composite_Auto_Complete
        , EQ                 = Filter.Composite_Equal
        , GE                 = Filter.Composite_Greater_Equal
        , GT                 = Filter.Composite_Greater_Than
        , LE                 = Filter.Composite_Less_Equal
        , LT                 = Filter.Composite_Less_Than
        , NE                 = Filter.Composite_Not_Equal
        )

    @property
    def _inner_attrs (self) :
        return self._attr.E_Type.user_attr
    # end def _inner_attrs

# end class Composite

class Date (_Type_) :

    Table  = dict \
        ( EQ                 = Filter.Date_Equal
        , GE                 = Filter.Date_Greater_Equal
        , GT                 = Filter.Date_Greater_Than
        , LE                 = Filter.Date_Less_Equal
        , LT                 = Filter.Date_Less_Than
        , NE                 = Filter.Date_Not_Equal
        )
    _Table = dict \
        ( AC                 = Filter.Date_Auto_Complete
        )

# end class Date

class Id_Entity (_Composite_) :

    deep   = True
    Table  = dict \
        ( EQ                 = Filter.Id_Entity_Equal
        , NE                 = Filter.Id_Entity_Not_Equal
        )
    _Table = dict \
        ( AC                 = Filter.Id_Entity_Auto_Complete
        , GE                 = Filter.Id_Entity_Greater_Equal
        , GT                 = Filter.Id_Entity_Greater_Than
        , LE                 = Filter.Id_Entity_Less_Equal
        , LT                 = Filter.Id_Entity_Less_Than
        )

    @property
    def _inner_attrs (self) :
        return self._attr.E_Type.primary
    # end def _inner_attrs

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

class E_Type_Attr_Query (TFL.Meta.Object) :
    """Query object for `E_Type` returning an essential attribute's `Q`"""

    def __init__ (self, E_Type) :
        self.E_Type = E_Type
    # end def __init__

    def __getattr__ (self, name) :
        head, _, tail = split_hst (name, ".")
        result = getattr (self.E_Type, head).Q
        if tail :
            result = getattr (Filter.Q, tail) (result)
        else :
            setattr (self, name, result)
        return result
    # end def __getattr__

# end class E_Type_Attr_Query

if __name__ != "__main__" :
    MOM.Attr._Export_Module ()
### __END__ MOM.Attr.Querier

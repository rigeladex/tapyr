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
#    MOM.Attr.Filter
#
# Purpose
#    Model query filters for MOM attributes
#
# Revision Dates
#    11-Nov-2011 (CT) Creation
#    12-Nov-2011 (CT) Move `AC` from `Table` to separate property
#    12-Nov-2011 (CT) Add `op_key` and use that as `Table` keys (`EQ`/`__eq__`)
#    14-Nov-2011 (CT) Change `Ckd.__getattr__` to support dotted attribute names
#    16-Nov-2011 (CT) Add translation markup (`_`)
#    17-Nov-2011 (CT) Add `NE` operator
#    17-Nov-2011 (CT) Add `_Type_` and `_M_Type_`
#    18-Nov-2011 (CT) Move `AC` into `_Table`; add `Op_Map`, `E_Type_Attr_Query`
#    20-Nov-2011 (CT) Add `Signatures` and `Sig_Key`
#    20-Nov-2011 (CT) Put `EQ`, `NE` into `Id_Entity.Table`
#    20-Nov-2011 (CT) Add `Children`
#    21-Nov-2011 (CT) Rename `_Type_.attr_name` to `._attr_name`
#    22-Nov-2011 (CT) Add `_Type_.as_json_cargo`
#    22-Nov-2011 (CT) Add `specialized`, streamline `as_json_cargo`
#    23-Nov-2011 (CT) Add `Base_Op_Table`, define `desc` for base operations
#     2-Dec-2011 (CT) Add `Boolean (_Type_)`
#     2-Dec-2011 (CT) Add `outer`, `Inner`, and `as_template_elem`
#     2-Dec-2011 (CT) Factor `_Composite_`, move parts of
#                     `_Type_.__getattr__` there
#    ��revision-date�����
#--

from   __future__  import unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._Attr

import _TFL._Meta.Object

from   _TFL.I18N             import _
from   _TFL.predicate        import filtered_join, split_hst
from   _TFL.Regexp           import Regexp, re

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL._Meta.Property
import _TFL.Filter

Q      = TFL.Attr_Query ()
id_sep = "__"
ui_sep = "/"

class _M_Filter_ (TFL.Meta.Object.__class__) :
    """Meta class for Filter classes."""

    Base_Op_Table = {}

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if not name.startswith ("_") :
            if not getattr (cls, "specialized", False) :
                cls.op_nam = name.lower ().replace ("_", "-")
            if cls.op_sym is None :
                cls.op_sym = cls.op_nam
            op_key = cls.op_fct
            if op_key.startswith ("__") :
                op_key = op_key.replace ("_", "").upper ()
            cls.op_key = op_key
            if op_key not in cls.Base_Op_Table :
                cls.Base_Op_Table [op_key] = cls
    # end def __init__

    def __str__ (cls) :
        return "<Attr.Filter %s [%s]>" % (cls.op_key, cls.op_sym)
    # end def __str__

# end class _M_Filter_

class _Filter_ (TFL.Meta.Object) :
    """Base class for attribute filters."""

    __metaclass__ = _M_Filter_

    op_fct        = None ### Must be redefined for subclasses or instances
    op_sym        = None ### Must be redefined for subclasses

    def __init__ (self, attr, cooker = None, name = None) :
        self.attr      = attr
        self.attr_name = name or self.attr.name
        self.cooker    = cooker
    # end def __init__

    def __call__ (self, value, prefix = None) :
        cooker = self.cooker
        if cooker is not None :
            try :
                value = cooker (value)
            except (ValueError, TypeError) :
                return None
        return self.query (value, prefix)
    # end def __call__

    def a_query (self, prefix = None) :
        name = self.attr_name
        if prefix :
            name = ".".join ((prefix, name))
        return getattr (Q, name)
    # end def a_query

    def query (self, value, prefix = None) :
        aq = self.a_query (prefix)
        q  = getattr (aq, self.op_fct)
        return q (value)
    # end def query

    def __str__ (self) :
        return "<Attr.%s %s.%s [%s]>" % \
            (self.__class__.__name__, self.attr_name, self.op_key, self.op_sym)
    # end def __str__

# end class _Filter_

class _Composite_ (_Filter_) :
    """Base class for composite-attribute filters."""

    specialized = True

    def __call__ (self, value, prefix = None) :
        name   = self.attr.name
        E_Type = self.attr.E_Type
        pf     = ".".join ((prefix, name)) if prefix else name
        def _gen () :
            for k, v in value.iteritems () :
                attr = getattr (E_Type, k)
                q    = getattr (attr.Q, self.op_key)
                r    = q (v, pf)
                if r is not None :
                    yield r
        qs = tuple (_gen ())
        if qs :
            return Q.AND (* qs)
    # end def __call__

# end class _Composite_

class _Date_ (_Filter_) :
    """Base class for date-attribute filters."""

    specialized = True

    pat = Regexp \
        ( r"^"
            r"(?P<year> [0-9]{4})"
            r"(?: [-/]"
              r"(?P<month> [0-9]{2})"
            r")?"
          r"[-/]?"
          r"$"
        , re.VERBOSE
        )

    def __call__ (self, value, prefix = None) :
        pat = self.pat
        if pat.match (value) :
            q    = self.a_query (prefix)
            args = (int (pat.year), )
            if pat.month :
                args = (int (pat.month, 10), ) + args
                q    = q.D.MONTH
            else :
                q    = q.D.YEAR
            return q (* args)
        else :
            return self.__super.__call__ (value, prefix)
    # end def __call__

# end class _Date_

class _Id_Entity_ (_Composite_) :
    """Base class for entity-attribute filters."""

    specialized = True

    def __call__ (self, value, prefix = None) :
        if isinstance (value, dict) :
            return self.__super.__call__ (value, prefix)
        else :
            return self.query (value, prefix)
    # end def __call__

# end class _Id_Entity_

class _String_ (_Filter_) :
    """Base class for string-attribute filters."""

    def query (self, value, prefix = None) :
        aq = self.a_query (prefix)
        q  = getattr (aq, self.op_fct) if value else aq.__eq__
        return q (value)
    # end def query

# end class _String_

class Contains (_String_) :
    """Attribute query filter for contains."""

    desc          = _ \
        ("Select entities where the attribute contains the specified value")
    op_fct        = _ ("CONTAINS")

# end class Contains

class Ends_With (_String_) :
    """Attribute query for ends-with."""

    desc          = _ \
        ( "Select entities where the attribute value ends "
          "with the specified value"
        )
    op_fct        = _ ("ENDSWITH")

# end class Ends_With

class Equal (_Filter_) :
    """Attribute query filter for equality."""

    desc          = _ \
        ("Select entities where the attribute is equal to the specified value")
    op_fct        = "__eq__"
    op_sym        = "=="

# end class Equal

class Greater_Equal (_Filter_) :
    """Attribute query filter for greater-equal."""

    desc          = _ \
        ( "Select entities where the attribute is greater than, "
          "or equal to, the specified value"
        )
    op_fct        = "__ge__"
    op_sym        = ">="

# end class Greater_Equal

class Greater_Than (_Filter_) :
    """Attribute query filter for greater-than."""

    desc          = _ \
        ( "Select entities where the attribute is greater than "
          "the specified value"
        )
    op_fct        = "__gt__"
    op_sym        = ">"

# end class Greater_Than

class Less_Equal (_Filter_) :
    """Attribute query filter for less-equal."""

    desc          = _ \
        ( "Select entities where the attribute is less than, "
          "or equal to, the specified value"
        )
    op_fct        = "__le__"
    op_sym        = "<="

# end class Less_Than

class Less_Than (_Filter_) :
    """Attribute query filter for less-than."""

    desc          = _ \
        ( "Select entities where the attribute is less than "
          "the specified value"
        )
    op_fct        = "__lt__"
    op_sym        = "<"

# end class Less_Than

class Not_Equal (_Filter_) :
    """Attribute query filter for in-equality."""

    desc          = _ \
        ( "Select entities where the attribute is not "
          "equal to the specified value"
        )
    op_fct        = "__ne__"
    op_sym        = "!="

# end class Not_Equal

class Starts_With (_String_) :
    """Attribute query for starts-with."""

    desc          = _ \
        ( "Select entities where the attribute value starts "
          "with the specified value"
        )
    op_fct        = _ ("STARTSWITH")

# end class Starts_With

class Auto_Complete (Equal) :
    """Attribute query filter for auto-completion."""

    op_sym        = "auto-complete"

# end class Auto_Complete

class Auto_Complete_S (Starts_With) :
    """String-Attribute query filter for auto-completion."""

    op_sym        = "auto-complete"

# end class Auto_Complete

class Composite_Auto_Complete (Auto_Complete, _Composite_) :
    """Composite-Attribute query filter for auto-completion."""

# end class Composite_Auto_Complete

class Composite_Equal (Equal, _Composite_) :
    """Composite-Attribute query filter for equality."""

# end class Composite_Equal

class Composite_Greater_Equal (Greater_Equal, _Composite_) :
    """Composite-Attribute query filter for greater-equal."""

# end class Composite_Greater_Equal

class Composite_Greater_Than (Greater_Than, _Composite_) :
    """Composite-Attribute query filter for greater-than."""

# end class Composite_Greater_Than

class Composite_Less_Equal (Less_Equal, _Composite_) :
    """Composite-Attribute query filter for less-than."""

# end class Composite_Less_Equal

class Composite_Less_Than (Less_Than, _Composite_) :
    """Composite-Attribute query filter for less-equal."""

# end class Composite_Less_Than

class Composite_Not_Equal (Not_Equal, _Composite_) :
    """Composite-Attribute query filter for in-equality."""

# end class Composite_Not_Equal

class Date_Auto_Complete (Auto_Complete, _Date_) :
    """Date-Attribute query filter for auto-completion."""

# end class Date_Auto_Complete

class Date_Equal (Equal, _Date_) :
    """Date-Attribute query filter for equality."""

# end class Date_Equal

class Date_Greater_Equal (Greater_Equal, _Date_) :
    """Date-Attribute query filter for greater-equal."""

# end class Date_Greater_Equal

class Date_Greater_Than (Greater_Than, _Date_) :
    """Date-Attribute query filter for greater-than."""

# end class Date_Greater_Than

class Date_Less_Equal (Less_Equal, _Date_) :
    """Date-Attribute query filter for less-than."""

# end class Date_Less_Equal

class Date_Less_Than (Less_Than, _Date_) :
    """Date-Attribute query filter for less-equal."""

# end class Date_Less_Than

class Date_Not_Equal (Not_Equal, _Date_) :
    """Date-Attribute query filter for in-equality."""

# end class Date_Not_Equal

class Id_Entity_Auto_Complete (Auto_Complete, _Id_Entity_) :
    """Id_Entity-Attribute query filter for auto-completion."""

# end class Id_Entity_Auto_Complete

class Id_Entity_Equal (Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for equality."""

# end class Id_Entity_Equal

class Id_Entity_Greater_Equal (Greater_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for greater-equal."""

# end class Id_Entity_Greater_Equal

class Id_Entity_Greater_Than (Greater_Than, _Id_Entity_) :
    """Id_Entity-Attribute query filter for greater-than."""

# end class Id_Entity_Greater_Than

class Id_Entity_Less_Equal (Less_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for less-than."""

# end class Id_Entity_Less_Equal

class Id_Entity_Less_Than (Less_Than, _Id_Entity_) :
    """Id_Entity-Attribute query filter for less-equal."""

# end class Id_Entity_Less_Than

class Id_Entity_Not_Equal (Not_Equal, _Id_Entity_) :
    """Id_Entity-Attribute query filter for in-equality."""

# end class Id_Entity_Not_Equal

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
        return "<Attr.Type.Filter %s %s>" % (cls.__name__, cls.Op_Keys)
    # end def __str__

# end class _M_Type_

class _Type_ (TFL.Meta.Object) :
    """Base class for Type classes.

       A Type class provides all filters for a set of Attr.Type classes.
    """

    __metaclass__ = _M_Type_

    Base_Op_Table = _Filter_.Base_Op_Table

    deep          = False
    Signatures    = {}

    ### `Table` maps the operations that can sensibly be selected in a UI
    Table   = dict \
        ( EQ                 = Equal
        , GE                 = Greater_Equal
        , GT                 = Greater_Than
        , LE                 = Less_Equal
        , LT                 = Less_Than
        , NE                 = Not_Equal
        )
    ### `_Table` maps additonal operations that don't make sense in a UI
    _Table  = dict \
        ( AC                 = Auto_Complete
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
            , attr     = self._attr
            , id       = self._id
            , q_name   = self._q_name
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
    def _id (self) :
        outer = self._outer
        return filtered_join (id_sep, (outer and outer._id, self._attr.name))
    # end def _id

    @TFL.Meta.Once_Property
    def _q_name (self) :
        outer = self._outer
        return filtered_join (".", (outer and outer._q_name, self._attr.name))
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
        attr = self._attr
        try :
            result_type = self.Op_Map [name]
        except KeyError :
            raise AttributeError (name)
        else :
            result = result_type (attr, self._cooker, self._attr_name)
            setattr (self, name, result)
            return result
    # end def __getattr__

    def __str__ (self) :
        return "<%s.Q [Attr.Type.Filter %s]>" % \
            (self._q_name, self.__class__.__name__)
    # end def __str__

# end class _Type_

class Boolean (_Type_) :

    Table  = dict \
        ( EQ                 = Equal
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
        ( AC                 = Composite_Auto_Complete
        , EQ                 = Composite_Equal
        , GE                 = Composite_Greater_Equal
        , GT                 = Composite_Greater_Than
        , LE                 = Composite_Less_Equal
        , LT                 = Composite_Less_Than
        , NE                 = Composite_Not_Equal
        )

    @property
    def _inner_attrs (self) :
        return self._attr.E_Type.user_attr
    # end def _inner_attrs

# end class Composite

class Date (_Type_) :

    Table  = dict \
        ( EQ                 = Date_Equal
        , GE                 = Date_Greater_Equal
        , GT                 = Date_Greater_Than
        , LE                 = Date_Less_Equal
        , LT                 = Date_Less_Than
        , NE                 = Date_Not_Equal
        )
    _Table = dict \
        ( AC                 = Date_Auto_Complete
        )

# end class Date

class Id_Entity (_Composite_) :

    deep   = True
    Table  = dict \
        ( EQ                 = Id_Entity_Equal
        , NE                 = Id_Entity_Not_Equal
        )
    _Table = dict \
        ( AC                 = Id_Entity_Auto_Complete
        , GE                 = Id_Entity_Greater_Equal
        , GT                 = Id_Entity_Greater_Than
        , LE                 = Id_Entity_Less_Equal
        , LT                 = Id_Entity_Less_Than
        )

    @property
    def _inner_attrs (self) :
        return self._attr.E_Type.primary
    # end def _inner_attrs

# end class Id_Entity

class String (_Type_) :

    Table  = dict \
        ( _Type_.Table
        , CONTAINS           = Contains
        , ENDSWITH           = Ends_With
        , STARTSWITH         = Starts_With
        )
    _Table = dict \
        ( AC                 = Auto_Complete_S
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
            result = getattr (Q, tail) (result)
        else :
            setattr (self, name, result)
        return result
    # end def __getattr__

# end class E_Type_Attr_Query

if __name__ != "__main__" :
    MOM.Attr._Export_Module ()
    MOM._Export ("Q")
### __END__ MOM.Attr.Filter

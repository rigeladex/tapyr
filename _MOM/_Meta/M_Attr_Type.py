# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer. All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.Meta.M_Attr_Type
#
# Purpose
#    Meta classes for MOM.Attr.Type classes
#
# Revision Dates
#    28-Sep-2009 (CT) Creation (factored from TOM.Meta.M_Attr_Type)
#    29-Sep-2009 (CT) `ckd_name` and `raw_name` added
#     7-Oct-2009 (CT) `M_Attr_Type_Named_Value` added
#     7-Oct-2009 (CT) `M_Attr_Type.__init__` changed to add `syntax`
#     9-Oct-2009 (CT) Handling of `default` and `raw_default` added
#     4-Nov-2009 (CT) `M_Attr_Type_Link_Role` changed to add `default_role_name`
#    27-Nov-2009 (CT) `M_Attr_Type_Link_Role` changed to remove `description`
#                     for classes without `role_type`
#    30-Dec-2009 (CT) `M_Attr_Type_Decimal` added
#    21-Jan-2010 (CT) `__init__` changed to take `default` from `dct`
#     2-Feb-2010 (CT) `M_Attr_Type_Named_Object` added
#     9-Feb-2010 (CT) `M_Attr_Type.__init__` changed to add `query`
#    22-Feb-2010 (CT) `M_Attr_Type_String` added (`ignore_case`)
#    12-Mar-2010 (CT) `M_Attr_Type_Typed_Collection` added
#    13-Mar-2010 (CT) `M_Attr_Type_Typed_Collection.Pickler` implemented
#    15-Mar-2010 (CT) `M_Attr_Type_Typed_Collection.Pickler` corrected
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL

import _MOM._Meta.M_Prop_Type

import _TFL._Meta.Once_Property

import pickle

class M_Attr_Type (MOM.Meta.M_Prop_Type) :
    """Meta class for MOM.Attr.Type classes."""

    count = 0

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        M_Attr_Type.count += 1
        if not name.startswith (("_A_", "A_")) :
            cls.ckd_name = "__%s"     % (cls.name, )
            cls.raw_name = "__raw_%s" % (cls.name, )
        if not hasattr (cls, "syntax") :
            if not name.startswith (("_A_", "A_Attr_Type")) :
                ### Adding `syntax` here (instead of as a class attribute in
                ### `A_Attr_Type`) allows descendent meta classes to define a
                ### meta property for `syntax` (which would be hidden by the
                ### class attribute)
                cls.syntax = ""
        raw_default = dct.get ("raw_default")
        default     = dct.get ("default")
        if raw_default :
            assert default is None, \
                ( "Can't specify both raw default and %s "
                  "and cooked default %s for %s"
                % (raw_default, default, cls)
                )
            if cls.symbolic_ref_pat.match (raw_default) :
                cls._symbolic_default = True
            ### Can't precompute `default` from `raw_default`
        elif default is not None :
            ### Precompute `raw_default` from `default`
            cls.raw_default = cls.as_string (default)
        query_fct = dct.get ("query_fct")
        query     = dct.get ("query")
        if query_fct :
            assert query is None, \
                ( "Can't specify both a `query_fct` and `query %s` for %s"
                % (query, cls)
                )
            cls.query = property (lambda s : s.query_fct ())
    # end def __init__

# end class M_Attr_Type

class M_Attr_Type_Decimal (M_Attr_Type) :
    """Meta class for MOM.Attr.A_Decimal classes."""

    def __init__ (cls, name, bases, dict) :
        cls.__m_super.__init__ (name, bases, dict)
        import decimal
        if "max_digits" in dict or "rounding" in dict :
            cls.D_Context = decimal.Context \
                (prec = cls.max_digits, rounding = cls.rounding)
        if "decimal_places" in dict :
            cls.D_Quant   = decimal.Decimal (10) ** -cls.decimal_places
    # end def __init__

# end class M_Attr_Type_Decimal

class M_Attr_Type_Link_Role (M_Attr_Type) :
    """Meta class for MOM.Attr.A_Link_Role classes."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.role_type :
            cls.default_role_name = drn = cls.role_type.type_base_name.lower ()
            if dct.get ("role_name") is None :
                cls.role_name = drn
        else :
            cls.description = None
    # end def __init__

# end class M_Attr_Type_Link_Role

class M_Attr_Type_Named_Value (M_Attr_Type) :
    """Meta class for MOM.Attr._A_Named_Value_ classes.

       `M_Attr_Type_Named_Value` adds Once_Property for `Elbat` (reverse
       mapping) for `Table` and for `syntax`, if these aren't defined by the
       descendent of `A_Named_Value`.
    """

    @TFL.Meta.Once_Property
    def Elbat (cls) :
        """Reversed mapping for `cls.Table`. Requires that `Table` is a
           unique mapping.
        """
        result = {None : ""}
        for i, v in cls.Table.iteritems () :
            if v in result :
                raise TypeError \
                    ( "Non-unique mapping for %s: "
                      "\n"
                      "    keys %r and %r both map to value '%s'."
                      "\n"
                      "Please specify reverse mapping `Elbat` manually."
                    % (cls, i, result [v], v)
                    )
            result [v] = i
        return result
    # end def Elbat

    @TFL.Meta.Once_Property
    def syntax (cls) :
        return \
            ( "The following string values are accepted as valid "
              "%s values: %s"
            % (cls.typ, ", ".join (sorted (cls.Table.iterkeys ())))
            )
    # end def syntax

# end class M_Attr_Type_Named_Value

class M_Attr_Type_Named_Object (M_Attr_Type_Named_Value) :
    """Meta class for MOM.Attr._A_Named_Object_ classes.

       `M_Attr_Type_Named_Object` adds `Type` to `cls.Pickler`, if any.
    """

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        Table = getattr (cls, "Table", None)
        if Table and cls.Pickler :
            max_length = max (len (k) for k in Table)
            cls.Pickler.Type = MOM.Attr._A_String_.New (max_length = max_length)
    # end def __init__

# end class M_Attr_Type_Named_Object

def _unicode_lower (s) :
    return unicode (s).lower ()
# end def _unicode_lower

class M_Attr_Type_String (M_Attr_Type) :
    """Meta class for MOM.Attr._A_String_ classes.

       `M_Attr_Type_String` interprets `ignore_case` and sets
       `needs_raw_value` and `simple_cooked` accordingly.
    """

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        cls.needs_raw_value   = bool (cls.ignore_case)
        if cls.ignore_case :
            cls.simple_cooked = staticmethod (_unicode_lower)
        else :
            cls.simple_cooked = unicode
    # end def __init__

# end class M_Attr_Type_String

class _M_Pickler_ (TFL.Meta.Object.__class__) :

    @TFL.Meta.Once_Property
    def Type (cls) :
        return MOM.Attr._A_Binary_String_
    # end def Type

# end class _M_Pickler_

class M_Attr_Type_Typed_Collection (M_Attr_Type) :
    """Meta class for MOM.Attr._A_Typed_Collection_ classes."""

    class _Pickler_ (TFL.Meta.Object) :

        __metaclass__ = _M_Pickler_

        @classmethod
        def as_cargo (cls, obj, attr_kind, attr_type, value) :
            if value is not None :
                cargo = cls._as_cargo (obj, attr_kind, attr_type, value)
                return pickle.dumps (cargo)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, obj, attr_kind, attr_type, cargo) :
            if cargo is not None :
                cargo = pickle.loads (cargo)
                return cls._from_cargo (obj, attr_kind, attr_type, cargo)
        # end def from_cargo

    # end class _Pickler_

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        assert not cls.needs_raw_value, \
            "Typed collection %s must not set `needs_raw_value`" % (cls, )
        C_Type = cls.C_Type
        if C_Type and not \
               (cls.Pickler or getattr (cls.Pickler, "Type", None) is C_Type) :
            if cls.C_Type.Pickler :
                _as_cargo   = cls._elements_as_cargo_p
                _from_cargo = cls._elements_from_cargo_p
            else :
                _as_cargo   = cls._elements_as_cargo_s
                _from_cargo = cls._elements_from_cargo_s
            cls.Pickler = cls._Pickler_.New \
                ( name_postfix = name
                , _as_cargo    = staticmethod (_as_cargo)
                , _from_cargo  = staticmethod (_from_cargo)
                )
    # end def __init__

    @staticmethod
    def _elements_as_cargo_p (obj, attr_kind, attr_type, value) :
        C_Type = attr_type.C_Type
        P      = C_Type.Pickler
        return list (P.as_cargo (obj, attr_kind, C_Type, v) for v in value)
    # end def _elements_as_cargo_p

    @staticmethod
    def _elements_from_cargo_p (obj, attr_kind, attr_type, cargo) :
        C_Type = attr_type.C_Type
        P      = C_Type.Pickler
        return list (P.from_cargo (obj, attr_kind, C_Type, c) for c in cargo)
    # end def _elements_from_cargo_p

    @staticmethod
    def _elements_as_cargo_s (obj, attr_kind, attr_type, value) :
        return value
    # end def _elements_as_cargo_s

    @staticmethod
    def _elements_from_cargo_s (obj, attr_kind, attr_type, cargo) :
        return cargo
    # end def _elements_from_cargo_s

# end class M_Attr_Type_Typed_Collection

class M_Attr_Type_Unit (M_Attr_Type) :
    """Meta class for MOM.Attr._A_Unit_ classes.

       `M_Attr_Type_Unit` defines the class attributes:

       .. attribute:: _default_unit

         The unit to be used if the user doesn't specify an explicit unit for
         the value of an attribute of this type.

       .. attribute:: syntax

         A description of the syntax for the attribute including the possible
         units and the default unit and the values of the optional class
         attributes `_syntax_spec_head` and `_syntax_spec_tail`, if defined
         in the class specifying the attribute type.
    """

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "_A_Unit_" :
            ud = getattr (cls, "_unit_dict", None)
            if ud :
                for n, v in ud.iteritems () :
                    if v == 1.0 :
                        du = n
                        setattr (cls, "_default_unit", du)
                        break
                else :
                    du = None
                if du and ud [du] == 1.0 :
                    syntax = "\n".join \
                        ( [s for s in
                              ( getattr (cls, "_syntax_spec_head", "")
                              , "The default unit is %s. If you specify "
                                "another unit, it must be separated from "
                                "the number by at least one space."
                                "\n"
                                "You can use the following units: %s."
                                % (du, ", ".join (sorted (ud.iterkeys ())))
                              , getattr (cls, "_syntax_spec_tail", "")
                              ) if s
                          ]
                        )
                    setattr (cls, "syntax", syntax)
                elif __debug__ :
                    print \
                        ( "Attribute type %s doesn't specify a `_default_unit`"
                          "with value 1.0 in `_unit_dict`"
                        ) % name
            elif __debug__ :
                if not ud :
                    print \
                        ( "Attribute type %s doesn't specify a _unit_dict"
                        ) % name
    # end def __init__

# end class M_Attr_Type_Unit

__doc__ = """
Class `MOM.Meta.M_Attr_Type`
============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: M_Attr_Type
.. autoclass:: M_Attr_Type_Decimal
.. autoclass:: M_Attr_Type_Link_Role
.. autoclass:: M_Attr_Type_Named_Value
.. autoclass:: M_Attr_Type_Named_Object
.. autoclass:: M_Attr_Type_String
.. autoclass:: M_Attr_Type_Unit

"""

if __name__ != "__main__" :
    MOM.Meta._Export ("*")
### __END__ MOM.Meta.M_Attr_Type

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2013 Mag. Christian Tanzer. All rights reserved
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
#     7-Oct-2009 (CT) `Named_Value` added
#     7-Oct-2009 (CT) `Root.__init__` changed to add `syntax`
#     9-Oct-2009 (CT) Handling of `default` and `raw_default` added
#     4-Nov-2009 (CT) `Link_Role` changed to add `default_role_name`
#    27-Nov-2009 (CT) `Link_Role` changed to remove `description`
#                     for classes without `role_type`
#    30-Dec-2009 (CT) `Decimal` added
#    21-Jan-2010 (CT) `__init__` changed to take `default` from `dct`
#     2-Feb-2010 (CT) `Named_Object` added
#     9-Feb-2010 (CT) `Root.__init__` changed to add `query`
#    22-Feb-2010 (CT) `String` added (`ignore_case`)
#    12-Mar-2010 (CT) `Typed_Collection` added
#    13-Mar-2010 (CT) `Typed_Collection.Pickler` implemented
#    15-Mar-2010 (CT) `Typed_Collection.Pickler` corrected
#    16-Mar-2010 (CT) `_Pickle_Mixin_` factored
#    23-Mar-2010 (CT) `assert` added to guard against `check` being a string
#    23-Mar-2010 (CT) `renameds` added
#     9-Apr-2010 (CT) Don't add attributes starting with `_` to `renameds`
#    19-Apr-2010 (CT) `_d_rank` added (sequence of attribute definition)
#    20-Apr-2010 (CT) `Named_Object` changed to create a derived
#                     `Pickler` to avoid aliasing
#    28-Apr-2010 (CT) s/_M_Pickler_/_M_Bin_Pickler_/
#     1-Jul-2010 (MG) `_M_Bin_Pickler.Pickle_Mixin` removed
#    26-Aug-2010 (CT) s/simple_cooked/cooked/
#     2-Sep-2010 (CT) Signatures of `Pickler.as_cargo` and `.from_cargo` changed
#     6-Sep-2010 (CT) `Typed_Collection` changed to use `tuple`
#                     and `R_Type` in `as_cargo` and `from_cargo`, respectively
#    14-Oct-2010 (CT) `symbolic_ref_pat` and `_symbolic_default` removed
#    24-Nov-2010 (CT) `Typed_Collection._elements_from_cargo_p`
#                     fixed (`C_Type`)
#    13-Dec-2011 (CT) Set `raw_name` to `ckd_name` unless `needs_raw_value`
#    16-Dec-2011 (CT) Set `raw_name` to `name` unless `needs_raw_value`
#                     (`name` because that will trigger `computed` if necessary)
#     8-Sep-2012 (CT) Add `Enum`
#     8-Sep-2012 (CT) Add `_unicode_ignore_case`
#    19-Sep-2012 (CT) Add `force_role_name` to `Link_Role`
#    13-Nov-2012 (CT) Add support for redefined `cooked` to `String`
#    20-Nov-2012 (CT) Change `Unit` to allow manual `_default_unit`
#    20-Nov-2012 (CT) Change `Unit` to use inherited `_default_unit`
#     5-Jun-2013 (CT) DRY names: export module, remove M_Attr_Type_ prefix
#     5-Jun-2013 (CT) Add `Surrogate`
#     7-Jun-2013 (CT) Add guards against redefinition to `Surrogate`
#    12-Jun-2013 (CT) Add and use `is_partial_p`
#    ««revision-date»»···
#--

from   _MOM                import MOM
from   _TFL                import TFL
from   _TFL.pyk            import pyk

import _MOM._Meta.M_Prop_Type

import _TFL._Meta.Once_Property

class Root (MOM.Meta.M_Prop_Type) :
    """Meta class for MOM.Attr.Type classes."""

    count = 0

    def __new__ (meta, name, bases, dct) :
        dct.setdefault \
            ( "is_partial_p"
            , (   name.startswith (("_A_", "A_"))
              or (name.startswith ("_") and name.endswith ("_"))
              )
            )
        return super (Root, meta).__new__ (meta, name, bases, dct)
    # end def __new__

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        Root.count += 1
        cls._d_rank = Root.count
        if not cls.is_partial_p :
            cls.ckd_name = "__%s" % (cls.name, )
            cls.raw_name = \
                (    "__raw_%s" % (cls.name, ) if cls.needs_raw_value
                else cls.name ### do not want `ckd_name` here (`computed`...)
                )
            cls.renameds = set ()
            for b in bases :
                bn = getattr (b, "ckd_name", None)
                if bn and (not b.name.startswith ("_")) and cls.name != b.name :
                    cls.renameds.add (b.name)
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
        check = dct.get ("check")
        if check is not None :
            assert not isinstance (check, basestring), \
                ( "%s.check needs to be a tuple, not a string: %r"
                % (name, check)
                )
    # end def __init__

# end class Root

class Decimal (Root) :
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

# end class Decimal

class Enum (Root) :
    """Meta class for MOM.Attr.A_Enum."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.C_Type is not None :
            cls.P_Type = cls.C_Type.P_Type
    # end def __init__

# end class Enum

class Link_Role (Root) :
    """Meta class for MOM.Attr.A_Link_Role classes."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if cls.role_type :
            cls.default_role_name = drn = cls.role_type.type_base_name.lower ()
            if dct.get ("role_name") is None :
                cls.role_name = cls.force_role_name or drn
        else :
            cls.description = None
    # end def __init__

# end class Link_Role

class Named_Value (Root) :
    """Meta class for MOM.Attr._A_Named_Value_ classes.

       `Named_Value` adds Once_Property for `Elbat` (reverse
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

# end class Named_Value

class Named_Object (Named_Value) :
    """Meta class for MOM.Attr._A_Named_Object_ classes.

       `Named_Object` adds `Type` to `cls.Pickler`, if any.
    """

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        Table = getattr (cls, "Table", None)
        if Table and cls.Pickler :
            max_length = max (len (k) for k in Table)
            if max_length != cls.Pickler.Type.max_length :
                cls.Pickler = cls.Pickler.New \
                    (Type = MOM.Attr._A_String_.New (max_length = max_length))
    # end def __init__

# end class Named_Object

def _unicode_lower (s) :
    return unicode (s).lower ()
# end def _unicode_lower

def _unicode_upper (s) :
    return unicode (s).upper ()
# end def _unicode_upper

_unicode_ignore_case = dict \
    ( { False        : unicode
      , True         : _unicode_lower
      }
    , lower          = _unicode_lower
    , upper          = _unicode_upper
    )

class String (Root) :
    """Meta class for MOM.Attr._A_String_ classes.

       `String` interprets `ignore_case` and sets
       `needs_raw_value` and `cooked` accordingly.
    """

    def __init__ (cls, name, bases, dct) :
        cls.needs_raw_value = bool (cls.ignore_case)
        cls.__m_super.__init__ (name, bases, dct)
        cooked = s_cooked = _unicode_ignore_case [cls.ignore_case]
        if "cooked" in dct :
            c_name = cls._m_mangled_attr_name ("cooked")
            setattr (cls, c_name, dct ["cooked"])
            def cooked (soc, value) :
                if value is not None :
                    r_cooked = getattr (soc, c_name)
                    return s_cooked (r_cooked (value))
            decorator = TFL.Meta.Class_and_Instance_Method
        else :
            decorator = staticmethod
        cls.cooked = decorator (cooked)
    # end def __init__

# end class String

class Surrogate (Root) :
    """Meta class for MOM.Attr.A_Surrogate."""

    max_surrogate_id = 0

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name != "A_Surrogate" :
            if cls.surrogate_id :
                raise TypeError \
                    ( "Cannot redefine surrogate attribute %s"
                      "\n    bases: %s"
                      "\n    %s"
                    % ( cls, bases
                      , "\n    ".join
                          ( "%s : %s"
                          % (k, v) for k, v in sorted (pyk.iteritems (dct))
                          )
                      )
                    )
            elif cls.dyn_doc_p :
                raise TypeError \
                    ( "Cannot define surrogate attribute %s with dynamic doc"
                      "\n    bases: %s"
                      "\n    %s"
                    % ( cls, bases
                      , "\n    ".join
                          ( "%s : %s"
                          % (k, v) for k, v in sorted (pyk.iteritems (dct))
                          )
                      )
                    )
            else :
                cls.__class__.max_surrogate_id += 1
                cls.surrogate_id = cls.max_surrogate_id
    # end def __init__

# end class Surrogate

class _M_Bin_Pickler_ (TFL.Meta.Object.__class__) :

    @TFL.Meta.Once_Property
    def Type (cls) :
        return MOM.Attr._A_Binary_String_
    # end def Type

# end class _M_Bin_Pickler_

class Typed_Collection (Root) :
    """Meta class for MOM.Attr._A_Typed_Collection_ classes."""

    class _Pickler_ (TFL.Meta.Object) :

        __metaclass__ = _M_Bin_Pickler_

        @classmethod
        def as_cargo (cls, attr_kind, attr_type, value) :
            if value is not None :
                return cls._as_cargo (attr_kind, attr_type, value)
        # end def as_cargo

        @classmethod
        def from_cargo (cls, scope, attr_kind, attr_type, cargo) :
            if cargo is not None :
                return cls._from_cargo (scope, attr_kind, attr_type, cargo)
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
    def _elements_as_cargo_p (attr_kind, attr_type, value) :
        C_Type = attr_type.C_Type
        P      = C_Type.Pickler
        return tuple (P.as_cargo (attr_kind, C_Type, v) for v in value)
    # end def _elements_as_cargo_p

    @staticmethod
    def _elements_from_cargo_p (scope, attr_kind, attr_type, cargo) :
        R_Type = attr_type.R_Type
        C_Type = attr_type.C_Type
        fpc    = C_Type.Pickler.from_cargo
        return R_Type (fpc (scope, attr_kind, C_Type, c) for c in cargo)
    # end def _elements_from_cargo_p

    @staticmethod
    def _elements_as_cargo_s (attr_kind, attr_type, value) :
        if value is not None :
            return tuple (value)
    # end def _elements_as_cargo_s

    @staticmethod
    def _elements_from_cargo_s (scope, attr_kind, attr_type, cargo) :
        if cargo is not None :
            return attr_type.R_Type (cargo)
    # end def _elements_from_cargo_s

# end class Typed_Collection

class Unit (Root) :
    """Meta class for MOM.Attr._A_Unit_ classes.

       `Unit` defines the class attributes:

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
            ud = dct.get ("_unit_dict")
            if ud :
                du = dct.get ("_default_unit")
                if du is None :
                    for n, v in ud.iteritems () :
                        if v == 1.0 :
                            du = n
                            setattr (cls, "_default_unit", du)
                            break
                if du and ud [du] == 1.0 :
                    syntax = "\n".join \
                        ( s for s in
                            ( getattr (cls, "_syntax_spec_head", "")
                            , "The default unit is %s. If you specify "
                              "another unit, it must be separated from "
                              "the number by at least one space."
                              "\n"
                              "You can use the following units: %s."
                              % (du, ", ".join (sorted (ud.iterkeys ())))
                            , getattr (cls, "_syntax_spec_tail", "")
                            )
                        if s
                        )
                    setattr (cls, "syntax", syntax)
                elif __debug__ :
                    print \
                        ( "Attribute type %s doesn't specify a `_default_unit`"
                          "with value 1.0 in `_unit_dict`"
                        ) % name
            elif __debug__ :
                if not getattr (cls, "_unit_dict", None) :
                    print \
                        ( "Attribute type %s doesn't specify a _unit_dict"
                        ) % name
    # end def __init__

# end class Unit

__doc__ = """
Module `MOM.Meta.M_Attr_Type`
==============================

.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

.. autoclass:: Root
.. autoclass:: Decimal
.. autoclass:: Link_Role
.. autoclass:: Named_Value
.. autoclass:: Named_Object
.. autoclass:: String
.. autoclass:: Unit

"""

if __name__ != "__main__" :
    MOM.Meta._Export_Module ()
### __END__ MOM.Meta.M_Attr_Type

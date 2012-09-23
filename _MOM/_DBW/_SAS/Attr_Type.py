# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Martin Glueck. All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.SAS.Attr_Type
#
# Purpose
#    Attribute type extension for the SAS backend
#
# Revision Dates
#    11-Feb-2010 (MG) Creation (based on SA.Attr_Type)
#    16-Feb-2010 (MG) `_sa_columns_named_object` fixed
#    18-Feb-2010 (MG) `_sa_columns_composite`: only add `hash_sig` attributes
#                     of primay composites to the `unique` list
#    25-Feb-2010 (MG) `_sa_columns_role_eb` change to `_sa_columns_a_object`
#    25-Feb-2010 (MG) `_sa_col_name` functions moved in here from `Attr_Kind`
#    25-Feb-2010 (MG) `_sa_columns_named_object` fixed
#     5-Mar-2010 (CT) Pass `convert_unicode` to `types.String`
#    10-Mar-2010 (MG) `_sa_columns_named_value` created, types for `A_Time`
#                     added
#    13-Mar-2010 (CT) `_sa_columns_simple` changed to handle `Pickler`, if any
#                     (and `Pickler` removed from `_sa_columns_named_value`)
#    13-Mar-2010 (CT) `Attr.A_Int_List, Attr.A_Date_List` replaced by
#                     `_A_Binary_String_` (`*_List` got a Pickler)
#    19-Mar-2010 (CT) Use `types.Binary` instead of `types.String` for
#                     `_A_Binary_String_`
#    23-Mar-2010 (MG) `owner_etype` added and used in `_sa_columns_composite`
#    21-Apr-2010 (CT) s/types.Binary/types.LargeBinary/
#    12-May-2010 (MG) `pid` is now the primary key of SA tables
#    12-May-2010 (MG) `_sa_string` use a `Text` type if no `max_length` is
#                     given to work under MySQL as well
#    21-Jun-2010 (CT) `_sa_file_name` added
#     1-Jul-2010 (MG) `SAS_PC_Transform` added
#     6-Sep-2010 (MG) Changes to allow link's to entities which are not
#                     relevant
#     6-Sep-2010 (CT) `Attr._A_Composite_Collection_` removed
#    24-Feb-2011 (CT) s/A_Object/A_Entity/
#    22-Jul-2011 (MG) `Case_Sensitive_String` added to support MySQL
#    25-Jul-2011 (MG) `SAS_Column_Class` added to support custom column
#                     classes
#    22-Sep-2011 (CT) s/A_Entity/A_Id_Entity/
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#    14-May-2012 (CT) Replace concrete `_sa_type` implementations for
#                     `A_Boolean`, `A_Date`, `A_Date_Time`, `A_Float`,
#                     `A_Int`, and `A_Time` by generic `_sa_type` for
#                     `A_Attr_Type`
#    10-Aug-2012 (MG) Add support of Sall/BigInteger types
#     8-Sep-2012 (CT) Change `_sa_type_generic` to allow `unicode`
#    23-Sep-2012 (RS) Fix integer type selection
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.Decorator
from   _MOM               import MOM
import _MOM._Attr.Type
import _MOM._Attr
import  cPickle
from   _MOM._DBW._SAS.Date_Column import Date_Column

from sqlalchemy     import types, schema
from sqlalchemy.sql import extract, expression

import datetime
import math

_sa_type_map = \
    { bool              : types.Boolean
    , datetime.date     : types.Date
    , datetime.datetime : types.DateTime
    , datetime.time     : types.Time
    , float             : types.Float
    , int               : types.Integer
    }

Attr = MOM.Attr

Attr.A_Attr_Type.SAS_Column_Class = schema.Column
Attr.A_Date     .SAS_Column_Class = Date_Column

def Add_Classmedthod  (name, * classes) :
    """Adds decorated function/class to `classes` using `name`.
    """
    def decorator (x) :
        for cls in classes :
            setattr (cls, name, classmethod (x))
        return x
    return decorator
# end def Add_Classmedthod

@TFL.Add_To_Class ("_sa_column_name", Attr.A_Attr_Type)
def _sa_normal_attr (self) :
    return self.name
# end def _sa_normal_attr

@TFL.Add_To_Class ("_sa_column_name", Attr._A_Id_Entity_)
def _sa_object (self) :
    return "%s_pid" % (self.name, )
# end def _sa_object

@Add_Classmedthod ("_sa_columns", Attr.A_Attr_Type)
def _sa_columns_simple (cls, attr, kind, unique, owner_etype, ** kw) :
    Pickler      = attr.Pickler
    Type         = getattr (Pickler, "Type", attr)
    sa_type      = Type._sa_type (Type, kind)
    col          = cls.SAS_Column_Class (attr._sa_col_name, sa_type, ** kw)
    col.mom_kind = kind
    return (col, )
# end def _sa_columns_simple

@Add_Classmedthod ("_sa_columns", Attr._A_Id_Entity_)
def _sa_columns_a_object (cls, attr, kind, unique, owner_etype, ** kw) :
    col = schema.Column \
        ( attr._sa_col_name
        , types.Integer ()
#        , schema.ForeignKey
#            ( "%s.%s"
#            % (attr.Class._sa_table.name, attr.Class._sa_pk_name)
#            )
        )
    col.mom_kind = kind
    return (col, )
# end def _sa_columns_a_object

@Add_Classmedthod ("_sa_columns", Attr._A_Named_Value_)
def _sa_columns_named_value (cls, attr, kind, unique, owner_etype, ** kw) :
    Type = attr.C_Type
    if Type :
        col = schema.Column \
            (attr._sa_col_name, Type._sa_type (Type, kind), ** kw)
        col.mom_kind = kind
        return (col, )
    return _sa_columns_simple (cls, attr, kind, unique, owner_etype, ** kw)
# end def _sa_columns_named_value

@Add_Classmedthod ("_sa_columns", Attr._A_Composite_)
def _sa_columns_composite (cls, attr, kind, unique, owner_etype, ** kw) :
    e_type   = kind.P_Type
    bases    = e_type.__bases__
    Manager  = MOM.DBW.SAS.Manager
    db_attrs = Manager._attr_dicts (e_type, bases)
    prefix   = "__%s_" % (attr.name, )
    unique_attrs          = set ()
    if kind.is_primary :
        unique_attrs      = set (k.attr.name for k in e_type.hash_sig)
    columns  = Manager._setup_columns \
        (e_type, db_attrs, bases, unique, prefix, unique_attrs)
    if not hasattr (e_type, "_sa_save_attrs") :
        e_type._sa_save_attrs = {}
    e_type._sa_save_attrs [owner_etype.type_name, kind.attr.name] = \
        db_attrs, columns
    kind._sa_prefix = prefix
    return columns
# end def _sa_columns_composite

class Case_Sensitive_String (types.TypeDecorator) :
    """A string column which is case sensitive (which is not the default for
       MySQL)
    """

    impl = types.String

    def load_dialect_impl (self, dialect) :
        self.impl.binary = True
        return super (Case_Sensitive_String, self).load_dialect_impl (dialect)
    # end def load_dialect_impl(dialect

# end class Case_Sensitive_String

@Add_Classmedthod ("_sa_type", Attr.A_Attr_Type)
def _sa_type_generic (cls, attr, kind, ** kw) :
    P_Type = attr.P_Type
    if P_Type is unicode :
        return _sa_string (cls, attr, kind, ** kw)
    else :
        try :
            T = _sa_type_map [P_Type]
        except KeyError :
            if P_Type is None :
                msg = \
                    ( "Attribute %s needs either a `Pickler` or "
                      "a `P_Type` definition"
                    % (kind, )
                    )
            else :
                msg = \
                    ( "`P_Type` %s is not supported for `%s`; use one of `%s`"
                      " or extend MOM.DBW.SAS.Attr_Type"
                    % (P_Type, kind, sorted (_sa_type_map))
                    )
            raise AttributeError (msg)
        else :
            return T ()
# end def _sa_type_generic

int_map = \
 ( (-0x8000,             0x7FFF,             types.SmallInteger)
 , (-0x80000000,         0x7FFFFFFF,         types.Integer)
 , (-0x8000000000000000, 0x7FFFFFFFFFFFFFFF, types.BigInteger)
 )
@Add_Classmedthod ("_sa_type", Attr.A_Int)
def _sa_type_int (cls, attr, kind, ** kw) :
    result    = None
    max_value = cls.max_value or  0x7FFFFFFF
    min_value = cls.min_value or -0x80000000
    for tmin, tmax, result in int_map :
        if (tmin <= min_value) and (max_value <= tmax) :
            break
    if result is None :
        raise TypeError \
            ( "Cannot map integer type with max-value %d and min-value %d "
              "to a database value"
            % (max_value, min_value)
            )
    return result
# end def _sa_type_int

@Add_Classmedthod ("_sa_type", Attr.A_Decimal)
def _sa_numeric (cls, attr, kind, ** kw) :
    return types.Numeric (attr.max_digits, attr.decimal_places)
# end def _sa_numeric

@Add_Classmedthod ("_sa_type", Attr._A_String_Base_)
def _sa_string (cls, attr, kind, ** kw) :
    length = getattr (attr, "max_length", None)
    if length :
        return Case_Sensitive_String (length, convert_unicode = True)
    return types.Text (convert_unicode = True)
# end def _sa_string

@Add_Classmedthod ("_sa_type", Attr._A_Filename_)
def _sa_file_name (cls, attr, kind, ** kw) :
    length = getattr (attr, "max_length", None)
    if length :
        return Case_Sensitive_String (length, convert_unicode = False)
    return types.Text (convert_unicode = False)
# end def _sa_file_name

@Add_Classmedthod ("_sa_type", Attr._A_Binary_String_)
def _sa_blob (cls, attr, kind, ** kw) :
    return types.LargeBinary (getattr (attr, "max_length", None))
# end def _sa_blob

class Python_Pickle_Transform (object) :
    """Pickle the pickle cargo of the object model and store it as string."""

    @classmethod
    def dump (cls, pickle_cargo) :
        assert len (pickle_cargo) == 1
        return (cPickle.dumps (pickle_cargo [0], cPickle.HIGHEST_PROTOCOL), )
    # end def dump

    @classmethod
    def load (cls, pickle_string) :
        assert len (pickle_string) == 1
        return (cPickle.loads (pickle_string [0]), )
    # end def load

# end class Python_Pickle_Transform

Attr.A_Attr_Type.             SAS_PC_Transform = None
Attr._A_Typed_Collection_.    SAS_PC_Transform = Python_Pickle_Transform

### __END__ MOM.DBW.SAS.Type

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck. All rights reserved
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
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.Decorator
from   _MOM               import MOM
import _MOM._Attr.Type
import _MOM._Attr

Attr = MOM.Attr

from sqlalchemy     import types, schema

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
def _sa_normal_attr(self) :
    return self.name
# end def _sa_normal_attr

@TFL.Add_To_Class ("_sa_column_name", Attr._A_Object_)
def _sa_object (self) :
    return "%s_id" % (self.name, )
# end def _sa_object

@Add_Classmedthod ("_sa_columns", Attr.A_Attr_Type)
def _sa_columns_simple (cls, attr, kind, unique, ** kw) :
    col = schema.Column (attr._sa_col_name, attr._sa_type (attr, kind), ** kw)
    col.mom_kind = kind
    return (col, )
# end def _sa_columns_simple

@Add_Classmedthod ("_sa_columns", Attr._A_Object_)
def _sa_columns_a_object (cls, attr, kind, unique, ** kw) :
    col = schema.Column \
        ( attr._sa_col_name
        , types.Integer ()
        , schema.ForeignKey
            ( "%s.%s"
            % (attr.Class._sa_table.name, attr.Class._sa_pk_name)
            )
        )
    col.mom_kind = kind
    return (col, )
# end def _sa_columns_a_object

@Add_Classmedthod ("_sa_columns", Attr._A_Named_Value_)
def _sa_columns_named_value (cls, attr, kind, unique, ** kw) :
    Pickler  = attr.Pickler
    Type     = getattr (Pickler, "Type", attr.C_Type)
    if Type :
        col      = schema.Column \
            (attr._sa_col_name, Type._sa_type (Type, kind), ** kw)
        col.mom_kind = kind
        return (col, )
    return _sa_columns_simple (cls, attr, kind, unique, ** kw)
# end def _sa_columns_named_value

@Add_Classmedthod ("_sa_columns", Attr._A_Composite_)
def _sa_columns_composite (cls, attr, kind, unique, ** kw) :
    e_type                = kind.C_Type
    bases                 = e_type.__bases__
    Manager               = MOM.DBW.SAS.Manager
    db_attrs, role_attrs  = Manager._attr_dicts    (kind.C_Type, bases)
    prefix                = "__%s_" % (attr.name, )
    assert not role_attrs
    unique_attrs          = set ()
    if kind.is_primary :
        unique_attrs      = set (k.attr.name for k in e_type.hash_sig)
    columns  = Manager._setup_columns \
        (e_type, db_attrs, bases, unique, prefix, unique_attrs)
    e_type._sa_save_attrs = db_attrs, columns, prefix
    return columns
# end def _sa_columns_composite

@Add_Classmedthod ("_sa_type", Attr.A_Boolean)
def _sa_bool (cls, attr, kind, ** kw)      : return types.Boolean   ()
@Add_Classmedthod ("_sa_type", Attr.A_Date)
def _sa_date (cls, attr, kind, ** kw)      : return types.Date      ()
@Add_Classmedthod ("_sa_type", Attr.A_Date_Time)
def _sa_date_time (cls, attr, kind, ** kw) : return types.DateTime  ()
@Add_Classmedthod ("_sa_type", Attr.A_Time)
def _sa_time (cls, attr, kind, ** kw)      : return types.Time      ()
@Add_Classmedthod ("_sa_type", Attr.A_Float)
def _sa_float (cls, attr, kind, ** kw)     : return types.Float     ()
@Add_Classmedthod ("_sa_type", Attr.A_Int)
def _sa_int (cls, attr, kind, ** kw)       : return types.Integer   ()

@Add_Classmedthod ("_sa_type", Attr.A_Decimal)
def _sa_numeric (cls, attr, kind, ** kw) :
    return types.Numeric (attr.max_digits, attr.decimal_places)
# end def _sa_numeric

@Add_Classmedthod ("_sa_type", Attr._A_String_Base_)
def _sa_string (cls, attr, kind, ** kw) :
    return types.String \
        ( getattr (attr, "max_length", None)
        , convert_unicode = True
        )
# end def _sa_string

@Add_Classmedthod ("_sa_type", Attr.A_Int_List, Attr.A_Date_List)
def _sa_blob (cls, attr, kind, ** kw) :
    return types.String ()
# end def _sa_blob

### __END__ MOM.DBW.SAS.Type

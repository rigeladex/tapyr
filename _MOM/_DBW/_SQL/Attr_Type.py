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
#    MOM.DBW.SQL.Attr_Type
#
# Purpose
#    Attribute type extension for the SQL backend
#
# Revision Dates
#     11-Feb-2010 (MG) Creation (based on SA.Attr_Type)
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

@Add_Classmedthod ("_sa_columns", Attr.A_Attr_Type)
def _sa_columns_simple (cls, attr, kind, unique, ** kw) :
    col = schema.Column (attr._sa_col_name, attr._sa_type (attr, kind), ** kw)
    col.mom_kind = kind
    return (col, )
# end def _sa_columns_simple

@Add_Classmedthod ("_sa_columns", Attr.A_Link_Role_EB)
def _sa_columns_role_eb (cls, attr, kind, unique, ** kw) :
    col = schema.Column \
        ( attr._sa_col_name
        , types.Integer ()
        , schema.ForeignKey
            ( "%s.%s"
            % (attr.role_type._sa_table.name, attr.role_type._sa_pk_name)
            )
        )
    col.mom_kind = kind
    return (col, )
# end def _sa_columns_role_eb

Type_Decorator_Cache = {}

@Add_Classmedthod ("_sa_columns", Attr._A_Named_Object_)
def _sa_columns_named_object (cls, attr, kind, unique, ** kw) :
    raise NotImplementedError
    key = attr.__class__.__bases__
    if key not in Type_Decorator_Cache :
        Pickler  = attr.Pickler
        Type     = Pickler.Type
        SQL_TD    = types.TypeDecorator
        sa_type  = SQL_TD.__class__ \
            ( "%s_S_TD" % (key [0].__name__)
            , (SQL_TD, )
            , dict
                ( impl                 = Type._sa_type (Type, kind).__class__
                , process_bind_param   =
                    lambda S, value, dict : Pickler.as_cargo   (attr, value)
                , process_result_value =
                    lambda S, value, dict : Pickler.from_cargo (attr, value)
                )
            )
        Type_Decorator_Cache [key] = sa_type
    return ( schema.Column \
               ( attr._sa_col_name
               , Type_Decorator_Cache [key] (getattr (attr, "max_length", None))
               , ** kw
               )
           ,
           )
# end def _sa_columns_named_object

@Add_Classmedthod ("_sa_columns", Attr._A_Composite_)
def _sa_columns_composite (cls, attr, kind, unique, ** kw) :
    e_type                = kind.C_Type
    bases                 = e_type.__bases__
    Manager               = MOM.DBW.SQL.Manager
    db_attrs, role_attrs  = Manager._attr_dicts    (kind.C_Type, bases)
    assert not role_attrs
    columns  = Manager._setup_columns \
        ( e_type, db_attrs, bases, unique, attr.name
        , set (k.attr.name for k in e_type.hash_sig)
        )
    e_type._sa_save_attrs = db_attrs, columns
    return columns
# end def _sa_columns_composite

@Add_Classmedthod ("_sa_type", Attr.A_Boolean)
def _sa_bool (cls, attr, kind, ** kw)      : return types.Boolean   ()
@Add_Classmedthod ("_sa_type", Attr.A_Date)
def _sa_date (cls, attr, kind, ** kw)      : return types.Date      ()
@Add_Classmedthod ("_sa_type", Attr.A_Date_Time)
def _sa_date_time (cls, attr, kind, ** kw) : return types.DateTime  ()
@Add_Classmedthod ("_sa_type", Attr.A_Float)
def _sa_float (cls, attr, kind, ** kw) :     return types.Float     ()
@Add_Classmedthod ("_sa_type", Attr.A_Int)
def _sa_int (cls, attr, kind, ** kw) :       return types.Integer   ()

@Add_Classmedthod ("_sa_type", Attr.A_Decimal)
def _sa_numeric (cls, attr, kind, ** kw) :
    return types.Numeric (attr.max_digits, attr.decimal_places)
# end def _sa_numeric

@Add_Classmedthod ("_sa_type", Attr._A_String_)
def _sa_string (cls, attr, kind, ** kw) :
    return types.String (getattr (attr, "max_length", None))
# end def _sa_string

### __END__ MOM.DBW.SQL.Type

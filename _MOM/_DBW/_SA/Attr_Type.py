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
#    MOM.DBW.SA.Type
#
# Purpose
#    Implement composite sort-key for list of sort criteria
#
# Revision Dates
#     2009-Oct-19 (MG) Creation
#     4-Nov-2009 (MG) Use `TFL.Add_To_Class`
#    31-Dec-2009 (MG) `_sa_numeric` added
#    30-Jan-2010 (MG) `_sa_date` added
#     6-Feb-2010 (MG) `_sa_date_time` and `_sa_named_object` added
#     6-Feb-2010 (MG) `_sa_column` function are now class methods and the
#                     attr instance is passed as parameter
#     6-Feb-2010 (MG) Column generation and type definition splitted
#     7-Feb-2010 (MG) `_sa_columns_composite` added
#    10-Feb-2010 (MG) `unique` parameter added to `_sa_columns` functions
#    10-Feb-2010 (MG) `_sa_columns_composite` pass list of unique attrs to
#                     `_setup_columns`
#    ««revision-date»»···
#--

from   _TFL               import TFL
import _TFL.Decorator
from   _MOM               import MOM
import _MOM._Attr.Type
import _MOM._Attr

Attr = MOM.Attr

from sqlalchemy     import types, schema # Table, Column, Integer, String, Boolean, MetaData, ForeignKey

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
    return \
        ( schema.Column (attr._sa_col_name, attr._sa_type (attr, kind), ** kw)
        ,
        )
# end def _sa_columns_simple

@Add_Classmedthod ("_sa_columns", Attr.A_Link_Role_EB)
def _sa_columns_role_eb (cls, attr, kind, unique, ** kw) :
    return ( schema.Column
               ( attr._sa_col_name
               , types.Integer ()
               , schema.ForeignKey
                   ( "%s.%s"
                   % (attr.role_type._sa_table.name, attr.role_type._sa_pk_name)
                   )
               )
           ,
           )
# end def _sa_columns_role_eb

Type_Decorator_Cache = {}

@Add_Classmedthod ("_sa_columns", Attr._A_Named_Object_)
def _sa_columns_named_object (cls, attr, kind, unique, ** kw) :
    key = attr.__class__.__bases__
    if key not in Type_Decorator_Cache :
        Pickler  = attr.Pickler
        Type     = Pickler.Type
        SA_TD    = types.TypeDecorator
        sa_type  = SA_TD.__class__ \
            ( "%s_S_TD" % (key [0].__name__)
            , (SA_TD, )
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
    Manager               = MOM.DBW.SA.Manager
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

### __END__ MOM.DBW.SA.Type

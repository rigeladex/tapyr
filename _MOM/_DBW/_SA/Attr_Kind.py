# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.SA.Attr_Kind
#
# Purpose
#    Add information needed by the SQAlchemy database backend to the
#    attribute kinds
#
# Revision Dates
#    20-Oct-2009 (MG) Creation
#    27-Oct-2009 (MG) Removed `unique` constraint because we actually need a
#                     unique-together which is not possible at a column level
#     4-Nov-2009 (MG) Use `TFL.Add_To_Class`
#     8-Feb-2010 (MG) Generation of mapper properties moved in here
#     8-Feb-2010 (MG) `_sa_query_prop` added
#     8-Feb-2010 (MG) `_sa_composite_comperator_class` and friends added
#    10-Feb-2010 (MG) Don't use `orm.synonym` but instead attach a `SA.Query`
#                     object to all `e_type`s
#    ««revision-date»»···
#--

from   _MOM             import MOM
import _MOM._Attr.Type
from   _TFL             import TFL
import _TFL.Decorator

from    sqlalchemy      import orm

@TFL.Add_To_Class ("_sa_column_attrs", MOM.Attr.Kind)
def _sa_kind (self) :
    return dict (nullable = True)
# end def _sa_kind

@TFL.Add_To_Class ("_sa_column_attrs", MOM.Attr.Primary)
def _sa_primary (self) :
    result              = _sa_kind (self)
    result ["nullable"] = False
    return result
# end def _sa_primary

@TFL.Add_To_Class ("_sa_col_name", MOM.Attr.Kind)
def _sa_normal_attr(self) :
    return self.name
# end def _sa_normal_attr

@TFL.Add_To_Class ("_sa_col_name", MOM.Attr.Link_Role)
def _sa_object (self) :
    return "%s_id" % (self.name, )
# end def _sa_object

### Mapper property functions
@TFL.Add_To_Class ("_sa_mapper_prop", MOM.Attr.Kind)
def _sa_kind_prop (self, name, ckd, e_type, properties) :
    ### we need to do this in 2 steps because otherways we hit a
    ### but in sqlalchemy (see: http://groups.google.com/group/sqlalchemy-devel/browse_thread/thread/0cbae608999f87f0?pli=1)
    properties [ckd]  = e_type._sa_table.c [name]
# end def _sa_kind_prop

@TFL.Add_To_Class ("_sa_mapper_prop", MOM.Attr.Link_Role)
def _sa_link_prop (self, name, ckd, e_type, properties) :
    properties [ckd]  = orm.relation (self.role_type)
# end def _sa_link_prop

@TFL.Add_To_Class ("_sa_mapper_prop", MOM.Attr._Composite_Mixin_)
def _sa_composite_prop (self, name, ckd, base_e_type, properties) :
    e_type            = self.attr.C_Type
    db_attrs, columns = e_type._sa_save_attrs
    prefix_len        = len ("__%s_" % (name, ))
    attr_names        = [c.name [prefix_len:] for c in columns]
    raw_or_coocked    = {}
    for attr_name in attr_names :
        if attr_name.startswith ("__raw_") :
            cdk_attr                   = attr_name [6:]
            raw_or_coocked [cdk_attr ] = (cdk_attr, attr_name)
        else :
            raw_or_coocked [attr_name] = attr_name
    del e_type._sa_save_attrs
    def _create (* args, ** kw) :
        attr_dict = dict (zip (attr_names, args))
        for attr_name, arg_names in raw_or_coocked.iteritems () :
            if isinstance (arg_names, tuple) :
                kw [attr_name] = tuple (attr_dict [n] for n in arg_names)
            else :
                kw [attr_name] = attr_dict [arg_name]
        #print args, kw
        #import pdb; pdb.set_trace ()
        return e_type.from_pickle_cargo (MOM.Scope.active, kw)
    # end def _create
    def __composite_values__ (self) :
        return [getattr (self, attr) for attr in attr_names]
    # end def __composite_values__
    def __set_composite_values__ (self, * args) :
        for v, an in zip (args, attr_names) :
            setattr (self, an, v)
    # end def __set_composite_values__
    e_type.__composite_values__     = __composite_values__
    e_type.__set_composite_values__ = __set_composite_values__
    properties [ckd]  = orm.composite \
        (_create
        , comparator_factory = _sa_composite_comperator_class
           (e_type, attr_names, db_attrs)
        , * columns
        )
# end def _sa_composite_prop

def _sa_composite_comperator_class (e_type, attr_names, db_attrs) :
    base       = orm.properties.CompositeProperty.Comparator
    properties = dict ()
    for idx, name in \
        (  (i, an) for (i, an) in enumerate (attr_names)
        if not an.startswith ("__raw_")
        )  :
        properties [name] = property \
            (_sa_composite_comperator_attr_prop (name, idx, db_attrs [name]))
    for name, kind in db_attrs.iteritems () :
        if isinstance (kind, MOM.Attr.Query) :
            properties [name] = property \
                (_sa_composite_comperator_query_prop (name, kind))
    return base.__class__ \
        ( "%s_SA_Comperator" % (e_type.type_base_name)
        , (base, )
        , properties
        )
# end def _sa_composite_comperator_class

def _sa_composite_comperator_attr_prop (name, idx, kind) :
    def _ (self) :
        return self.__clause_element__ ().clauses [idx]
    # end def _
    return _
# end def _sa_composite_comperator_attr_prop

def _sa_composite_comperator_query_prop (name, kind) :
    query = kind.attr.query
    def _ (self) :
        return query._sa_filter (self)
    # end def _
    return _
# end def _sa_composite_comperator_query_prop

@TFL.Add_To_Class ("_sa_mapper_prop", MOM.Attr.Query)
def _sa_query_prop (self, name, ckd, base_e_type, properties) :
    properties [ckd]  = orm.column_property \
        (self.attr.query (base_e_type._sa_table.c))
# end def _sa_query_prop

### __END__ MOM.DBW.SA.Attr_Kind

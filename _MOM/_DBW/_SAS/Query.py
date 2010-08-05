# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DBW.SAS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SAS.Query
#
# Purpose
#    A wrapper which provides access to the SQL column objects trough the
#    attribute names of Entities.
#
# Revision Dates
#    12-Feb-2010 (MG) Creation (based on SA.Query)
#    18-Feb-2010 (MG) `MOM_Composite_Query`: comperison operators added
#    24-Mar-2010 (MG) Composite handling fixed
#    27-Apr-2010 (MG) `SAS_EQ_Clause` method added to support named value
#                     attributes
#     3-May-2010 (MG) Support for joins for filter and order_by added
#     4-May-2010 (CT) `_add_q` factored from `MOM_Query.__init__`,
#                     `ckd_name` added
#     5-May-2010 (MG) `Join_Quer.__call__` fixed to support ordering as well
#     7-May-2010 (MG) `MOM_Query.__init__` inherit `_query_fct` dict as well
#    12-May-2010 (MG) New `pid` style
#     5-Aug-2010 (MG) `MOM_Composite_Query.__ne__, __eq__` fixed
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object
import _TFL.Sorted_By

from   _MOM                  import MOM
from   _MOM.import_MOM       import Q
import _MOM._DBW._SAS

from    sqlalchemy           import sql

class Query (TFL.Meta.Object) :
    """A query object for non MOM objects"""

    def __init__ (self, cls, sa_table, ** attr_map) :
        cls._SAQ              = self
        self._CLASS           = cls
        self._ID_ENTITY_ATTRS = dict ()
        columns               = sa_table.columns
        for col in columns :
            setattr (self, col.name, col)
        for syn, attr in attr_map.iteritems () :
            setattr (self, syn, getattr (self, attr))
    # end def __init__

    def SAS_EQ_Clause (self, attr, value) :
        return (), (getattr (self, attr) == value, )
    # end def SAS_EQ_Clause

    def __getattr__ (self, name) :
        return getattr (self._CLASS, name)
    # end def __getattr__

# end class Query

class _MOM_Query_ (TFL.Meta.Object) :
    """Base class for all queries for MOM objects"""

    def SAS_EQ_Clause (self, attr, cooked) :
        db = cooked
        if   attr == "type_name" :
            attr = "Type_Name"
        elif isinstance (cooked, MOM.Id_Entity) :
            db   = cooked.pid
        else :
            kind = getattr (self._E_TYPE [0], attr, None)
            if kind and isinstance (kind.attr, MOM.Attr._A_Named_Value_) :
                db = kind.Pickler.as_cargo (None, kind, kind.attr, cooked)
        return (), (getattr (self, attr) == db, )
    # end def SAS_EQ_Clause

    def __getattr__ (self, name) :
        if name in self._query_fct :
            return self._query_fct [name].query._sa_filter (self)
        raise AttributeError (name)
    # end def __getattr__

# end class class _MOM_Query_

class MOM_Query (_MOM_Query_) :
    """Query for MOM Entities"""

    def __init__ (self, e_type, sa_table, db_attrs, bases) :
        e_type._SAQ           = self
        self._E_TYPE          = e_type, bases
        self._SA_TABLE        = sa_table
        columns               = sa_table.columns
        self.pid              = columns [e_type._sa_pk_name]
        self._ATTRIBUTES      = []
        self._COMPOSITES      = []
        self._ID_ENTITY_ATTRS = {}
        self._query_fct       = {}
        delayed               = []
        if e_type is e_type.relevant_root :
            self.Type_Name = columns.Type_Name
            self.pid       = columns.pid
            self._ATTRIBUTES.extend (("Type_Name", "pid"))
        for name, kind in db_attrs.iteritems () :
            attr = kind.attr
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                attr_name = "_SAQ_%s" % (name, )
                self._COMPOSITES.append (name)
                comp_query = MOM_Composite_Query (e_type, attr.C_Type, kind)
                self._add_q (comp_query, name, attr.ckd_name)
            elif isinstance (kind, MOM.Attr.Query) :
                delayed.append ((name, kind, attr))
            else :
                col        = columns [attr._sa_col_name]
                attr_names = [name]
                self._add_q (col, name, attr.ckd_name)
                if kind.needs_raw_value :
                    self._add_q (columns [attr._sa_raw_col_name], attr.raw_name)
                if isinstance (kind, MOM.Attr.Link_Role) :
                    self._add_q       (col, attr.role_name)
                    attr_names.append (attr.role_name)
                if isinstance (attr, MOM.Attr._A_Object_) :
                    join_query = Join_Query (self)
                    for an in attr_names :
                        self._ID_ENTITY_ATTRS [an] = join_query
        for b_saq in (b._SAQ for b in bases if getattr (b, "_SAQ", None)) :
            self._COMPOSITES.extend (b_saq._COMPOSITES)
            for name in b_saq._ATTRIBUTES :
                setattr (self, name, b_saq [name])
                self._ATTRIBUTES.append (name)
            for an, jf in b_saq._ID_ENTITY_ATTRS.iteritems () :
                if an not in self._ID_ENTITY_ATTRS :
                    self._ID_ENTITY_ATTRS [an] = jf
            for an, attr in b_saq._query_fct.iteritems () :
                if an not in self._query_fct :
                    self._query_fct [an] = attr
        for name, kind, attr in delayed :
            query_fct = getattr (attr, "query_fct")
            if query_fct :
                self._query_fct [name] = attr
            else :
                query = attr.query._sa_filter (self)
                self._add_q (query, name)
    # end def __init__

    def _add_q (self, q, * names) :
        for n in names :
            setattr (self, n, q)
            self._ATTRIBUTES.append (n)
    # end def _add_q

    def __getitem__ (self, name) :
        return getattr (self, name)
    # end def __getitem__

# end class MOM_Query

class MOM_Composite_Query (_MOM_Query_) :
    """Query attributes of an composite attribite"""

    def __init__ (self, owner_etype, e_type, kind) :
        self._E_TYPE      = e_type
        prefix            = kind._sa_prefix
        db_attrs, columns = e_type._sa_save_attrs.pop \
            ((owner_etype.type_name, kind.attr.name))
        prefix_len                = len (prefix)
        attr_names                = [c.name [prefix_len:] for c in columns]
        self._ATTRIBUTES          = attr_names
        self._ID_ENTITY_ATTRS     = {}
        for idx, name in \
            (  (i, an) for (i, an) in enumerate (attr_names)
            if not an.startswith ("__raw_")
            )  :
            setattr (self, name, columns [idx])
        self._query_fct = {}
        for name, kind in db_attrs.iteritems () :
            if isinstance (kind, MOM.Attr.Query) :
                query_fct = getattr (kind.attr, "query_fct")
                if query_fct :
                    self._query_fct [name] = kind.attr
                else :
                    setattr (self, name, kind.attr.query._sa_filter (self))
    # end def __init__

    def __eq__ (self, rhs) :
        result = []
        for an in self._ATTRIBUTES :
            result.append (getattr (self, an) == getattr (rhs, an, rhs))
        return sql.and_ (* result)
    # end def __eq__

    def __ne__ (self, rhs) :
        result = []
        for an in self._ATTRIBUTES :
            result.append (getattr (self, an) != getattr (rhs, an, rhs))
        return sql.and_ (* result)
    # end def __ne__

    def __le__ (self, rhs) :
        raise TypeError ("`<` is not supported for composits")
    # end def __le__

    def __lt__ (self, rhs) :
        raise TypeError ("`<=` is not supported for composits")
    # end def __lt__

    def __gt__ (self, rhs) :
        raise TypeError ("`>` is not supported for composits")
    # end def __gt__

    def __ge__ (self, rhs) :
        raise TypeError ("`>=` is not supported for composits")
    # end def __ge__

# end class MOM_Composite_Query

class Join_Query (_MOM_Query_) :
    """A query which requires the joining of two table."""

    def __init__ (self, source) :
        self.source     = source
    # end def __init__

    def __call__ (self, attr_name, desc = False) :
        base, sub_attr = attr_name.split (".", 1)
        column         = getattr (self.source, base)
        o_SAQ          = column.mom_kind.Class._SAQ
        fk             = tuple (column.foreign_keys) [0]
        sub_sb         = TFL.Sorted_By (getattr (TFL.Getter, sub_attr) (Q))
        joins, oc      = sub_sb._sa_order_by (o_SAQ, desc = desc)
        joins.append ((self.source._SA_TABLE, o_SAQ._SA_TABLE))
        return joins, oc
    # end def __call__

# end class Join_Query

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Query

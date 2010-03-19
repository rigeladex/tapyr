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
#    12-Feb-2010  (MG) Creation (based on SA.Query)
#    18-Feb-2010 (MG) `MOM_Composite_Query`: comperison operators added
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object

from   _MOM                  import MOM
import _MOM._DBW._SAS

from    sqlalchemy           import sql

class Query (TFL.Meta.Object) :
    """A query object for non MOM objects"""

    def __init__ (self, cls, sa_table, ** attr_map) :
        cls._SAQ    = self
        self._CLASS = cls
        columns     = sa_table.columns
        for col in columns :
            setattr (self, col.name, col)
        for syn, attr in attr_map.iteritems () :
            setattr (self, syn, getattr (self, attr))
    # end def __init__

    def __getattr__ (self, name) :
        return getattr (self._CLASS, name)
    # end def __getattr__

# end class Query

class MOM_Query (TFL.Meta.Object) :

    def __init__ (self, e_type, sa_table, db_attrs, bases) :
        e_type._SAQ        = self
        self._E_TYPE       = e_type, bases
        self._SA_TABLE     = sa_table
        columns            = sa_table.columns
        self.id            = columns [e_type._sa_pk_name]
        self._ATTRIBUTES   = []
        self._COMPOSITES   = []
        self._query_fct    = {}
        delayed            = []
        if e_type is e_type.relevant_root :
            self.Type_Name = columns.Type_Name
            self.id        = columns.id
            self._ATTRIBUTES.extend (("Type_Name", "id"))
        for name, kind in db_attrs.iteritems () :
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                attr_name = "_SAQ_%s" % (name, )
                self._COMPOSITES.append (name)
                self._ATTRIBUTES.append (name)
                comp_query = MOM_Composite_Query (kind.C_Type, name)
                setattr (self, name, getattr (kind.C_Type, attr_name))
            elif isinstance (kind, MOM.Attr.Query) :
                delayed.append ((name, kind))
            else :
                col = columns [kind.attr._sa_col_name]
                setattr (self, name, col)
                if isinstance (kind, MOM.Attr.Link_Role) :
                    setattr (self, kind.role_name, col)
                self._ATTRIBUTES.append (name)
        for b_saq in (b._SAQ for b in bases if getattr (b, "_SAQ", None)) :
            self._COMPOSITES.extend (b_saq._COMPOSITES)
            for name in b_saq._ATTRIBUTES :
                setattr                 (self, name, b_saq [name])
                self._ATTRIBUTES.append (name)
        for name, kind in delayed :
            query_fct = getattr (kind.attr, "query_fct")
            if query_fct :
                self._query_fct [name] = kind.attr
            else :
                setattr (self, name, kind.attr.query._sa_filter (self))
    # end def __init__

    def __getattr__ (self, name) :
        if name in self._query_fct :
            return self._query_fct [name].query._sa_filter (self)
        raise AttributeError (name)
    # end def __getattr__

    def __getitem__ (self, name) :
        return getattr (self, name)
    # end def __getitem__

# end class MOM_Query

class MOM_Composite_Query (TFL.Meta.Object) :
    """Query attributes of an composite attribite"""

    def __init__ (self, e_type, attr_name) :
        setattr (e_type, "_SAQ_%s" % (attr_name, ), self)
        self._E_TYPE              = e_type
        db_attrs, columns, prefix = e_type._sa_save_attrs
        prefix_len                = len (prefix)
        attr_names                = [c.name [prefix_len:] for c in columns]
        self._ATTRIBUTES          = attr_names
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

    def __getattr__ (self, name) :
        if name in self._query_fct :
            return self._query_fct [name].query._sa_filter (self)
        raise AttributeError (name)
    # end def __getattr__

    def __eq__ (self, rhs) :
        result = []
        for an in self._ATTRIBUTES :
            result.append (getattr (self, an) == getattr (rhs, an))
        return sql.and_ (* result)
    # end def __eq__

    def __ne__ (self, rhs) :
        return not self == rhs
    # end def __ne__

    def __le__ (self, rhs) :
        raise TypeError ("`<` is not supported for composits")
    # end def __lt__

    def __le__ (self, rhs) :
        raise TypeError ("`<=` is not supported for composits")
    # end def __lt__

    def __gt__ (self, rhs) :
        raise TypeError ("`>` is not supported for composits")
    # end def __gt__

    def __ge__ (self, rhs) :
        raise TypeError ("`>=` is not supported for composits")
    # end def __ge__

# end class MOM_Composite_Query


if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Query

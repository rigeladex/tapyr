# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DBW.SA.
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
#    MOM.DBW.SA.Query
#
# Purpose
#    A wrapper which provides access to the SA column objects trough the
#    attribute names of Entities.
#    We use this instead of the `orm.synonym` aproch becasue the synonym does
#    not work correct for composite attributes
#
# Revision Dates
#    10-Feb-2010 (MG) Creation
#    10-Feb-2010 (MG) Collect `_COMPOSITES` as well
#    10-Feb-2010 (MG) `MOM_Composite_Query` added
#    11-Feb-2010 (MG) `MOM_Query`: support for `Query` attributes added
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object
from   _MOM                  import MOM
import _MOM._DBW._SA

class Query (TFL.Meta.Object) :
    """A query object for a normally mapped class"""

    def __init__ (self, cls, sa_table) :
        cls._SAQ    = self
        self._CLASS = cls
        columns     = sa_table.columns
        for col in columns :
            setattr (self, col.name, col)
    # end def __init__

    def __getattr__ (self, name) :
        return getattr (self._CLASS, name)
    # end def __getattr__

# end class Query

class MOM_Query (TFL.Meta.Object) :

    def __init__ (self, e_type, sa_table, db_attrs, bases) :
        e_type._SAQ      = self
        self._E_TYPE     = e_type, bases
        columns          = sa_table.columns
        self.Type_Name   = columns.Type_Name
        self.id          = columns [e_type._sa_pk_name]
        self._ATTRIBUTES = []
        self._COMPOSITES = []
        self._query_fct  = {}
        for name, kind in db_attrs.iteritems () :
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                attr_name = "_SAQ_%s" % (name, )
                self._COMPOSITES.append (name)
                self._ATTRIBUTES.append (name)
                setattr (self, name, getattr (kind.C_Type, attr_name))
                delattr (kind.C_Type, attr_name)
            elif isinstance (kind, MOM.Attr.Query) :
                query_fct = getattr (kind.attr, "query_fct")
                if query_fct :
                    self._query_fct [name] = kind.attr
                else :
                    setattr (self, name, kind.attr.query._sa_filter (self))
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

    def __init__ (self, e_type, attr_name, attr_names, db_attrs, columns) :
        setattr (e_type, "_SAQ_%s" % (attr_name, ), self)
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

# end class MOM_Composite_Query


if __name__ != "__main__" :
    MOM.DBW.SA._Export ("*")
### __END__ MOM.DBW.SA.Query

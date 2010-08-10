# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck All rights reserved
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
#    MOM.DBW.SAS.Q_Result
#
# Purpose
#    Provide the Q_Result interface using filter/order/... functions of
#    the sql layer of SASAlchemy
#
# Revision Dates
#    11-Feb-2010 (MG) Creation (based on SA.Q_Result)
#    27-Apr-2010 (MG) `filter`: user new `SAS_EQ_Clause` method of SAQ
#     3-May-2010 (MG) Support for joins for filter and order_by added
#     5-May-2010 (MG) `_join`and `_inner_join` added
#     7-May-2010 (MG) `_joins` changed: joins is now a list instead of a set
#    12-May-2010 (MG) New pid style
#    10-Aug-2010 (MG) `order_by`: add the columns used for the order clause
#                     to the select statement
#    ««revision-date»»···
#--

from   _TFL                 import TFL
from   _MOM                 import MOM
import _TFL._Meta.Object
import _MOM._DBW._SAS.Filter
import _MOM._DBW._SAS.Sorted_By
from    sqlalchemy          import sql

class Q_Result (TFL.Meta.Object) :
    """Q_Result using SQL-query funtion for the operations"""

    def __init__ (self, e_type, session, sa_query = None) :
        self.e_type   = e_type
        self.session  = session
        if sa_query is None :
            sa_query  = e_type._SAS.select
        self.sa_query = sa_query
    # end def __init__

    def all (self) :
        return list (self)
    # end def all

    def count (self) :
        ### this is sort of hackish )o;
        #col         = self.sa_query._columns \
        #    ["%s_pid" % (self.e_type._sa_table.name, )]
        count_query = self.sa_query._clone ()
        count_query._columns.clear ()
        count_query._raw_columns = [sql.func.count ("*").label ("count")]
        count_query._populate_column_collection ()
        result = self.session.connection.execute (count_query)
        count  = result.fetchone ().count
        result.close ()
        return count
    # end def count

    def distinct (self) :
        return self.__class__ \
            (self.e_type, self.session, self.sa_query.distinct ())
    # end def distinct

    def filter (self, * criteria, ** eq_kw) :
        joins         = []
        filter_clause = []
        for c in criteria :
            if not isinstance (c, sql.expression.Operators) :
                ajoins, aclause = c._sa_filter (self.e_type._SAQ)
            else :
                ajoins  = ()
                aclause = (c)
            joins.extend         (ajoins)
            filter_clause.extend (aclause)
        for attr, value in eq_kw.iteritems () :
            ajoins, aclause = self.e_type._SAQ.SAS_EQ_Clause (attr, value)
            joins.extend         (ajoins)
            filter_clause.extend (aclause)
        sa_criteria = (sql.expression.and_ (* filter_clause), )
        sa_query    = self._joins (joins)
        return self.__class__ \
            (self.e_type, self.session, sa_query.where (* sa_criteria))
    # end def filter

    def first (self) :
        try :
            return tuple (self.limit (1)) [0]
        except IndexError :
            return None
    # end def first

    def _from_row (self, row) :
        return self.session.instance_from_row (self.e_type, row)
    # end def _from_row

    def _joins (self, joins) :
        if joins :
            joined   = set ()
            sql_join = self.sa_query.froms [-1]
            for src, dst in reversed (joins) :
                if dst not in joined :
                    joined.add    (dst)
                    sql_join = sql_join.join (dst)
            return self.sa_query.select_from (sql_join)
        return self.sa_query
    # end def _joins

    def limit (self, limit) :
        return self.__class__ \
            (self.e_type, self.session, self.sa_query.limit (limit))
    # end def limit

    def offset (self, offset) :
        return self.__class__ \
            (self.e_type, self.session, self.sa_query.offset (offset))
    # end def offset

    def one (self) :
        execute = self.session.connection.execute
        result  = self.limit (2).all ()
        count   = len (result)
        if count != 1 :
            raise IndexError ("Query result contains %s entries" % (count, ))
        return result [0]
    # end def one

    def order_by (self, criterion) :
        if not isinstance (criterion, sql.expression.Operators) :
            joins, order_clause = criterion._sa_order_by (self.e_type._SAQ)
        else :
            joins               = ()
            order_clause        = (criterion, )
        sa_query                = self._joins (joins)
        for oc in order_clause :
            sa_query.append_column (oc)
        return self.__class__ \
            (self.e_type, self.session, sa_query.order_by (* order_clause))
    # end def order_by

    def __getattr__ (self, name) :
        return getattr (self.sa_query, name)
    # end def __getattr__

    def __iter__ (self) :
        if not getattr (self.session, "_no_flush", False) :
            ### before we make the query, let's flush the session
            self.session.flush ()
        result = self.session.connection.execute (self.sa_query)
        for row in result :
            yield self._from_row (row)
        result.close ()
    # end def __iter__

# end class Q_Result

class Q_Result_Changes (Q_Result) :
    """Special handling of attribute translation for changes"""

    def __init__ (self, Type, session, sa_query = None) :
        if sa_query is None  :
            sa_table = Type._sa_table
            sa_query = sql.select ((sa_table, ))
        self.__super.__init__ (Type, session, sa_query)
    # end def __init__

    def filter (self, * filter, ** kw) :
        pid = kw.pop ("pid", None)
        if pid is not None :
            kw ["pid"]    = pid
        return self.__super.filter (* filter, ** kw)
    # end def filter

    def _from_row (self, row) :
        return self.session.recreate_change (row)
    # end def _from_row

# end class Q_Result_Changes

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Q_Result

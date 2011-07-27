# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2011 Martin Glueck All rights reserved
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
#    16-Aug-2010 (MG) `_clone` factored, `joined_tables` added
#     1-Sep-2010 (MG) New version of `Q_Result*` added to support `attr*` and
#                     `set` functions
#     2-Sep-2010 (CT) Bug fixes in new version of `Q_Result`
#     2-Sep-2010 (MG) `_attrs` factored and improved to used
#                     `kind.from_pickle_cargo`
#     6-Sep-2010 (MG) Old implementaion removed, `_join` changed to allow
#                     specifying of the join condition
#     7-Sep-2010 (MG) `attr` and `attrs` changed to return `_Q_Result_Attrs_`
#    13-Oct-2010 (MG) Support for `raw` parameter added to `attr/(s)`
#    18-Jul-2011 (CT) `count` changed ro return `int (count)`
#    19-Jul-2011 (CT) `_Q_Result_Attrs_._from_row_tuple` changed to not apply
#                     `str` for kind-less attributes (e.g., `pid`)
#    22-Jul-2011 (MG) `__str__` added
#    26-Jul-2011 (MG) Caching of `_sa_query` and `_kinds` fixed, caching of
#                     query result in `__iter__` added, `count` for
#                     `_Q_Result_Attrs_` fixed
#    27-Jul-2011 (MG) `_Q_Result_Attrs_.count` changed to use sub queries
#    ��revision-date�����
#--

from   _TFL                 import TFL
import _TFL.Decorator
import _TFL.Accessor
import _TFL._Meta.Object

from   _MOM                 import MOM
import _MOM._DBW._SAS.Filter
import _MOM._DBW._SAS.Sorted_By

from    sqlalchemy          import sql

class _Q_Result_ (TFL.Meta.Object) :
    """Base class for Q_Result using SQLAlchemy to query a SQL database."""

    _sa_query = None
    _result   = None

    class List (list) :
        def copy (self) : return self.__class__ (self)
    # end class List

    _Query_Attrs    = dict \
        ( _distinct = (False,   False)
        , _limit    = (None,    False)
        , _offset   = (None,    False)
        , _joins    = (List (), True)
        , _columns  = (List (), True)
        , _filter   = (List (), True)
        , _order_by = (List (), True)
        )

    def __init__ (self, e_type, session, parent = None) :
        self.e_type        = e_type
        self.session       = session
        for name, (default, copy) in self._Query_Attrs.iteritems () :
            value = getattr (parent, name, default)
            if copy :
                value = value.copy ()
            setattr (self, name, value)
    # end def __init__

    def attr (self, getter, raw = False) :
        return self._Q_Result_Attrs_ \
            (self.e_type, self.session, self, getter, raw)
    # end def attr

    def attrs (self, * getters, ** kw) :
        if not getters :
            raise TypeError \
                ( "%s.attrs() requires at least one argument"
                % self.__class__.__name
                )
        return self._Q_Result_Attrs_ \
            (self.e_type, self.session, self, getters, kw.pop ("raw", False))
    # end def attrs

    def all (self) :
        return list (self)
    # end def all

    def _clone (self) :
        return self.__class__ (self.e_type, self.session, self)
    # end def _clone

    def count (self) :
        sa_query = self.sa_query \
            ([sql.func.count ("*").label ("count")], True, False)
        result   = self.session.connection.execute (sa_query)
        count    = result.fetchone ().count
        result.close ()
        return int (count)
    # end def count

    def distinct (self) :
        result           = self._clone ()
        result._distinct = True
        return result
    # end def distinct

    def filter (self, * criteria, ** eq_kw) :
        result = self._clone ()
        for c in criteria :
            if not isinstance (c, sql.expression.Operators) :
                ajoins, aclause = c._sa_filter (self.e_type._SAQ)
            else :
                ajoins          = ()
                aclause         = (c)
            result._joins .extend (ajoins)
            result._filter.extend (aclause)
        for attr, value in eq_kw.iteritems () :
            ajoins, aclause = self.e_type._SAQ.SAS_EQ_Clause (attr, value)
            result._joins .extend (ajoins)
            result._filter.extend (aclause)
        return result
    # end def filter

    def first (self) :
        try :
            return tuple (self.limit (1)) [0]
        except IndexError :
            return None
    # end def first

    def _join (self, sa_query, joins, joined_tables) :
        if joins :
            sql_join      = sa_query.froms [-1]
            no_joins      = len (joined_tables)
            for src, dst, cond in reversed (joins) :
                if dst not in joined_tables :
                    joined_tables.add        (dst)
                    sql_join = sql_join.join (dst, onclause = cond)
            if len (joined_tables) > no_joins :
                sa_query = sa_query.select_from (sql_join)
        return sa_query, joined_tables
    # end def _join

    def limit (self, limit) :
        result = self._clone ()
        result._limit = limit
        return result
    # end def limit

    def offset (self, offset) :
        result = self._clone ()
        result._offset = offset
        return result
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
        result = self._clone ()
        if not isinstance (criterion, sql.expression.Operators) :
            joins, order_clause = criterion._sa_order_by (self.e_type._SAQ)
        else :
            joins               = ()
            order_clause        = (criterion, )
        result._joins   .extend (joins)
        result._order_by.extend (order_clause)
        result._columns .extend \
            (getattr (oc, "element", oc) for oc in order_clause)
        return result
    # end def order_by

    def _query_rows (self, sa_query = None) :
        if not getattr (self.session, "_no_flush", False) :
            ### before we make the query, let's flush the session
            self.session.flush ()
        if sa_query is None :
            sa_query = self.sa_query ()
        result       = self.session.connection.execute (sa_query)
        for row in result :
            yield row
        result.close ()
    # end def _query_rows

    def sa_query (self, columns = (), joins = False, cache = True) :
        if columns or self._sa_query is None or cache is False :
            sa_query, joined = self._sql_query (columns, joins)
            sa_query, joined = self._join      (sa_query, self._joins, joined)
            if self._filter :
                sa_query = sa_query.where (sql.expression.and_ (* self._filter))
            if self._order_by :
                sa_query = sa_query.order_by (* self._order_by)
            if self._distinct :
                sa_query = sa_query.distinct ()
            if self._limit is not None :
                sa_query = sa_query.limit  (self._limit)
            if self._offset is not None :
                sa_query = sa_query.offset (self._offset)
            if columns :
                return sa_query
            if not cache :
                return sa_query
            self._sa_query = sa_query
        return self._sa_query
    # end def sa_query

    def _sql_query (self, columns, joins) :
        SAS          = self.e_type._SAS
        if not columns :
            sa_query = SAS.select
            joined   = SAS.joined_tables.copy ()
        else :
            if joins :
                sa_query = sql.select (columns, from_obj = (SAS.joins, ))
                joined   = SAS.joined_tables.copy ()
            else :
                sa_query = sql.select (columns)
                joined   = set ()
        return sa_query, joined
    # end def _sql_query

    def set (self, * args, ** kw) :
        if not self._filter :
            raise TypeError \
                ( "%s.set() requires at least one filter criteria"
                % (self.__class__.__name)
                )
        tables = TFL.defaultdict (dict)
        SAQ    = self.e_type._SAQ
        kw     = dict (args, ** kw)
        where  = sql.expression.and_ (* self._filter)
        conn   = self.session.connection
        for n, v in kw.iteritems () :
            column = getattr (TFL.Getter, n) (SAQ)
            tables [column.table] [column.name] = v
        for t, vd in tables.iteritems () :
            conn.execute (t.update ().values (** vd).where (where))
    # end def set

    def where (self, expr) :
        self._filter.append (expr)
        return self
    # end def where

    def __iter__ (self) :
        if self._result is None :
            self._result = []
            for row in self._query_rows () :
                element = self._from_row (row)
                self._result.append (element)
                yield element
        else :
            for element in self._result :
                yield element
    # end def __iter__

    def __str__ (self) :
        sa_query = "\n     ".join \
            (l.strip () for l in str (self.sa_query ()).split ("\n"))
        return "SQL: %s" % (sa_query, )
    # end def __str__

# end class _Q_Result_

class Q_Result (_Q_Result_) :
    """Reconstruct MOM entities from the query results."""

    def _from_row (self, row) :
        return self.session.instance_from_row (self.e_type, row)
    # end def _from_row

# end class Q_Result

@TFL.Add_New_Method (_Q_Result_)
class _Q_Result_Attrs_ (_Q_Result_) :
    """Return only the values of the explicitly stated attributes instead of
       MOM instances.
    """

    _Query_Attrs    = dict \
        (_Q_Result_._Query_Attrs, _attr_cols = (_Q_Result_.List (), True))

    def __init__ ( self, e_type, session, parent
                 , getter_or_getters = None
                 , raw               = False
                 ) :
        self.__super.__init__ (e_type, session, parent)
        if getter_or_getters is not None :
            if not isinstance (getter_or_getters, tuple) :
                getters        = (getter_or_getters, )
                self._from_row = self._from_row_single
            else :
                getters        = getter_or_getters
                self._from_row = self._from_row_tuple
            self._attr_cols.extend (self._getters_to_columns (getters, raw))
    # end def __init__

    def count (self) :
        sa_query = sql.select \
            ( [sql.func.count ("*").label ("count")]
            , from_obj = self.sa_query ()
            )
        result   = self.session.connection.execute (sa_query)
        count    = result.fetchone ().count
        result.close ()
        return int (count)
        return len (self.all ())
    # end def count

    def distinct (self, * criteria) :
        return TFL.Q_Result (self).distinct (* criteria)
    # end def distinct

    def _getters_to_columns (self, getters, raw) :
        Q   = MOM.Q
        SAQ = self.e_type._SAQ
        for getter in getters :
            if isinstance (getter, basestring) :
                getter = getattr (Q, getter)
            if raw :
                attr_name = getter._name
                if "." in attr_name :
                    path, attr_name = attr_name.rsplit (".", 1)
                    SAQ             = getattr (Q, path) (SAQ)
                attr_kind           = getattr (SAQ._E_TYPE [0], attr_name, None)
                if attr_kind and attr_kind.needs_raw_value :
                    attr_name       = attr_kind.raw_name
                yield getattr (SAQ, attr_name)
            else :
                yield getter (SAQ)
    # end def _getters_to_columns

    def _from_row_tuple (self, row) :
        result = []
        scope  = self.session.scope
        for k, cols in self._kinds :
            if isinstance (cols, (list, tuple)) :
                pc = dict ((c.MOM_Kind.attr.name, (row [c], )) for c in cols)
            else :
                pc = row [cols]
            if k :
                result.append (k.from_pickle_cargo (scope, (pc, )))
            else :
                result.append (pc)
        return tuple (result)
    # end def _from_row_tuple

    def _from_row_single (self, row) :
        return self._from_row_tuple (row) [0]
    # end def _from_row_single

    def sa_query (self, columns = (), joins = False, cache = True) :
        if self._sa_query is None or cache is False :
            if not columns :
                joins       = False
                comp_query  = MOM.DBW.SAS.MOM_Composite_Query
                columns     = []
                kinds       = []
                for req_col in self._attr_cols :
                    if isinstance (req_col, comp_query) :
                        cols = req_col._COLUMNS
                        columns.extend (cols)
                    else :
                        cols = req_col
                        columns.append (cols)
                    kinds.append       ((req_col.MOM_Kind, cols))
            else :
                joins       = True
                kinds       = [(None, c) for c in columns]
            sa_query = self.__super.sa_query (columns, joins, cache)
            if not cache :
                return sa_query
            self._sa_query = sa_query
            self._kinds    = kinds
        return self._sa_query
    # end def sa_query

# end class _Q_Result_Attrs_

class Q_Result_Changes (_Q_Result_) :
    """Special handling of attribute translation for changes"""

    def _sql_query (self, columns, joins) :
        sa_table = self.e_type._sa_table
        if columns :
            return sql.select (columns, from_obj = (sa_table, )), set ()
        return sql.select ((sa_table, )), set ()
    # end def _sql_query

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

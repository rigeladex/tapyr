# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.Q_Result
#
# Purpose
#    Implement SAW query results
#
# Revision Dates
#     5-Jul-2013 (CT) Creation
#     7-Jul-2013 (CT) Use `session.q_cache`
#    11-Jul-2013 (CT) Add `polymorphic`; use `cols` for `joined` cache
#    12-Jul-2013 (CT) Use `A_Join.__class__`, not home-grown code
#    15-Jul-2013 (CT) Add `_Attr_` and `_Attrs_`; factor `_get_col_exprs`
#    16-Jul-2013 (CT) Add `E_Type_Reload`
#    18-Jul-2013 (CT) Remove `as_scalar` from `_Attr_._sa_query`
#    19-Jul-2013 (CT) Delay `order_by` application to reverse the criteria
#    20-Jul-2013 (CT) Use `ETW.joined`, `.joined_strict` to initialize `_joined`
#    21-Jul-2013 (CT) Set `Q_Result.E_Type.polymorphic` to `.polymorphic_epks`
#    22-Jul-2013 (CT) Factor `sa_query_count`, use `sql.func.count`
#    24-Jul-2013 (CT) Change `__str__` to add linebreaks for `AND|OR` of `WHERE`
#    24-Jul-2013 (CT) Change `_clone` to reset `_order_by_cached`,
#                     add `_sa_query_ob`
#    25-Jul-2013 (CT) Rename `_query_iter` to `row_iter`, add `** kw` to it
#    26-Jul-2013 (CT) Factor `_Attr_Base_`, add support for composite attrs
#    28-Jul-2013 (CT) Add `bind` and `bvar_man`
#    30-Jul-2013 (CT) Remove `set`
#     1-Aug-2013 (CT) Change `E_Type_Reload` to use `spk`, not `pid`
#     1-Aug-2013 (CT) Add `SCM_Change`
#     2-Aug-2013 (CT) Don't include `last_cid` in query of `E_Type_Reload`
#     4-Aug-2013 (CT) Change `_get_filters` to call `fix_bool`
#     5-Aug-2013 (CT) Assign `_SAW_Q_Result` for `MOM.Id_Entity`,
#                     `MOM.MD_Change`
#     9-Aug-2013 (CT) Simplify `_extend_join` to check for `table` in `joined`
#    11-Sep-2013 (CT) Change `_get_filters` to use `SAW.QX`
#    17-Sep-2013 (CT) Change `_get_order_by` to use `SAW.QX`
#    17-Sep-2013 (CT) Change `order_by` to allow multiple criteria
#    18-Sep-2013 (CT) Facter `_get_xs`, add and use `_get_attr_exprs`
#    23-Sep-2013 (CT) Rename `_Base_.__str__` to `.__repr__`
#    ��revision-date�����
#--

from   __future__                import division, print_function
from   __future__                import absolute_import, unicode_literals

from   _TFL                      import TFL
from   _TFL.pyk                  import pyk

from   _MOM.import_MOM           import MOM, Q
from   _MOM._DBW._SAW            import SAW, SA

import _MOM._DBW._SAW.Attr

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
from   _TFL.Decorator            import subclass_responsibility

import _TFL.Accessor
import _TFL.Decorator
import _TFL.predicate
import _TFL.Regexp

import itertools
import operator

@pyk.adapt__bool__
class _Base_ (TFL.Meta.Object) :
    """Base class for SAW Q_Result classes"""

    _order_by_cached     = None
    _sa_query_ob         = None

    def __init__ (self, session = None) :
        self.session     = session
        self.bvar_man    = Q.BVAR_Man ()
        self._joined     = set ()
        self._order_bys  = []
        self.polymorphic = False
    # end def __init__

    @TFL.Meta.Once_Property
    def QX (self) :
        from _MOM._DBW._SAW import QX
        return QX
    # end def QX

    @property
    def sa_query (self) :
        result = self._sa_query_ob
        if result is None :
            result = self._sa_query
            obs    = self._order_by
            if obs :
                result = result.order_by (* obs)
            self._sa_query_ob = result
        return result
    # end def sa_query

    @property
    def sa_query_count (self) :
        result = SA.sql.select \
            ( [SA.sql.func.count ("*").label ("count")]
            , from_obj = self._sa_query.alias ("__count__")
            )
        return result
    # end def sa_query_count

    @property
    def session (self) :
        return self.__dict__ ["session"]
    # end def session

    @session.setter
    def session (self, value) :
        old_value = self.__dict__.get ("session")
        if old_value is None or old_value is value :
            self.__dict__ ["session"] = value
        else :
            raise AttributeError \
                ("Cannot change session from %s to %s" % (old_value, value))
    # end def session

    @property
    def _order_by (self) :
        result = self._order_by_cached
        if result is None :
            result = self._order_by_cached = []
            for obs in reversed (self._order_bys) :
                result.extend (obs)
        return result
    # end def _order_by

    def all (self) :
        return list (self)
    # end def all

    def attr (self, getter) :
        return self._Attr_ (self, getter)
    # end def attr

    def attrs (self, * getters, ** kw) :
        if not getters :
            raise TypeError \
                ( "%s.attrs() requires at least one argument"
                % self.__class__.__name__
                )
        return self._Attrs_ (self, getters)
    # end def attrs

    def bind (self, _session = None, ** bindings) :
        result = self._clone ()
        result.bvar_man.bind (** bindings)
        if _session is not None :
            result.session = _session
        return result
    # end def bind

    def count (self) :
        q_result = self.session and self.session.q_cache.get (self)
        if q_result is not None :
            return len (q_result)
        else :
            cq     = self.sa_query_count
            qr     = self.session.connection.execute (cq)
            result = int (qr.scalar ())
            return result
    # end def count

    def distinct (self) :
        result = self._clone ()
        result._sa_query = result._sa_query.distinct ()
        return result
    # end def distinct

    def filter (self, * criteria, ** kw) :
        if kw :
            crits = list (criteria)
            crits.extend (getattr (Q, k) == v for k, v in pyk.iteritems (kw))
            criteria = tuple (crits)
        assert criteria
        result           = self._clone ()
        sa_query         = result._sa_query
        where_exp, join  = result._get_filters  (criteria, sa_query)
        if join is not None :
            sa_query     = sa_query.select_from (join)
        result._sa_query = sa_query.where       (where_exp)
        return result
    # end def filter

    def first (self) :
        try :
            ### cache ??? `self.limit` creates a new Q_Result
            return TFL.first (self.limit (1))
        except IndexError :
            return None
    # end def first

    def group_by (self, * columns) :
        result           = self._clone ()
        result._sa_query = result._sa_query.group_by \
            (* self._get_group_by (columns))
        return result
    # end def group_by

    def limit (self, limit) :
        result           = self._clone ()
        result._sa_query = result._sa_query.limit (limit)
        return result
    # end def limit

    def offset (self, offset) :
        result           = self._clone ()
        result._sa_query = result._sa_query.offset (offset)
        return result
    # end def offset

    def one (self) :
        result = tuple (self.limit (2))
        count  = len (result)
        if count != 1 :
            raise IndexError \
                ( "Query result contains %s entries"
                % (self.count () if count else 0, )
                )
        return result [0]
    # end def one

    def order_by (self, * criteria) :
        result    = self._clone ()
        sa_query  = result._sa_query
        obs, join = result._get_order_by  (criteria, sa_query)
        if join is not None :
            result._sa_query = sa_query.select_from (join)
        ### `obs` is a list; use `append` here to be apple to later reverse
        ### `_order_bys` while keeping the sequence of items in `obs`
        ### this allows later `order_by` calls to dominate earlier ones
        result._order_bys.append (obs)
        return result
    # end def order_by

    def row_iter (self, session, ** kw) :
        qkw    = dict (self.bvar_man.bindings, ** kw)
        result = session.connection.execute (self.sa_query, ** qkw)
        try :
            for row in result :
                yield row
        finally :
            result.close ()
    # end def row_iter

    def _clone (self, ** kw) :
        cls    = self.__class__
        result = cls.__new__   (cls)
        result.__dict__.update \
            ( self.__dict__
            , bvar_man         = self.bvar_man.clone ()
            , _joined          = set (self._joined)
            , _order_bys       = list (self._order_bys)
            , _order_by_cached = None
            , _sa_query_ob     = None
            , ** kw
            )
        return result
    # end def _clone

    def _extend_join (self, join, joined, jxs) :
        for a_join in jxs :
            if a_join.table not in joined :
                joined.add (a_join.table)
                join = a_join (join)
        return join
    # end def _extend_join

    def _get_attr_exprs (self, axes, sa_query) :
        axes = list \
            (   (getattr (Q, ax) if isinstance (ax, pyk.string_types) else ax)
            for ax in axes
            )
        return self._get_xs (axes, sa_query, "XS_ATTR", TFL.Method.extend)
    # end def _get_attr_exprs

    def _get_filters (self, criteria, sa_query) :
        wxs, join = self._get_xs \
            (criteria, sa_query, "XS_FILTER", TFL.Method.append)
        wxs = wxs [0] if len (wxs) == 1 else SA.expression.and_ (* wxs)
        return wxs, join
    # end def _get_filters

    def _get_group_by (self, columns) :
        ETW = getattr (self, "ETW", None)
        if ETW is None :
            for c in columns :
                yield c
        else :
            ETW_Q = ETW.QC
            for c in columns :
                if isinstance (c, pyk.string_types) :
                    c = getattr (Q, c)
                yield c (ETW_Q)
    # end def _get_group_by

    def _get_order_by (self, criteria, sa_query) :
        return self._get_xs \
            ( self.QX.fixed_order_by (criteria), sa_query
            , "XS_ORDER_BY", TFL.Method.extend
            )
    # end def _get_order_by

    def _get_xs (self, criteria, sa_query, xs_name, adder) :
        QX     = self.QX
        joined = self._joined
        join   = orig_join = sa_query.froms [-1]
        xs     = []
        for c in criteria :
            if isinstance (c, SA.Operators) :
                xs.append (c)
            else :
                qx   = QX.Mapper (self) (c)
                x    = getattr (qx, xs_name)
                join = self._extend_join (join, joined, qx.JOINS)
                adder (xs, x)
        return xs, None if join is orig_join else join
    # end def _get_xs

    def __bool__ (self) :
        result = self.session.q_cache.get (self)
        ### XXX cache
        return bool (result or self.first () is not None)
    # end def __bool__

    def __iter__ (self) :
        session = self.session
        result  = session.q_cache.get (self)
        if result is None :
            result = []
            for row in self.row_iter (session) :
                element = self._from_row (row)
                result.append (element)
                yield element
            session.q_cache [self] = result
        else :
            for element in result :
                yield element
    # end def __iter__

    def __repr__ (self) :
        def q_parts (self) :
            for p in str (self.sa_query).split ("\n") :
                p = p.strip ()
                if ", " in p and p.startswith ("SELECT") :
                    h, t = p.split (" ", 1)
                    p = "\n       ".join \
                        ((h, ",\n       ".join (sorted (t.split (", ")))))
                elif "JOIN" in p :
                    rerep = TFL.Re_Replacer \
                        ( "((?:[A-Z]+ )*JOIN)"
                        , "\n       \\1"
                        )
                    p  = rerep (p)
                    ps = list (x.rstrip () for x in p.split ("\n"))
                    p  = "\n".join (ps)
                elif "WHERE" in p :
                    rerep = TFL.Re_Replacer \
                        ( "((?:\s+)*(?:AND|OR)\s+)"
                        , "\n       \\1"
                        )
                    p  = rerep (p)
                    ps = list (x.rstrip () for x in p.split ("\n"))
                    p  = "\n".join (ps)
                if "ORDER BY" in p :
                    rerep = TFL.Re_Replacer \
                        ( "\s+(ORDER BY)"
                        , "\n     \\1"
                        )
                    p  = rerep (p)
                yield p
        sa_query = "\n     ".join (q_parts (self))
        return "SQL: %s" % (sa_query, )
    # end def __repr__

# end class _Base_

class _Attr_Base_ (_Base_) :
    """Base class for `_Attr_` and `_Attrs_`"""

    def __init__ (self, parent, axes) :
        self.__super.__init__ (parent.session)
        self.__dict__.update  (parent.__dict__, _joined = set (parent._joined))
        cols, join = self._get_attr_exprs (axes, self._sa_query)
        self.cols  = cols
        self._setup_query (cols, join)
    # end def __init__

    def _col_value_from_row (self, col, row, scope) :
        if isinstance (col, MOM.DBW.SAW.Attr.Kind_Wrapper_C) :
            pc     = col.row_as_pickle_cargo    (row)
            result = col.kind.from_pickle_cargo (scope, pc)
        else :
            result = row [col]
            kind   = getattr (col, "MOM_Kind", None)
            if kind is not None :
                result = kind.from_pickle_cargo (scope, (result, ))
        return result
    # end def _col_value_from_row

    def _setup_query (self, cols, join) :
        def _gen (cols) :
            for c in cols :
                if isinstance (c, MOM.DBW.SAW.Attr.Kind_Wrapper_C) :
                    for cc in c.columns :
                        yield cc
                else :
                    yield c
        sa_query = self._sa_query
        if join is not None :
            sa_query   = sa_query.select_from       (join)
        self._sa_query = sa_query.with_only_columns (_gen (cols))
    # end def _setup_query

# end class _Attr_Base_

@TFL.Add_New_Method (_Base_)
class _Attr_ (_Attr_Base_) :
    """Q_Result for a single attribute value"""

    def __init__ (self, parent, ax) :
        self.__super.__init__ (parent, [ax])
        cols = self.cols
        if len (cols) != 1 :
            raise TypeError \
                ("attr %r must result in a single column; got %s" % (ax, cols))
        self.col = cols [0]
    # end def __init__

    def _from_row (self, row) :
        return self._col_value_from_row (self.col, row, self.session.scope)
    # end def _from_row

# end class _Attr_

@TFL.Add_New_Method (_Base_)
class _Attrs_ (_Attr_Base_) :
    """Q_Result for a tuple of attribute values"""

    def _from_row (self, row) :
        def _gen (row, cols, scope) :
            for col in self.cols :
                yield self._col_value_from_row (col, row, scope)
        return tuple (_gen (row, self.cols, self.session.scope))
    # end def _from_row

# end class _Attrs_

@TFL.Add_To_Class ("_SAW_Q_Result", MOM.Id_Entity)
class E_Type (_Base_) :
    """Q_Result for E_Type queries"""

    def __init__ (self, E_Type, session = None, _strict = False) :
        self.__super.__init__ (session)
        self.E_Type      = E_Type
        self.ETW         = ETW = E_Type._SAW
        self._sa_query   = ETW.select_strict if _strict else ETW.select
        self._joined     = ETW.joined_strict if _strict else ETW.joined
        self._strict     = _strict
        self.polymorphic = E_Type.polymorphic_epks
    # end def __init__

    def _from_row (self, row) :
        return self.session.instance_from_row (self.ETW, row)
    # end def _from_row

# end class E_Type

@TFL.Add_To_Class ("_SAW_Q_Result", MOM.MD_Change)
class SCM_Change (E_Type) :
    """Q_Result delivering MOM.SCM.Change instances with parent/children."""

    def _from_row (self, row) :
        return self.session.scm_change_from_row (self.ETW, row)
    # end def _from_row

# end class SCM_Change

class E_Type_Reload (E_Type) :
    """Q_Result for reloading an entity from the database.

       Reload is done unconditionally to ensure that the database sees an
       access to the row. Otherwise, XXX @RSC: please add explanation @RSC
    """

    def __init__ (self, E_Type) :
        self.__super.__init__ (E_Type)
        self._init_p = False
    # end def __init__

    @property
    def _sa_query (self) :
        result = self.__dict__ ["_sa_query"]
        if not self._init_p :
            E_Type   = self.E_Type
            Q_spk    = getattr (Q, E_Type.spk_attr_name)
            filters  = (Q_spk == SA.sql.bindparam ("spk"), )
            obs      = ()
            wx, join = self._get_filters (filters, result)
            if join is not None :
                raise RuntimeError \
                    ("Reload filters must not do an extra join %s" % (join, ))
            result = result.where (wx)
            if obs :
                result = result.order_by (* obs)
            result = self.__dict__ ["_sa_query"] = result.limit (1)
            self._init_p = True
        return result
    # end def _sa_query

    @_sa_query.setter
    def _sa_query (self, value) :
        self.__dict__ ["_sa_query"] = value
    # end def _sa_query

    def reload (self, entity, session) :
        kw  = dict (spk = entity.spk)
        row = session.connection.execute (self._sa_query, ** kw).first ()
        if row is not None :
            ETW          = self.ETW
            last_cid_col = ETW.last_cid_col
            if last_cid_col is not None :
                if row [last_cid_col] == entity.last_cid :
                    return ### no need to `reload` from `row` into `entity`
            self.ETW.reload (entity, row)
    # end def reload

# end class E_Type_Reload

if __name__ != "__main__" :
    MOM.DBW.SAW._Export_Module ()
### __END__ MOM.DBW.SAW.Q_Result

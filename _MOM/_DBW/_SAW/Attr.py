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
# You should have received a copy of the GNU Affero General Public Licenes
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.Attr
#
# Purpose
#    Attribute handling for SAW
#
# Revision Dates
#    25-Jun-2013 (CT) Creation
#     1-Jul-2013 (CT) Change 3rd arg of `Kind_Wrapper` from `prefix` to `outer`
#     1-Jul-2013 (CT) Add `Kind_Wrapper.col_values`
#     2-Jul-2013 (CT) Factor `col_values_from_cargo`, add `row_as_pickle_cargo`
#     3-Jul-2013 (CT) Change `Kind_Wrapper.raw_name` to put `__raw` in front
#     3-Jul-2013 (CT) Add `Kind_Wrapper_Q`, factor `_Kind_Wrapper_`
#     3-Jul-2013 (CT) Add `_Kind_Wrapper_.Derived`, `.eff`, `.q_able_names`
#     4-Jul-2013 (CT) Change `Kind_Wrapper.columns` to return `eff.columns`,
#                     if any
#     4-Jul-2013 (CT) Add `Kind_Composite_Wrapper.q_able_attrs`
#     4-Jul-2013 (CT) Add `Kind_Wrapper.name` and use in `__str__`
#     4-Jul-2013 (CT) Factor `pc_transform`, `col_values*`, and
#                     `row_as_pickle_cargo` up to `_Kind_Wrapper_`
#     5-Jul-2013 (CT) Add `prefix` to `q_able_names`; add `update_col_map`
#     8-Jul-2013 (CT) Use `.ATW.SA_Type`; add `_saw_column_type_type_name`
#     8-Jul-2013 (CT) Add `q_exp_get` to `_Kind_Wrapper_`
#     8-Jul-2013 (CT) Add `Kind_EPK_Wrapper`
#     9-Jul-2013 (CT) Split `Kind_Wrapper_P` from `Kind_Wrapper_Q`,
#                     add `q_exp_get` to them and `Kind_Composite_Wrapper`
#     9-Jul-2013 (CT) Add `q_exp_bin` to `_Kind_Wrapper_`
#    10-Jul-2013 (CT) Set `_SAW` of kind descriptors
#    10-Jul-2013 (CT) Add `Kind_Wrapper_R` for `_Rev_Query_` attributes
#    11-Jul-2013 (CT) Implement `Kind_Wrapper_R.q_exp_get`
#    11-Jul-2013 (CT) Add `QR.polymorphic` to force `outerjoin` when necessary
#    12-Jul-2013 (CT) Add `q_exp_call`, `q_exp_func`, `q_exp_una`
#    12-Jul-2013 (CT) Add support for `sqx_filter` to `Kind_Wrapper_R`
#    12-Jul-2013 (CT) Reify `A_Join`
#    15-Jul-2013 (CT) Add `q_exp_get_ob`
#    15-Jul-2013 (CT) Redefine `_q_exp_bin_combine` for
#                     `Kind_Composite_Wrapper`, `Kind_EPK_Wrapper`,
#                     and `Kind_Wrapper_R`
#    18-Jul-2013 (CT) Deal with instances of `.attr.E_Type` in
#                     `Kind_Composite_Wrapper._q_exp_bin_combine`
#    19-Jul-2013 (CT) Add support for `Q.RAW`
#    21-Jul-2013 (CT) Change `Kind_Composite_Wrapper._q_exp_bin_combine` to
#                     delegate dealing with nested attributes to `.__super`
#    21-Jul-2013 (CT) Fix `Kind_Wrapper_Q.q_exp_get`
#                     (pass self.outer to `sf`, if any)
#    21-Jul-2013 (CT) Fix `Kind_EPK_Wrapper.q_exp_get` (`jxs`)
#    21-Jul-2013 (CT) Fix `Kind_Wrapper_R._q_exp_bin_combine` (don't add joins)
#    22-Jul-2013 (CT) Add `alias`, use `attr_join_etw_alias`
#    23-Jul-2013 (CT) Add `_setup_alias_columns`, `_setup_alias_attrs`
#    23-Jul-2013 (CT) Redefine `Kind_Wrapper_P.q_exp_bin` and
#                     change `Kind_Wrapper_R._wrap_super_q_exp` to
#                     * OR-combine children's expressions
#    23-Jul-2013 (CT) Add `Kind_Composite_Wrapper.__getattr__` to trigger `QC`
#    23-Jul-2013 (CT) Factor `_column_joins`, `_column_joins_pkn`
#    24-Jul-2013 (CT) Fix handling of extra columns due to `sqx_filter`
#    30-Jul-2013 (CT) Don't pass `tail_name` to kind-wrapper for `tail_name`
#    30-Jul-2013 (CT) Support `tail_name` in `Kind_Wrapper_Q.q_exp_get`
#    30-Jul-2013 (CT) Change `Kind_Wrapper_P.q_exp_bin` to use
#                     `_q_exp_bin_cols` and `_q_exp_bin_combine`,
#                     not `__super.q_exp_bin`
#    30-Jul-2013 (CT) Redefine `Kind_Wrapper_P.q_exp_call`, `.q_exp_func`
#    30-Jul-2013 (CT) Factor `_q_exp_bin_cols` and `_q_exp_call_parts`
#    30-Jul-2013 (CT) Add support for column attributes like `Date_Column.year`
#                     (`_col_from_key`, `_saw_col_from_key`)
#     1-Aug-2013 (CT) Add support for `MD_Change` to `_q_exp_bin_cols`
#     3-Aug-2013 (CT) Change `col_values_from_cargo` to use `default`, not
#                     `None`, for non-nullable columns
#     4-Aug-2013 (CT) Add `fix_bool` and `_saw_bool` methods
#     4-Aug-2013 (CT) Add and use Single_Dispatch_Method `_saw_kind_wrapper`
#     4-Aug-2013 (CT) Add `Kind_Date_Wrapper`, `Kind_Date_Time_Wrapper`, and
#                     `Kind_Time_Wrapper` plus the supporting infrastructure
#     6-Aug-2013 (CT) Factor `_q_exp_bin_apply`, `_q_exp_call_apply`
#     6-Aug-2013 (CT) Add optional argument `columns` to `update_col_map`
#     6-Aug-2013 (CT) Use `.attr._saw_kind_wrapper`, if any
#     9-Aug-2013 (CT) Factor `_col_q_able_names`, redefine for
#                     `Kind_EPK_Wrapper`
#     9-Aug-2013 (CT) Use `self.kind`, not `self.eff.kind`, unless accessing
#                     `columns`
#    25-Aug-2013 (CT) Use `MOM.Id_Entity.E_Spec._Attributes`
#    25-Aug-2013 (CT) Add `default` to `_saw_column_kw`, `_saw_columns_raw_kind`
#    26-Aug-2013 (CT) Add `col_args` to `_saw_columns_surrogate`
#    ««revision-date»»···
#--

from   __future__                 import division, print_function
from   __future__                 import absolute_import, unicode_literals

from   _MOM                       import MOM
from   _TFL                       import TFL
from   _TFL.pyk                   import pyk

from   _MOM._DBW._SAW             import SAW, SA
from   _MOM.SQ                    import Q

import _MOM._Attr.Type
import _MOM._DBW._SAW.Manager

from   _TFL._Meta.Single_Dispatch import Single_Dispatch_Method
from   _TFL.predicate             import \
    bool_split, filtered_join, rsplit_hst, uniq

import _TFL._Meta.Object
import _TFL.Decorator

import datetime
import functools
import itertools
import math
import operator

MOM.Attr.A_Attr_Type.SAW_Column_Type = SA.schema.Column

class A_Join (TFL.Meta.Object) :
    """Encapsulate a join bound to an attribute"""

    def __init__ (self, toc, s_col, t_col, joiner, op = None) :
        self.table  = \
            toc if not isinstance (toc, SA.schema.Column) else toc.table
        self.cols   = s_col, t_col
        self.joiner = joiner
        self.op     = op if op is not None else operator.__eq__
    # end def __init__

    def __call__ (self, toj) :
        """Join to table or join `toj`"""
        return self.joiner (toj, self.table, self.op (* self.cols))
    # end def __call__

    def __repr__ (self) :
        return "<%s %s on (%s, %s)>" % \
            ((self.__class__.__name__, self.table) + self.cols)
    # end def __repr__

# end class A_Join

class _Kind_Wrapper_ (TFL.Meta.Object) :

    columns         = ()
    db_attrs_o      = db_attrs     = {}
    q_able_attrs_o  = q_able_attrs = {}

    _ETW            = TFL.Meta.Alias_Property ("ETW")

    def __init__ (self, ETW, kind, outer = None, parent = None) :
        self.ATW    = ETW.ATW
        self.ETW    = ETW
        self.PNS    = ETW.PNS
        self.DBW    = ETW.PNS.Manager
        self.kind   = kind
        self.attr   = kind.attr
        self.outer  = outer
        self.eff    = parent if parent is not None else self
    # end def __init__

    @TFL.Meta.Once_Property
    def ckd_name (self) :
        return filtered_join \
            ("__", (self.prefix, self.eff.attr._saw_column_name))
    # end def ckd_name

    @TFL.Meta.Once_Property
    def is_required (self) :
        return self.kind.is_required
    # end def is_required

    @TFL.Meta.Once_Property
    def is_surrogate (self) :
        return isinstance (self.eff.attr, MOM.Attr.A_Surrogate)
    # end def is_surrogate

    @TFL.Meta.Once_Property
    def name (self) :
        return filtered_join (".", (self.prefix, self.eff.attr.name))
    # end def name

    @TFL.Meta.Once_Property
    def prefix (self) :
        outer = self.outer
        if outer :
            return outer.ckd_name
        return ""
    # end def prefix

    @TFL.Meta.Once_Property
    def q_able_names (self) :
        result = self.attr.q_able_names
        if self is not self.eff :
            result = uniq (itertools.chain (result, self.eff.q_able_names))
        prefix = self.prefix
        if prefix :
            result = (".".join ((prefix, name)) for name in result)
        return tuple (sorted (result))
    # end def q_able_names

    @TFL.Meta.Once_Property
    def raw_name (self) :
        return filtered_join ("__", (self.prefix, self.eff.attr.raw_name))
    # end def raw_name

    @TFL.Meta.Once_Property
    def unique (self) :
        return (self.ckd_name, ) if self.eff.kind.is_primary else ()
    # end def unique

    def alias (self, ETW_alias, ** kw) :
        cls    = self.__class__
        result = cls.__new__      (cls)
        result.__dict__.update    (self.__dict__, ETW = ETW_alias, ** kw)
        self._setup_alias_columns (ETW_alias, result)
        return result
    # end def alias

    def col_values (self, entity) :
        return self.col_values_from_cargo (self.kind.get_pickle_cargo (entity))
    # end def col_values

    def col_values_from_cargo (self, pickle_cargo) :
        is_surrogate = self.is_surrogate
        for column, value in zip (self.columns, pickle_cargo) :
            if value is None :
                if is_surrogate :
                    continue
                elif not column.nullable :
                    try :
                        kind  = column.MOM_Kind
                        value = kind.raw_default \
                            if column.MOM_Is_Raw else kind.default
                    except AttributeError as exc :
                        print \
                            ( "*" * 3, self
                            , ".col_values_from_cargo got exception for"
                            , column, "MOM_Kind.default: ", exc
                            )
                        continue
            yield column.name, value
    # end def col_values

    def Derived (self, ETW, kind, outer = None) :
        if kind is self.kind :
            return self
        else :
            return self.__class__ (ETW, kind, outer = outer, parent = self.eff)
    # end def Derived

    def q_exp_bin (self, q_exp, QR, ETW, tail_name) :
        lcols, rcols, jxs = self._q_exp_bin_cols (q_exp, QR, ETW, tail_name)
        cols, jx          = self._q_exp_bin_combine \
            (q_exp, QR, ETW, tail_name, lcols, rcols)
        jxs += jx
        return cols, jxs
    # end def q_exp_bin

    def q_exp_call (self, q_exp, QR, ETW, tail_name) :
        func, args, jxs = self._q_exp_call_parts (q_exp, QR, ETW, tail_name)
        return (func (* args), ), jxs
    # end def q_exp_call

    def q_exp_func (self, q_exp, QR, ETW, tail_name) :
        lhs        = q_exp.lhs
        op_name    = q_exp.op.__name__.lower ()
        func       = getattr (SA.sql.func, op_name)
        cols, jxs  = lhs._saw_filter (QR, ETW)
        return [func (c) for c in cols], jxs
    # end def q_exp_func

    def q_exp_get \
            (self, q_getter, QR, col, tail_name, saw_name = "_saw_filter") :
        cols, jxs = [col], ()
        key       = q_getter._name
        if tail_name :
            ETW   = self.outer.ETW if self.outer else self.ETW
            try :
                t_col = ETW.QC [key]
            except KeyError :
                return self._q_exp_get_from_key \
                    (ETW, key, q_getter, QR, col, tail_name, "_saw_filter")
            if isinstance (t_col, _Kind_Wrapper_) :
                cols, jxs = t_col.q_exp_get \
                    (q_getter, QR, col, "", saw_name)
            else :
                cols = [t_col]
        if isinstance (q_getter, Q.RAW._Get_Raw_) :
            if len (cols) > 1 :
                raise TypeError \
                    ("Got more than 1 column for %s: %s" % (q_getter, cols))
            col = self.columns [0]
            akw = col.MOM_Wrapper
            if akw.attr.needs_raw_value :
                col  = akw.columns [-1]
                cols = [col]
        return cols, jxs
    # end def q_exp_get

    def q_exp_get_ob (self, q_getter, QR, col, tail_name) :
        return self.q_exp_get \
            (q_getter, QR, col, tail_name, saw_name = "_saw_order_by")
    # end def q_exp_get_ob

    def q_exp_get_ob_epk (self, q_getter, QR, head_col, tail_name) :
        ET     = self.attr.E_Type
        ETW    = ET._SAW
        result = obs, jxs = [], []
        if ET.epk_sig :
            for k in ET.epk_sig :
                q_g    = getattr (Q, k)
                ob, jx = q_g._saw_order_by (QR, ETW)
                obs.extend (ob)
                jxs.extend (jx)
            outer  = QR.polymorphic or not self.is_required
            joiner = TFL.Method.outerjoin if outer else TFL.Method.join
            jxs.extend (self._column_joins_pkn (ETW, obs, head_col, joiner))
        return result
    # end def q_exp_get_ob_epk

    def q_exp_una (self, q_exp, QR, ETW, tail_name) :
        lhs        = q_exp.lhs
        op_name    = q_exp.op.__name__
        cols, jxs  = lhs._saw_filter (QR, ETW)
        return [getattr (c, op_name) () for c in cols], jxs
    # end def q_exp_una

    def row_as_pickle_cargo (self, row) :
        result = tuple (row [c] for c in self.columns)
        return result
    # end def row_as_pickle_cargo

    def update_col_map (self, mapper, col_map, prefix = None, columns = None) :
        if columns is None :
            columns = self.columns
        for col in columns :
            names = self._col_q_able_names (col)
            for n in names :
                if prefix :
                    if n.startswith (prefix) :
                        n = n [len (prefix) + 1:]
                if n in col_map :
                    c_col = col_map [n]
                    if c_col is not col :
                        print \
                            ( "%s Name conflict for %s %r %r"
                            % ("*" * 5, self, c_col, col)
                            )
                else :
                    col_map [n] = col
    # end def update_col_map

    def _col_q_able_names (self, col) :
        w = col.MOM_Wrapper
        return (w.raw_name, ) if col.MOM_Is_Raw else w.q_able_names
    # end def _col_q_able_names

    def _column_joins (self, cols, head_col, joiner) :
        for col in cols :
            try :
                ### only do this for real columns
                ctab = col.table
            except AttributeError :
                pass
            else :
                yield (A_Join (col, col, head_col, joiner))
    # end def _column_joins

    def _column_joins_pkn (self, ETW, cols, head_col, joiner) :
        pkn = ETW.spk_name
        for col in cols :
            try :
                ### only do this for real columns
                ctab = col.table
            except AttributeError :
                pass
            else :
                yield (A_Join (col, ctab.c [pkn], head_col, joiner))
    # end def _column_joins_pkn

    def _q_exp_bin_apply (self, q_exp, QR, ETW, lhs, op_name, rhs) :
        return getattr (lhs, op_name) (rhs)
    # end def _q_exp_bin_apply

    def _q_exp_bin_cols (self, q_exp, QR, ETW, tail_name) :
        lhs        = q_exp.lhs
        rhs        = q_exp.rhs
        lcols, jxs = lhs._saw_filter (QR, ETW)
        try :
            sf     = getattr (rhs, "_saw_filter")
        except AttributeError :
            if isinstance (lhs, Q.RAW._Get_Raw_) :
                lcol0 = lcols and lcols [0]
                if not getattr (lcol0, "MOM_Is_Raw", False) :
                    lk = getattr (lcol0, "MOM_Kind", None)
                    if lk is not None :
                        rhs = lk.from_string (rhs)
            if isinstance (rhs, (MOM.Id_Entity, MOM.MD_Change)) :
                rhs = rhs.spk ### XXX ??? is this needed ???
            rcols = [rhs]
        else :
            rcols, rjxs  = sf (QR, ETW)
            jxs         += rjxs
        return lcols, rcols, jxs
    # end def _q_exp_bin_cols

    def _q_exp_bin_combine \
            (self, q_exp, QR, ETW, tail_name, lcols, rcols, jxs = ()) :
        op_name   = q_exp.op.__name__
        lhss, lxs = bool_split (lcols, Q.MOM_EXTRA)
        rhss, rxs = bool_split (rcols, Q.MOM_EXTRA)
        ll        = len (lhss)
        rl        = len (rhss)
        if rl == 1 < ll :
            rhss  = itertools.repeat (rhss [0], ll)
        elif ll != rl :
            raise NotImplementedError \
                ( "Cannot combine query expression `%s` for (%s, %s) "
                  "combination: %s, %s"
                % (q_exp, ll, rl, lcols, rcols)
                )
        applier   = functools.partial (self._q_exp_bin_apply, q_exp, QR, ETW)
        cols      = list (applier (l, op_name, r) for l, r in zip (lhss, rhss))
        extras    = lxs + rxs
        if extras :
            cols  = [SA.expression.and_ (* (cols + extras))]
        return cols, jxs
    # end def _q_exp_bin_combine

    def _q_exp_call_apply (self, q_exp, QR, ETW, lhs, op_name) :
        return getattr (lhs, op_name)
    # end def _q_exp_call_apply

    def _q_exp_call_parts (self, q_exp, QR, ETW, tail_name) :
        args       = q_exp.args
        lhs        = q_exp.lhs
        op_name    = q_exp.op.__name__
        cols, jxs  = lhs._saw_filter (QR, ETW)
        if len (cols) > 1 :
            raise ValueError ("%s expands to more than one column" % (q_exp, ))
        if op_name == "in_" :
            if len (args) > 1 :
                raise NotImplementedError \
                    ( "%s expression for more than 1 argument is "
                      "not implemented"
                    % (q_exp, )
                    )
            arg0 = args [0]
            if isinstance (arg0, MOM.DBW.SAW.Q_Result._Base_) :
                args = q_exp.args = (arg0.sa_query, )
        applier  = functools.partial (self._q_exp_call_apply, q_exp, QR, ETW)
        return applier (cols [0], op_name), args, jxs
    # end def _q_exp_call_parts

    def _q_exp_get_from_key \
            (self, ETW, key, q_getter, QR, col, tail_name, saw_name) :
        k, _, t = rsplit_hst (key, ".")
        if k and t :
            try :
                col = ETW.QC [k]
            except KeyError :
                pass
            else :
                try :
                    akw = col.MOM_Wrapper
                except AttributeError :
                    pass
                else :
                    return akw.q_exp_get_field (q_getter, QR, col, t, saw_name)
        raise TypeError \
            ( "Unknown column expression %s for %s"
            % (key, ETW.type_name)
            )
    # end def _q_exp_get_from_key

    def _setup_alias_columns (self, ETW_alias, result) :
        def _gen (self, ETW_alias, result) :
            for c in self.columns :
                ac             = ETW_alias._get_sa_col_alias (c)
                ac.MOM_Is_Raw  = getattr (c, "MOM_Is_Raw", False)
                ac.MOM_Kind    = self.kind
                ac.MOM_Wrapper = result
                yield ac
        result.__dict__ ["columns"] = tuple (_gen (self, ETW_alias, result))
    # end def _setup_alias_columns

    def __repr__ (self) :
        kind = self.kind
        return "<SAW : %s `%s` [%s]>" % \
            (kind.typ, self.name, ", ".join (str (c) for c in self.columns))
    # end def __repr__

# end class _Kind_Wrapper_

@TFL.Add_To_Class ("_SAW_Wrapper", MOM.Attr._DB_Attr_)
class Kind_Wrapper (_Kind_Wrapper_) :
    """SAW specific information about a db-attribute kind descriptor in
       the context of a specific E_Type_Wrapper
    """

    @TFL.Meta.Once_Property
    def columns (self) :
        eff = self.eff
        if eff is self :
            return self.kind._saw_columns (self.DBW, self)
        else :
            return eff.columns
    # end def columns

# end class Kind_Wrapper

@TFL.Add_To_Class ("_SAW_Wrapper", MOM.Attr._EPK_Mixin_)
class Kind_EPK_Wrapper (Kind_Wrapper) :
    """SAW specific information about an epk-referring db-attribute kind
       descriptor in the context of a specific E_Type_Wrapper
    """

    def q_exp_get \
            (self, q_getter, QR, head_col, tail_name, saw_name = "_saw_filter"):
        if tail_name and tail_name != "pid" :
            tq        = getattr (q_getter.Q, tail_name)
            method    = getattr (tq, saw_name)
            ETW, xtra = self.ETW.attr_join_etw_alias (self, self.attr.E_Type)
            cols, jxs = method  (QR, ETW)
            jxs       = list (jxs)
            cjxs      = []
            joiner    = \
                TFL.Method.outerjoin if QR.polymorphic else TFL.Method.join
            if not jxs :
                cjxs  = list \
                    (self._column_joins_pkn (ETW, cols, head_col, joiner))
            if xtra :
                a, b = xtra
                cjxs = list (self._column_joins ([a], b, joiner)) + cjxs
            if cjxs :
                jxs   = cjxs + jxs
            else :
                jcol  = ETW.spk_col
                jxs   = list \
                    (self._column_joins ([jcol], head_col, joiner)) + jxs
            return cols, jxs
        else :
            return [head_col], ()
    # end def q_exp_get

    def q_exp_get_ob (self, q_getter, QR, head_col, tail_name) :
        if tail_name :
            return self.__super.q_exp_get_ob (q_getter, QR, head_col, tail_name)
        else :
            return self.q_exp_get_ob_epk (q_getter, QR, head_col, tail_name)
    # end def q_exp_get_ob

    def _col_q_able_names (self, col) :
        ### Use `self.q_able_names` here to support derived attributes with
        ### q-able additional names, e.g., link roles
        return self.q_able_names
    # end def _col_q_able_names

    def _q_exp_bin_combine \
            (self, q_exp, QR, ETW, tail_name, lcols, rcols, jxs = ()) :
        op_name   = q_exp.op.__name__
        lhss, lxs = bool_split (lcols, Q.MOM_EXTRA)
        ll        = len (lhss)
        if ll == 1 and isinstance (lhss [0], Kind_Composite_Wrapper) :
            ### We get here for query expressions like::
            ###   `Q.person.lifetime == ("2013/07/15", )` for an E_Type where
            ###   `person` is an `_A_Id_Entity_`, e.g., PAP.Person_has_Phone
            akw       = lhss [0]
            q_getter  = q_exp.lhs
            k         = q_getter._name.split (".", 1) [1]
            lh        = getattr (Q, k)
            qx        = getattr (lh, op_name) (q_exp.rhs)
            akw_ETW   = akw.outer.ETW if akw.outer else akw.ETW
            spk_col   = akw_ETW.spk_col
            ref_col   = self.columns [0]
            outer     = QR.polymorphic or not akw.is_required
            joiner    = TFL.Method.outerjoin if outer else TFL.Method.join
            jxs      += tuple (self._column_joins ([spk_col], ref_col, joiner))
            cols, jxs = akw._q_exp_bin_combine \
                (qx, QR, ETW, "", [akw], rcols, jxs)
            if lxs :
                cols = [SA.expression.and_ (* (cols + lxs))]
            return cols, jxs
        else :
            return self.__super._q_exp_bin_combine \
                (q_exp, QR, ETW, tail_name, lcols, rcols, jxs)
    # end def _q_exp_bin_combine

# end class Kind_EPK_Wrapper

class _Kind_Wrapper_PQ_ (_Kind_Wrapper_) :

    @property
    def MOM_Wrapper (self) :
        return self
    # end def MOM_Wrapper

    @property
    def type_name (self) :
        return "%-40.40s" % (self, )
    # end def type_name

    def update_col_map (self, mapper, col_map, prefix = None) :
        if self.outer :
            col_map [self.attr.name] = self
        else :
            col_map.update ((qn, self) for qn in self.q_able_names)
    # end def update_col_map

# end class _Kind_Wrapper_PQ_

@TFL.Add_To_Class ("_SAW_Wrapper_PQ", MOM.Attr._DB_Attr_)
class Kind_Wrapper_P (_Kind_Wrapper_PQ_) :
    """SAW specific information about a partial db-attribute kind
       descriptor in the context of a specific E_Type_Wrapper
    """

    def q_exp_bin (self, q_exp, QR, ETW, tail_name) :
        lcols = []
        rcols = []
        jxs   = []
        for ETW in self.ETW.children :
            ls, rs, js = self._q_exp_bin_cols (q_exp, QR, ETW, tail_name)
            if 0 < len (ls) != len (rs) != 1 :
                raise NotImplementedError \
                    ( "Polymorphic query expression involving multiple "
                      "columns is not implemented: %s applied to %s --> %s, %s"
                    % (q_exp, ETW.type_name, ls, rs)
                    )
            lcols.extend (ls)
            rcols.extend (rs)
            jxs.extend   (js)
        wxs, jx = self._q_exp_bin_combine \
            (q_exp, QR, ETW, tail_name, lcols, rcols)
        jxs += jx
        return (SA.expression.or_ (* wxs), ), jxs
    # end def q_exp_bin

    def q_exp_call (self, q_exp, QR, ETW, tail_name) :
        calls   = []
        jxs     = []
        for ETW in self.ETW.children :
            func, args, js = self._q_exp_call_parts (q_exp, QR, ETW, tail_name)
            calls.append ((func, args))
            jxs.extend   (js)
        return (SA.expression.or_ (* tuple (f (* a) for f, a in calls)), ), jxs
    # end def q_exp_call

    def q_exp_func (self, q_exp, QR, ETW, tail_name) :
        lhs     = q_exp.lhs
        op_name = q_exp.op.__name__.lower ()
        func    = getattr (SA.sql.func, op_name)
        cols    = []
        jxs     = []
        for ETW in self.ETW.children :
            cs, jx = lhs._saw_filter (QR, ETW)
            if len (cs) > 1 :
                raise NotImplementedError \
                    ( "Polymorphic query expression involving multiple "
                      "columns is not implemented: %s applied to %s --> %s"
                    % (q_exp, ETW.type_name, cs)
                    )
            cols.extend (cs)
            jxs.extend  (js)
        return (SA.expression.or_ (* tuple (func (c) for c in cols)), ), jxs
    # end def q_exp_func

    def q_exp_get \
            (self, q_getter, QR, head_col, tail_name, saw_name = "_saw_filter"):
        jxs = []
        wxs = []
        for ETW in self.ETW.children :
            sf     = getattr (q_getter, saw_name)
            wx, jx = sf (QR, ETW)
            wxs.extend (wx)
            jxs.extend (jx)
        return wxs, jxs
    # end def q_exp_get

    def __repr__ (self) :
        tail = " (%s)" % \
            (" | ".join (sorted (c.type_name for c in self.ETW.children)), )
        kind = self.kind
        return "<SAW : %s `%s`%s>" % (kind.typ, self.name, tail)
    # end def __repr__

# end class Kind_Wrapper_P

@TFL.Add_To_Class ("_SAW_Wrapper_PQ", MOM.Attr.Query)
class Kind_Wrapper_Q (_Kind_Wrapper_PQ_) :
    """SAW specific information about an Query kind
       descriptor in the context of a specific E_Type_Wrapper
    """

    def q_exp_get \
            (self, q_getter, QR, head_col, tail_name, saw_name = "_saw_filter"):
        q = self.attr.query
        try :
            sf = getattr (q, saw_name)
        except AttributeError :
            raise TypeError ("Invalid filter criterion %s" % q_getter)
        ETW = self.outer if self.outer else self.ETW
        cols, jxs = sf (QR, ETW)
        if tail_name :
            ### if `q` resolves to ref-attribute(s), we need to delegate
            ### `tail_name` to that/those
            t_cols = []
            jxs    = list (jxs)
            for c in cols :
                try :
                    w = c.MOM_Wrapper
                except AttributeError :
                    raise TypeError \
                        ("%s doesn't support access to %s" % (c, tail_name))
                else :
                    qg     = getattr (getattr (Q, w.attr.name), tail_name)
                    sf     = getattr (qg, saw_name)
                    cs, js = sf (QR, w.ETW)
                    t_cols.extend (cs)
                    jxs.extend    (js)
            cols = t_cols
        return cols, jxs
    # end def q_exp_get

    def __repr__ (self) :
        kind = self.kind
        return "<SAW : %s `%s`>" % (kind.typ, self.name)
    # end def __repr__

# end class Kind_Wrapper_Q

@TFL.Add_To_Class ("_SAW_Wrapper_PQ", MOM.Attr._Rev_Query_)
class Kind_Wrapper_R (_Kind_Wrapper_PQ_) :
    """SAW specific information about an _Rev_Query_ kind
       descriptor in the context of a specific E_Type_Wrapper
    """

    @TFL.Decorator
    def _wrap_super_q_exp (method) :
        method_name = method.__name__
        def _ (self, q_exp, QR, ETW, tail_name) :
            super_method = getattr (self.__super, method_name)
            cols, jxs    = super_method (q_exp, QR, ETW, tail_name)
            if self.attr.Ref_Type._SAW.sa_table is None :
                ### polymorphic : need to OR the expressions of the children
                cols = [SA.expression.or_ (* cols)]
            return cols, jxs
        return _
    # end def _wrap_super_q_exp

    @_wrap_super_q_exp
    def q_exp_bin (self, q_exp, QR, ETW, tail_name) :
        pass

    @_wrap_super_q_exp
    def q_exp_call (self, q_exp, QR, ETW, tail_name) :
        pass

    @_wrap_super_q_exp
    def q_exp_func (self, q_exp, QR, ETW, tail_name) :
        pass

    def q_exp_get \
            (self, q_getter, QR, head_col, tail_name, saw_name = "_saw_filter"):
        Q             = q_getter.Q ### might be `Q.RAW`
        attr          = self.attr
        ETW           = self.outer.ETW if self.outer else self.ETW
        spk_col       = ETW.spk_col
        ref_etw, xtra = self.ETW.attr_join_etw_alias (self, attr.Ref_Type)
        ref_col       = ref_etw.QC [attr.ref_name]
        ref_filter    = attr.ref_filter (Q)
        polymorph     = ref_etw.sa_table is None
        x_cols        = []
        with QR.LET (polymorphic = polymorph or QR.polymorphic) :
            if not polymorph :
                joiner    = TFL.Method.join
                cols, jxs = [ref_col], []
            else :
                joiner    = TFL.Method.outerjoin
                cols, jxs = ref_col.q_exp_get \
                    (ref_filter, QR, ref_col, "", saw_name)
            if xtra :
                a, b = xtra
                jxs.extend (self._column_joins ([a], b, joiner))
            jxs.extend (self._column_joins (cols, spk_col, joiner))
            if attr.sqx_filter is not None :
                ### if called from `q_exp_bin`, ... `q_exp_una` the
                ### col-expressions from `sqx_filter` must not
                ### participate in those operations:
                ###     --> mark as `MOM_EXTRA`
                sqx_method = getattr (attr.sqx_filter, saw_name)
                for c in cols :
                    xcs, xjxs = sqx_method (QR, ref_etw)
                    x_cols.extend (xcs)
                    jxs.extend    (xjxs)
            rev_sq = attr.sqx (spk_col)
            if rev_sq._attr :
                ### `A_Role_Ref` and `A_Role_Ref_Set` need this
                ### need to get the right alias here so that `join` and
                ### `q_getter_ref` for `tail_name` (next `if` below) match
                ref_col       = ref_etw.QC [rev_sq._attr]
                ref_wrapper   = ref_col.MOM_Wrapper
                ref_etw, xtra = ref_wrapper.ETW.attr_join_etw_alias \
                    (ref_wrapper, ref_wrapper.attr.E_Type)
                cols, rjxs    = ref_col.MOM_Wrapper.q_exp_get \
                    (getattr (Q, tail_name), QR, ref_col, tail_name, saw_name)
                if xtra :
                    a, b = xtra
                    jxs.extend (self._column_joins ([a], b, joiner))
                jxs.extend (rjxs)
            if tail_name and tail_name != "pid" and saw_name == "_saw_filter" :
                q_getter_ref = getattr (Q, tail_name)
                cols, rjxs   = q_getter_ref._saw_filter (QR, ref_etw)
                jxs.extend (rjxs)
        cols = tuple (uniq (cols))
        if x_cols :
            def _gen (xs) :
                for x in xs :
                    x.MOM_EXTRA = True
                    yield x
            cols = tuple (itertools.chain (cols, _gen (x_cols)))
        return cols, jxs
    # end def q_exp_get

    def q_exp_get_ob (self, q_getter, QR, head_col, tail_name) :
        if tail_name :
            return self.__super.q_exp_get_ob (q_getter, QR, head_col, tail_name)
        else :
            return self.q_exp_get_ob_epk (q_getter, QR, head_col, tail_name)
    # end def q_exp_get_ob

    @_wrap_super_q_exp
    def q_exp_una (self, q_exp, QR, ETW, tail_name) :
        pass

    def _q_exp_bin_combine \
            (self, q_exp, QR, ETW, tail_name, lcols, rcols, jxs = ()) :
        op_name   = q_exp.op.__name__
        lhss, lxs = bool_split (lcols, Q.MOM_EXTRA)
        ll        = len (lhss)
        if ll == 1 and isinstance (lhss [0], Kind_Composite_Wrapper) :
            ### We get here for query expressions like::
            ###   `Q.person.lifetime == ("2013/07/15", )` for an E_Type where
            ###   `person` is a `Rev_Ref`, e.g., of `Auth.Account`
            akw      = lhss [0]
            q_getter = q_exp.lhs
            k        = q_getter._name.split (".", 1) [1]
            lh       = getattr (Q, k)
            qx       = getattr (lh, op_name) (q_exp.rhs)
            cols, jxs = akw._q_exp_bin_combine \
                (qx, QR, ETW, "", [akw], rcols, jxs)
            if lxs :
                cols = [SA.expression.and_ (* (cols + lxs))]
            return cols, jxs
        else :
            return self.__super._q_exp_bin_combine \
                (q_exp, QR, ETW, tail_name, lcols, rcols, jxs)
    # end def _q_exp_bin_combine

    def __repr__ (self) :
        kind = self.kind
        return "<SAW : %s `%s`>" % (kind.typ, self.name)
    # end def __repr__

# end class Kind_Wrapper_R

@TFL.Add_To_Class ("_SAW_Wrapper", MOM.Attr._Composite_Mixin_)
class Kind_Composite_Wrapper (_Kind_Wrapper_) :
    """SAW specific information about an composite-attribute kind descriptor in
       the context of a specific E_Type_Wrapper
    """

    is_surrogate   = False
    q_able_attrs_i = {}

    def __init__ (self, ETW, kind, outer = None, parent = None) :
        self.e_type = kind.attr.P_Type
        self.__super.__init__ (ETW, kind, outer = outer, parent = parent)
        self._setup_attrs     (ETW, parent)
    # end def __init__

    @TFL.Meta.Once_Property
    def columns (self) :
        def _gen (self) :
            for an, akw in sorted (pyk.iteritems (self.db_attrs_o)) :
                yield akw.columns
        return tuple (itertools.chain (* _gen (self)))
    # end def columns

    @TFL.Meta.Once_Property
    def type_name (self) :
        return self.attr.E_Type.type_name
    # end def type_name

    @TFL.Meta.Once_Property
    def unique (self) :
        if self.kind.is_primary :
            return tuple \
                (akw.ckd_name for akw in pyk.itervalues (self.db_attrs))
        return ()
    # end def unique

    def alias (self, ETW_alias, ** kw) :
        result = self.__super.alias (ETW_alias, ** kw)
        self._setup_alias_attrs     (ETW_alias, result)
        return result
    # end def alias

    def col_values (self, entity) :
        c_entity = self.kind.get_value (entity)
        for kind_wrapper in pyk.itervalues (self.db_attrs) :
            for k, v in kind_wrapper.col_values (c_entity) :
                yield k, v
    # end def col_values

    def col_values_from_cargo (self, pickle_cargos) :
        pickle_cargo = pickle_cargos [0]
        for name, kind_wrapper in pyk.iteritems (self.db_attrs) :
            attr_pc = pickle_cargo.get (name)
            if attr_pc is not None :
                for k, v in kind_wrapper.col_values_from_cargo (attr_pc) :
                    yield k, v
    # end def col_values

    def q_exp_get \
            (self, q_getter, QR, head_col, tail_name, saw_name = "_saw_filter"):
        if tail_name :
            return self.__super.q_exp_get \
                (q_getter, QR, head_col, tail_name, saw_name)
        else :
            return [self], ()
    # end def q_exp_get

    def q_exp_get_ob (self, q_getter, QR, head_col, tail_name) :
        if tail_name :
            result = self.__super.q_exp_get_ob \
                (q_getter, QR, head_col, tail_name)
        else :
            ET     = self.attr.E_Type
            result = obs, jxs = [], []
            if ET.usr_sig :
                for k in ET.usr_sig :
                    ob, jx = self.q_exp_get_ob \
                        (getattr (q_getter, k), QR, head_col, k)
                    obs.extend (ob)
                    jxs.extend (jx)
        return result
    # end def q_exp_get_ob

    def row_as_pickle_cargo (self, row) :
        return (self.ETW.row_as_pickle_cargo (row, self.db_attrs), )
    # end def row_as_pickle_cargo

    def update_col_map (self, mapper, col_map, prefix = None) :
        self.__super.update_col_map (mapper, col_map)
        self._setup_QC (mapper.__class__ (self, self.ckd_name), col_map)
    # end def update_col_map

    def _q_exp_bin_combine \
            (self, q_exp, QR, ETW, tail_name, lcols, rcols, jxs = ()) :
        if tail_name :
            return self.__super._q_exp_bin_combine \
                (q_exp, QR, ETW, tail_name, lcols, rcols, jxs)
        else :
            assert lcols [0] is self
            ET       = self.attr.E_Type
            q_getter = q_exp.lhs
            op_name  = q_exp.op.__name__
            lcols    = []
            rcol0    = rcols and rcols [0]
            if isinstance (rcol0, ET) :
                rcols = rcol0.attr_tuple ()
            if isinstance (rcols, (tuple, list)) :
                for k in ET.usr_sig [:len (rcols)]:
                    ob, jx = self.q_exp_get_ob \
                        (getattr (q_getter, k), QR, self, k)
                    lcols.extend (ob)
                    jxs += jx
            elif isinstance (rcols, dict) :
                rcols_list = []
                for k, v in pyk.iteritems (rcols) :
                    ob, jx = self.q_exp_get_ob \
                        (getattr (q_getter, k), QR, self, k)
                    lcols.extend      (ob)
                    rcols_list.append (v)
                    jxs += jx
                rcols = rcols_list
            return self.__super._q_exp_bin_combine \
                (q_exp, QR, ETW, tail_name, lcols, rcols, jxs)
    # end def _q_exp_bin_combine

    def _setup_alias_attrs (self, ETW_alias, result) :
        parent = result.eff
        result.db_attrs_o = result.db_attrs = dict \
            (  (k, v.alias (ETW_alias, outer = result, parent = parent))
            for k, v in pyk.iteritems (self.db_attrs)
            )
        result.q_able_attrs_o = result.q_able_attrs = dict (result.db_attrs)
        result.q_able_attrs.update \
            (  (k, v.alias (ETW_alias, outer = result, parent = parent))
            for k, v in pyk.iteritems (self.q_able_attrs)
            if  k not in result.db_attrs
            )
    # end def _setup_alias_attrs

    def _setup_alias_columns (self, ETW_alias, result) :
        ### let Once_Property `columns` do its work for `result`
        result.__dict__.pop ("columns", None)
    # end def _setup_alias_columns

    def _setup_attrs (self, ETW, parent) :
        PNS      = self.PNS
        e_type   = self.attr.P_Type
        PTW      = ETW.ATW [e_type]
        self.db_attrs_o = self.db_attrs = dict \
            (   ( a.name
                , a._saw_kind_wrapper
                    (PTW.DBW, PTW, outer = self, parent = parent)
                )
            for a in e_type.db_attr
            )
        self.q_able_attrs_o = self.q_able_attrs = dict (self.db_attrs)
        self.q_able_attrs.update \
            (   ( a.name
                , a._saw_kind_wrapper_pq
                    (PTW.DBW, PTW, outer = self, parent = parent)
                )
            for a in e_type.q_able
            if  a.name not in self.db_attrs
            )
    # end def _setup_attrs

    def _setup_QC (self, QC, col_map) :
        self.QC        = QC
        QC.MOM_Wrapper = self
        col_map.update ((qn, QC) for qn in self.q_able_names)
        for k, akw in pyk.iteritems (self.q_able_attrs) :
            if k not in self.db_attrs :
                col_map [akw.name] = akw
    # end def _setup_QC

    def __getattr__ (self, name) :
        if name == "QC" :
            try :
                self.ETW.QC.Map ### trigger setup of `QC`
            except Exception as exc :
                raise AttributeError \
                    ("Access to `QC` of %s triggered %s" % (self, exc))
            else :
                return self.QC
        raise AttributeError (name)
    # end def __getattr__

# end class Kind_Composite_Wrapper

class _Kind_Wrapper_Field_Extractor_ (_Kind_Wrapper_) :
    """Kind wrapper that can extract fields from the column"""

    fields = set ()

    def q_exp_get_field \
            (self, q_getter, QR, col, tail_name, saw_name = "_saw_filter") :
        if tail_name in self.fields :
            f = self.attr._saw_extract_field (self.ETW.DBW, col, tail_name)
            cols, jxs = [f], ()
        else :
            raise AttributeError (tail_name)
        return cols, jxs
    # end def q_exp_get

# end class _Kind_Wrapper_Field_Extractor_

@TFL.Add_To_Class ("_SAW_Wrapper", MOM.Attr.A_Date)
class Kind_Date_Wrapper (_Kind_Wrapper_Field_Extractor_, Kind_Wrapper) :

    fields = set (("year", "month", "day"))

# end class Kind_Date_Wrapper

@TFL.Add_To_Class ("_SAW_Wrapper", MOM.Attr.A_Time)
class Kind_Time_Wrapper (_Kind_Wrapper_Field_Extractor_, Kind_Wrapper) :

    fields = set (("hour", "minute", "second"))

# end class Kind_Time_Wrapper

@TFL.Add_To_Class ("_SAW_Wrapper", MOM.Attr.A_Date_Time)
class Kind_Date_Time_Wrapper (_Kind_Wrapper_Field_Extractor_, Kind_Wrapper) :

    fields = Kind_Date_Wrapper.fields | Kind_Time_Wrapper.fields

# end class Kind_Date_Time_Wrapper

### Attr-Kind specific functions returning the right Kind_Wrapper ##############
MOM.Attr.A_Attr_Type._SAW_Wrapper      = None
MOM.Attr.A_Attr_Type._saw_kind_wrapper = None

@TFL.Add_To_Class ("_saw_kind_wrapper", MOM.Attr.Kind)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_kind_wrapper (self, DBW, ETW, ** kw) :
    attr = self.attr
    skw  = attr._saw_kind_wrapper
    if skw is not None :
        result = skw (DBW, ETW, self, ** kw)
    else :
        SW     = attr._SAW_Wrapper if attr._SAW_Wrapper else self._SAW_Wrapper
        result = SW  (ETW, self, ** kw)
    return result
# end def _saw_kind_wrapper

@TFL.Add_To_Class ("_saw_kind_wrapper_pq", MOM.Attr.Kind)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_kind_wrapper_pq (self, DBW, ETW, ** kw) :
    return self._SAW_Wrapper_PQ (ETW, self, ** kw)
# end def _saw_kind_wrapper_pq

### Attr-Kind specific functions returning column keyword arguments ############
@TFL.Add_To_Class ("_saw_column_kw", MOM.Attr.Kind)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_kw (self, DBW) :
    default = self.attr.default
    is_None = default is None
    result  = dict (nullable = is_None)
    if not is_None :
        result.update (default = default)
    return result
# end def _saw_column_kw

@TFL.Add_To_Class ("_saw_column_kw", MOM.Attr.Primary)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_kw_primary (self, DBW) :
    result              = super (MOM.Attr.Primary, self)._saw_column_kw (DBW)
    result ["nullable"] = False
    return result
# end def _saw_column_kw_primary

### Attr-Kind specific functions returning columns #############################
@TFL.Add_To_Class ("_saw_columns", MOM.Attr.Kind)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_columns_kind (self, DBW, wrapper) :
    attr = self.attr
    return attr._saw_columns (DBW, wrapper, ** self._saw_column_kw (DBW))
# end def _saw_columns_kind

@TFL.Add_To_Class ("_saw_columns", MOM.Attr._Raw_Value_Mixin_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_columns_raw_kind (self, DBW, wrapper) :
    attr     = self.attr
    raw_name = wrapper.raw_name
    raw_type = DBW.PNS.Attr._saw_column_type_string \
        (self, DBW, wrapper, attr.Pickled_Type_Raw)
    raw_col  = SA.schema.Column \
        (raw_name, raw_type, default = attr.raw_default or "")
    raw_col.MOM_Is_Raw  = True
    raw_col.MOM_Kind    = wrapper.kind
    raw_col.MOM_Wrapper = wrapper
    return super (MOM.Attr._Raw_Value_Mixin_, self)._saw_columns \
        (DBW, wrapper) + (raw_col, )
# end def _saw_columns_raw_kind

### Attr-Type specific functions returning column names ########################
@TFL.Add_To_Class ("_saw_column_name", MOM.Attr.A_Attr_Type)
@property
def _saw_column_name (self) :
    return self.name.lower ()
# end def _saw_column_name

### Attr-Type specific functions returning columns #############################
@TFL.Add_To_Class ("_saw_one_typed_column", MOM.Attr.A_Attr_Type)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_one_typed_column (self, DBW, wrapper, col_type, * args, ** kw) :
    col = self.SAW_Column_Type (wrapper.ckd_name, col_type, * args, ** kw)
    col.MOM_Is_Raw  = False
    col.MOM_Kind    = wrapper.kind
    col.MOM_Wrapper = wrapper
    return (col, )
# end def _saw_one_typed_column

@TFL.Add_To_Class ("_saw_columns", MOM.Attr.A_Attr_Type)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_columns_type (self, DBW, wrapper, ** kw) :
    col_type = self._saw_column_type (DBW, wrapper, self.Pickled_Type)
    return self._saw_one_typed_column (DBW, wrapper, col_type, ** kw)
# end def _saw_columns_type

@TFL.Add_To_Class ("_saw_columns", MOM.Attr._A_Composite_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_columns_composite (self, DBW, wrapper, ** kw) :
    raise RuntimeError \
        ( "_saw_columns_composite should never be called for %s.%s"
        % (self.det, self.name)
        )
# end def _saw_columns_composite

@TFL.Add_To_Class ("_saw_columns", MOM.Attr._A_Id_Entity_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_columns_id_entity (self, DBW, wrapper, ** kw) :
    col_type = wrapper.ATW.SA_Type.Id_Entity
    result = self._saw_one_typed_column (DBW, wrapper, col_type, ** kw)
    wrapper.ETW.fk_cols.append (result [0])
    return result
# end def _saw_columns_id_entity

@TFL.Add_To_Class ("_saw_columns", MOM.Attr._A_Named_Value_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_columns_named_value (self, DBW, wrapper, ** kw) :
    Type = self.C_Type
    if Type :
        if MOM.Attr.is_attr_type (Type) :
            pts            = self.Pickled_Type
            col_type       = Type._saw_column_type (self, DBW, wrapper, pts)
        else :
            pts            = Type.Pickled_Type
            pts._attr_type = self
            col_type       = self._saw_column_type (DBW, wrapper, pts)
        result = self._saw_one_typed_column (DBW, wrapper, col_type, ** kw)
    else :
        result = super (MOM.Attr._A_Named_Value_, self)._saw_columns \
            (DBW, wrapper, ** kw)
    return result
# end def _saw_columns_named_value

@TFL.Add_To_Class ("_saw_columns", MOM.Attr.A_Surrogate)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_columns_surrogate (self, DBW, wrapper, ** kw) :
    seq      = wrapper.ETW.sequence
    col_args = seq.col_args if seq.sa_column is None else ()
    col_type = DBW.PNS.Attr._saw_column_type_int \
        (self, DBW, wrapper, self.Pickled_Type)
    return self._saw_one_typed_column \
        (DBW, wrapper, col_type, * col_args, primary_key = True, ** kw)
# end def _saw_columns_surrogate

### Attr-Type specific functions returning sa-specific types ###################
@TFL.Add_To_Class ("_saw_column_type", MOM.Attr.A_Attr_Type)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type (self, DBW, wrapper, pts) :
    p_type = pts.p_type
    if p_type is None :
        raise TypeError \
            ( "Attribute %s.%s needs either a `Pickler` with `Type` or "
              "a `P_Type` definition"
            % (wrapper.kind.e_type.type_name, wrapper.kind, )
            )
    elif p_type is pyk.text_type :
        result = DBW.PNS.Attr._saw_column_type_string (self, DBW, wrapper, pts)
    else :
        if pts._Pickler_Type is not None :
            result = pts._Pickler_Type._saw_column_type \
                (self, DBW, wrapper, pts)
        else :
            p_type_map = wrapper.ATW.SA_Type.P_Type_Map
            try :
                col_type = p_type_map [p_type]
            except KeyError :
                raise TypeError \
                    ( "`P_Type` %s is not supported for `%s`; "
                      "use one of `%s` or extend MOM.DBW.SAW.Attr"
                    % ( p_type, wrapper.kind
                      , sorted (t.__name__ for t in p_type_map)
                      )
                    )
            else :
                result = col_type ()
    return result
# end def _saw_column_type

@TFL.Add_To_Class ("_saw_column_type", MOM.Attr._A_Binary_String_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type_binary_string (self, DBW, wrapper, pts) :
    return wrapper.ATW.SA_Type.LargeBinary (pts.max_length)
# end def _saw_column_type_binary_string

@TFL.Add_To_Class ("_saw_column_type", MOM.Attr.A_Binary_String_P)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type_binary_string_pickled (self, DBW, wrapper, pts) :
    return wrapper.ATW.SA_Type.PickleType ()
# end def _saw_column_type_binary_string_pickled

@TFL.Add_To_Class ("_saw_column_type", MOM.Attr.A_Decimal)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type_decimal (self, DBW, wrapper, pts) :
    return wrapper.ATW.SA_Type.Numeric (pts.max_digits, pts.decimal_places)
# end def _saw_column_type_decimal

@TFL.Add_To_Class ("_saw_column_type", MOM.Attr._A_Int_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type_int (self, DBW, wrapper, pts) :
    return wrapper.ATW.SA_Type.sized_int_type (pts)
# end def _saw_column_type_int

@TFL.Add_To_Class ("_saw_column_type", MOM.Attr._A_String_Base_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type_string (self, DBW, wrapper, pts) :
    kw     = dict (convert_unicode = pts.p_type is pyk.text_type)
    length = pts.length
    if length :
        kw.update (length = length)
        sa_type = wrapper.ATW.SA_Type.String
    else :
        sa_type = wrapper.ATW.SA_Type.Text
    return sa_type (** kw)
# end def _saw_column_type_string

@TFL.Add_To_Class \
    ( "_saw_column_type"
    , MOM.Id_Entity.E_Spec._Attributes.type_name
    , MOM.MD_Change.E_Spec._Attributes.type_name
    )
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type_type_name (self, DBW, wrapper, pts) :
    return wrapper.ATW.SA_Type.Type_Name
# end def _saw_column_type_type_name

### Functions to check column for truth ########################################

@TFL.Add_To_Class ("_saw_bool", MOM.Attr.Kind)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_bool_kind (self, DBW, col) :
    not_null = col != None
    result   = self.attr._saw_bool (DBW, col)
    if result is None :
        result = not_null
    elif col.nullable :
        result = not_null & result
    return result
# end def _saw_bool_kind

@TFL.Add_To_Class ("_saw_bool", MOM.Attr._Raw_Value_Mixin_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_bool_raw (self, DBW, col) :
    if col.MOM_Is_Raw :
        result = col != ""
        if col.nullable :
            result = (col != None) & result
    else :
        result = super (MOM.Attr._Raw_Value_Mixin_, self)._saw_bool (DBW, col)
    return result
# end def _saw_bool_raw

MOM.Attr.A_Attr_Type._saw_bool = None

@TFL.Add_To_Class ("_saw_bool", MOM.Attr.A_Attr_Type)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_bool_type (self, DBW, col) :
    pass
# end def _saw_bool_type

@TFL.Add_To_Class ("_saw_bool", MOM.Attr.A_Boolean)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_bool_bool (self, DBW, col) :
    return col == True
# end def _saw_bool_bool

@TFL.Add_To_Class ("_saw_bool", MOM.Attr._A_Number_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_bool_number (self, DBW, col) :
    return col != self.cooked (0)
# end def _saw_bool_number

@TFL.Add_To_Class ("_saw_bool", MOM.Attr._A_String_Base_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_bool_string (self, DBW, col) :
    if self.default == "" :
        return col != ""
# end def _saw_bool_string

def fix_bool (QR, ETW, wxs) :
    def _gen (DBW, wxs) :
        for wx in wxs :
            if isinstance (wx, SA.schema.Column) :
                try :
                    ak = wx.MOM_Kind
                except AttributeError :
                    pass
                else :
                    wx = ak._saw_bool (DBW, wx)
            yield wx
    result = tuple (_gen (ETW.DBW, wxs))
    if all (isinstance (wx, SA.schema.Column)  for wx in wxs) :
        result = (SA.expression.or_ (* result), )
    return result
# end def fix_bool

### Functions to extract fields from date column ##############################
@TFL.Add_To_Class ("_saw_extract_field", MOM.Attr._A_Date_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_extract_date_field (self, DBW, col, field) :
    return SA.sql.extract (field, col)
# end def _saw_extract_date_field

if __name__ != "__main__" :
    MOM.DBW.SAW._Export_Module ()
### __END__ MOM.DBW.SAW.Attr

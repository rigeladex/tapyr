# -*- coding: iso-8859-15 -*-
# Copyright (C) 2011 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.NAV.E_Type.
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
#    GTW.NAV.E_Type.Query_Restriction
#
# Purpose
#    Model a query restriction as specified by `req_data` of a `GET` request
#
# Revision Dates
#    14-Nov-2011 (CT) Creation
#    16-Nov-2011 (CT) Creation continued (order_by, ...)
#    17-Nov-2011 (CT) Creation continued.. (NEXT, PREV, ...)
#    19-Nov-2011 (CT) Creation continued... (FIRST, LAST)
#    21-Nov-2011 (CT) Creation continued... (order_by_names, order_by_ui_names)
#    22-Nov-2011 (CT) Creation continued.... (Query_Restriction_Spec)
#    23-Nov-2011 (CT) Creation continued.... (fix `offset_f`, add `op_map`)
#    25-Nov-2011 (CT) Creation continued..... (restrict `offset_f` to `total_f`)
#    26-Nov-2011 (CT) Creation continued...... (fix `offset` and `offset_f`)
#     2-Dec-2011 (CT) Creation continued....... (guard `sig_map` for `f`...)
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL
from   _MOM.import_MOM          import MOM, Q

import _GTW._NAV._E_Type

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Record

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import uniq
from   _TFL.Regexp              import Regexp, re

from   itertools                import chain as ichain
import json

class Query_Restriction (TFL.Meta.Object) :
    """Model a query restriction as specified by `req_data` of a `GET` request."""

    filters     = ()
    filters_q   = ()
    limit       = 0
    name_sep    = MOM.Attr.Filter.id_sep
    offset      = 0
    op_sep      = "___"
    order_by    = ()
    order_by_q  = ()
    query_b     = None
    query_f     = None
    ui_sep      = MOM.Attr.Filter.ui_sep

    _a_pat      = Regexp \
        ( "".join
            ( ( r"(?P<name> [a-zA-Z0-9]+ (?: _{1,2}[a-zA-Z0-9]+)*)"
              , op_sep
              , r"(?P<op> [A-Z]+)"
              , r"$"
              )
            )
        , re.VERBOSE
        )

    @classmethod
    def from_request_data (cls, E_Type, req_data) :
        data   = dict (req_data.iteritems ())
        result = cls \
            ( limit           = data.pop ("limit",  None)
            , offset          = data.pop ("offset", None)
            , other_req_data  = data
            )
        limit = result.limit
        if limit :
            if "LAST" in data :
                result.offset = - limit
            elif "FIRST" in data :
                result.offset = 0
            elif "NEXT" in data :
                result.offset += limit
            elif "PREV" in data :
                result.offset  = result.offset - limit
        elif "FIRST" in data or "PREV" in data :
            result.offset = 0
        result._setup_filters  (E_Type, data)
        result._setup_order_by (E_Type, data)
        return result
    # end def from_request_data

    def __init__ (self, limit = None, offset = None, ** kw) :
        if limit :
            self.limit  = max (int (limit), 0)
        if offset :
            self.offset = int (offset)
        self.__dict__.update (kw)
    # end def __init__

    def __call__ (self, base_query) :
        self.query_b = base_query
        result = base_query
        if self.filters_q :
            result = result.filter (* self.filters_q)
        if self.order_by_q :
            result = result.order_by (self.order_by_q)
        self.query_f = result
        offset = self.offset_f
        if offset :
            result = result.offset   (offset)
        if self.limit :
            result = result.limit    (self.limit)
        return result
    # end def __call__

    @Once_Property
    def next_p (self) :
        limit  = self.limit
        if limit :
            offset = self.offset_f
            total  = self.total_f
            return offset + limit < total
    # end def next_p

    @Once_Property
    def offset_f (self) :
        result  = self.offset
        total_f = self.total_f
        limit   = self.limit
        if result < - total_f :
            result = self.offset = 0
        elif result < 0 :
            result = total_f + result
        result = max (min (result, total_f - limit), 0)
        return result
    # end def offset_f

    @Once_Property
    def order_by_names (self) :
        if self.order_by :
            return ", ".join (ob.name for ob in self.order_by)
    # end def order_by_names

    @Once_Property
    def order_by_ui_names (self) :
        if self.order_by :
            return ", ".join \
                (   "%s%s" % (ob.sign, "/".join (ob.ui_names))
                for ob in self.order_by
                )
    # end def order_by_ui_names

    @Once_Property
    def prev_p (self) :
        return self.offset_f > 0
    # end def prev_p

    @Once_Property
    def total_f (self) :
        if self.query_f is not None :
            return self.query_f.count ()
        return 0
    # end def total_f

    @Once_Property
    def total_u (self) :
        if self.query_b is not None :
            return self.query_b.count ()
        return 0
    # end def total_u

    def _filter_matches (self, data, pat) :
        for k in sorted (data) :
            if pat.match (k) :
                yield k, pat
    # end def _filter_matches

    def _nested_attrs (self, E_Type, names) :
        T = E_Type
        for name in names :
            attr = getattr (T, name)
            yield attr
            T = getattr (attr, "E_Type", None)
    # end def _nested_attrs

    def _setup_attr (self, E_Type, pat, k, value) :
        name   = pat.name
        op     = pat.op
        names  = name.split ("__")
        attrs  = tuple (self._nested_attrs (E_Type, names))
        q      = attrs [-1].Q
        prefix = ".".join (names [:-1]) or None
        qop    = getattr (q, op)
        f = TFL.Record \
            ( attr     = attrs [-1]
            , key      = k
            , name     = ".".join (names)
            , op       = qop.op_sym
            , op_nam   = _T (qop.op_nam)
            , op_desc  = _T (qop.desc)
            , ui_names = tuple (_T (a.ui_name) for a in attrs)
            , value    = value
            )
        return f, qop (value, prefix)
    # end def _setup_attr

    def _setup_filters (self, E_Type, data) :
        matches = tuple \
            (   self._setup_attr (E_Type, pat, k, data.pop (k))
            for k, pat in self._filter_matches (data, self._a_pat)
            )
        if matches :
            self.filters, self.filters_q = zip (* matches)
    # end def _setup_filters

    def _setup_order_by_1 (self, E_Type, s) :
        s     = s.strip ()
        sign  = "-" if s.startswith ("-") else ""
        names = s [bool (sign): ].split (".")
        attrs = tuple (self._nested_attrs (E_Type, names))
        last  = attrs [-1]
        ET    = getattr (attrs [-1], "E_Type", None)
        if ET :
            pre  = ".".join (names)
            keys = tuple ("%s%s.%s" % (sign, pre, k) for k in ET.sorted_by)
        else :
            keys = (s, )
        f = TFL.Record \
            ( attr     = attrs [-1]
            , name     = s
            , sign     = sign
            , ui_names = tuple (_T (a.ui_name) for a in attrs)
            )
        return f, keys
    # end def _setup_order_by_1

    def _setup_order_by (self, E_Type, data) :
        s = data.pop ("order_by", "").strip ()
        if s :
            order_by = \
                (self._setup_order_by_1 (E_Type, n) for n in s.split (","))
            self.order_by, criteria = zip (* order_by)
            self.order_by_q = TFL.Sorted_By (* ichain (* criteria))
    # end def _setup_order_by

    def __nonzero__ (self) :
        return bool (self.limit or self.offset or self.filters_q)
    # end def __nonzero__

# end class Query_Restriction

class Query_Restriction_Spec (TFL.Meta.Object) :
    """Query restriction spec for a GTW.NAV.E_Type page."""

    def __init__ (self, E_Type, field_names) :
        self.E_Type = E_Type
        self.field_names = field_names
    # end def __init__

    @property
    def as_json (self) :
        return json.dumps (self.as_json_cargo, sort_keys = True)
    # end def as_json

    @property
    def as_json_cargo (self) :
        return dict \
            ( filters   = [f.as_json_cargo for f in self.filters]
            , name_sep  = Query_Restriction.name_sep
            , op_map    = self.op_map
            , op_sep    = Query_Restriction.op_sep
            , sig_map   = self.sig_map
            , ui_sep    = Query_Restriction.ui_sep
            )
    # end def as_json_cargo

    @Once_Property
    def filters (self) :
        ET = self.E_Type
        return tuple (getattr (ET.AQ, f) for f in self.field_names)
    # end def filters

    @Once_Property
    def filters_transitive (self) :
        def _gen (filters) :
            for f in filters :
                yield f
                for c in f.Children :
                    yield c
        return tuple (_gen (self.filters))
    # end def filters_transitive

    @property
    def op_map (self) :
        result = {}
        for k, v in MOM.Attr.Filter._Type_.Base_Op_Table.iteritems () :
            result [k] = dict (desc = _T (v.desc), sym = _T (v.op_sym))
        return result
    # end def op_map

    @Once_Property
    def sig_map (self) :
        result = {}
        Signatures = MOM.Attr.Filter._Type_.Signatures
        for f in uniq (f.Op_Keys for f in self.filters_transitive) :
            if f :
                result [Signatures [f]] = f
        return result
    # end def sig_map

# end class Query_Restriction_Spec

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Query_Restriction

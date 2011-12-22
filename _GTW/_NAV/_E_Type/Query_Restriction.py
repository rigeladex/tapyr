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
#    17-Nov-2011 (CT) Creation continued (NEXT, PREV, ...)
#    19-Nov-2011 (CT) Creation continued (FIRST, LAST)
#    21-Nov-2011 (CT) Creation continued (order_by_names, order_by_ui_names)
#    22-Nov-2011 (CT) Creation continued (Query_Restriction_Spec)
#    23-Nov-2011 (CT) Creation continued (fix `offset_f`, add `op_map`)
#    25-Nov-2011 (CT) Creation continued (restrict `offset_f` to `total_f`)
#    26-Nov-2011 (CT) Creation continued (fix `offset` and `offset_f`)
#     2-Dec-2011 (CT) Creation continued (guard `sig_map` for `f`...)
#     4-Dec-2011 (CT) Creation continued (`MOM.Attr.Querier`, `.AQ`)
#     5-Dec-2011 (CT) Creation continued (add `label` to `op_map`)
#     6-Dec-2011 (CT) Creation continued (filter `None` in `_setup_filters`)
#     7-Dec-2011 (CT) Creation continued (classmethod `Filter`)
#    13-Dec-2011 (CT) Creation continued (classmethod `Filter_Atoms`)
#    20-Dec-2011 (CT) Creation continued (factor to `MOM.Attr.Querier.E_Type`)
#    22-Dec-2011 (CT) Creation continued (make `field_names` optional)
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

from   _GTW.HTML                import Styler
import _GTW._NAV._E_Type

from   _MOM.import_MOM          import MOM, Q

import _TFL._Meta.Object
import _TFL._Meta.Property
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Record

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import uniq
from   _TFL.Regexp              import Regexp, re

from   itertools                import chain as ichain

class Query_Restriction (TFL.Meta.Object) :
    """Model a query restriction as specified by `req_data` of a `GET` request."""

    filters     = ()
    filters_q   = ()
    limit       = 0
    name_sep    = MOM.Attr.Querier.id_sep
    offset      = 0
    op_sep      = MOM.Attr.Querier.op_sep
    order_by    = ()
    order_by_q  = ()
    query_b     = None
    query_f     = None
    ui_sep      = MOM.Attr.Querier.ui_sep

    _name_p     = r"(?P<name> [a-zA-Z0-9]+ (?: _{1,2}[a-zA-Z0-9]+)*)"
    _op_p       = r"(?P<op> [A-Z]+)"
    _a_pat      = Regexp \
        ( "".join ((_name_p, op_sep, _op_p, r"$"))
        , re.VERBOSE
        )

    _a_pat_opt  = Regexp \
        ( "".join ((_name_p, r"(?:", op_sep, _op_p, r")?", r"$"))
        , re.VERBOSE
        )

    @classmethod
    def Filter (cls, E_Type, key, value = None, default_op = "AC") :
        pat = cls._a_pat_opt
        if pat.match (key) :
            result, _ = cls._setup_attr (E_Type, pat, key, value, default_op)
            return result
    # end def Filter

    @classmethod
    def Filter_Atoms (cls, af) :
        ET = af.attr.E_Type
        return tuple \
            (cls.Filter (ET, q._id) for q in af.attr.AQ.Unwrapped_Atoms)
    # end def Filter_Atoms

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
            return ", ".join (ob.ui_name for ob in self.order_by)
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

    @TFL.Meta.Class_and_Instance_Method
    def _setup_attr (soc, E_Type, pat, k, value, default_op = "EQ") :
        op     = pat.op
        if not op :
            op = default_op
            k  = soc.op_sep.join ((k, default_op))
        names  = pat.name.split ("__")
        name   = ".".join (names)
        q      = getattr (E_Type.AQ, name)
        qop    = getattr (q, op)
        ate    = q.As_Template_Elem
        fq     = qop (value)
        f      = dict \
            ( ate._kw
            , attr   = q._attr
            , edit   = value
            , id     = k
            , name   = k
            , op     = TFL.Record
                ( desc   = _T (qop.desc)
                , label  = Styler (_T (qop.op_sym))
                )
            , AQ     = q
            , value  = value
            )
        return TFL.Record (** f), fq
    # end def _setup_attr

    def _setup_filters (self, E_Type, data) :
        matches = \
            (   self._setup_attr (E_Type, pat, k, data.pop (k))
            for k, pat in self._filter_matches (data, self._a_pat)
            )
        matches = tuple ((f, fq) for f, fq in matches if fq is not None)
        if matches :
            self.filters, self.filters_q = zip (* matches)
    # end def _setup_filters

    def _setup_order_by_1 (self, E_Type, s) :
        s     = s.strip ()
        sign  = "-" if s.startswith ("-") else ""
        name  = s [bool (sign): ]
        q     = getattr (E_Type.AQ, name)
        ET    = getattr (q._attr, "E_Type", None)
        if ET :
            keys = tuple ("%s%s.%s" % (sign, name, k) for k in ET.sorted_by)
        else :
            keys = (s, )
        ate   = q.As_Template_Elem
        f     = dict \
            ( ate._kw
            , attr     = q._attr
            , name     = s
            , sign     = sign
            , ui_name  = "%s%s" % (sign, ate.ui_name)
            )
        return TFL.Record (** f), keys
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

class Query_Restriction_Spec (MOM.Attr.Querier.E_Type) :
    """Query restriction spec for a GTW.NAV.E_Type page."""

    def __init__ (self, E_Type, field_names = None) :
        sel = MOM.Attr.Selector.Name (* field_names) if field_names else None
        self.__super.__init__ (E_Type, sel)
    # end def __init__

    @property
    def As_Json_Cargo (self) :
        result = self.__super.As_Json_Cargo
        op_map = result ["op_map"]
        for k, v in op_map.iteritems () :
            v ["label"] = Styler (v ["sym"])
        return result
    # end def As_Json_Cargo

# end class Query_Restriction_Spec

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Query_Restriction

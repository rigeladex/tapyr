# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.MOM.
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
#    GTW.RST.MOM.Query_Restriction
#
# Purpose
#    Provide query restriction for RESTful MOM resources
#
# Revision Dates
#     3-Jul-2012 (CT) Creation (factored from GTW.NAV.E_Type.Query_Restriction)
#     4-Jul-2012 (CT) Fix typo
#    19-Jul-2012 (CT) Add and use `default_limit` and `default_offset`
#    10-Dec-2012 (CT) Remove `default_limit` and `default_offset`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _MOM                     import MOM
from   _TFL                     import TFL

import _GTW._RST._MOM

import _TFL._Meta.Object
import _TFL._Meta.Property
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Record

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import uniq
from   _TFL.Regexp              import Regexp, re

from   itertools                import chain as ichain

class RST_Query_Restriction (TFL.Meta.Object) :
    """Query restriction for RESTful MOM resources."""

    _real_name  = "Query_Restriction"

    attributes  = ()
    filters     = ()
    filters_q   = ()
    limit       = 0
    offset      = 0
    order_by    = ()
    order_by_q  = ()
    query_b     = None
    query_f     = None

    _name_p     = r"(?P<name> [a-zA-Z0-9]+ (?: _{1,2}[a-zA-Z0-9]+)*)"
    _op_p       = r"(?P<op> [A-Z]+)"
    _op_sep     = MOM.Attr.Querier.op_sep
    _a_pat      = Regexp \
        ( "".join ((_name_p, _op_sep, _op_p, r"$"))
        , re.VERBOSE
        )

    _a_pat_opt  = Regexp \
        ( "".join ((_name_p, r"(?:", _op_sep, _op_p, r")?", r"$"))
        , re.VERBOSE
        )

    @classmethod
    def Filter (cls, E_Type, key, value = None, default_op = "AC") :
        pat = cls._a_pat_opt
        if pat.match (key) :
            result, _ = cls._setup_attr_match \
                (E_Type, pat, key, value, default_op)
            return result
    # end def Filter

    @classmethod
    def Filter_Atoms (cls, af) :
        ET = af.attr.E_Type
        return tuple \
            (cls.Filter (ET, q._id) for q in af.attr.AQ.Unwrapped_Atoms)
    # end def Filter_Atoms

    @classmethod
    def from_request (cls, E_Type, request, ** kw) :
        data   = dict (kw, ** dict (request.req_data.iteritems ()))
        result = cls \
            ( limit          = data.pop ("limit",  0)
            , offset         = data.pop ("offset", 0)
            )
        limit  = result.limit
        if limit :
            if "LAST" in data :
                result.offset  = - limit
            elif "FIRST" in data :
                result.offset  = 0
            elif "NEXT" in data :
                result.offset += limit
            elif "PREV" in data :
                result.offset -= limit
        elif "FIRST" in data or "PREV" in data :
            result.offset = 0
        result._setup_attributes (E_Type, request, data)
        result._setup_filters    (E_Type, request, data)
        result._setup_order_by   (E_Type, request, data)
        return result
    # end def from_request

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
            result = result.filter   (* self.filters_q)
        if self.order_by_q :
            result = result.order_by (self.order_by_q)
        self.query_f = result
        offset = self.offset_f
        if offset is not None :
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
    def _qop_desc (soc, qop) :
        return TFL.Record \
            ( desc   = _T (qop.desc)
            , label  = _T (qop.op_sym)
            )
    # end def _qop_desc

    @TFL.Meta.Class_and_Instance_Method
    def _setup_attr (soc, E_Type, k, name, op, value) :
        q      = getattr (E_Type.AQ, name)
        qop    = getattr (q, op)
        fq     = qop (value)
        f      = dict \
            ( q.As_Template_Elem._kw
            , attr   = q._attr
            , edit   = value
            , id     = k
            , name   = k
            , op     = soc._qop_desc (qop)
            , AQ     = q
            , value  = value
            )
        return TFL.Record (** f), fq
    # end def _setup_attr

    @TFL.Meta.Class_and_Instance_Method
    def _setup_attr_aq (soc, E_Type, aq) :
        if aq :
            name, op, value = aq.split (",", 3)
            k = soc._op_sep.join (("__".join ((name.split ("."))), op))
            result = soc._setup_attr (E_Type, k, name, op, value)
            return result
        return None, None
    # end def _setup_attr_aq

    @TFL.Meta.Class_and_Instance_Method
    def _setup_attr_match (soc, E_Type, pat, k, value, default_op = "EQ") :
        op     = pat.op
        if not op :
            op = default_op
            k  = soc._op_sep.join ((k, default_op))
        names  = pat.name.split  ("__")
        return soc._setup_attr   (E_Type, k, ".".join (names), op, value)
    # end def _setup_attr_match

    def _setup_attributes (self, E_Type, request, data) :
        def _gen (fs) :
            for f in fs :
                r = f.strip ()
                if r :
                    yield r
        self.attributes = tuple (_gen (data.pop ("fields", "").split (",")))
    # end def _setup_attributes

    def _setup_filters (self, E_Type, request, data) :
        matches = \
            (   self._setup_attr_match (E_Type, pat, k, data.pop (k))
            for k, pat in self._filter_matches (data, self._a_pat)
            )
        aqs     = \
            (   self._setup_attr_aq (E_Type, aq)
            for aq in request.req_data_list.get ("AQ")
            )
        f_fq_s  = tuple \
            ((f, fq) for f, fq in ichain (matches, aqs) if fq is not None)
        if f_fq_s :
            self.filters, self.filters_q = zip (* f_fq_s)
    # end def _setup_filters

    def _setup_order_by_1 (self, E_Type, s) :
        s     = s.strip ()
        sign  = "-" if s.startswith ("-") else ""
        name  = s [bool (sign): ]
        if name == "pid" : ### XXX move into MOM.Attr.Querier
            keys = (s, )
            f    = dict (attr = None, name = s, sign = sign, ui_name = s)
        else :
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

    def _setup_order_by (self, E_Type, request, data) :
        s = data.pop ("order_by", "").strip ()
        if s :
            def _gen (ns) :
                for n in ns :
                    try :
                        r = self._setup_order_by_1 (E_Type, n)
                    except AttributeError as exc :
                        pass
                    else :
                        yield r
            order_by = tuple (_gen (s.split (",")))
            if order_by :
                self.order_by, criteria = zip (* order_by)
                self.order_by_q = TFL.Sorted_By (* ichain (* criteria))
    # end def _setup_order_by

    def __nonzero__ (self) :
        return bool (self.limit or self.offset or self.filters_q)
    # end def __nonzero__

Query_Restriction = RST_Query_Restriction # end class

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*")
### __END__ GTW.RST.MOM.Query_Restriction

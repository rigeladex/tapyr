# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    25-Mar-2013 (CT) Factor `_name_1_p`, add `_type_p`, `_name_1q_p`
#    26-Mar-2013 (CT) Add support for `polymorphic_epk` attributes
#    27-Mar-2013 (CT) Change `__call__` to not apply `offset` for value `0`
#    27-Mar-2013 (CT) Fix how `_setup_attr_pepk` calculates `value`
#     2-Apr-2013 (CT) Add support for `polymorphic_epk` to `Filter` and
#                     `Filter_Atoms`
#     2-Apr-2013 (CT) Add optional argument `q` to `_setup_attr`
#     9-Apr-2013 (CT) Add exception handler to `af_args_api`
#    11-Apr-2013 (CT) Factor `_pepk_filter` from `Filter` and fix
#     7-May-2013 (CT) Add exception handler to `_setup_attr`
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

import _TFL.multimap
import _TFL.Record

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import first, uniq
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

    _id_sep     = MOM.Attr.Querier.id_sep
    _op_sep     = MOM.Attr.Querier.op_sep
    _ui_sep     = MOM.Attr.Querier.ui_sep

    _name_1_p   = r"[a-zA-Z0-9]+ (?: _[a-zA-Z0-9]+)*"
    _type_p     = r"[A-Za-z0-9_.]+"
    _name_1q_p  = " ".join \
        ( ( _name_1_p                             ### leading name
          ,   r"(?: "
          ,     r"\[", _type_p, r"\]"             ### type_name
          ,     _id_sep                           ### name separator
          ,     _name_1_p                         ### trailing name
          ,   r")?"
          )
        )
    _name_p     = " ".join \
        ( ( r"(?P<name>"
          ,   _name_1q_p                          ### leading name
          ,   r"(?: "
          ,     _id_sep                           ### name separator
          ,     _name_1q_p                        ### trailing name
          ,   r")*"
          , r")"
          )
        )
    _op_p       = r"(?P<op> [A-Z]+)"

    _a_pat      = Regexp \
        ( "".join ((_name_p, _op_sep, _op_p, r"$"))
        , re.VERBOSE
        )

    _a_pat_opt  = Regexp \
        ( "".join ((_name_p, r"(?:", _op_sep, _op_p, r")?", r"$"))
        , re.VERBOSE
        )
    _t_pat      = Regexp \
        ( "".join
            ((r"\[", r"(?P<type>", _type_p, r")", r"\](?: \.|", _id_sep, r")?"))
        , re.VERBOSE
        )

    @classmethod
    def Filter (cls, E_Type, key, value = None, default_op = "AC") :
        data  = { key : value }
        t_pat = cls._t_pat
        if t_pat.search (key) :
            name, typ, tail = t_pat.split (key, 1, 2)
            return cls._pepk_filter \
                (E_Type, key, name, typ, tail, value, default_op)
        else :
            request = TFL.Record (req_data = data, req_data_list = data)
            fs, fqs = cls.attr_filters \
                (E_Type, request, data, None, cls._a_pat_opt, default_op)
            if fs :
                return fs [0]
    # end def Filter

    @classmethod
    def Filter_Atoms (cls, af) :
        ET = af.attr.E_Type
        AQ = af.attr.AQ
        if ET.polymorphic_epk :
            AQ = af.AQ
            ET = AQ.E_Type
        return tuple \
            (cls.Filter (ET, q._id) for q in AQ.Unwrapped_Atoms)
    # end def Filter_Atoms

    @classmethod
    def from_request (cls, scope, E_Type, request, ** kw) :
        data   = dict (kw, ** dict (request.req_data.iteritems ()))
        result = cls \
            ( limit          = data.pop ("limit",  0)
            , offset         = data.pop ("offset", 0)
            )
        limit  = result.limit
        if limit :
            if "FIRST" in data :
                result.offset  = 0
            elif "LAST" in data :
                result.offset  = - limit
            elif "NEXT" in data :
                result.offset += limit
            elif "PREV" in data :
                result.offset -= limit
        elif "FIRST" in data or "PREV" in data :
            result.offset = 0
        result._setup_attributes (E_Type, request, data)
        result._setup_filters    (E_Type, request, data, scope)
        result._setup_order_by   (E_Type, request, data)
        return result
    # end def from_request

    @classmethod
    def nested (cls, scope, ETM, tail_args) :
        E_Type  = ETM.E_Type
        request = TFL.Record \
            ( req_data      = {}
            , req_data_list = dict (AQ = list (",".join (v) for v in tail_args))
            )
        filters, filters_q  = cls.attr_filters (E_Type, request, {}, scope)
        return cls (ETM = ETM, filters = filters, filters_q = filters_q)
    # end def nested

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

    @TFL.Meta.Class_and_Instance_Method
    def af_args_api (soc, req_data_list, default_op = "EQ") :
        for aq in req_data_list.get ("AQ", []) :
            if aq :
                try :
                    name, op, value = aq.split (",", 3)
                except (ValueError, TypeError) :
                    raise ValueError \
                        ( _T( "AQ argument must contain the values "
                              "`attribute_name`, `operator`, `value` "
                              "separated by commas; got `%s` instead"
                            )
                        % (aq, )
                        )
                head, typ, tail = soc._t_pat.split (name, 1, 2)
                if not op :
                    op = default_op
                fn = soc._op_sep.join \
                    ((soc._id_sep.join ((head.split ("."))), op))
                yield fn, head, typ, tail, op, value
    # end def af_args_api

    @TFL.Meta.Class_and_Instance_Method
    def af_args_fif (soc, req_data, a_pat = None, default_op = "EQ") :
        if a_pat is None :
            a_pat = soc._a_pat
        t_pat = soc._t_pat
        for fn in sorted (req_data) :
            if a_pat.match (fn) :
                name   = a_pat.name
                op     = a_pat.op
                value  = req_data [fn]
                if not op :
                    op = default_op
                    fn = soc._op_sep.join ((fn, default_op))
                head, typ, tail = t_pat.split (name, 1, 2)
                h_name = ".".join (head.split (soc._id_sep))
                t_name = ".".join (tail.split (soc._id_sep))
                yield fn, h_name, typ, t_name, op, value
    # end def af_args_fif

    @TFL.Meta.Class_and_Instance_Method
    def attr_filters \
            ( soc, E_Type, request, data, scope
            , a_pat = None
            , default_op = "EQ"
            ) :
        filters   = []
        filters_q = []
        map       = TFL.mm_dict_mm_list ()
        af_args   = ichain \
            ( soc.af_args_api (request.req_data_list, default_op)
            , soc.af_args_fif (data, a_pat, default_op)
            )
        for fn, name, typ, tail, op, value in af_args :
            if typ :
                map [name] [typ].append ((tail, op, value))
            else :
                f, fq = soc._setup_attr (E_Type, fn, name, op, value)
                filters.append   (f)
                filters_q.append (fq)
        for name, t_map in map.iteritems () :
            if len (t_map) > 1 :
                raise ValueError \
                    ( "Got types %s instead of exactly one type"
                    % (sorted (t_map), )
                    )
            typ    = first (t_map)
            nqr    = soc.nested (scope, scope [typ], t_map [typ])
            fs, fq = soc._setup_attr_pepk (E_Type, name, nqr)
            filters.extend   (fs)
            filters_q.append (fq)
        return tuple (filters), tuple (filters_q)
    # end def attr_filters

    @classmethod
    def _pepk_filter (cls, E_Type, key, name, typ, tail, value, default_op) :
        q = getattr (E_Type.AQ, name)
        if not q :
            raise ValueError \
                (_T ("Unknown attribute %s.%s") % (E_Type.type_name, name))
        try :
            qd = q [typ]
        except KeyError :
            raise ValueError \
                ( _T ("Unknown type %s for attribute %s.%s")
                % (typ, E_Type.type_name, name)
                )
        op     = None
        if tail :
            t_name = tail
            if cls._a_pat_opt.match (tail) :
                t_name = cls._a_pat_opt.name
                op     = cls._a_pat_opt.op
            else :
                try :
                    t_name, op, v = tail.split (",", 3)
                except (ValueError, TypeError) :
                    pass
            qa = getattr (qd, t_name)
            if not qa :
                raise ValueError \
                    ( _T ( "Unknown attribute %s.%s[%s].%s")
                    % ((E_Type.type_name, name, typ, tail))
                    )
        else :
            qa = qd
        f, fq = cls._setup_attr (E_Type, key, name, op or default_op, value, qa)
        return f
    # end def _pepk_filter

    @TFL.Meta.Class_and_Instance_Method
    def _qop_desc (soc, qop) :
        return TFL.Record \
            ( desc   = _T (qop.desc)
            , label  = _T (qop.op_sym)
            )
    # end def _qop_desc

    @TFL.Meta.Class_and_Instance_Method
    def _setup_attr (soc, E_Type, fn, name, op, value, q = None) :
        if q is None :
            try :
                q   = getattr (E_Type.AQ, name)
            except AttributeError as exc :
                raise AttributeError \
                    ( _T ("%s doesn't have an attribute named `%s`")
                    % (E_Type.type_name, name)
                    )
        qop     = getattr (q, op)
        fq      = qop (value)
        qate    = q.As_Template_Elem
        f       = dict \
            ( qate._kw
            , attr   = q._attr
            , edit   = value
            , id     = fn
            , name   = fn
            , op     = soc._qop_desc (qop)
            , AQ     = q
            , value  = value
            )
        return TFL.Record (** f), fq
    # end def _setup_attr

    @TFL.Meta.Class_and_Instance_Method
    def _setup_attr_pepk (soc, E_Type, name, nqr) :
        q      = getattr (E_Type.AQ, name)
        qop    = q.IN
        value  = nqr (nqr.ETM.query ()).attr ("pid")
        fq     = qop (value)
        fs     = []
        for nf in nqr.filters :
            f    = nf.copy ()
            f.id = f.name = soc._id_sep.join \
                (("%s[%s]" % (name, nqr.ETM.type_name), nf.id))
            f.full_name = ".".join \
                (("%s[%s]" % (q._full_name, nqr.ETM.type_name), nf.full_name))
            f.ui_name = soc._ui_sep.join ((q._ui_name_T, nf.ui_name))
            fs.append (f)
        return fs, fq
    # end def _setup_attr_pepk

    def _setup_attributes (self, E_Type, request, data) :
        def _gen (fs) :
            for f in fs :
                r = f.strip ()
                if r :
                    yield r
        self.attributes = tuple (_gen (data.pop ("fields", "").split (",")))
    # end def _setup_attributes

    def _setup_filters (self, E_Type, request, data, scope) :
        self.filters, self.filters_q = self.attr_filters \
            (E_Type, request, data, scope)
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

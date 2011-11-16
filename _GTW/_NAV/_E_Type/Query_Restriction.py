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
#    16-Nov-2011 (CT) Creation continued
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV._E_Type

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

import _TFL.Record

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Regexp, re

class Query_Restriction (TFL.Meta.Object) :
    """Model a query restriction as specified by `req_data` of a `GET` request."""

    count     = 0
    filters   = ()
    filters_q = ()
    limit     = None
    offset    = None
    query_b   = None
    query_f   = None

    _np      = r"[a-zA-Z0-9]+ (?: _{1,2}[a-zA-Z0-9]+)*"
    _a_pat   = Regexp \
        ( r"(?P<name> [a-zA-Z0-9]+ (?: _{1,2}[a-zA-Z0-9]+)*)"
          r"___"
          r"(?P<op> [A-Z]+)"
          r"$"
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
        result._setup_filters (E_Type, data)
        return result
    # end def from_request_data

    def __init__ (self, limit = None, offset = None, ** kw) :
        if limit is not None :
            self.limit  = int (limit)
        if offset is not None :
            self.offset = int (offset)
        self.__dict__.update (kw)
    # end def __init__

    def __call__ (self, base_query) :
        self.query_b = self.query_f = base_query
        result = base_query
        if self.filters_q :
            result = self.query_f = result.filter (* self.filters_q)
        if self.offset :
            result = result.offset (self.offset)
        if self.limit :
            result = result.limit  (self.limit)
        return result
    # end def __call__

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
            T = getattr (attr, "P_Type", None)
    # end def _nested_attrs

    def _setup_attr (self, E_Type, pat, k, value) :
        name  = pat.name
        op    = pat.op
        names = name.split ("__")
        attrs = tuple (self._nested_attrs (E_Type, names))
        q     = attrs [-1].Q
        pre   = ".".join (names [:-1]) or None
        f = TFL.Record \
            ( key      = k
            , name     = ".".join (names)
            , op       = op
            , ui_names = tuple (_T (a.ui_name) for a in attrs)
            , value    = value
            )
        return f, getattr (q, op) (value, pre)
    # end def _setup_attr

    def _setup_filters (self, E_Type, data) :
        matches = tuple \
            (   self._setup_attr (E_Type, pat, k, data.pop (k))
            for k, pat in self._filter_matches (data, self._a_pat)
            )
        if matches :
            self.filters, self.filters_q = (tuple (l) for l in zip (* matches))
    # end def _setup_filters

    def __nonzero__ (self) :
        return bool (self.limit or self.offset or self.filters_q)
    # end def __nonzero__

# end class Query_Restriction

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Query_Restriction

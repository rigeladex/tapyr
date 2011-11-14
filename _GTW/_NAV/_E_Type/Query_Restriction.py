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
#    14-Nov-2011 (CT) Add `__nonzero__`
#    ««revision-date»»···
#--

from   __future__  import unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV._E_Type

import _TFL._Meta.Object

from   _TFL.I18N                import _, _T, _Tn
from   _TFL.Regexp              import Regexp, re

class Query_Restriction (TFL.Meta.Object) :
    """Model a query restriction as specified by `req_data` of a `GET` request."""

    limit  = None
    offset = None

    _np    = r"[a-zA-Z0-9]+ (?: _[a-zA-Z0-9]+)*"
    _a_pat = Regexp \
        ( "".join
            ( ( r"(?P<name> ", _np, r")"
              , r"(?: __ (?P<rest> "
              ,             _np
              ,             r"(?: __ ", _np, r")*"
              ,       r" )"
              , r")?"
              , r"___"
              , r"(?P<op> [A-Z]+)"
              , r"$"
              )
            )
        , re.VERBOSE
        )

    def __init__ (self, E_Type, req_data) :
        data = self.other_req_data = dict (req_data.iteritems ())
        if "limit" in data :
            self.limit  = int (data.pop ("limit"))
        if "offset" in data :
            self.offset = int (data.pop ("offset"))
        self.filters = tuple (self._setup_filters (E_Type, self._a_pat, data))
    # end def __init__

    def __call__ (self, base_query) :
        result = base_query
        if self.filters :
            result = result.filter (* self.filters)
        if self.offset :
            result = result.offset (self.offset)
        if self.limit :
            result = result.limit  (self.limit)
        return result
    # end def __call__

    def _setup_attr (self, E_Type, pat, value) :
        name = pat.name
        rest = pat.rest
        op   = pat.op
        pre  = None
        q    = getattr (E_Type, name).Q
        if rest :
            rest = rest.replace ("__", ".")
            pre  = ".".join ([name] + rest.split (".") [:-1])
            q    = getattr  (q, rest)
        return getattr (q, op) (value, pre)
    # end def _setup_attr

    def _setup_filters (self, E_Type, pat, data) :
        for k in tuple (data) :
            if pat.match (k) :
                yield self._setup_attr (E_Type, pat, data.pop (k))
    # end def _setup_filters

    def __nonzero__ (self) :
        return bool (self.limit or self.offset or self.filters)
    # end def __nonzero__

# end class Query_Restriction

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Query_Restriction

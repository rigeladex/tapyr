# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package GTW.NAV.E_Type.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    GTW.NAV.E_Type._Mgr_Base_
#
# Purpose
#    Common base class for Admin and Manager of GTW.NAV.E_Type
#
# Revision Dates
#    20-Jan-2010 (CT) Creation
#     5-Mar-2010 (CT) `page_args` added
#    15-Mar-2010 (CT) `kind_filter` and `kind_name` removed
#    17-Mar-2010 (CT) Derived from `GTW.NAV.E_Type.Mixin`
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type.Mixin

import _TFL.Filter

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import filtered_join

class _Mgr_Base_ (GTW.NAV.E_Type.Mixin) :
    """Common base class for Admin and Manager of GTW.NAV.E_Type."""

    page_args       = {}
    sort_key        = None

    def __init__ (self, parent, ** kw) :
        ETM    = kw ["ETM"]
        E_Type = ETM._etype
        top    = self.top
        desc   = kw.pop  ("desc", E_Type.__doc__)
        name   = unicode (kw.pop ("name", E_Type.ui_name))
        title  = kw.pop  ("title", _Tn (name))
        self.__super.__init__ \
            ( parent       = parent
            , E_Type       = E_Type
            , desc         = desc
            , name         = name
            , title        = title
            , ** kw
            )
        self._objects = []
        self._old_cid = -1
    # end def __init__

    @property
    def count (self) :
        if self.query_filters :
            result = self.query ().count_transitive ()
        else :
            result = self.ETM.count_transitive
        return result
    # end def count

    def query (self) :
        return self.ETM.query_s \
            (* self.query_filters, sort_key = self.sort_key)
    # end def query

    @Once_Property
    def query_filters (self) :
        return tuple ()
    # end def query_filters

    def _get_entries (self) :
        scope = self.top.scope
        cid   = scope.ems.max_cid
        if self._old_cid != cid or scope.async_changes () :
            self._objects = self._get_objects ()
            self._old_cid = cid
        return self._objects
    # end def _get_entries

    _entries = property (_get_entries, lambda s, v : True)

    def _get_objects (self) :
        T = self.Page
        kw = self.page_args
        return [T (self, o, ** kw) for o in self.query ()]
    # end def _get_objects

# end class _Mgr_Base_

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("_Mgr_Base_")
### __END__ GTW.NAV.E_Type._Mgr_Base_

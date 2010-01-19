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
#    GTW.NAV.E_Type.Manager
#
# Purpose
#    Navigation directory listing the instances of one E_Type
#
# Revision Dates
#    19-Jan-2010 (CT) Creation (ported from DJO.NAV.Model.Manager)
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type.Instance

import _TFL.Filter
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import filtered_join

Q = TFL.Attr_Query ()

class Manager (GTW.NAV.Dir) :
    """Navigation directory listing the instances of one E_Type."""

    Page            = GTW.NAV.E_Type.Instance

    admin_args      = {}
    sort_key        = None

    _admin          = None

    def __init__ (self, src_dir, parent, ** kw) :
        ETM    = kw.pop ("ETM")
        E_Type = ETM._etype
        etn    = E_Type.type_name
        kn     = unicode (kw.get ("kind_name"))
        top    = self.top
        desc   = kw.pop ("desc", E_Type.__doc__)
        name   = filtered_join \
            (u"-", (unicode (kw.pop ("name", E_Type.ui_name)), kn))
        title  = kw.pop  ("title", filtered_join ("-", (_Tn (name), kn)))
        assert (etn, kn) not in top.E_Types
        top.E_Types [etn, kn] = self
        self.__super.__init__ \
            ( src_dir, parent
            , ETM          = ETM
            , E_Type       = E_Type
            , desc         = desc
            , name         = name
            , title        = title
            , ** kw
            )
        self._old_count = -1
    # end def __init__

    @property
    def admin (self) :
        if self._admin is None :
            Admin = self.top.Admin
            if Admin :
                self._admin = Admin._get_child (self.name)
        return self._admin
    # end def admin

    @property
    def count (self) :
        if self.query_filters :
            return self.query ().count_transitive ()
        else :
            return self.ETM.count_transitive ()
    # end def count

    @property
    def href_create (self) :
        admin = self.admin
        if admin :
            return admin.href_create ()
    # end def href_change

    @Once_Property
    def kind_filter (self) :
        if self.kind_name :
            return Q.kind == self.E_Type.kind.from_string (self.kind_name)
    # end def kind_filter

    def query (self) :
        return self.ETM.query_s \
            (* self.query_filters, sort_key = self.sort_key)
    # end def query

    @Once_Property
    def query_filters (self) :
        result = []
        if self.kind_filter :
            result.append (self.kind_filter)
        if self.disp_filter :
            result.append (self.disp_filter)
        return tuple (result)
    # end def query_filters

    def _get_entries (self) :
        count = self.count
        if self._old_count != count :
            ### XXX Doesn't catch changes to fields of objects
            self._objects   = self._get_objects ()
            self._old_count = count
        return self._objects
    # end def _get_entries

    _entries = property (_get_entries, lambda s, v : True)

    def _get_objects (self) :
        T = self.Page
        return [T (o, self) for o in self.query ()]
    # end def _get_objects

# end class Manager

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Manager

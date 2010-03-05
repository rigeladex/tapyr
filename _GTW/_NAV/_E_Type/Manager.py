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
#    20-Jan-2010 (CT) `_Mgr_Base_` factored
#     5-Mar-2010 (CT) `Manager.__init__` corrected
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._NAV.Base
import _GTW._NAV._E_Type._Mgr_Base_
import _GTW._NAV._E_Type.Instance

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.I18N                import _, _T, _Tn

from   posixpath                import join  as pjoin

class Manager (GTW.NAV.E_Type._Mgr_Base_, GTW.NAV.Dir) :
    """Navigation directory listing the instances of one E_Type."""

    Page            = GTW.NAV.E_Type.Instance

    admin_args      = {}

    def __init__ (self, src_dir, ** kw) :
        self.__super.__init__ (src_dir = src_dir, ** kw)
        etn = self.E_Type.type_name
        kn  = self.kind_name
        top = self.top
        assert (etn, kn) not in top.E_Types
        top.E_Types [etn, kn] = self
    # end def __init__

    @Once_Property
    def admin (self) :
        Admin = self.top.Admin
        if Admin :
            return Admin._get_child (self.name)
    # end def admin

    def href_create (self) :
        admin = self.admin
        if admin :
            return admin.href_create ()
    # end def href_change

    def href_display (self, obj) :
        return pjoin (self.abs_href, obj.lid)
    # end def href_display

    @Once_Property
    def query_filters (self) :
        result = []
        if self.kind_filter :
            result.append (self.kind_filter)
        if self.disp_filter :
            result.append (self.disp_filter)
        return tuple (result)
    # end def query_filters

# end class Manager

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Manager

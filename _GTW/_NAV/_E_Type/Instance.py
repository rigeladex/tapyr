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
#    GTW.NAV.E_Type.Instance
#
# Purpose
#    Navigation page modelling a single instance of a E_Type
#
# Revision Dates
#    19-Jan-2010 (CT) Creation
#    20-Jan-2010 (CT) `FO` factored to GTW
#    25-Jan-2010 (CT) `rendered` changed to take `handler` instead of `context`
#     5-Mar-2010 (CT) `__init__` fixed
#     5-Mar-2010 (CT) `attr_mapper` and `__getattr__` using it added
#    17-Mar-2010 (CT) `permalink` added
#    17-Mar-2010 (CT) `GTW.NAV.E_Type.Mixin` added as ancestor
#    19-Mar-2010 (CT) `permalink` changed to use the real `E_Type.Manager`
#    24-Mar-2010 (CT) `Instance_Y` added
#    29-Apr-2010 (CT) `Instance.permalink` changed to use `man.href_display`
#                     instead of home-grown code
#    29-Apr-2010 (CT) `Instance_Y` removed
#    29-Apr-2010 (CT) `__init__` changed to sanitize `name`
#    30-Apr-2010 (CT) `Instance_Mixin` factored
#    ««revision-date»»···
#--

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW.FO
import _GTW._NAV.Base
import _GTW._NAV._E_Type.Mixin

import _TFL._Meta.Object
from   _TFL._Meta.Once_Property import Once_Property

class Instance (GTW.NAV.E_Type.Instance_Mixin, GTW.NAV.Page) :
    """Navigation page modelling a single instance of a E_Type."""

    allows_children = False

    @property
    def contents (self) :
        return self.obj.contents
    # end def contents

    @property
    def changer (self) :
        admin = self.admin
        if admin :
            return admin._get_child ("change", self.obj.lid)
    # end def changer

    def href_change (self) :
        admin = self.admin
        if admin :
            return admin.href_change (self.obj)
    # end def href_change

    def href_delete (self) :
        admin = self.admin
        if admin :
            return admin.href_delete (self.obj)
    # end def href

# end class Instance

if __name__ != "__main__" :
    GTW.NAV.E_Type._Export ("*")
### __END__ GTW.NAV.E_Type.Instance

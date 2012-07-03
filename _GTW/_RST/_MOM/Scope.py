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
#    GTW.RST.MOM.Scope
#
# Purpose
#    Provide RESTful resource for a MOM scope
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#     3-Jul-2012 (CT) Factored from _GTW/_RST/MOM.py
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST._MOM.E_Type

from   _MOM.import_MOM          import MOM, Q

_Ancestor = GTW.RST.Node

class RST_Scope (_Ancestor) :
    """RESTful node for a scope."""

    _real_name                 = "Scope"

    E_Type                     = GTW.RST.MOM.E_Type

    def __init__ (self, ** kw) :
        if "entries" not in kw :
            kw ["entries"] = tuple \
                (   self.E_Type
                      ( ETM  = et.type_name
                      , name = et.type_name.replace (".", "-")
                      )
                for et in self.top.scope._T_Extension
                if  issubclass (et, MOM.Id_Entity)
                        and (et.children or not et.is_partial)
                )
        self.__super.__init__ (** kw)
    # end def __init__

    def _get_child (self, child, * grandchildren) :
        if child == "pid" :
            child = "MOM-Id_Entity"
        return self.__super._get_child (child, * grandchildren)
    # end def _get_child

Scope = RST_Scope # end class

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*")
### __END__ GTW.RST.MOM.Scope

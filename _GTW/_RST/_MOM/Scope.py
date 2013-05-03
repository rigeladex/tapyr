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
#    GTW.RST.MOM.Scope
#
# Purpose
#    Provide RESTful resource for a MOM scope
#
# Revision Dates
#    22-Jun-2012 (CT) Creation
#     3-Jul-2012 (CT) Factored from _GTW/_RST/MOM.py
#     7-Aug-2012 (CT) Change class prefix from `RST_` to `RST_MOM_`
#     7-Aug-2012 (CT) Add prefix and suffix `_` to class names
#    13-Sep-2012 (CT) Sort `Scope.entries` by `type_name`
#     4-Oct-2012 (CT) Add `href_e_type`, `resource_from_e_type`
#     5-Oct-2012 (CT) Add `json_indent` to `JSON.json_dump_kw`
#    20-Oct-2012 (CT) Set `E_Type_Desc._prop_map ["rest_api"]`
#     3-May-2013 (CT) Create `RAT` if `auth_required`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _GTW                     import GTW
from   _TFL                     import TFL

import _GTW._RST.Resource
import _GTW._RST.RAT
import _GTW._RST._MOM.E_Type

from   _MOM.import_MOM          import MOM, Q

from   posixpath                import join as pp_join

_Ancestor = GTW.RST.Dir

class _RST_MOM_Scope_ (_Ancestor) :
    """RESTful node for a scope."""

    _real_name                 = "Scope"

    E_Type                     = GTW.RST.MOM.E_Type

    def __init__ (self, ** kw) :
        root = self.top
        json_indent = kw.pop ("json_indent", None)
        if "entries" not in kw :
            kw ["entries"] = tuple \
                (   self.E_Type
                      ( ETM  = et.type_name
                      , name = et.type_name.replace (".", "-")
                      )
                for et in sorted \
                    (root.scope.T_Extension, key = TFL.Getter.type_name)
                if  issubclass (et, MOM.Id_Entity)
                        and (et.children_np or not et.is_partial)
                )
        self.__super.__init__ (** kw)
        if json_indent or self.DEBUG :
            import _GTW._RST.Mime_Type
            GTW.RST.Mime_Type.JSON.json_dump_kw.update \
                ( indent    = json_indent or 2
                , sort_keys = True
                )
        if self.auth_required :
            root.E_Type_Desc._prop_map ["rest_api"] = self
            if not hasattr (root.SC, "RAT") :
                root.add_entries (GTW.RST.RAT (name = "RAT"))
    # end def __init__

    def href_e_type (self, e_type) :
        if not isinstance (e_type, basestring) :
            e_type = e_type.type_name
        return pp_join (self.abs_href, e_type.replace (".", "-"))
    # end def href_obj

    def resource_from_e_type (self, e_type) :
        if not isinstance (e_type, basestring) :
            e_type = getattr (e_type, "type_name")
        result = self._entry_map.get (e_type.replace (".", "-"))
        return result
    # end def resource_from_e_type

    def _get_child (self, child, * grandchildren) :
        if child == "pid" :
            child = "MOM-Id_Entity"
        return self.__super._get_child (child, * grandchildren)
    # end def _get_child

Scope = _RST_MOM_Scope_ # end class

if __name__ != "__main__" :
    GTW.RST.MOM._Export ("*")
### __END__ GTW.RST.MOM.Scope

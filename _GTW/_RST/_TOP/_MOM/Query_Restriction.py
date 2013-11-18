# -*- coding: utf-8 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.RST.TOP.MOM.
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
#    GTW.RST.TOP.MOM.Query_Restriction
#
# Purpose
#    Provide query restriction for RESTful TOP.MOM resources
#
# Revision Dates
#    30-Jul-2012 (CT) Creation (factored from GTW.NAV.E_Type.Query_Restriction)
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _GTW.HTML                        import Styler_Safe

from   _GTW._RST._MOM.Query_Restriction import *
import _GTW._RST._TOP._MOM

from   _TFL.I18N                        import _, _T, _Tn

_Ancestor = RST_Query_Restriction

class TOP_Query_Restriction (_Ancestor) :
    """Query restriction for RESTful TOP.MOM resources."""

    _real_name  = "Query_Restriction"

    @TFL.Meta.Class_and_Instance_Method
    def _qop_desc (soc, qop) :
        return TFL.Record \
            ( desc   = _T (qop.desc)
            , label  = Styler_Safe (_T (qop.op_sym))
            )
    # end def _qop_desc

Query_Restriction = TOP_Query_Restriction # end class

class TOP_Query_Restriction_Spec (MOM.Attr.Querier.E_Type) :
    """Query restriction spec for a E_Type-specific page."""

    _real_name = "Query_Restriction_Spec"

    def __init__ (self, E_Type, field_names = None) :
        sel = MOM.Attr.Selector.Name (* field_names) if field_names else None
        self.__super.__init__ (E_Type, sel)
    # end def __init__

    @property
    def As_Json_Cargo (self) :
        result = self.__super.As_Json_Cargo
        op_map = result ["op_map"]
        for k, v in op_map.iteritems () :
            v ["label"] = Styler_Safe (v ["sym"])
        return result
    # end def As_Json_Cargo

Query_Restriction_Spec = TOP_Query_Restriction_Spec # end class

if __name__ != "__main__" :
    GTW.RST.TOP.MOM._Export ("*")
### __END__ GTW.RST.TOP.MOM.Query_Restriction

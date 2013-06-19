# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Prop.
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
#    MOM.Prop.Type
#
# Purpose
#    Base class for attribute and predicate types
#
# Revision Dates
#    11-Mar-2013 (CT) Creation (factored from MOM.Attr.A_Attr_Type)
#     3-Jun-2013 (CT) Change argument of `fix_doc` from `e_type` to `et_scope`
#    14-Jun-2013 (CT) Use `dyn_doc_p` to `fix_doc`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

import _TFL._Meta.M_Auto_Combine
import _TFL._Meta.Object
import _TFL._Meta.Property
import _TFL.Caller

class _Prop_Type_ (TFL.Meta.Object) :
    """Base class for attribute and predicate types"""

    __metaclass__       = TFL.Meta.M_Auto_Combine
    _real_name          = "Type"
    _sets_to_combine    = ("_doc_properties", )
    _doc_properties     = ("description", "explanation")

    @TFL.Meta.Class_and_Instance_Method
    def fix_doc (soc, et_scope) :
        for name, v in pyk.iteritems (soc.dyn_doc_p) :
            try :
                v = v % et_scope
            except Exception :
                pass
            else :
                setattr (soc, name, v)
        if soc.description :
            soc.__doc__ = soc.description
    # end def fix_doc

Type = _Prop_Type_ # end class

if __name__ != "__main__" :
    MOM.Prop._Export ("*")
### __END__ MOM.Prop.Type

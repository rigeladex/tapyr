# -*- coding: utf-8 -*-
# Copyright (C) 2013-2015 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.Prop.
#
# This module is licensed under the terms of the BSD 3-Clause License
# <http://www.c-tanzer.at/license/bsd_3c.html>.
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
#    14-Jun-2013 (CT) Add `DET`, `DET_Base`, and `DET_Root`
#    26-Jan-2015 (CT) Use `M_Auto_Update_Combined`, not `M_Auto_Combine_Dict`,
#                     as metaclass
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

import _TFL._Meta.M_Auto_Update_Combined
import _TFL._Meta.Object
import _TFL._Meta.Property
import _TFL.Caller

class _Prop_Type_ \
          ( TFL.Meta.BaM
              ( TFL.Meta.Object
              , metaclass = TFL.Meta.M_Auto_Update_Combined
              )
          ) :
    """Base class for attribute and predicate types"""

    _real_name               = "Type"

    _attrs_to_update_combine = ("_doc_properties", )
    _doc_properties          = set (("description", "explanation"))

    ### set by MOM.Meta.M_Prop_Spec
    DET = DET_Base = DET_Root = None

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

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package GTW.OMP.NET.
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
#    GTW.OMP.NET.SAW_PG
#
# Purpose
#    SAW specific functions and classes for GTW.OMP.NET attribute types
#
# Revision Dates
#     2-Aug-2013 (CT) Creation
#     6-Aug-2013 (CT) Finish creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                       import GTW
from   _MOM                       import MOM
from   _TFL                       import TFL
from   _TFL.pyk                   import pyk

import _GTW._OMP._NET.Attr_Type
import _GTW._OMP._NET.SAW

from   _MOM._DBW._SAW             import SAW, SA
from   _MOM.SQ                    import Q

import _MOM._DBW._SAW.Attr
import _MOM._DBW._SAW._PG.Attr
import _MOM._DBW._SAW._PG.SA_Type

from   _TFL._Meta.Single_Dispatch import Single_Dispatch_Method

import _TFL._Meta.Object
import _TFL.Decorator

class Kind_CIDR_Wrapper \
          (SAW.Attr._Kind_Wrapper_Field_Extractor_, SAW.Attr.Kind_Wrapper) :

    fields = set (("mask_len", ))
    op_map = dict \
        ( contains = ">>="
        , in_      = "<<="
        )

    def _q_exp_call_apply (self, q_exp, QR, ETW, lhs, op_name) :
        op_map = self.op_map
        try :
            op = op_map [op_name]
        except KeyError :
            result = self.__super._q_exp_call_apply \
                (q_exp, QR, ETW, lhs, op_name)
        else :
            result = lhs.op (op)
        return result
    # end def _q_exp_call_apply

# end class Kind_CIDR_Wrapper

class _CIDR_Type_ (GTW.OMP.NET.SAW._CIDR_Type_) :
    """Augmented CIDR type that converts between R_IP_Address and
       PostgreSQL CIDR.
    """

    impl = SAW.PG.SA_Type.CIDR

# end class _CIDR_Type_

PG_Man_Class = SAW.PG.Manager.__class__

@GTW.OMP.NET._A_CIDR_._saw_column_type.add_type (PG_Man_Class)
def _saw_column_type_CIDR_PG (self, DBW, wrapper, pts) :
    return _CIDR_Type_ ()
# end def _saw_column_type_CIDR_PG

@GTW.OMP.NET._A_CIDR_._saw_extract_field.add_type (PG_Man_Class)
def _saw_extract_field_mask_CIDR_PG (self, DBW, col, field) :
    if field == "mask_len" :
        return SA.sql.func.masklen (col)
    raise AttributeError (field)
# end def _saw_extract_field_mask_CIDR_PG

@GTW.OMP.NET._A_CIDR_._saw_kind_wrapper.add_type (PG_Man_Class)
def _saw_kind_wrapper_CIDR_PG (self, DBW, ETW, kind, ** kw) :
    return Kind_CIDR_Wrapper (ETW, kind, ** kw)
# end def _saw_kind_wrapper_CIDR_PG

if __name__ != "__main__" :
    GTW.OMP.NET._Export_Module ()
### __END__ GTW.OMP.NET.SAW_PG

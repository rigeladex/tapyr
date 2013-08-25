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
#    GTW.OMP.NET.SAW
#
# Purpose
#    SAW specific functions and classes for GTW.OMP.NET attribute types
#
# Revision Dates
#     2-Aug-2013 (CT) Creation
#     6-Aug-2013 (CT) Continue creation
#     7-Aug-2013 (CT) Finish creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _GTW                       import GTW
from   _MOM                       import MOM
from   _TFL                       import TFL
from   _TFL.pyk                   import pyk

import _GTW._OMP._NET.Attr_Type

from   _MOM._DBW._SAW             import SAW, SA
from   _MOM.SQ                    import Q

import _MOM._DBW._SAW.Attr

from   _TFL._Meta.Single_Dispatch import Single_Dispatch_Method

import _TFL._Meta.Object
import _TFL.Decorator

from   rsclib.IP_Address        import IP_Address as R_IP_Address

import operator

class _CIDR_Type_ (SA.types.TypeDecorator) :
    """Augmented CIDR type that converts between R_IP_Address and string"""

    impl = SAW.SA_Type.String

    def process_bind_param   (self, value, dialect) :
        if value is not None :
            return str (value)
    # end def process_bind_param

# end class _CIDR_Type_

class _ACV_ (TFL.Meta.Object) :

    def __init__ (self, akw, entity) :
        self.entity = entity
        if isinstance (entity, SA.schema.Column) :
            akw             = entity.MOM_Wrapper
            self.col_values = acvs = akw._accidental_columns
            cv_iter         = ((c, c) for c in acvs)
        else :
            if isinstance (entity, MOM.Id_Entity) :
                akw  = entity._SAW.db_attrs [akw.name]
                cidr = akw.kind.get_value   (entity)
                accs = akw._accidental_columns
            else :
                cidr = entity
                accs = self.accidental_columns (akw)
                if isinstance (cidr, pyk.string_types) :
                    cidr = self.Attr_Type.P_Type (cidr)
            self.col_values = acvs = []
            self._setup (akw, cidr)
            cv_iter = zip (accs, acvs)
        for c, v in cv_iter :
            setattr (self, c.name, v)
            setattr (self, c._saw_postfix, v)
        self.akw = akw
    # end def __init__

    @classmethod
    def accidental_columns (cls, akw) :
        return ()
    # end def accidental_columns

    @classmethod
    def _new_column (cls, akw, postfix, type) :
        name                = "__".join ((akw.ckd_name, postfix))
        result              = SA.schema.Column (name, type)
        result._saw_postfix = postfix
        return result
    # end def _new_column

    def _setup (self, akw, cidr) :
        pass
    # end def _setup

    def __getattr__ (self, name) :
        if name == "mask_len" :
            ### for IPx_Address, mask_len is a constant and therefore not set
            ### by __init__
            return self.akw.mask_col
        raise AttributeError (name)
    # end def __getattr__

    def __iter__ (self) :
        return iter (self.col_values)
    # end def __iter__

    def __repr__ (self) :
        return "%s : %s" % \
            ( self.__class__.__name__
            , ", ".join
                (   "%s = %s" % (c._saw_postfix, v)
                for c, v in zip (self.akw._accidental_columns, self.col_values)
                )
            )
    # end def __repr__

# end class _ACV_

class _ACV_Network_ (_ACV_) :

    @classmethod
    def accidental_columns (cls, akw) :
        acs = super (_ACV_Network_, cls).accidental_columns (akw)
        aco = (cls._new_column (akw, "mask_len", SA.types.SmallInteger), )
        return acs + aco
    # end def accidental_columns

    def _setup (self, akw, cidr) :
        self.__super._setup (akw, cidr)
        add = self.col_values.append
        add (cidr.mask)
    # end def _setup

# end class _ACV_Network_

def _acv_add_to_class (Attr_Type) :
    def decorator (cls) :
        setattr (Attr_Type, "_SAW_ACV",  cls)
        setattr (cls,       "Attr_Type", Attr_Type)
        return cls
    return decorator
# end def decorator

@_acv_add_to_class (GTW.OMP.NET.A_IP4_Address)
class ACV_IP4_Address (_ACV_) :

    @classmethod
    def accidental_columns (cls, akw) :
        acs = super (ACV_IP4_Address, cls).accidental_columns (akw)
        aco = (cls._new_column (akw, "numeric", SA.types.Integer), )
        return acs + aco
    # end def accidental_columns

    def _setup (self, akw, cidr) :
        self.__super._setup (akw, cidr)
        add = self.col_values.append
        add (cidr.ip + akw.min_value)
    # end def _setup

    def __getattr__ (self, name) :
        if name == "upper_bound" :
            ### for IP4_Address, upper_bound is a constant and therefore not set
            ### by __init__
            return self.numeric
        return self.__super.__getattr__ (name)
    # end def __getattr__

# end class ACV_IP4_Address

@_acv_add_to_class (GTW.OMP.NET.A_IP4_Network)
class ACV_IP4_Network (_ACV_Network_, ACV_IP4_Address) :

    @classmethod
    def accidental_columns (cls, akw) :
        acs = super (cls, ACV_IP4_Network).accidental_columns (akw)
        aco = (cls._new_column (akw, "upper_bound", SA.types.Integer), )
        return acs + aco
    # end def accidental_columns

    def _setup (self, akw, cidr) :
        self.__super._setup (akw, cidr)
        add = self.col_values.append
        add (cidr._broadcast + akw.min_value)
    # end def _setup

# end class ACV_IP4_Network

@_acv_add_to_class (GTW.OMP.NET.A_IP6_Address)
class ACV_IP6_Address (_ACV_) :

    @classmethod
    def accidental_columns (cls, akw) :
        acs = super (ACV_IP6_Address, cls).accidental_columns (akw)
        aco = \
            ( cls._new_column (akw, "numeric__lo", SA.types.BigInteger)
            , cls._new_column (akw, "numeric__hi", SA.types.BigInteger)
            )
        return acs + aco
    # end def accidental_columns

    def _setup (self, akw, cidr) :
        self.__super._setup (akw, cidr)
        add       = self.col_values.append
        ip        = cidr.ip
        min_value = akw.min_value
        add ((ip &  akw.max_value) + min_value)
        add ((ip >> 64)            + min_value)
    # end def _setup

    def __getattr__ (self, name) :
        if name.startswith ("upper_bound__") :
            ### for IP4_Address, upper_bound are constants and therefore not set
            ### by __init__
            return getattr (self, "numeric__" + name [-2:])
        return self.__super.__getattr__ (name)
    # end def __getattr__

# end class ACV_IP6_Address

@_acv_add_to_class (GTW.OMP.NET.A_IP6_Network)
class ACV_IP6_Network (_ACV_Network_, ACV_IP6_Address) :

    @classmethod
    def accidental_columns (cls, akw) :
        acs = super (ACV_IP6_Network, cls).accidental_columns (akw)
        aco = \
            ( cls._new_column (akw, "upper_bound__lo", SA.types.BigInteger)
            , cls._new_column (akw, "upper_bound__hi", SA.types.BigInteger)
            )
        return acs + aco
    # end def accidental_columns

    def _setup (self, akw, cidr) :
        self.__super._setup (akw, cidr)
        add       = self.col_values.append
        bc        = cidr._broadcast
        min_value = akw.min_value
        add ((bc &  akw.max_value) + min_value)
        add ((bc >> 64)            + min_value)
    # end def _setup

# end class ACV_IP6_Network

class _Kind_CIDR_Wrapper_ \
          (SAW.Attr._Kind_Wrapper_Field_Extractor_, SAW.Attr.Kind_Wrapper) :

    fields = set (("mask_len", ))
    op_map = dict \
        ( __eq__        = TFL.Getter.op_eq
        , __ge__        = TFL.Getter.op_ge
        , __gt__        = TFL.Getter.op_gt
        , __le__        = TFL.Getter.op_le
        , __lt__        = TFL.Getter.op_lt
        , __ne__        = TFL.Getter.op_ne
        , contains      = TFL.Getter.op_contains
        , in_           = TFL.Getter.op_in
        )

    def __init__ (self, * args, ** kw) :
        self.__super.__init__ (* args, ** kw)
        self.col_map = {}
    # end def __init__

    @TFL.Meta.Once_Property
    def ACV (self) :
        return self.attr._SAW_ACV
    # end def ACV

    @TFL.Meta.Once_Property
    def columns (self) :
        eff = self.eff
        if eff is self :
            result = list (self.__super.columns)
            assert len (result) == 1
            result.extend (self._accidental_columns)
            result = tuple (result)
        else :
            result = eff.columns
        return result
    # end def columns

    @TFL.Meta.Once_Property
    def mask_col (self) :
        return self.col_map ["mask_len"]
    # end def mask_col

    @TFL.Meta.Once_Property
    def QC (self) :
        return dict \
            ((c.name, c) for c in self.columns)
    # end def QC

    @TFL.Meta.Once_Property
    def _accidental_columns (self) :
        result  = self.ACV.accidental_columns (self)
        col_map = self.col_map
        for c in result :
            col_map [c._saw_postfix] = c
        return result
    # end def _accidental_columns

    def col_values (self, entity) :
        acv    = self.ACV (self, entity)
        result = self.__super.col_values (entity)
        acvs   = \
            ((c.name, cv) for c, cv in zip (self._accidental_columns, acv))
        return tuple (result) + tuple (acvs)
    # end def col_values

    def q_exp_get_ob (self, q_getter, QR, col, tail_name) :
        if tail_name :
            return self.__super.q_exp_get \
                (q_getter, QR, col, tail_name, saw_name = "_saw_order_by")
        else :
            return self._q_exp_get_ob (q_getter, QR, col, tail_name)
    # end def q_exp_get_ob

    def update_col_map (self, mapper, col_map, prefix = None, columns = None) :
        columns = self.columns [:- len (self._accidental_columns)]
        self.__super.update_col_map (mapper, col_map, prefix, columns)
    # end def update_col_map

    def _q_exp_bin_apply (self, q_exp, QR, ETW, lhs, op_name, rhs) :
        op_map  = self.op_map
        opg     = op_map.get (op_name)
        if opg is None or isinstance (lhs, (SA.Operators, SA.expression)) :
            result = self.__super._q_exp_bin_apply \
                (q_exp, QR, ETW, lhs, op_name, rhs)
        else :
            ACV    = self.ACV
            l_acv  = ACV (self, lhs)
            r_acv  = ACV (self, rhs)
            result = opg (self) (q_exp, QR, ETW, l_acv, op_name, r_acv)
        return result
    # end def _q_exp_bin_apply

    def _q_exp_call_apply (self, q_exp, QR, ETW, lhs, op_name) :
        op_map  = self.op_map
        try :
            opg = op_map [op_name]
        except KeyError :
            result = self.__super._q_exp_call_apply \
                (q_exp, QR, ETW, lhs, op_name)
        else :
            l_ACV = r_ACV = self.ACV
            if op_name == "in_" :
                r_ACV = self.ACV_N
            elif op_name == "contains" :
                l_ACV = self.ACV_N
            l_acv  = l_ACV  (self, lhs)
            op     = opg    (self)
            @TFL.Attributed (__name__ = op.__name__)
            def result (rhs) :
                r_acv = r_ACV (self, rhs)
                return op (q_exp, QR, ETW, l_acv, op_name, r_acv)
        return result
    # end def _q_exp_call_apply

# end class _Kind_CIDR_Wrapper_

class _Kind_CIDR_Wrapper_4_ (_Kind_CIDR_Wrapper_) :

    ACV_N      = ACV_IP4_Network

    min_value  = MOM.Attr.A_Int.min_value_32

    ### for IP4_Address, a single function can do all work, using `operator`
    op_eq      = \
    op_ge      = \
    op_gt      = \
    op_le      = \
    op_lt      = \
    op_ne      = TFL.Meta.Alias_Property ("op_bin")

    def op_bin (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        return getattr (operator, op_name) (l_acv.numeric, r_acv.numeric)
    # end def op_bin

    def op_contains (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        result = SA.sql.and_ \
            ( l_acv.numeric <= r_acv.numeric
            , r_acv.numeric <= l_acv.upper_bound
            )
        return result
    # end def op_contains

    def op_in (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        result = SA.sql.and_ \
            ( r_acv.numeric <= l_acv.numeric
            , l_acv.numeric <= r_acv.upper_bound
            )
        return result
    # end def op_in

# end class _Kind_CIDR_Wrapper_4_

class _Kind_CIDR_Wrapper_6_ (_Kind_CIDR_Wrapper_) :

    ACV_N      = ACV_IP6_Network

    max_value  = MOM.Attr.A_Int.max_value_64
    min_value  = MOM.Attr.A_Int.min_value_64

    def op_contains (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        AND    = SA.sql.and_
        OR     = SA.sql.or_
        result = OR \
            ( AND
                ( l_acv.numeric__hi <  r_acv.numeric__hi
                , r_acv.numeric__hi <  l_acv.upper_bound__hi
                )
            , AND
                ( l_acv.numeric__hi == r_acv.numeric__hi
                , l_acv.numeric__lo <= r_acv.numeric__lo
                , r_acv.numeric__lo <= l_acv.upper_bound__lo
                )
            , AND
                ( r_acv.numeric__hi == l_acv.upper_bound__hi
                , l_acv.numeric__lo <= r_acv.numeric__lo
                , r_acv.numeric__lo <= l_acv.upper_bound__lo
                )
            )
        return result
    # end def op_contains

    def op_eq (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        AND    = SA.sql.and_
        result = AND \
            ( l_acv.numeric__hi == r_acv.numeric__hi
            , l_acv.numeric__lo == r_acv.numeric__lo
            )
        return result
    # end def op_eq

    def op_ge (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        AND    = SA.sql.and_
        OR     = SA.sql.or_
        result = OR \
            ( l_acv.numeric__hi >  r_acv.numeric__hi
            , AND
                ( l_acv.numeric__hi == r_acv.numeric__hi
                , l_acv.numeric__lo >= r_acv.numeric__lo
                )
            )
        return result
    # end def op_ge

    def op_gt (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        AND    = SA.sql.and_
        OR     = SA.sql.or_
        result = OR \
            ( l_acv.numeric__hi >  r_acv.numeric__hi
            , AND
                ( l_acv.numeric__hi == r_acv.numeric__hi
                , l_acv.numeric__lo >  r_acv.numeric__lo
                )
            )
        return result
    # end def op_gt

    def op_in (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        AND = SA.sql.and_
        OR  = SA.sql.or_
        return OR \
            ( AND
                ( r_acv.numeric__hi <  l_acv.numeric__hi
                , l_acv.numeric__hi <  r_acv.upper_bound__hi
                )
            , AND
                ( r_acv.numeric__hi == l_acv.numeric__hi
                , r_acv.numeric__lo <= l_acv.numeric__lo
                , l_acv.numeric__lo <= r_acv.upper_bound__lo
                )
            , AND
                ( l_acv.numeric__hi == r_acv.upper_bound__hi
                , r_acv.numeric__lo <= l_acv.numeric__lo
                , l_acv.numeric__lo <= r_acv.upper_bound__lo
                )
            )
    # end def op_in

    def op_le (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        AND    = SA.sql.and_
        OR     = SA.sql.or_
        result = OR \
            ( l_acv.numeric__hi <  r_acv.numeric__hi
            , AND
                ( l_acv.numeric__hi == r_acv.numeric__hi
                , l_acv.numeric__lo <= r_acv.numeric__lo
                )
            )
        return result
    # end def op_le

    def op_lt (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        AND    = SA.sql.and_
        OR     = SA.sql.or_
        result = OR \
            ( l_acv.numeric__hi <  r_acv.numeric__hi
            , AND
                ( l_acv.numeric__hi == r_acv.numeric__hi
                , l_acv.numeric__lo <  r_acv.numeric__lo
                )
            )
        return result
    # end def op_lt

    def op_ne (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        return SQ.sql.not_ (self.op_eq (q_exp, QR, ETW, l_acv, op_name, r_acv))
    # end def op_ne

# end class _Kind_CIDR_Wrapper_6_

class _Kind_CIDR_Wrapper_Net_Mixin (_Kind_CIDR_Wrapper_) :

    def op_contains (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        result = SA.sql.and_ \
            ( self.__super.op_contains (q_exp, QR, ETW, l_acv, op_name, r_acv)
            , l_acv.mask_len <= r_acv.mask_len
            )
        return result
    # end def op_contains

    def op_eq (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        return SA.sql.and_ \
            ( self.__super.op_eq (q_exp, QR, ETW, l_acv, op_name, r_acv)
            , l_acv.mask_len == r_acv.mask_len
            )
    # end def op_eq

    def op_ge (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        _super = self.__super
        return SA.sql.or_ \
            ( _super.op_gt (q_exp, QR, ETW, l_acv, op_name, r_acv)
                ### yes, really `__super.op_gt`
            , SA.sql.and_
                ( _super.op_eq (q_exp, QR, ETW, l_acv, op_name, r_acv)
                , l_acv.mask_len <= r_acv.mask_len
                )
            )
    # end def op_ge

    def op_gt (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        _super = self.__super
        return SA.sql.or_ \
            ( _super.op_gt (q_exp, QR, ETW, l_acv, op_name, r_acv)
            , SA.sql.and_
                ( _super.op_eq (q_exp, QR, ETW, l_acv, op_name, r_acv)
                , l_acv.mask_len < r_acv.mask_len
                )
            )
    # end def op_gt

    def op_in (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        result = SA.sql.and_ \
            ( self.__super.op_in (q_exp, QR, ETW, l_acv, op_name, r_acv)
            , r_acv.mask_len <= l_acv.mask_len
            )
        return result
    # end def op_in

    def op_le (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        _super = self.__super
        return SA.sql.or_ \
            ( _super.op_lt (q_exp, QR, ETW, l_acv, op_name, r_acv)
                ### yes, really `__super.op_lt`
            , SA.sql.and_
                ( _super.op_eq (q_exp, QR, ETW, l_acv, op_name, r_acv)
                , l_acv.mask_len >= r_acv.mask_len
                )
            )
    # end def op_le

    def op_lt (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        _super = self.__super
        return SA.sql.or_ \
            ( _super.op_lt (q_exp, QR, ETW, l_acv, op_name, r_acv)
            , SA.sql.and_
                ( _super.op_eq (q_exp, QR, ETW, l_acv, op_name, r_acv)
                , l_acv.mask_len > r_acv.mask_len
                )
            )
    # end def op_lt

    def op_ne (self, q_exp, QR, ETW, l_acv, op_name, r_acv) :
        return SA.sql.and_ \
            ( self.__super.op_ne (q_exp, QR, ETW, l_acv, op_name, r_acv)
            , l_acv.mask_len != r_acv.mask_len
            )
    # end def op_ne

# end class _Kind_CIDR_Wrapper_Net_Mixin

@TFL.Add_To_Class ("_SAW_Wrapper", GTW.OMP.NET.A_IP4_Address)
class Kind_Wrapper_IP4_Address (_Kind_CIDR_Wrapper_4_) :

    mask_col  = SA.sql.bindparam ("mask_len", value = 32)

    def _q_exp_get_ob (self, q_getter, QR, col, tail_name) :
        return (self.col_map ["numeric"], ), ()
    # end def _q_exp_get_ob

# end class Kind_Wrapper_IP4_Address

@TFL.Add_To_Class ("_SAW_Wrapper", GTW.OMP.NET.A_IP4_Network)
class Kind_Wrapper_IP4_Network \
          (_Kind_CIDR_Wrapper_Net_Mixin, _Kind_CIDR_Wrapper_4_) :

    def _q_exp_get_ob (self, q_getter, QR, col, tail_name) :
        col_map = self.col_map
        return (col_map ["numeric"], col_map ["mask_len"]), ()
    # end def _q_exp_get_ob

# end class Kind_Wrapper_IP4_Network

@TFL.Add_To_Class ("_SAW_Wrapper", GTW.OMP.NET.A_IP6_Address)
class Kind_Wrapper_IP6_Address (_Kind_CIDR_Wrapper_6_) :

    mask_col  = SA.sql.bindparam ("mask_len", value = 128)

    def _q_exp_get_ob (self, q_getter, QR, col, tail_name) :
        col_map = self.col_map
        return (col_map ["numeric__hi"], col_map ["numeric__lo"]), ()
    # end def _q_exp_get_ob

# end class Kind_Wrapper_IP6_Address

@TFL.Add_To_Class ("_SAW_Wrapper", GTW.OMP.NET.A_IP6_Network)
class Kind_Wrapper_IP6_Network \
          (_Kind_CIDR_Wrapper_Net_Mixin, _Kind_CIDR_Wrapper_6_) :

    def _q_exp_get_ob (self, q_getter, QR, col, tail_name) :
        col_map = self.col_map
        return \
            ( col_map ["numeric__hi"]
            , col_map ["numeric__lo"]
            , col_map ["mask_len"]
            ), ()
    # end def _q_exp_get_ob

# end class Kind_Wrapper_IP6_Network

@TFL.Add_To_Class ("_saw_column_type", GTW.OMP.NET._A_CIDR_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_column_type_CIDR (self, DBW, wrapper, pts) :
    return _CIDR_Type_ ()
# end def _saw_column_type_CIDR

@TFL.Add_To_Class \
    ("_saw_extract_field", GTW.OMP.NET.A_IP4_Network, GTW.OMP.NET._A_CIDR_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_extract_field_mask_CIDR (self, DBW, col, field) :
    if field == "mask_len" :
        return col.MOM_Wrapper.mask_col
    raise AttributeError (field)
# end def _saw_extract_field_mask_CIDR

@TFL.Add_To_Class ("_saw_kind_wrapper", GTW.OMP.NET._A_CIDR_)
@Single_Dispatch_Method (T = SAW.Manager.__class__)
def _saw_kind_wrapper_CIDR (self, DBW, ETW, kind, ** kw) :
    return self._SAW_Wrapper (ETW, kind, ** kw)
# end def _saw_kind_wrapper_CIDR

if __name__ != "__main__" :
    GTW.OMP.NET._Export_Module ()
### __END__ GTW.OMP.NET.SAW

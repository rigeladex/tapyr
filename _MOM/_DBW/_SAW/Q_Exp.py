# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.
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
#    MOM.DBW.SAW.Q_Exp
#
# Purpose
#    Augment Q_Exp-classes with saw-specific behavior
#
# Revision Dates
#     8-Jul-2013 (CT) Creation
#     9-Jul-2013 (CT) Add `_saw_filter_bin`, `_saw_filter_una`
#     9-Jul-2013 (CT) Factor `_saw_attr_wrapper`
#    11-Jul-2013 (CT) Add `_saw_filter_call`, `_saw_filter_bool`,
#                     `_saw_filter_func`
#    12-Jul-2013 (CT) Use `q_exp_call`, `q_exp_func`, and `q_exp_una`,
#                     not home-grown code
#    13-Jul-2013 (CT) Add `_saw_order_by_una`, `_saw_order_by_sb`
#    15-Jul-2013 (CT) Add `_saw_order_by_get`
#    18-Jul-2013 (CT) Add legacy lifters for `tn_pid`
#    19-Jul-2013 (CT) Change `_saw_attr_wrapper` to handle raw names
#    27-Jul-2013 (CT) Add support for `Q.BVAR` (`_saw_filter_bvar`)
#    28-Jul-2013 (CT) Change `_saw_filter_bvar` to add `self` to `QR.bvar_man`
#    30-Jul-2013 (CT) Add `Q.SUM` (`_saw_filter_sum`)
#     4-Aug-2013 (CT) Change `_saw_filter_bool` to use `fix_bool`
#    22-Aug-2013 (CT) Remove kludge for `tn_pid`
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM                       import MOM
from   _TFL                       import TFL
from   _TFL.pyk                   import pyk

from   _MOM._DBW._SAW             import SAW, SA
from   _MOM.SQ                    import Q

import _MOM._DBW._SAW.Attr

from   _TFL._Meta.Single_Dispatch import Single_Dispatch_Method
from   _TFL.predicate             import split_hst

import _TFL.Accessor
import _TFL.Decorator
import _TFL.Filter
import _TFL.Q_Exp
import _TFL.Sorted_By

import operator

TFL._Filter_Q_.predicate_precious_p = True

_ob_cache = {}

@TFL.Add_To_Class ("_saw_attr_wrapper", TFL.Q_Exp.Q_Root)
def _saw_attr_wrapper (self, QR, ETW) :
    head, _, tail = split_hst (self._name, ".")
    try :
        wrapper = ETW.q_able_attrs [head]
    except KeyError as exc :
        ### raw names aren't in `q_able_attrs`, but they are in `ETW.QC`
        try :
            col  = ETW.QC [head]
        except KeyError as exc :
            raise TypeError \
                ("Unknown attribute `%s` for %s" % (head, ETW.type_name))
        else :
            wrapper = col.MOM_Wrapper
    return wrapper, head, tail
# end def _saw_attr_wrapper

@TFL.Add_To_Class ("_saw_filter", TFL.Q_Exp._Bin_Bool_, TFL.Q_Exp._Bin_Expr_)
def _saw_filter_bin (self, QR, ETW) :
    akw, head, tail = self.lhs._saw_attr_wrapper (QR, ETW)
    return akw.q_exp_bin (self, QR, ETW, tail)
# end def _saw_filter_bin

@TFL.Add_To_Class ("_saw_filter", TFL.Q_Exp.BVAR)
def _saw_filter_bvar (self, QR, ETW) :
    QR.bvar_man.add (self)
    return (SA.sql.bindparam (self._name), ), ()
# end def _saw_filter_bvar

@TFL.Add_To_Class ("_saw_filter", TFL.Filter_And, TFL.Filter_Or, TFL.Filter_Not)
def _saw_filter_bool (self, QR, ETW) :
    sa_exp   = getattr (SA.expression, self.op_name + "_")
    jxs      = []
    wxs      = []
    fix_bool = SAW.Attr.fix_bool
    for p in self.predicates :
        try :
            sf = p._saw_filter
        except AttributeError :
            raise TypeError \
                ("Unsupported predicate `%s` for %s" % (p, ETW.type_name))
        else :
            wx, jx = sf (QR, ETW)
            wxs.extend  (fix_bool (QR, ETW, wx))
            jxs.extend  (jx)
    return (sa_exp (* wxs), ), jxs
# end def _saw_filter_bool

@TFL.Add_To_Class ("_saw_filter", TFL.Attr_Query._Call_)
def _saw_filter_call (self, QR, ETW) :
    akw, head, tail = self.lhs._saw_attr_wrapper (QR, ETW)
    return akw.q_exp_call (self, QR, ETW, tail)
# end def _saw_filter_call

@TFL.Add_To_Class ("_saw_filter", TFL.Q_Exp._Func_)
def _saw_filter_func (self, QR, ETW) :
    akw, head, tail = self.lhs._saw_attr_wrapper (QR, ETW)
    return akw.q_exp_func (self, QR, ETW, tail)
# end def _saw_filter_func

@TFL.Add_To_Class ("_saw_filter", TFL.Q_Exp._Get_)
def _saw_filter_get (self, QR, ETW) :
    akw, head, tail = self._saw_attr_wrapper (QR, ETW)
    try :
        col  = ETW.QC [head]
    except KeyError :
        raise TypeError \
            ("Unknown attribute `%s` for %s" % (self._name, ETW.type_name))
    return akw.q_exp_get (self, QR, col, tail)
# end def _saw_filter_get

@TFL.Add_To_Class ("_saw_filter", TFL.Q_Exp._Sum_)
def _saw_filter_sum (self, QR, ETW) :
    rhs = self.rhs
    try :
        sf     = getattr (rhs, "_saw_filter")
    except AttributeError :
        cols, jxs = [rhs], ()
    else :
        cols, jxs = sf (QR, ETW)
    SUM = SA.sql.func.SUM
    return [SUM (c) for c in cols], ()
# end def _saw_filter_sum

@TFL.Add_To_Class ("_saw_filter", TFL.Q_Exp._Una_Bool_, TFL.Q_Exp._Una_Expr_)
def _saw_filter_una (self, QR, ETW) :
    akw, head, tail = self.lhs._saw_attr_wrapper (QR, ETW)
    return akw.q_exp_una (self, QR, ETW, tail)
# end def _saw_filter_una

@TFL.Add_To_Class ("_saw_order_by", TFL.Q_Exp.Q_Root)
def _saw_order_by_q_exp (self, QR, ETW) :
    return self._saw_filter (QR, ETW)
# end def _saw_order_by_q_exp

@TFL.Add_To_Class ("_saw_order_by", TFL.Q_Exp._Get_)
def _saw_order_by_get (self, QR, ETW) :
    akw, head, tail = self._saw_attr_wrapper (QR, ETW)
    try :
        col  = ETW.QC [head]
    except KeyError :
        raise TypeError \
            ("Unknown attribute `%s` for %s" % (self._name, ETW.type_name))
    return akw.q_exp_get_ob (self, QR, col, tail)
# end def _saw_order_by_get

@TFL.Add_To_Class ("_saw_order_by", TFL.Q_Exp._Una_Expr_)
def _saw_order_by_una (self, QR, ETW) :
    desc     = self.op is operator.__neg__
    meth     = self.lhs._saw_order_by if desc else self._saw_filter
    obs, jxs = meth (QR, ETW)
    if desc :
        obs = [o.desc () for o in obs]
    return obs, jxs
# end def _saw_order_by_una

@TFL.Add_To_Class ("_saw_order_by", TFL.Sorted_By)
def _saw_order_by_sb (self, QR, ETW) :
    ck       = (self, ETW)
    result   = _ob_cache.get (ck)
    if result is None :
        result   = _ob_cache [ck] = obs, jxs = [], []
        for crit in self.criteria :
            desc = False
            if isinstance (crit, pyk.string_types) :
                desc = crit.startswith ("-")
                crit = getattr (Q, crit [desc:])
            try :
                so   = crit._saw_order_by
            except AttributeError :
                raise TypeError \
                    ( "Unsupported sorted-by criterion `%s` for %s"
                    % (crit, ETW.type_name)
                    )
            else :
                ob, jx = so (QR, ETW)
                if desc :
                    ob = [o.desc () for o in ob]
                obs.extend (ob)
                jxs.extend (jx)
    return result
# end def _saw_order_by_sb

if __name__ != "__main__" :
    MOM.DBW.SAW._Export_Module ()
### __END__ MOM.DBW.SAW.Q_Exp

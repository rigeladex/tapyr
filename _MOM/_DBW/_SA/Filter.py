# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SA.Filter
#
# Purpose
#    Extend FTL.Filter to support the generation of the SQLAlchemy specific
#    filter/order_by clauses
#
# Revision Dates
#     1-Dec-2009 (MG) Creation
#    10-Dec-2009 (MG) Adopted to new `Q_Exp`, support for `Filter_*` added
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL.Q_Exp
import _TFL.Decorator
import _TFL.Filter
from    sqlalchemy.sql   import expression

@TFL.Add_To_Class ("_sa_filter", TFL.Q_Exp.Get)
def _sa_filter (self, e_type, Attr_Map = {}) :
    return getattr (e_type, self.name)
# end def _sa_filter

@TFL.Add_To_Class ("_sa_filter", TFL.Q_Exp.Bin_Bool, TFL.Q_Exp.Bin_Expr)
def _sa_filter (self, e_type, Attr_Map = {}) :
    args = []
    for arg in self.lhs, self.rhs :
        if hasattr (arg, "_sa_filter") :
            arg = arg._sa_filter (e_type, Attr_Map)
        args.append (arg)
    return getattr (args [0], self.op.__name__) (args [1])
# end def _sa_filter

@TFL.Add_To_Class ("_sa_filter", TFL.Filter_And, TFL.Filter_Or, TFL.Filter_Not)
def _sa_filter (self, e_type, Attr_Map = {}) :
    sa_exp = getattr \
        ( expression
        , "%s_" % (self.__class__.__name__.rsplit ("_",1) [-1].lower (), )
        )
    return sa_exp (* (p._sa_filter (e_type) for p in self.predicates))
# end def _sa_filter

### __END__ MOM.DBW.SA.Filter

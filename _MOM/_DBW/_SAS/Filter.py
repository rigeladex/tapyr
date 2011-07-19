# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2011 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SAS.Filter
#
# Purpose
#    Extend FTL.Filter to support the generation of the code required to use
#    the SQL layer of SQLAlchemy
#
# Revision Dates
#    12-Feb-2010 (MG) Creation (based on SA.Filter)
#     3-May-2010 (MG) Add support for joins for filtering
#     7-May-2010 (MG) Join handling changed (is now a list instead of a set
#                     to keep join order)
#    10-Aug-2010 (MG) `TFL.Q_Exp.Get._sa_filter` fixed
#     2-Sep-2010 (CT) `Get.name`  changed to `Get._name` (ditto for
#                     `Get.getter`)
#     6-Sep-2010 (MG) The join list now requires a 3 element (the join
#                     conidition or `None`)
#    ««revision-date»»···
#--

from   _TFL              import TFL
import _TFL.Accessor
import _TFL.Decorator
import _TFL.Filter
import _TFL.Q_Exp
from    sqlalchemy.sql   import expression
from    _MOM.Q_Exp_Raw   import Get_Raw

SAS_Attr_Map = dict \
    ( type_name = TFL.Getter.Type_Name
    )

@TFL.Add_To_Class ("_sa_filter", TFL.Q_Exp.Get)
def _sa_filter (self, SAQ) :
    joins      = []
    if "." in self._name :
        attr       = self._name.split (".", 1) [0]
        _sa_filter = SAQ._ID_ENTITY_ATTRS.get (attr, None)
        if _sa_filter :
            return _sa_filter (self._name)
    result = SAS_Attr_Map.get (self._name, self._getter) (SAQ)
    if isinstance (result, (list, tuple)) :
        joins, columns = result
    else :
        columns        = (result, )
        col            = columns [0]
        ### if the column is not in the table the SAQ object is linked to ->
        ### add a join to correct table as well
        if col.table != SAQ._SA_TABLE :
           joins.append ((SAQ._SA_TABLE, col.table, None))
    return joins, columns
# end def _sa_filter

@TFL.Add_To_Class ("_sa_filter", TFL.Q_Exp.Bin_Bool, TFL.Q_Exp.Bin_Expr)
def _sa_filter (self, SAQ) :
    args    = []
    joins   = []
    for arg in self.lhs, self.rhs :
        if hasattr (arg, "_sa_filter") :
            ajoins, afilter = arg._sa_filter (SAQ)
            joins.extend (ajoins)
            args.extend  (afilter)
        else :
            if ( args
               and isinstance (self.lhs, Get_Raw)
               and not getattr (args [0], "IS_RAW_COL", False)
               ) :
                arg = args [0].MOM_Kind.from_string (arg)
            args.append (arg)
    return joins, (getattr (args [0], self.op.__name__) (args [1]), )
# end def _sa_filter

@TFL.Add_To_Class ("_sa_filter", TFL.Attr_Query.Call)
def _sa_filter (self, SAQ) :
    joins, clause = self.lhs._sa_filter (SAQ)
    op            = self.op.__name__.lower ()
    return joins, (getattr (clause [0], op) (* self.args), )
# end def _sa_filter

TFL._Filter_Q_.predicate_precious_p = True
@TFL.Add_To_Class ("_sa_filter", TFL.Filter_And, TFL.Filter_Or, TFL.Filter_Not)
def _sa_filter (self, SAQ) :
    sa_exp = getattr \
        ( expression
        , "%s_" % (self.__class__.__name__.rsplit ("_",1) [-1].lower (), )
        )
    joins  = []
    clause = []
    for p in self.predicates :
            ajoins, afilter = p._sa_filter (SAQ)
            joins.extend  (ajoins)
            clause.extend (afilter)
    return joins, (sa_exp (* clause), )
# end def _sa_filter

### __END__ MOM.DBW.SAS.Filter

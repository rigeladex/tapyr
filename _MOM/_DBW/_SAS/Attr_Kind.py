# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glück. All rights reserved
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
#    MOM.DBW.SAS.Attr_Kind
#
# Purpose
#    Add information needed by the SQL database backend to the
#    attribute kinds
#
# Revision Dates
#    11-Feb-2010 (MG) Creation (based on SA.Attr_Kind)
#    15-Feb-2010 (MG) Mapper property functions removed
#    25-Feb-2010 (MG) `_sa_col_name` functions moved into `Attr_Type`
#    ««revision-date»»···
#--

from   _MOM             import MOM
import _MOM._Attr.Type
from   _TFL             import TFL
import _TFL.Decorator

from    sqlalchemy      import orm

@TFL.Add_To_Class ("_sa_column_attrs", MOM.Attr.Kind)
def _sa_kind (self) :
    return dict (nullable = True)
# end def _sa_kind

@TFL.Add_To_Class ("_sa_column_attrs", MOM.Attr.Primary)
def _sa_primary (self) :
    result              = _sa_kind (self)
    result ["nullable"] = False
    return result
# end def _sa_primary

### __END__ MOM.DBW.SAS.Attr_Kind

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library; if not, write to the Free
# Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SA.Attr_Kind
#
# Purpose
#    Add information needed by the SQAlchemy database backend to the
#    attribute kinds
#
# Revision Dates
#    20-Oct-2009 (MG) Creation
#    27-Oct-2009 (MG) Removed `unique` constraint because we actually need a
#                     unique-together which is not possible at a column level
#     4-Nov-2009 (MG) Use `TFL.Add_To_Class`
#    ««revision-date»»···
#--

from   _MOM             import MOM
import _MOM._Attr.Type
from   _TFL             import TFL
import _TFL.Decorator

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

@TFL.Add_To_Class ("_sa_col_name", MOM.Attr.Kind)
def _sa_normal_attr(self) :
    return self.name
# end def _sa_normal_attr

@TFL.Add_To_Class ("_sa_col_name", MOM.Attr.Link_Role)
def _sa_object (self) :
    return "%s_id" % (self.name, )
# end def _sa_object

### __END__ MOM.DBW.SA.Attr_Kind

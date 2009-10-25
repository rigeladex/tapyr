# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glueck. All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    MOM.DBW.SA.Type
#
# Purpose
#    Implement composite sort-key for list of sort criteria
#
# Revision Dates
#     2009-Oct-19 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM               import MOM
import _MOM._Attr.Type
import _MOM._Attr

Attr = MOM.Attr

from sqlalchemy     import types, schema # Table, Column, Integer, String, Boolean, MetaData, ForeignKey

def _sa_bool (self, kind, ** kw) :
    return schema.Column (self.name, types.Boolean, ** kw)
# end def _sa_bool

def _sa_string (self, kind, ** kw) :
    return schema.Column (self.name, types.String (self.max_length), ** kw)
# end def _sa_string

def _sa_int (self, kind, ** kw) :
    return schema.Column (self.name, types.Integer, ** kw)
# end def _sa_int

def _sa_float (self, kind, ** kw) :
    return schema.Column (self.name, types.Float, ** kw)
# end def _sa_float

Attr.A_Boolean._sa_column   = _sa_bool
Attr.A_String._sa_column    = _sa_string
Attr.A_Int._sa_column       = _sa_int
Attr.A_Float._sa_column     = _sa_float

### __END__ MOM.DBW.SA.Type

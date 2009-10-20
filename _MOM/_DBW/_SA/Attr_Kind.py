# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Martin Glück. All rights reserved
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
#    MOM.DBW.SA.Attr_Kind
#
# Purpose
#    Add information needed by the SQAlchemy database backend to the
#    attribute kinds
#
# Revision Dates
#    20-Oct-2009 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM             import MOM
import _MOM._Attr.Type

def _sa_kind (self) :
    return dict (nullable = True)
# end def _sa_kind

def _sa_primary (self) :
    ### __super does not work, don't know whay
    # result = self.__super._sa_column_attrs ()
    result = _sa_kind (self)
    #result ["nullable"] = False
    result ["unique"]   = True
    return result
# end def _sa_primary

def _sa_required (self) :
    ### __super does not work, don't know whay
    # result = self.__super._sa_column_attrs ()
    result = _sa_kind (self)
    result ["nullable"] = False
    return result
# end def _sa_required

MOM.Attr.Kind.    _sa_column_attrs = _sa_kind
MOM.Attr.Primary. _sa_column_attrs = _sa_primary
#MOM.Attr.Required._sa_column_attrs = _sa_required

### __END__ MOM.DBW.SA.Attr_Kind

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
#    MOM.DBW.SA.Session
#
# Purpose
#    SQAlchemy specific session
#
# Revision Dates
#     2009-Oct-19 (MG) Creation
#    ««revision-date»»···
#--

from   _MOM       import MOM
import _MOM._DBW
import _MOM._DBW.Session
import _MOM._DBW._SA
import _MOM._DBW._SA.Type

from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import engine

class _M_SA_Session_ (MOM.DBW.Session.__class__) :
    """Meta class used to create the mapper classes for SQLAlchemy"""

    metadata = schema.MetaData () ### XXX

    def Mapper (cls, e_type) :
        columns   = cls._setup_columns           (e_type)
        prop_dict = cls._setup_mapper_properties (e_type)
        sa_table  = schema.Table \
            (e_type.type_name, cls.metadata, * columns)
        orm.mapper (e_type, sa_table, properties = prop_dict)
        return e_type
    # end def Mapper

    def _setup_columns (cls, e_type) :
        result = [schema.Column ("id",   types.Integer, primary_key = True)]
        for name, attr_kind in e_type._Attributes._attr_dict.iteritems () :
            result.append (attr_kind.attr._sa_column (attr_kind))
        return result
    # end def _setup_columns

    def _setup_mapper_properties (cls, e_type) :
        result = {}
        for name, attr_kind in e_type._Attributes._attr_dict.iteritems () :
            result [name] = orm.synonym (attr_kind.ckd_name, map_column = True)
        return result
    # end def _setup_mapper_properties

# end class _M_SA_Session_

class _SA_Session_ (MOM.DBW.Session) :
    """SQLAlchemy specific session class"""

    _real_name    = "Session"
    __metaclass__ = _M_SA_Session_

    type_name     = "SA"

    ### XXX
    engine        = engine.create_engine ('sqlite:///:memory:', echo = False)
    SA_Session    = orm.sessionmaker    (bind = engine)

    def __init__ (self, scope) :
        self.scope   = scope
        self.session = self.SA_Session ()
    # end def __init__

Session = _SA_Session_ # end class _SA_Session_

if __name__ != '__main__':
    MOM.DBW.SA._Export ("*")
### __END__ ### MOM.DBW.Session

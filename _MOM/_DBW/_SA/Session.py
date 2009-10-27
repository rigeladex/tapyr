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
#    19-Oct-2009 (MG) Creation
#    24-Oct-2009 (MG) Creation continued
#    27-Oct-2009 (MG) Create `UniqueConstraint` for essential primary key
#                     columns
#    ««revision-date»»···
#--

from   _MOM       import MOM
import _MOM._DBW
import _MOM._DBW.Session
import _MOM._DBW._SA
import _MOM._DBW._SA.Attr_Type
import _MOM._DBW._SA.Attr_Kind

from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import engine

class _M_SA_Session_ (MOM.DBW.Session.__class__) :
    """Meta class used to create the mapper classes for SQLAlchemy"""

    metadata = schema.MetaData () ### XXX

    def Mapper (cls, e_type) :
        if e_type.relevant_root :
            bases      = \
                [  b for b in e_type.__bases__
                if getattr (b, "_Attributes", None)
                ]
            if len (bases) > 1 :
                raise NotImplementedError \
                    ("Multiple inheritance currently not supported")
            col_props = dict ()
            unique    = []
            attr_dict = cls._attr_dict     (e_type)
            columns   = cls._setup_columns (e_type, attr_dict, bases, unique)
            if unique :
                columns.append (schema.UniqueConstraint (* unique))
            sa_table  = schema.Table \
                ( e_type.type_name.replace (".", "__")
                , cls.metadata
                , * columns
                )
            col_props  ["properties"] = cls._setup_mapper_properties \
                (e_type, attr_dict, sa_table, bases)
            cls._setup_inheritance (e_type, sa_table, bases, col_props)
            orm.mapper             (e_type, sa_table, ** col_props)
            e_type._sa_table = sa_table
        return e_type
    # end def Mapper

    def _attr_dict (self, e_type) :
        result     = {}
        attr_dict  = e_type._Attributes._attr_dict
        if e_type is e_type.relevant_root :
            for name, attr_kind in attr_dict.iteritems () :
                if attr_kind.save_to_db :
                    result [name] = attr_kind
        else :
            root_attrs = e_type.relevant_root._Attributes._attr_dict
            for name, attr_kind in attr_dict.iteritems () :
                if attr_kind.save_to_db and name not in root_attrs :
                    result [name] = attr_kind
        return result
    # end def _attr_dict

    def _setup_columns (cls, e_type, attr_dict, bases, unique) :
        result = []
        if e_type is not e_type.relevant_root :
            base    = bases [0]
            pk_name = "%s_id" % (base._sa_table.name)
            result.append \
                ( schema.Column
                    ( pk_name, types.Integer
                    , schema.ForeignKey (base._sa_table.c [base._sa_pk_name])
                    , primary_key = True
                    )
                )
        else :
            pk_name = "id"
            result.append \
                ( schema.Column
                    (pk_name, types.Integer, primary_key = True)
                )
        ### we add the inheritance_type in any case to make EMS.SA easier
        result.append \
            ( schema.Column
                ("inheritance_type", types.String (length = 30))
            )
        e_type._sa_pk_name = pk_name
        for name, attr_kind in attr_dict.iteritems () :
            if attr_kind.is_primary :
                unique.append (name)
            result.append \
                ( attr_kind.attr._sa_column
                    (attr_kind, ** attr_kind._sa_column_attrs ())
                )
            if attr_kind.needs_raw_value :
                result.append \
                    ( schema.Column
                        ( attr_kind.attr.raw_name
                        , types.String (length = 60)
                        )
                    )
        return result
    # end def _setup_columns

    def _setup_inheritance (cls, e_type, sa_table, bases, col_prop) :
        e_type._sa_inheritance = True
        if e_type is not e_type.relevant_root :
            col_prop ["inherits"]             = bases [0]
            col_prop ["polymorphic_identity"] = e_type.type_name
        elif e_type.children :
            col_prop ["polymorphic_on"]       = sa_table.c.inheritance_type
            col_prop ["polymorphic_identity"] = e_type.type_name
        else :
            e_type._sa_inheritance            = False
        return col_prop
    # end def _setup_inheritance

    def _setup_mapper_properties (cls, e_type, attr_dict, sa_table, bases) :
        result = {}
        for name, attr_kind in attr_dict.iteritems () :
            ckd           = attr_kind.ckd_name
            ### we need to do this in 2 steps because otherways we hit a
            ### but in sqlalchemy (see: http://groups.google.com/group/sqlalchemy-devel/browse_thread/thread/0cbae608999f87f0?pli=1)
            result [name] = orm.synonym (ckd, map_column = False)
            result [ckd]  = sa_table.c [name]
        return result
    # end def _setup_mapper_properties

# end class _M_SA_Session_

class _SA_Session_ (MOM.DBW.Session) :
    """SQLAlchemy specific session class"""

    _real_name    = "Session"
    __metaclass__ = _M_SA_Session_

    type_name     = "SA"

    ### XXX
    engine        = engine.create_engine ('sqlite:///test.sqlite', echo = False)
    SA_Session    = orm.sessionmaker    (bind = engine)

    def __init__ (self, scope) :
        self.scope   = scope
        self.session = self.SA_Session ()
    # end def __init__

Session = _SA_Session_ # end class _SA_Session_

if __name__ != '__main__':
    MOM.DBW.SA._Export ("*")
### __END__ ### MOM.DBW.Session

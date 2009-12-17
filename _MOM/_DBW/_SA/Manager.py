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
#    MOM.DBW.SA.Manager
#
# Purpose
#    SQAlchemy specific manager backend
#
# Revision Dates
#    19-Oct-2009 (MG) Creation
#    24-Oct-2009 (MG) Creation continued
#    27-Oct-2009 (MG) Create `UniqueConstraint` for essential primary key
#                     columns
#    19-Nov-2009 (CT) `_M_SA_Manager_._attr_dict` simplified
#    19-Nov-2009 (CT) s/Mapper/etype_decorator/
#     4-Dec-2009 (MG) Renamed from `Session` to `Manager`
#     4-Dec-2009 (MG) Once property `session` removed
#    10-Dec-2009 (MG) `load_scope` and `register_scope` added
#    15-Dec-2009 (MG) `Instance_Recreation` mapper extension added
#    15-Dec-2009 (MG) `populate_instance` and `reconstruct_instance` added
#    16-Dec-2009 (MG) `_create_engine` and `_create_session` factored,
#                     assigning of `scope` to `session` moved into
#                     `_create_session`
#                     `prepare` added
#    16-Dec-2009 (MG) Change management added
#    17-Dec-2009 (MG) Set `pid` for instances loaded from the database
#    ««revision-date»»···
#--

from   _MOM       import MOM
import _MOM._DBW
import _MOM._DBW._Manager_
import _MOM._DBW._SA
import _MOM._DBW._SA.Attr_Type
import _MOM._DBW._SA.Attr_Kind
import _MOM._SCM.Change

from sqlalchemy import orm
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import engine as SA_Engine

Type_Name_Type = types.String (length = 30)

class Instance_Recreation (orm.interfaces.MapperExtension) :
    """Ensure that the MOM instances `loaded` from the database are created
       the correct way (e.g.: SA does not call `__init__` if the object is
       loaded/queried from the database).
    """

    def create_instance (self, mapper, select_context, row, etype) :
        instance = etype.__new__ \
            (etype, home_scope = select_context.session.scope)
        instance._sa_pending_reset_attributes = True
        return instance
    # end def create_instance

    def populate_instance (self, mapper, selectcontext, row, instance, **flags) :
        if getattr (instance, "_sa_pending_reset_attributes", False) :
            instance._init_attributes ()
            del instance._sa_pending_reset_attributes
        return orm.EXT_CONTINUE
    # end def populate_instance

    def reconstruct_instance (self, mapper, instance) :
        instance._finish__init__ ()
        instance.pid = (instance.relevant_root.type_name, instance.id)
    # end def reconstruct_instance

# end class Instance_Recreation

class Cached_Role_Clearing (Instance_Recreation) :
    """Clear the cached role attributes if a link is delete"""

    def after_delete (self, mapper, connection, link) :
        for acr in link.auto_cache_roles :
            acr (link, no_value = True)
        return orm.EXT_CONTINUE
    # end def after_delete

# end class Cached_Role_Clearing

class _M_SA_Manager_ (MOM.DBW._Manager_.__class__) :
    """Meta class used to create the mapper classes for SQLAlchemy"""

    metadata         = schema.MetaData () ### XXX

    def create_database (cls, db_uri, scope) :
        engine  = cls._create_engine (db_uri)
        cls.metadata.create_all      (engine)
        return cls._create_session   (engine, scope)
    # end def create_database

    def connect_database (cls, db_uri, scope) :
        return cls._create_session (cls._create_engine (db_uri), scope)
    # end def connect_database

    def _create_engine (cls, db_uri) :
        return SA_Engine.create_engine (db_uri or "sqlite:///:memory:")
    # end def _create_engine

    def _create_session (self, engine, scope) :
        Session       = orm.sessionmaker (bind = engine)
        session       = Session          ()
        session.scope = scope
        return session
    # end def _create_session

    def _create_scope_table (cls, metadata) :
        cls.sa_scope = schema.Table \
            ( "scope_metadata", metadata
            , schema.Column
                ("root_id",        types.Integer, primary_key = True)
            , schema.Column
                ("scope_guid",     types.String (length = 64))
            , schema.Column
                ("root_type_name", Type_Name_Type)
            )
    # end def _create_scope_table

    def _create_SCM_table (cls, metadata) :
        MOM.SCM.Change._Change_._sa_table = schema.Table \
            ( "change_history", metadata
            , schema.Column ("cid",       types.Integer,  primary_key = True)
            , schema.Column ("Type_Name", Type_Name_Type, nullable    = True)
            , schema.Column ("id",        types.Integer,  nullable    = True)
            , schema.Column ("data",      types.Binary,   nullable    = True)
            , schema.Column
                  ( "parent_cid"
                  , types.Integer
                  , schema.ForeignKey ("change_history.cid")
                  )
            )
    # end def _create_SCM_table

    def prepare (cls) :
        cls._create_scope_table           (cls.metadata)
        cls._create_SCM_table             (cls.metadata)
    # end def prepare

    def update_etype (cls, e_type) :
        ### not all e_type's have a relevant_root attribute (e.g.: MOM.Entity)
        if getattr (e_type, "relevant_root", None) :
            bases      = \
                [  b for b in e_type.__bases__
                if getattr (b, "_Attributes", None)
                ]
            if len (bases) > 1 :
                raise NotImplementedError \
                    ("Multiple inheritance currently not supported")
            map_props = dict ()
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
            map_props  ["properties"] = cls._setup_mapper_properties \
                (e_type, attr_dict, sa_table, bases)
            if issubclass (e_type, MOM.Link) :
                map_props ["extension"] = Cached_Role_Clearing ()
            else :
                map_props ["extension"] = Instance_Recreation  ()
            cls._setup_inheritance (e_type, sa_table, bases, map_props)
            orm.mapper             (e_type, sa_table, ** map_props)
            e_type._sa_table = sa_table
    # end def update_etype

    def _attr_dict (self, e_type) :
        attr_dict  = e_type._Attributes._attr_dict
        result     = {}
        root       = e_type.relevant_root
        if e_type is root :
            inherited_attrs = {}
        else :
            inherited_attrs = root._Attributes._attr_dict
        for name, attr_kind in attr_dict.iteritems () :
            if attr_kind.save_to_db and name not in inherited_attrs :
                result [name] = attr_kind
        return result
    # end def _attr_dict

    def load_scope (cls, session, scope) :
        si            = session.query (cls.sa_scope).one ()
        scope.guid    = si.scope_guid
        if si.root_type_name :
            scope.root = getattr \
                (scope, si.root_type_name).query (id = si.root_it).one ()
    # end def load_scope

    def register_scope (cls, session,  scope) :
        kw = dict (scope_guid = scope.guid)
        if scope.root :
            kw ["root_id"]        = scope.root.id
            kw ["root_type_name"] = scope.root.type_name
        session.execute (cls.sa_scope.insert ().values (** kw))
    # end def register_scope

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
        ### we add the type_name in any case to make EMS.SA easier
        result.append (schema.Column ("Type_Name", Type_Name_Type))
        e_type._sa_pk_name = pk_name
        for name, attr_kind in attr_dict.iteritems () :
            attr_kind.attr._sa_col_name = attr_kind._sa_col_name ()
            if attr_kind.is_primary :
                unique.append (attr_kind.attr._sa_col_name)
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
        e_type.has_children    = False
        if e_type is not e_type.relevant_root :
            col_prop ["inherits"]             = bases [0]
            col_prop ["polymorphic_identity"] = e_type.type_name
        elif e_type.children :
            col_prop ["polymorphic_on"]       = sa_table.c.Type_Name
            col_prop ["polymorphic_identity"] = e_type.type_name
            col_prop ["with_polymorphic"]     = "*"
        else :
            e_type._sa_inheritance            = False
            col_prop ["polymorphic_on"]       = sa_table.c.Type_Name
            col_prop ["polymorphic_identity"] = e_type.type_name
        return col_prop
    # end def _setup_inheritance

    def _setup_mapper_properties (cls, e_type, attr_dict, sa_table, bases) :
        result = dict ()
        for name, attr_kind in attr_dict.iteritems () :
            ckd           = attr_kind.ckd_name
            if isinstance (attr_kind, MOM.Attr.Link_Role) :
                result [name] = orm.synonym  (ckd, map_column = False)
                result [ckd]  = orm.relation (attr_kind.role_type)
            else :
                ### we need to do this in 2 steps because otherways we hit a
                ### but in sqlalchemy (see: http://groups.google.com/group/sqlalchemy-devel/browse_thread/thread/0cbae608999f87f0?pli=1)
                result [name] = orm.synonym (ckd, map_column = False)
                result [ckd]  = sa_table.c [name]
        for assoc, roles in getattr (e_type, "link_map", {}).iteritems () :
            for r in roles :
                attr_name = "__".join (assoc.type_name.split (".") + [r.name])
                if not hasattr (e_type, attr_name) :
                    result [attr_name] = orm.dynamic_loader (assoc, cascade = "all")
        return result
    # end def _setup_mapper_properties

# end class _M_SA_Manager_

class Manager (MOM.DBW._Manager_) :
    """SQLAlchemy specific Manager class"""

    __metaclass__ = _M_SA_Manager_
    type_name     = "SA"

# end class Manager

if __name__ != '__main__':
    MOM.DBW.SA._Export ("*")
### __END__ MOM.DBW.Manager

# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck. All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
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
#    17-Dec-2009 (MG) `Instance_Recreation.after_delete` added to update the
#                     change management
#    18-Dec-2009 (MG) Set `children` of change to children of wrapper during
#                     change reconstruction from database
#    21-Dec-2009 (CT) s/load_scope/load_root/
#    30-Dec-2009 (MG) `create_instance` fixed
#    26-Jan-2010 (MG) `commit` added
#    27-Jan-2010 (MG) Db Table generation moved into `etype_decorator`
#                     (needed because when the many to many relations are
#                     setup we need the DB table for the `secondary` argument)
#    27-Jan-2010 (MG) Bug in `_attr_dict` fixed (wrong base class was used to
#                     determin which attribues need to be in the DB)
#                     `_attr_dict` renamed to `_attr_dicts` and changed to
#                     collect the cached role attributes as well
#    27-Jan-2010 (MG) Support for cached roles added
#    30-Jan-2010 (MG) Detection of multiple inheritance changed
#     6-Feb-2010 (MG) `_sa_column` requires attribute instances as parameter
#                     as well
#     6-Feb-2010 (MG) An MOM Attribute can now define multiple columns
#     7-Feb-2010 (MG) Guard against non exitsing `relevant_root` added
#                     (needed for `An_Entity)
#                     `_setup_columns`: parameter `prefix` added
#                     `_setup_composite` added and used
#     8-Feb-2010 (MG) `_setup_composite` changed: don't pass the real e_type
#                     to SA but instance use a function which mappes the
#                     attributes from the database to the attributes of the
#                     entity
#     8-Feb-2010 (MG) Database creation for postgres added
#     8-Feb-2010 (MG) `_setup_composite._create`: changed to use
#                     `from_pickle_cargo` instance of creating the instance
#     8-Feb-2010 (MG) Generator of mapper properties moced into attr kind
#     8-Feb-2010 (MG) `_attr_dicts`: collect `Query` attributes as well
#                     `_setup_columns`: only add columsn which need to be
#                     save to the database to the table
#    ««revision-date»»···
#--
from   _TFL                      import TFL
import _TFL.defaultdict
from   _MOM                      import MOM
import _MOM._DBW
import _MOM._DBW._Manager_
import _MOM._DBW._SA
import _MOM._DBW._SA.Attr_Type
import _MOM._DBW._SA.Attr_Kind
import _MOM._SCM.Change

from   sqlalchemy import orm
from   sqlalchemy import schema
from   sqlalchemy import types
from   sqlalchemy import engine as SA_Engine
import sqlalchemy.orm.collections

Type_Name_Type = types.String (length = 30)

class Instance_Recreation (orm.interfaces.MapperExtension) :
    """Ensure that the MOM instances `loaded` from the database are created
       the correct way (e.g.: SA does not call `__init__` if the object is
       loaded/queried from the database).
    """

    def create_instance (self, mapper, select_context, row, etype) :
        instance = etype.__new__ \
            (etype, scope = select_context.session.scope)
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
        instance.pid = MOM.EMS.SA.PID \
            (instance.relevant_root.type_name, instance.id)
    # end def reconstruct_instance

    def after_delete (self, mapper, connection, entity) :
        if entity.pid :
            entity.home_scope.record_change (MOM.SCM.Change.Destroy, entity)
    # end def after_delete

# end class Instance_Recreation

class SA_Change (object) :
    """The python object representing a OMO change object"""

    _change = None

    def __init__ (self, change) :
        self._type_name = change.pid.Type_Name
        self._obj_id    = change.pid.id
        self._data      = change.as_pickle ()
        self._change    = change
    # end def __init__

    @orm.reconstructor
    def _from_database (self) :
        self._change          = MOM.SCM.Change._Change_.from_pickle (self._data)
        self._change.cid      = self._id
        self._change.children = self.children
        self._change.parent   = self.parent
    # end def _from_database

    def __getattr__ (self, name) :
        return getattr (self._change, name)
    # end def __getattr__

    def __repr__ (self) :
        return repr (self._change)
    # end def __repr__

    def __str__ (self) :
        return str (self._change)
    # end def __str__

    def __nonzero__ (self) :
        return bool (self._change)
    # end def __nonzero__

# end class SA_Change

class SA_Change_Mapper (orm.interfaces.MapperExtension) :

    def after_insert (self, mapper, connection, instance) :
        instance._change.cid = instance._id
    # end def after_insert

# end class SA_Change_Mapper

class _M_SA_Manager_ (MOM.DBW._Manager_.__class__) :
    """Meta class used to create the mapper classes for SQLAlchemy"""

    metadata         = schema.MetaData () ### XXX

    def create_database (cls, db_uri, scope) :
        if db_uri and not db_uri.startswith ("sqlite://") :
            ### we need to issue a create database command
            create_db_uri, db_name = db_uri.rsplit ("/", 1)
            if db_uri.startswith ("postgresql://") :
                cls._create_postgres_db (create_db_uri, db_name)
            elif not db_uri.startswith ("sqlite://") :
                engine  = cls._create_engine (create_db_uri)
                engine.execute ("CREATE DATABASE %s")
        engine  = cls._create_engine (db_uri)
        cls.metadata.create_all      (engine)
        return cls._create_session   (engine, scope)
    # end def create_database

    def _create_postgres_db ( cls, db_uri, db_name
                            , encoding = "utf8"
                            , template = "template0"
                            ) :
        import psycopg2.extensions as PE
        engine = cls._create_engine (db_uri + "/postgres")
        conn   = engine.connect ()
        conn.connection.connection.set_isolation_level \
            (PE.ISOLATION_LEVEL_AUTOCOMMIT)
        conn.execute \
            ( "CREATE DATABASE %s ENCODING='%s' TEMPLATE %s"
            % (db_name, encoding, template)
            )
    # end def _create_postgres_db

    def connect_database (cls, db_uri, scope) :
        return cls._create_session (cls._create_engine (db_uri), scope)
    # end def connect_database

    def _create_engine (cls, db_uri) :
        return SA_Engine.create_engine (db_uri or "sqlite:///:memory:")
    # end def _create_engine

    def _create_session (self, engine, scope) :
        Session                = orm.sessionmaker (bind = engine)
        session                = Session          ()
        session.change_session = Session          ()
        session.scope          = scope
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
        SA_Change._sa_table = Table = schema.Table \
            ( "change_history", metadata
            , schema.Column ("_id",        types.Integer,  primary_key = True)
            , schema.Column ("_type_name", Type_Name_Type, nullable    = True)
            , schema.Column ("_obj_id",    types.Integer,  nullable    = True)
            , schema.Column ("_data",      types.Binary,   nullable    = True)
            , schema.Column
                  ( "_parent_id"
                  , types.Integer
                  , schema.ForeignKey ("change_history._id")
                  )
            )
        orm.mapper \
            ( SA_Change, Table
            , extension = (SA_Change_Mapper ())
            , properties = dict
                ( children = orm.relation
                    ( SA_Change
                    , backref = orm.backref
                        ("parent", remote_side = [Table.c._id])
                    )
                )
            )
    # end def _create_SCM_table

    def prepare (cls) :
        cls._create_scope_table           (cls.metadata)
        cls._create_SCM_table             (cls.metadata)
        cls.role_cacher = TFL.defaultdict (set)
    # end def prepare

    def etype_decorator (cls, e_type) :
        if getattr (e_type, "relevant_root", None) :
            bases      = \
                [  b for b in e_type.__bases__
                if getattr (b, "_Attributes", None)
                ]
            if len (bases) > 1 :
                ### we have more than one base which has an _Attribute class
                ### let's see how many bases `add` _Attributes (have
                ### `_own_names`)
                bases = [b for b in bases if b._Attributes._own_names]
                if len (bases) > 1 :
                    raise NotImplementedError \
                        ( "Multiple inheritance currently not supported\n"
                          "%s, %s"
                        % (e_type.type_name, bases)
                        )
            unique               = []
            db_attrs, role_attrs = cls._attr_dicts (e_type, bases)
            columns   = cls._setup_columns (e_type, db_attrs, bases, unique)
            if unique :
                columns.append (schema.UniqueConstraint (* unique))
            e_type._sa_table = schema.Table \
                (e_type.type_name.replace (".", "__"), cls.metadata, * columns)
            ### save the gathered attribute dict and bases for the
            ### update_etype run
            e_type._sa_save_attrs = bases, db_attrs, role_attrs
            if issubclass (e_type, MOM.Link) :
                for cr in e_type.auto_cache_roles :
                    cls.role_cacher [cr.other_role.role_type.type_name].add \
                        ((cr, e_type))
                e_type.auto_cache_roles = ()
            attr_spec = e_type._Attributes
            for name, attr_kind in role_attrs.iteritems () :
                attr_cls             = attr_spec._own_names [name]
                attr_cls.kind        = MOM.Attr.Cached
                attr_cls.Kind_Mixins = (MOM.Attr.Computed_Mixin, )
                attr_spec._add_prop (e_type, name, attr_cls)
        return e_type
    # end def etype_decorator

    def update_etype (cls, e_type, app_type) :
        ### not all e_type's have a relevant_root attribute (e.g.: MOM.Entity)
        if getattr (e_type, "relevant_root", None) :
            sa_table                    = e_type._sa_table
            bases, db_attrs, role_attrs = e_type._sa_save_attrs
            ### remove the attributes saved during the `etype_decorator` run
            del e_type._sa_save_attrs
            map_props                 = dict ()
            map_props  ["properties"] = cls._setup_mapper_properties \
                (app_type, e_type, db_attrs, role_attrs, sa_table, bases)
            map_props ["extension"]   = Instance_Recreation  ()
            cls._setup_inheritance (e_type, sa_table, bases, map_props)
            orm.mapper             (e_type, sa_table, ** map_props)
    # end def update_etype

    def _attr_dicts (self, e_type, bases) :
        attr_dict  = e_type._Attributes._attr_dict
        db_attrs   = {}
        role_attrs = {}
        root       = bases and bases [0]
        if e_type is getattr (e_type, "relevant_root", e_type):
            inherited_attrs = {}
        else :
            inherited_attrs = root._Attributes._attr_dict
        for name, attr_kind in attr_dict.iteritems () :
            if name not in inherited_attrs :
                if (  attr_kind.save_to_db
                   or isinstance (attr_kind, MOM.Attr.Query)
                   ) :
                    db_attrs [name] = attr_kind
                elif isinstance ( attr_kind
                                , ( MOM.Attr.Cached_Role
                                  , MOM.Attr.Cached_Role_Set
                                  )
                                ) :
                    role_attrs [name] = attr_kind
        return db_attrs, role_attrs
    # end def _attr_dicts

    def commit (self) :
        self.session.change_session.commit ()
        return sell.__super.commit         ()
    # end def commit

    def load_root (cls, session, scope) :
        si         = session.query (cls.sa_scope).one ()
        scope.guid = si.scope_guid
        if si.root_type_name :
            return getattr \
                (scope, si.root_type_name).query (id = si.root_it).one ()
    # end def load_root

    def register_scope (cls, session,  scope) :
        kw = dict (scope_guid = scope.guid)
        if scope.root :
            kw ["root_id"]        = scope.root.id
            kw ["root_type_name"] = scope.root.type_name
        session.execute (cls.sa_scope.insert ().values (** kw))
    # end def register_scope

    def _setup_columns (cls, e_type, db_attrs, bases, unique, prefix = None) :
        result = []
        if getattr (e_type, "relevant_root", None) :
            ### if the e_type has no relevant root it is an `An_Entity` which
            ### does not need a primary key
            if e_type is not e_type.relevant_root :
                base    = bases [0]
                pk_name = "%s_id" % (base._sa_table.name)
                result.append \
                    ( schema.Column
                        ( pk_name, types.Integer
                        , schema.ForeignKey (base._sa_table.c[base._sa_pk_name])
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
        for name, kind in ((n, k) for (n, k) in db_attrs.iteritems () if k.save_to_db):
            attr               = kind.attr
            col_name           = kind._sa_col_name ()
            if prefix :
                col_name       = "__%s_%s" % (prefix, col_name)
            attr._sa_col_name  = col_name
            if kind.is_primary :
                unique.append (attr._sa_col_name)
            result.extend \
                (attr._sa_columns (attr, kind, ** kind._sa_column_attrs ()))
            if kind.needs_raw_value :
                raw_name     = attr.raw_name
                if prefix :
                    raw_name = "__%s_%s" % (prefix, raw_name)
                result.append \
                    (schema.Column (raw_name, types.String (length = 60)))
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

    def _setup_mapper_properties ( cls
                                 , app_type
                                 , e_type
                                 , db_attrs
                                 , role_attrs
                                 , sa_table
                                 , bases
                                 ) :
        result = dict ()
        for name, attr_kind in db_attrs.iteritems () :
            ckd           = attr_kind.ckd_name
            attr_kind._sa_mapper_prop (name, ckd, e_type, result)
        for cr, assoc_et in cls.role_cacher.get (e_type.type_name, ()) :
            cls._cached_role \
                (app_type, getattr (e_type, cr.attr_name), cr, assoc_et)
        ### we need this attributes to trigger the cascading
        for assoc, roles in getattr (e_type, "link_map", {}).iteritems () :
            for r in roles :
                attr_name = "__".join (assoc.type_name.split (".") + [r.name])
                if not hasattr (e_type, attr_name) :
                    result [attr_name] = orm.dynamic_loader (assoc, cascade = "all")
        return result
    # end def _setup_mapper_properties

    def _cached_role (cls, app_type, attr_kind, cr, assoc_et) :
        assoc_sa    = assoc_et._sa_table
        q_attr      = assoc_sa.c \
            [getattr (assoc_et, cr.role_name      ).attr._sa_col_name]
        f_attr      = assoc_sa.c \
            [getattr (assoc_et, cr.other_role.name).attr._sa_col_name]
        singleton   = isinstance (cr, MOM.Role_Cacher_1)
        result_et   = app_type [attr_kind.Class.type_name]
        def computed_crn (self) :
            session = self.home_scope.ems.session
            pk      = getattr (self, self._sa_pk_name)
            links   = session.query (q_attr).filter (f_attr == pk)
            query   = session.query (result_et).filter \
                (getattr (result_et, result_et._sa_pk_name).in_ (links))
            if singleton :
                return query.first ()
            return query
        # end def computed_crn
        attr_kind.attr.computed = computed_crn
    # end def _cached_role

# end class _M_SA_Manager_

class Manager (MOM.DBW._Manager_) :
    """SQLAlchemy specific Manager class"""

    __metaclass__ = _M_SA_Manager_
    type_name     = "SA"

# end class Manager

if __name__ != '__main__':
    MOM.DBW.SA._Export ("*")
### __END__ MOM.DBW.Manager

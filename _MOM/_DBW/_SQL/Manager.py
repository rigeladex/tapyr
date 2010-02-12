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
#    MOM.DBW.SQL.Manager
#
# Purpose
#    Manager using the SQL layer of SQAlchemy.
#
# Revision Dates
#    11-Feb-2010 (MG) Creation (based on SA.Manager)
#    ««revision-date»»···
#--
from   _TFL                      import TFL
import _TFL.defaultdict
from   _MOM                      import MOM
import _MOM._DBW
import _MOM._DBW._Manager_
import _MOM._DBW._SQL
import _MOM._DBW._SQL.Attr_Type
import _MOM._DBW._SQL.Attr_Kind
import _MOM._DBW._SQL.Query
import _MOM._DBW._SQL.Session
import _MOM._SCM.Change

from   sqlalchemy import schema, types, sql
from   sqlalchemy import engine as SQL_Engine

Type_Name_Type = types.String (length = 30)

class _M_SQL_Manager_ (MOM.DBW._Manager_.__class__) :
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
        return SQL_Engine.create_engine (db_uri or "sqlite:///:memory:")
    # end def _create_engine

    def _create_session (self, engine, scope) :
        return MOM.DBW.SQL.Session (scope, engine)
    # end def _create_session

    def _create_scope_table (cls, metadata) :
        cls.sa_scope = Table = schema.Table \
            ( "scope_metadata", metadata
            , schema.Column
                ("root_id",        types.Integer, primary_key = True)
            , schema.Column
                ("scope_guid",     types.String (length = 64))
            , schema.Column
                ("root_type_name", Type_Name_Type)
            )
        MOM.DBW.SQL.Query (Table, Table)
    # end def _create_scope_table

    def _create_SCM_table (cls, metadata) :
        MOM.SCM.Change._Change_._sa_table = Table = schema.Table \
            ( "change_history", metadata
            , schema.Column ("cid",       types.Integer,  primary_key = True)
            , schema.Column ("Type_Name", Type_Name_Type, nullable    = True)
            , schema.Column ("obj_id",    types.Integer,  nullable    = True)
            , schema.Column ("data",      types.Binary,   nullable    = True)
            , schema.Column
                  ( "parent_cid"
                  , types.Integer
                  , schema.ForeignKey ("change_history.cid")
                  )
            )
        MOM.DBW.SQL.Query \
            (MOM.SCM.Change._Change_, Table, parent = "parent_cid")
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
                if getattr (b, "relevant_root", None)
                ]
            if len (bases) > 1 :
                ### we have more than one base which has a relevant_root
                raise NotImplementedError \
                    ( "Multiple inheritance currently not supported\n"
                      "%s, %s"
                    % (e_type.type_name, bases)
                    )
            unique               = []
            e_type._sa_pk_base   = {}
            db_attrs, role_attrs = cls._attr_dicts (e_type, bases)
            columns   = cls._setup_columns (e_type, db_attrs, bases, unique)
            if unique :
                unique = [schema.UniqueConstraint (* unique)]
            e_type._sa_table = schema.Table \
                (e_type.type_name.replace (".", "__"), cls.metadata
                , * (columns + unique)
                )
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
                attr_spec._add_prop    (e_type, name, attr_cls)
            MOM.DBW.SQL.SQL_Interface (e_type, columns, bases)
        return e_type
    # end def etype_decorator

    def update_etype (cls, e_type, app_type) :
        ### not all e_type's have a relevant_root attribute (e.g.: MOM.Entity)
        if getattr (e_type, "relevant_root", None) :
            sa_table                    = e_type._sa_table
            bases, db_attrs, role_attrs = e_type._sa_save_attrs
            ### remove the attributes saved during the `etype_decorator` run
            del e_type._sa_save_attrs
            MOM.DBW.SQL.MOM_Query     (e_type, sa_table, db_attrs, bases)
            e_type._SQL.setup_selects ()
        if 0:
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
        result     = session.connection.execute \
            (cls.sa_scope.select ().limit (1))
        si        = result.fetchone ()
        result.close ()
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
        session.commit  ()
    # end def register_scope

    def _setup_columns ( cls, e_type, db_attrs, bases, unique
                       , prefix       = None
                       , unique_attrs = set ()
                       ) :
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
                e_type._sa_pk_base [base.type_name] = pk_name
            else :
                pk_name = "id"
                result.append \
                    ( schema.Column
                        (pk_name, types.Integer, primary_key = True)
                    )
                result.append (schema.Column ("Type_Name", Type_Name_Type))
            e_type._sa_pk_name = pk_name
        for name, kind in ((n, k) for (n, k) in db_attrs.iteritems () if k.save_to_db):
            attr               = kind.attr
            col_name           = kind._sa_col_name ()
            if prefix :
                col_name       = "__%s_%s" % (prefix, col_name)
            attr._sa_col_name  = col_name
            if kind.is_primary or name in unique_attrs :
                unique.append (attr._sa_col_name)
            result.extend \
                ( attr._sa_columns
                    (attr, kind, unique, ** kind._sa_column_attrs ())
                )
            if kind.needs_raw_value :
                raw_name     = attr.raw_name
                if prefix :
                    raw_name = "__%s_%s" % (prefix, raw_name)
                col = schema.Column (raw_name, types.String (length = 60))
                col.mom_kind = kind
                col.mom_raw  = True
                result.append (col)
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
        MOM.DBW.SQL.MOM_Query (e_type, sa_table, db_attrs, bases)
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

# end class _M_SQL_Manager_

class Manager (MOM.DBW._Manager_) :
    """SQLAlchemy specific Manager class"""

    __metaclass__ = _M_SQL_Manager_
    type_name     = "SQL"

# end class Manager

if __name__ != '__main__':
    MOM.DBW.SQL._Export ("*")
### __END__ MOM.DBW.Manager

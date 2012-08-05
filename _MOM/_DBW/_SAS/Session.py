# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DBW.SAS.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SAS.Session
#
# Purpose
#    A database session
#
# Revision Dates
#    11-Feb-2010 (MG) Creation
#    16-Feb-2010 (MG) `_query_object` removed
#    16-Feb-2010 (MG) `Type_Name` added
#                     `attr_kind.get_pickle_cargo` is now used to get the
#                     values of the cooked and raw attribute values
#    16-Feb-2010 (MG) `delete` enhanced: dispose the connection pool of the
#                     engine to make sure all connection will be closed
#    20-Feb-2010 (MG) `SAS_Interface.reconstruct` fixed PID creation
#    25-Feb-2010 (MG) Bug on `Session._setup_columns` fixed (raw values where
#                     not handled correctly)
#    26-Feb-2010 (MG) `_setup_columns` fixed
#    18-Mar-2010 (MG) `Session.delete`: delete link's before the actual object get's
#                     deleted from the database
#    18-Mar-2010 (MG) `SAS_Interface.delete`: need to delete the entries in the tables
#                     top-down
#    19-Mar-2010 (MG) Bug in `value_dict` fixed and streamlined
#    23-Mar-2010 (CT) `_setup_columns` fixed ???
#                     (s/et/e_type/ in if-clause for `_Composite_Mixin_`)
#    24-Mar-2010 (MG) `_setup_columns` use new `_sa_prefix` attribute of kind
#    11-May-2010 (MG) `value_dict` remove items from `attrs` once handled
#    12-May-2010 (MG) New `pid` style
#    17-May-2010 (MG) `add` changed to allow `id` parameter
#     1-Jun-2010 (MG) Rollback handling fixed
#    29-Jun-2010 (CT) s/from_pickle_cargo/from_attr_pickle_cargo/
#     1-Jul-2010 (MG) `_Session_` factored, `Session_S` and `Session_PC` added
#     1-Jul-2010 (MG) `SAS_Interface.pickle_cargo` factored
#     1-Jul-2010 (MG) `Session_PC.produce_entities` and
#                     `Session_PC.produce_changes` implemented
#     1-Jul-2010 (CT) `compact` added (does nothing for now)
#     1-Jul-2010 (MG) `SAS_PC_Transform` support added
#     2-Jul-2010 (MG) `produce_changes` changed and `consume` added
#     2-Jul-2010 (MG) `db_meta_data` added
#     5-Jul-2010 (MG) `register_scope` and `load_root` moved in here
#     5-Jul-2010 (MG) `change_readonly` implemented
#    15-Jul-2010 (MG) `register_scope` changed to use `guid` from `db_meta_data`
#                     `insert_cargo` fixed
#    15-Jul-2010 (MG) `_Session_.load_root`: check for compatible database
#                     version hash added
#    15-Jul-2010 (MG) `_Session_.close`: close the PID-manager as well to
#                     make sure all connections are closed
#     2-Aug-2010 (MG) `_pickle_cargo_for_table` fixed
#    11-Aug-2010 (CT) `_new_db_meta_data` factored and redefined for
#                     `Session_PC`
#    11-Aug-2010 (MG) `load_info` factored from `load_root`
#    11-Aug-2010 (MG) `readonly` handling added
#    13-Aug-2010 (CT) s/read_only/readonly/g
#    15-Aug-2010 (MG) `commit`: use `self.scope.rollback` instead of
#                     `self.rollback` to clear all internal fields as well
#    15-Aug-2010 (MG) `_close_connection` factored, `pid_query` added
#    16-Aug-2010 (CT) Adapted to change of signature of `DB_Meta_Data.COPY`
#    16-Aug-2010 (MG) `SAS_Interface.joined_tables` added
#    16-Aug-2010 (MG) `Session_S.recreate_change` fixed to create all
#                     children changes as well
#                     `_consume_change_iter` fixed to add the parent change
#                     before the children will be added
#     8-Sep-2010 (MG) `Session_S.update_change` added
#    15-Sep-2010 (CT) `flush` changed to use `pending_attr_changes`,
#                     guard for `entity` added
#    24-Feb-2011 (CT) s/A_Object/A_Entity/
#     8-Jun-2011 (MG) `temp_connection` added and used
#     8-Jun-2011 (MG) `temp_connection` removed again because in did not work
#                     with `sqlite` (which can only handle one connection per
#                     thread ((o:)
#     9-Jun-2011 (MG) `SAS_Interface.last_cid` added
#                     `SAS_Interface.reconstruct`: `r_last_cid` added
#                     `SAS_Interface.update` changed to honor
#                     `engine.query_last_cid_on_update`
#                     `_Session_.load_info`: no need to `rollback`
#    22-Sep-2011 (CT) s/A_Entity/A_Id_Entity/
#    22-Sep-2011 (CT) s/C_Type/P_Type/ for _A_Composite_ attributes
#    20-Jan-2012 (CT) Esthetics
#    29-Mar-2012 (MG) `Session.delete`: filter partial links
#    30-Mar-2012 (MG) `_in_rollback` checks added to prevent database
#                     activities during transaction rollback
#    10-Apr-2012 (CT) Remove debug message from `flush`
#    27-Apr-2012 (MG) `Session_PC.consume` handling of `max_cid` added
#    27-Apr-2012 (MG) `_Session_.close` try to close the connection added
#                     (this is required for Sqlite to make sure that the file
#                     is really closed)
#    06-May-2012 (MG) `_close_connection`: call to `expunge` added
#    11-Jun-2012 (MG) `add_change` set new attributes of change record
#    13-Jun-2012 (CT) Add call of `_finish__init__` to `reconstruct`
#    15-Jun-2012 (MG) `SAS_Interface.reload` added
#    15-Jun-2012 (MG) `Session_S.instance_from_row` support for entity
#                     reloading added
#    22-Jun-2012 (MG) `close_connections` added
#     1-Aug-2012 (MG) `_consume_change_iter` Set `type_name` and `kind`
#     3-Aug-2012 (CT) Use `Ref_Req_Map` instead of `link_map`
#     3-Aug-2012 (MG) Enhance `expunge`
#     3-Aug-2012 (MG) Consider new `Ref_Opt_Map` in delete
#     4-Aug-2012 (CT) Factor `_rollback_uncommitted_changes` to `EMS`
#     4-Aug-2012 (CT) Change `delete` not to set `entity.pid` to None
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object
import _TFL.Accessor
import _TFL.Decorator
import _TFL.I18N

from   _MOM                  import MOM
import _MOM.DB_Meta_Data
import _MOM._DBW._SAS

import  operator
import  itertools
from    sqlalchemy           import sql
import  cPickle              as     Pickle
import  contextlib

ddict_list = lambda : TFL.defaultdict (list)
attrgetter = operator.attrgetter

class Type_Name (object) :
    """A fake kind which is used to retrive the type_name of an entity"""

    class attr (object) :
        name             = "Type_Name"
        SAS_PC_Transform = None
    # end class attr

    @classmethod
    def get_pickle_cargo (cls, entity) :
        return (entity.type_name, )
    # end def get_pickle_cargo

# end class Type_Name

class SAS_Interface (TFL.Meta.Object) :
    """Helper object to store the information how to get all/some values
       needed for the database insert/update from the entity
    """

    def __init__ (self, e_type, columns, bases) :
        e_type._SAS         = self
        self.e_type         = e_type
        self.table          = e_type._sa_table
        self.bases          = bases
        self.pk             = self.table.c [e_type._sa_pk_name]
        self.last_cid       = self.table.c.get ("last_cid")
        self.column_map     = cm = self._gather_columns (e_type, columns, bases)
        ### e_type `None`is used during the reconstruct to get all attributes
        ### for this e_type
        self.e_type_columns = e_type_columns = TFL.defaultdict (ddict_list)
        if e_type is e_type.relevant_root :
            columns = [cm ["Type_Name"]]
            e_type_columns [e_type] [Type_Name] = columns
            e_type_columns [None]   [Type_Name] = columns
        self._setup_columns (e_type, e_type_columns)
    # end def __init__

    def delete (self, session, entity) :
        if not session._in_rollback :
            session.connection.execute \
                (self.table.delete ().where (self.pk == entity.pid))
            for b in self.bases :
                b._SAS.delete (session, entity)
    # end def delete

    def _gather_columns (self, e_type, columns, bases) :
        result   = {}
        for et in reversed (bases) :
            result.update (et._SAS.column_map)
        for c in columns :
            c.mom_e_type    = e_type
            result [c.name] = c
        return result
    # end def _gather_columns

    def insert (self, session, entity) :
        if not session._in_rollback :
            session.write_access = True
            base_pks = dict ()
            if not self.bases :
                base_pks ["pid"] = entity.pid
            pk_map   = self.e_type._sa_pk_base
            for b in self.bases :
                base_pks [pk_map [b.type_name]] = b._SAS.insert \
                    (session, entity)
            result = session.connection.execute \
                ( self.table.insert ().values
                    (self.value_dict (entity, self.e_type, base_pks))
                )
            return result.inserted_primary_key [0]
    # end def insert

    def insert_cargo (self, session, pid, pickle_cargo, type_name = None) :
        if not session._in_rollback :
            session.write_access = True
            type_name = type_name or self.e_type.type_name
            for b in self.bases :
                b._SAS.insert_cargo (session, pid, pickle_cargo, type_name)
            session.connection.execute \
                ( self.table.insert ().values
                    ( self._pickle_cargo_for_table
                        (pickle_cargo, self.e_type, pid, default = type_name))
                )
    # end def insert_cargo

    def _pickle_cargo_for_table ( self, pickle_cargo
                                , e_type
                                , pid
                                , columns = None
                                , default = None
                                ) :
        if columns is None :
            columns = self.e_type_columns [e_type]
        result      = {}
        result [self.e_type._sa_pk_name] = pid
        for kind in columns :
            attr_name          = kind.attr.name
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                result.update \
                    ( self._pickle_cargo_for_table
                        ( pickle_cargo [attr_name] [0]
                        , kind.P_Type
                        , pid
                        , default = kind.P_Type.type_name
                        , columns = columns [kind] [e_type]
                        )
                    )
            else :
                attr_default     = default
                if hasattr (kind, "get_value") :
                    attr_default = kind.get_value (None)
                attr_pc      = pickle_cargo.get (attr_name, (attr_default, ))
                pc_transform = kind.attr.SAS_PC_Transform
                if pc_transform :
                    attr_pc = pc_transform.dump (attr_pc)
                for column, value in zip (columns [kind], attr_pc) :
                    result [column.name] = value
        return result
    # end def _pickle_cargo_for_table

    def pickle_cargo (self, row) :
        pickle_cargo = TFL.defaultdict (list)
        self._pickle_cargo (self.e_type_columns, pickle_cargo, row)
        return pickle_cargo
    # end def pickle_cargo

    def _pickle_cargo (self, e_type_columns, pickle_cargo, row) :
        for kind, columns in e_type_columns [None].iteritems () :
            if kind :
                if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                    comp_cargo = TFL.defaultdict (list)
                    self._pickle_cargo (columns, comp_cargo, row)
                    pickle_cargo [kind.attr.name] = (comp_cargo, )
                else :
                    kind_pc                       = [row [c] for c in columns]
                    pc_transform                  = kind.attr.SAS_PC_Transform
                    if pc_transform :
                        kind_pc                   = pc_transform.load (kind_pc)
                    pickle_cargo [kind.attr.name] = kind_pc
    # end def _pickle_cargo

    def reconstruct (self, session, row) :
        scope        = session.scope
        pickle_cargo = self.pickle_cargo (row)
        entity       = self.e_type.from_attr_pickle_cargo (scope, pickle_cargo)
        entity.pid   = row [self.e_type._SAQ.pid]
        entity.r_last_cid = entity.last_cid
        entity._finish__init__ ()
        return entity
    # end def reconstruct

    def reload (self, entity, row) :
        pickle_cargo      = self.pickle_cargo (row)
        entity.reload_from_pickle_cargo (pickle_cargo)
        entity.r_last_cid = entity.last_cid
        return entity
    # end def reload

    def _setup_columns (self, e_type, e_type_columns, prefix = "") :
        cm = self.column_map
        for kind in e_type.db_attr :
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                s_prefix = kind._sa_prefix
                columns  = TFL.defaultdict (ddict_list)
                et       = self._setup_columns (kind.P_Type, columns, s_prefix)
            else :
                attr    = kind.attr
                raw_col = None
                if isinstance (attr, MOM.Attr._A_Id_Entity_) :
                    col = cm.get ("%s%s_pid" % (prefix, kind.attr.name), None)
                else :
                    col = cm.get ("%s%s"     % (prefix, kind.attr.name), None)
                    if kind.needs_raw_value :
                        raw_col = cm ["%s%s" % (prefix, kind.attr.raw_name)]
                et      = col.mom_e_type
                columns = [col]
                if raw_col is not None :
                    columns.append (raw_col)
            e_type_columns [et]   [kind] = columns
            e_type_columns [None] [kind] = columns
        return et
    # end def _setup_columns

    def finish (self) :
        ### setup the select statement for this class with all the joins
        tables      = [self.table]
        joins  = self.table
        for b in self.transitive_bases :
            joins = joins.outerjoin (b._sa_table)
            tables.append           (b._sa_table)
        for c in self.transitive_children :
            joins = joins.outerjoin (c._sa_table)
            tables.append           (c._sa_table)
        self.joins  = joins
        self.select = sql.select \
            (tables, from_obj = (joins, ), use_labels = True)
        self.joined_tables = set (tables)
    # end def finish

    @TFL.Meta.Once_Property
    def transitive_bases (self) :
        result = []
        for b in self.bases :
            result.append (b)
            result.extend (b._SAS.transitive_bases)
        return result
    # end def transitive_bases

    @TFL.Meta.Once_Property
    def transitive_children (self) :
        result = []
        for c in self.e_type.children.itervalues () :
            result.append (c)
            result.extend (c._SAS.transitive_children)
        return result
    # end def transitive_children

    def value_dict ( self, entity
                   , e_type         = None
                   , defaults       = None
                   , attrs          = None
                   , columns        = None
                   ) :
        if columns is None :
            columns = self.e_type_columns [e_type]
        result      = defaults or {}
        attrs       = attrs or set (kind.attr.name for kind in columns)
        for attr_name in tuple (attrs) :
            attrs.remove (attr_name)
            kind = getattr (e_type, attr_name, Type_Name)
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                result.update \
                    ( self.value_dict
                        ( getattr (entity, attr_name)
                        , kind.P_Type
                        , columns = columns [kind] [e_type]
                        )
                    )
            else :
                pickle_cargo = kind.get_pickle_cargo (entity)
                pc_transform = kind.attr.SAS_PC_Transform
                if pc_transform :
                    pickle_cargo = pc_transform.dump (pickle_cargo)
                for column, value in zip (columns [kind], pickle_cargo) :
                    result [column.name] = value
        return result
    # end def value_dict

    def update (self, session, entity, attrs = set ()) :
        ### TFL.BREAK ()
        if not session._in_rollback :
            for b in self.bases :
                b._SAS.update (session, entity, attrs)
            values     = self.value_dict \
                (entity, e_type = self.e_type, attrs = attrs)
            if values :
                session.write_access = True
                update = self.table.update ().values (values)
                where  = self.pk == entity.pid
                if (   session.engine.query_last_cid_on_update
                   and (self.last_cid is not None)
                   and getattr (entity, "r_last_cid", None)
                   ) :
                    where  = sql.and_ \
                        (where, self.last_cid == entity.r_last_cid)
                result     = session.connection.execute (update.where (where))
                if not result.rowcount :
                    session.scope.rollback          ()
                    raise MOM.Error.Commit_Conflict ()
    # end def update

# end class SAS_Interface

class _Session_ (TFL.Meta.Object) :
    """A database session"""

    transaction = None

    def __init__ (self, scope, engine) :
        self.scope        = scope
        self.engine       = engine
        self.write_access = False
        self._in_rollback = 0
    # end def __init__

    def change_readonly (self, state) :
        meta_data          = self.db_meta_data
        meta_data.readonly = state
        kw                 = dict \
            ( pk        = self._scope_pk
            , meta_data = meta_data
            , readonly  = state
            )
        self.execute (self._sa_scope.update ().values (** kw))
        self.commit  ()
    # end def change_readonly

    def close (self, delete_engine = True) :
        self.rollback            ()
        self.scope.ems.pm.close  ()
        ### close all connections inside the pool
        ### import pdb; pdb.set_trace ()
        try :
            self.connection.close ()
            del self.connection
        except :
            pass
        self.engine.close         (delete_engine)
        if delete_engine :
            self.engine = None
    # end def close

    def close_connections (self) :
        self.close (False)
    # end def close_connections

    def _close_connection (self, method) :
        if self.transaction :
            method (self.engine, self.transaction, self.connection)
            self.transaction  = None
            del self.connection
            self.write_access = False
    # end def _close_connection

    def commit (self) :
        if self.readonly and self.write_access :
            self.scope.rollback ()
            raise MOM.Error.Readonly_DB
        self._close_connection  (TFL.Method.commit)
    # end def commit

    def compact (self) :
        pass
    # end def compact

    @TFL.Meta.Once_Property
    def connection (self) :
        result           = self.engine.connect ()
        self.transaction = result.begin        ()
        return result
    # end def connection

    def create (self) :
        self.db_meta_data = self._new_db_meta_data (self.scope)
    # end def create

    def execute (self, * args, ** kw) :
        if not self._in_rollback :
            return self.connection.execute (* args, ** kw)
    # end def execute

    def load_info (self) :
        scope = self.scope
        q     = self.connection.execute (self._sa_scope.select ().limit (1))
        si = q.fetchone                 ()
        meta_data         = si.meta_data
        self.db_meta_data = meta_data
        meta_readonly     = getattr (meta_data, "readonly", False)
        if meta_readonly != si.readonly :
            self.change_readonly (meta_readonly)
        scope.guid        = meta_data.guid
        if meta_data.dbv_hash != scope.app_type.db_version_hash :
            self._close_connection   (TFL.Method.rollback)
            self.engine.close        ()
            self.engine   = None
            raise MOM.Error.Incompatible_DB_Version \
                ( TFL.I18N._T
                   ( "Cannot load database because of a database version hash "
                     "missmatch:\n"
                     "  Tool  database version hash: %s\n"
                     "  Scope database version hash: %s\n"
                   )
                % (scope.app_type.db_version_hash, meta_data.dbv_hash)
                )
        self._scope_pk    = si.pk
    # end def load_info

    @property
    def readonly (self) :
        ### re-read the read only flag from the database to be sure to be
        ### up-to-date
        scope = self.scope
        q     = self.execute (self._sa_scope.select ())
        si    = q.fetchone   ()
        return si and si.readonly
    # end def readonly

    def register_scope (self, scope) :
        kw               = dict ()
        kw ["meta_data"] = self.db_meta_data
        kw ["readonly"]  = getattr (self.db_meta_data, "readonly", False)
        result = self.execute (self._sa_scope.insert ().values (** kw))
        self.commit           ()
        self._scope_pk   = result.inserted_primary_key [0]
    # end def register_scope

    def rollback (self) :
        self._close_connection  (TFL.Method.rollback)
    # end def rollback

    def _new_db_meta_data (self, scope) :
        return MOM.DB_Meta_Data.NEW (scope.app_type, scope)
    # end def _new_db_meta_data

# end class _Session_

class Session_S (_Session_) :
    """A Session bound to a scope"""

    def __init__ (self, scope, engine) :
        self.__super.__init__ (scope, engine)
        self._pid_map = {}
        self._cid_map = {}
        self.expunge  ()
        self._in_rollback = 0
    # end def __init__

    def add (self, entity, pid = None) :
        with self.scope.ems.pm.context (entity, pid) :
            entity.__class__._SAS.insert  (self, entity)
        self._pid_map [entity.pid] = entity
    # end def add

    def add_change (self, change) :
        if not self._in_rollback :
            table  = MOM.SCM.Change._Change_._sa_table
            result = self.execute \
                ( table.insert
                    ( values = dict
                        ( pid       = change.pid
                        , type_name = getattr (change, "type_name", "")
                        , kind      = change.kind
                        , data      = change.as_pickle ()
                        )
                    )
                )
            change.cid = result.inserted_primary_key [0]
    # end def add_change

    def commit (self) :
        try :
            self.flush                      ()
            self.__super.commit             ()
            self._flushed_changes = set     ()
            del self._saved
            self._mark_entities_for_reload  ()
        except self.engine.Commit_Conflict_Exception, exc:
            self.scope.rollback             ()
            raise MOM.Error.Commit_Conflict ()
    # end def commit

    @TFL.Meta.Once_Property
    def connection (self) :
        self._saved = dict \
            ( pid_map = self._pid_map.copy ()
            , cid_map = self._cid_map.copy ()
            )
        return self.__super.connection
    # end def connection

    def delete (self, entity) :
        self.flush        ()
        self._pid_map.pop (entity.pid)
        if not self._in_rollback :
            def _find_entites (ref_map) :
                for ET, attrs in ref_map.iteritems () :
                    if not ET.is_partial :
                        ETM        = self.scope [ET.type_name]
                        query_args = TFL.Filter_Or \
                            (* (getattr (MOM.Q, a) == entity for a in attrs))
                        for e in self.scope [ET.type_name].query (query_args) :
                            yield e, attrs
            # end def _find_entites
            pid_map = self._pid_map.copy ()
            ref_map = getattr (entity.__class__, "Ref_Req_Map", {})
            for e, _ in _find_entites (ref_map) :
                e.destroy ()
            ref_map = getattr (entity.__class__, "Ref_Opt_Map", {})
            for e, attrs in _find_entites (ref_map) :
                e.set (** dict ((a, None) for a in attrs))
            self._pid_map = pid_map
            entity.__class__._SAS.delete (self, entity)
    # end def delete

    def expunge (self, clear_change = False) :
        self._mark_entities_for_reload (True)
        if clear_change :
            self._pid_map = {}
            self._cid_map = {}
    # end def expunge

    def flush (self) :
        #self.engine.echo = True
        pending = self.scope.uncommitted_changes.pending_attr_changes
        for pid, attrs in pending.iteritems () :
            entity = self._pid_map.get (pid)
            if entity is not None :
                entity.__class__._SAS.update (self, entity, attrs)
        pending.clear ()
        #self.engine.echo = False
    # end def flush

    def instance_from_row (self, e_type, row) :
        ### get the real etype for this entity from the database
        e_type = getattr (self.scope, row [e_type._SAQ.Type_Name])
        pid    = row [e_type._SAQ.pid]
        pim    = self._pid_map
        entity = pim.get (pid, None)
        if entity is None :
            entity    = e_type._SAS.reconstruct (self, row)
            pim [pid] = entity
        elif isinstance (entity, MOM.DBW.SAS._Reload_Mixin_) :
            ### the object is already in the cache and has not been reloaded
            ### and we have the wohle information needed for reloading ->
            ### reload it
            entity.__class__._RESTORE_CLASS (entity)
            e_type._SAS.reload              (entity, row)
        return entity
    # end def instance_from_row

    def load_root (self, scope) :
        meta_data     = self.db_meta_data
        if meta_data.root_epk :
            epk       = list (meta_data.root_epk)
            type_name = root_epk.pop ()
            etm       = scope [root_type_name]
            epk       = dict ((k,v) for (k,v) in zip (etm.epk_sig, epk))
            return etm.query (** epk).one ()
    # end def load_root

    def pid_query (self, pid) :
        return self._pid_map.get (pid)
    # end def pid_query

    def query (self, Type) :
        return Type.select ()
    # end def query

    def _mark_entities_for_reload (self, force_reload = False) :
        for e in self._pid_map.itervalues () :
            if force_reload :
                setattr (e, e.__class__.last_cid.ckd_name, -1)
            e.__class__ = e.__class__._RELOAD_E_TYPE
    # end def _mark_entities_for_reload


    def recreate_change (self, row) :
        cid = row.cid
        if row.cid not in self._cid_map :
            change              = MOM.SCM.Change._Change_.from_pickle (row.data)
            change.cid          = cid
            self._cid_map [cid] = change
            pcid                = row.parent_cid
            if pcid :
                if pcid not in self._cid_map :
                    ### recreate the parent first
                    parent = self.scope.ems.changes (cid = pcid).one ()
                self._cid_map [pcid].add_change (change)
            self.scope.ems.changes (parent_cid = cid).all ()
        return self._cid_map [cid]
    # end def recreate_change

    def rollback (self) :
        if self.transaction :
            self._in_rollback += 1
            scope              = self.scope
            with scope.historian.temp_recorder (MOM.SCM.Ignorer) :
                scope.ems._rollback_uncommitted_changes ()
            self.__super.rollback ()
            self._in_rollback -= 1
            self._pid_map      = self._saved ["pid_map"]
            self._cid_map      = self._saved ["cid_map"]
    # end def rollback

    def _modify_change_iter (self, change_list) :
        for c in change_list :
            if c not in self._flushed_changes :
                self._flushed_changes.add (c)
                if isinstance (c, MOM.SCM.Change._Attr_) :
                    yield c
                for cc in self._modify_change_iter (c.children) :
                    yield cc
    # end def _modify_change_iter

    def update_change (self, change) :
        table  = MOM.SCM.Change._Change_._sa_table
        self.execute \
            ( table
                .update (values = dict (data = change.as_pickle ()))
                .where  (table.c.cid == change.cid)
            )
    # end def update_change

# end class Session_S

class Session_PC (_Session_) :
    """A session bound to a DB manager dealing with pickle cargos"""

    def change_query (self, ** kw) :
        query = MOM.DBW.SAS.Q_Result_Changes (MOM.SCM.Change._Change_, self)
        return query.filter (** kw).order_by (TFL.Sorted_By ("cid"))
    # end def change_query

    def consume (self, entity_iter, change_iter, chunk_size) :
        apt      = self.scope.app_type
        pm       = self.scope.ems.pm
        self.register_scope (self.scope)
        for no, (type_name, pc, pid) in enumerate (entity_iter) :
            apt [type_name]._SAS.insert_cargo (self, pid, pc)
            pm.reserve (TFL.Record (type_name = type_name), pid)
            if no and not (no % chunk_size) :
                ### commit chunk_size object. To large transactions could
                ### lead to performance issues
                self.commit ()
        self.commit         ()
        self._count  = 0
        self.max_cid = 0
        self._consume_change_iter (change_iter, chunk_size, None)
        self.commit         ()
        pm.dbs.reserve_cid  (self.connection, self.max_cid)
        self.commit         ()
    # end def consume

    def _consume_change_iter (self, change_iter, chunk_size, parent_cid) :
        table  = MOM.SCM.Change._Change_._sa_table
        for no, (chg_cls, chg_dct, children_pc) in enumerate (change_iter) :
            cid          = chg_dct ["cid"]
            self.max_cid = max (self.max_cid, cid)
            self.execute \
                ( table.insert
                    ( values = dict
                        ( cid        = cid
                        , pid        = chg_dct.get ("pid", None)
                        , kind       = chg_cls.kind
                        , type_name  = chg_dct.get ("type_name", "")
                        , data       = Pickle.dumps
                              ((chg_cls, chg_dct, []), Pickle.HIGHEST_PROTOCOL)
                        , parent_cid = parent_cid
                        )
                    )
                )
            self._count    += 1
            if self._count == chunk_size :
                self.commit ()
                self._count = 0
            self._consume_change_iter (children_pc, chunk_size, cid)
    # end def _consume_change_iter

    def flush (self) :
        pass ### needed because Q_Result calls flush
    # end def flush

    def instance_from_row (self, e_type, row) :
        ### get the real etype for this entity from the database
        ### e_type = getattr (self.scope.app_type, row [e_type._SAQ.Type_Name])
        return dict (e_type._SAS.pickle_cargo (row))
    # end def instance_from_row

    def produce_changes (self) :
        for pc in self.change_query (parent_cid = None) :
            yield pc
    # end def produce_changes

    def produce_entities (self) :
        pm       = self.scope.ems.pm
        apt      = self.scope.app_type
        Q_Result = MOM.DBW.SAS.Q_Result
        for pid, type_name in pm :
            try :
                e_type = apt [type_name]
                pc     = Q_Result (e_type, self).filter (pid = pid).one ()
                yield type_name, pc, pid
            except LookupError :
                ### stale entry in the PID table
                pass
    # end def produce_entities

    def recreate_change (self, row) :
        cls, dct, children = Pickle.loads (row.data)
        ### we need to set the cid for this change in the pickle
        dct ["cid"]        = row.cid
        ### before we return the pickle cartgo for this change we need to
        ### create the children list (because we do not save them in the
        ### pickle stored in the database)
        children = self.change_query (parent_cid = row.cid).all ()
        return cls, dct, children
    # end def recreate_change

    def _new_db_meta_data (self, scope) :
        if scope.src :
            return MOM.DB_Meta_Data.COPY \
                (scope.src.db_meta_data, scope.app_type, scope)
        else :
            return self.__super._new_db_meta_data (scope)
    # end def _new_db_meta_data

# end class Session_PC

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*", "_Session_")
### __END__ MOM.DBW.SAS.Session

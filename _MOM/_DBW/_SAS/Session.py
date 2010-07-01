# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
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
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object
import _TFL.Accessor

from   _MOM                  import MOM
import _MOM._DBW._SAS

import  operator
import  itertools
from    sqlalchemy           import sql

ddict_list = lambda : TFL.defaultdict (list)
attrgetter = operator.attrgetter

class Type_Name (object) :
    """A fake kind which is used to retrive the type_name of an entity"""

    class attr (object) :
        name = "Type_Name"
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
        base_pks = dict (pid = entity.pid)
        pk_map   = self.e_type._sa_pk_base
        for b in self.bases :
            base_pks [pk_map [b.type_name]] = b._SAS.insert (session, entity)
        result = session.connection.execute \
            ( self.table.insert ().values
                (self.value_dict (entity, self.e_type, base_pks))
            )
        return result.inserted_primary_key [0]
    # end def insert

    def reconstruct (self, session, row) :
        scope        = session.scope
        pickle_cargo = TFL.defaultdict (list)
        self._reconstruct (session, self.e_type_columns, pickle_cargo, row)
        entity     = self.e_type.from_attr_pickle_cargo (scope, pickle_cargo)
        entity.pid = row [self.e_type._SAQ.pid]
        return entity
    # end def reconstruct

    def _reconstruct (self, session, e_type_columns, pickle_cargo, row) :
        for kind, columns in e_type_columns [None].iteritems () :
            if kind :
                if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                    comp_cargo = TFL.defaultdict (list)
                    self._reconstruct (session, columns, comp_cargo, row)
                    pickle_cargo [kind.attr.name] = (comp_cargo, )
                else :
                    for column in columns :
                        pickle_cargo [kind.attr.name].append (row [column])
    # end def _reconstruct

    def _setup_columns (self, e_type, e_type_columns, prefix = "") :
        cm = self.column_map
        for kind in ( k for k in e_type.attributes.itervalues ()
                      if k.save_to_db
                    ) :
            if isinstance (kind, MOM.Attr._Composite_Mixin_) :
                s_prefix = kind._sa_prefix
                columns  = TFL.defaultdict (ddict_list)
                et       = self._setup_columns (kind.C_Type, columns, s_prefix)
            else :
                attr    = kind.attr
                raw_col = None
                if isinstance (attr, MOM.Attr._A_Object_) :
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
        tables = [self.table]
        joins  = self.table
        for b in self.transitive_bases :
            joins = joins.outerjoin (b._sa_table)
            tables.append           (b._sa_table)
        for c in self.transitive_children :
            joins = joins.outerjoin (c._sa_table)
            tables.append           (c._sa_table)
        self.select = sql.select \
            (tables, from_obj = (joins, ), use_labels = True)
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
                        , kind.C_Type
                        , columns = columns [kind] [e_type]
                        )
                    )
            else :
                for column, value in zip \
                    (columns [kind], kind.get_pickle_cargo (entity)) :
                    result [column.name] = value
        return result
    # end def value_dict

    def update (self, session, entity, attrs = set ()) :
        ### TFL.BREAK ()
        for b in self.bases :
            b._SAS.update (session, entity, attrs)
        values     = self.value_dict \
            (entity, e_type = self.e_type, attrs = attrs)
        if values :
            update = self.table.update ().values (values)
            return session.connection.execute \
                (update.where (self.pk == entity.pid))
    # end def update

# end class SAS_Interface

class _Session_ (TFL.Meta.Object) :
    """A database session"""

    transaction = None

    def __init__ (self, scope, engine) :
        self.scope  = scope
        self.engine = engine
    # end def __init__

    def commit (self) :
        self.transaction.commit     ()
        self.connection.close       ()
        self.transaction      = None
        del self.connection
    # end def commit

    @TFL.Meta.Once_Property
    def connection (self) :
        result           = self.engine.connect ()
        self.transaction = result.begin        ()
        return result
    # end def connection

    def close (self) :
        self.rollback            ()
        ### close all connections inside the pool
        self.engine.pool.dispose ()
        self.engine = None
    # end def close

    def execute (self, * args, ** kw) :
        return self.connection.execute (* args, ** kw)
    # end def execute

    def rollback (self) :
        if self.transaction :
            self.transaction.rollback ()
            self.connection.close     ()
            self.transaction = None
            del self.connection
    # end def rollback

# end class _Session_

class Session_S (_Session_) :
    """A Session bound to a scope"""

    def __init__ (self, scope, engine) :
        self.__super.__init__ (scope, engine)
        self.expunge  ()
    # end def __init__

    def add (self, entity, id = None) :
        with self.scope.ems.pm.context (entity, id) :
            entity.__class__._SAS.insert  (self, entity)
        self._pid_map [entity.pid] = entity
    # end def add

    def add_change (self, change) :
        DBW    = self.scope.ems.DBW
        table  = MOM.SCM.Change._Change_._sa_table
        result = self.connection.execute \
            ( table.insert
                ( values = dict
                    ( pid       = change.pid
                    , data      = change.as_pickle ()
                    )
                )
            )
        change.cid = result.inserted_primary_key [0]
    # end def add_change

    def commit (self) :
        self.flush                  ()
        self.__super.commit         ()
        self._flushed_changes = set ()
        del self._saved
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
        self.flush                   ()
        self._pid_map.pop            (entity.pid)
        execute = self.connection.execute
        link_map = getattr (entity.__class__, "link_map", {})
        for assoc, roles in link_map.iteritems () :
            role = tuple (roles) [0]
            for row in execute \
                    ( assoc._SAS.select.where
                        (getattr (assoc._SAQ, role.attr.name) == entity.pid)
                    ) :
                self.instance_from_row (assoc, row).destroy ()
        entity.__class__._SAS.delete (self, entity)
        entity.pid = None
    # end def delete

    def expunge (self) :
        self._pid_map         = {}
        ### only used during loading of changes from the database
        self._cid_map         = {}
    # end def expunge

    def flush (self) :
        #self.engine.echo = True
        for pid, attrs in self.scope.attr_changes.iteritems () :
            entity  = self._pid_map.get  (pid, None)
            entity.__class__._SAS.update (self, entity, attrs)
        self.scope.attr_changes.clear    ()
        #self.engine.echo = False
    # end def flush

    def instance_from_row (self, e_type, row) :
        ### get the real etype for this entity from the database
        e_type = getattr (self.scope, row [e_type._SAQ.Type_Name])
        pid    = row [e_type._SAQ.pid]
        if pid not in self._pid_map :
            entity             = e_type._SAS.reconstruct (self, row)
            self._pid_map [pid] = entity
        return self._pid_map [pid]
    # end def instance_from_row

    def query (self, Type) :
        return Type.select ()
    # end def query

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
        return self._cid_map [cid]
    # end def recreate_change

    def rollback (self) :
        if self.transaction :
            scope = self.scope
            for c in reversed (scope.ems.uncommitted_changes) :
                if c.undoable :
                    c.undo (scope)
            self.__super.rollback ()
            self._pid_map    = self._saved ["pid_map"]
            self._cid_map    = self._saved ["cid_map"]
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

# end class Session_S

class Session_PC (_Session_) :
    """A session bound to a DB mangager deailing with pickle cargos"""

# end class Session_PC

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Session



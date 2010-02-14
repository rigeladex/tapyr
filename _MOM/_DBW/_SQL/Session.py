# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DBW.SQL.
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
#    MOM.DBW.SQL.Session
#
# Purpose
#    A database session
#
# Revision Dates
#    11-Feb-2010 (MG) Creation
#    ««revision-date»»···
#--

from   _TFL                  import TFL
import _TFL._Meta.Object
import _TFL.Accessor

from   _MOM                  import MOM
import _MOM._DBW._SQL
from   _MOM._EMS.SQL         import PID

import  operator
import  itertools
from    sqlalchemy           import sql

ddict_list = lambda : TFL.defaultdict (list)
attrgetter = operator.attrgetter

class SQL_Interface (TFL.Meta.Object) :
    """Helper object to store the information how to get all/some values
       needed for the database insert/update from the entity
    """

    def __init__ (self, e_type, columns, bases) :
        e_type._SQL         = self
        self.e_type         = e_type
        self.columns        = columns
        self.table          = e_type._sa_table
        self.bases          = bases
        self.pk             = self.table.c [e_type._sa_pk_name]
        self.all_columns    = self._gather_columns (e_type, bases)
        self.e_type_getters = e_type_getters = TFL.defaultdict (ddict_list)
        for c in self.all_columns :
            e_type = None
            kind   = getattr (c, "mom_kind", None)
            getter = None
            if c.name == "Type_Name" :
                getter = attrgetter ("type_name")
                e_type = self.e_type.relevant_root
            elif kind :
                getter = self._add_attribute (c, kind)
                e_type = c.mom_e_type
            if getter :
                e_type_getters [e_type] [kind].append ((c, getter))
                e_type_getters [None]   [kind].append ((c, getter))
    # end def __init__

    def _add_attribute (self, column, kind) :
        name   = column.name
        raw    = getattr (column, "mom_raw",  None)
        if isinstance (kind.attr, MOM.Attr._A_Object_) :
            getter = getattr (TFL.Getter, kind.attr.ckd_name).id
        else :
            getter = attrgetter \
                (kind.attr.raw_name if raw else kind.attr.ckd_name)
        return getter
    # end def _add_attribute

    def delete (self, session, entity) :
        for b in self.bases :
            b._SQL.delete (session, entity)
        session.connection.execute \
            (self.table.delete ().where (self.pk == entity.id))
    # end def delete

    def _gather_columns (self, e_type, bases) :
        result   = []
        seen     = set ()
        for c in self.columns :
            key = (getattr (c, "mom_kind", None), getattr (c, "mom_raw", False))
            if not key [0] or key not in seen :
                c.mom_e_type = self.e_type
                result.append (c)
            seen.add (key)
        for et in bases :
            for c in et._SQL.all_columns :
                kind = getattr (c, "mom_kind", None)
                if kind :
                    kind = (kind, getattr (kind, "mom_raw", False))
                if not kind or kind not in seen :
                    result.append (c)
                seen.add (kind)
        return result
    # end def _gather_columns

    def insert (self, session, entity) :
        base_pks = dict ()
        pk_map   = self.e_type._sa_pk_base
        for b in self.bases :
            base_pks [pk_map [b.type_name]] = b._SQL.insert (session, entity)
        result = session.connection.execute \
            ( self.table.insert ().values
                (self.value_dict (entity, self.e_type, base_pks))
            )
        return result.inserted_primary_key [0]
    # end def insert

    def _query_object (self, session, kind, id) :
        obj = MOM.DBW.SQL.Q_Result (kind.Class, session).filter (id = id).one ()
        return obj.epk
    # end def _query_object

    def reconstruct (self, session, row) :
        scope        = session.scope
        pickle_cargo = TFL.defaultdict (list)
        for kind, getters in self.e_type_getters [None].iteritems () :
            if kind :
                for column, _ in getters :
                    if isinstance (kind.attr, MOM.Attr._A_Object_) :
                        cargo = self._query_object \
                            (session, kind, row [column])
                    else :
                        cargo = row [column]
                    pickle_cargo [kind.attr.name].append (cargo)
        entity     = self.e_type.from_pickle_cargo (scope, pickle_cargo)
        entity.id  = row [self.e_type._SAQ.id]
        entity.pid = MOM.EMS.SQL.PID (entity.type_name, entity.id)
        return entity
    # end def reconstruct

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
            result.extend (b._SQL.transitive_bases)
        return result
    # end def transitive_bases

    @TFL.Meta.Once_Property
    def transitive_children (self) :
        result = []
        for c in self.e_type.children.itervalues () :
            result.append (c)
            result.extend (c._SQL.transitive_children)
        return result
    # end def transitive_children

    def value_dict ( self, entity
                   , e_type   = None
                   , defaults = {}
                   , attrs    = None
                   ) :
        result = defaults.copy ()
        for kind, getters in self.e_type_getters [e_type].iteritems () :
            if not attrs or kind.attr.name in attr :
                for column, get in getters :
                    result [column.name] = get (entity)
        return result
    # end def value_dict

    def update (self, session, entity) :
        for b in self.bases :
            b._SQL.update (session, entity)
        values     = self.value_dict (entity, e_type = self.e_type)
        if values :
            update = self.table.update ().values (values)
            return session.connection.execute \
                (update.where (self.pk == entity.id))
    # end def update

# end class SQL_Interface

class Session (TFL.Meta.Object) :
    """A database session"""

    transaction = None

    def __init__ (self, scope, engine) :
        self.scope  = scope
        self.engine = engine
        self.expunge ()
    # end def __init__

    def add (self, entity) :
        entity.id  = entity.__class__._SQL.insert (self, entity)
        entity.pid = MOM.EMS.SQL.PID (entity.relevant_root.type_name, entity.id)
        self._id_map  [entity.pid] = entity
    # end def add

    def add_change (self, change) :
        DBW    = self.scope.ems.DBW
        table  = MOM.SCM.Change._Change_._sa_table
        result = self.connection.execute \
            ( table.insert
                ( values = dict
                    ( Type_Name = change.pid.Type_Name
                    , obj_id    = change.pid.id
                    , data      = change.as_pickle ()
                    )
                )
            )
        change.cid = result.inserted_primary_key [0]
    # end def add_change

    def commit (self) :
        self.flush                  ()
        self.transaction.commit     ()
        self.connection.close       ()
        self._flushed_changes = set ()
        self.transaction      = None
        del self.connection
        del self._saved
    # end def commit

    @TFL.Meta.Once_Property
    def connection (self) :
        result           = self.engine.connect ()
        self.transaction = result.begin        ()
        self._saved = dict \
            ( id_map  = self._id_map. copy ()
            , cid_map = self._cid_map.copy ()
            )
        return result
    # end def connection

    def close (self) :
        self.rollback ()
    # end def close

    def delete (self, entity) :
        self.flush                   ()
        self._id_map.pop             (entity.pid)
        entity.__class__._SQL.delete (self, entity)
        execute = self.connection.execute
        link_map = getattr (entity.__class__, "link_map", {})
        for assoc, roles in link_map.iteritems () :
            role = tuple (roles) [0]
            for row in execute \
                    ( assoc._SQL.select.where
                        (getattr (assoc._SAQ, role.attr.name) == entity.id)
                    ) :
                self.instance_from_row (assoc, row).destroy ()
        entity.pid = None
        entity.id  = None
    # end def delete

    def execute (self, * args, ** kw) :
        return self.connection.execute (* args, ** kw)
    # end def execute

    def expunge (self) :
        self._id_map          = {}
        ### only used during loading of changes from the database
        self._cid_map         = {}
        self._flushed_changes = set ()
    # end def expunge

    def flush (self) :
        #self.engine.echo = True
        for c in self._modify_change_iter (self.scope.ems.uncommitted_changes) :
            ### XXX make context manager
            self._no_flush = True
            entity         = c.entity (self.scope)
            self._no_flush = False
            entity.__class__._SQL.update (self, entity)
        self.engine.echo = False
    # end def flush

    def _instance_from_map (self, type_name, epk) :
        return self._id_map.get (PID (type_name, epk))
    # end def instance_from_map

    def instance_from_row (self, e_type, row) :
        ### get the real etype for this entity from the database
        e_type = getattr (self.scope, row [e_type._SAQ.Type_Name])
        id     = PID (e_type.relevant_root.type_name, row [e_type._SAQ.id])
        if id not in self._id_map :
            entity            = e_type._SQL.reconstruct (self, row)
            self._id_map [id] = entity
        return self._id_map [id]
    # end def instance_from_row

    def query (self, Type) :
        return Type.select ()
    # end def query

    def recreate_change (self, row) :
        cid      = row.cid
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
            self.transaction.rollback ()
            self.connection.close     ()
            self.transaction = None
            self._id_map     = self._saved ["id_map"]
            self._cid_map    = self._saved ["cid_map"]
            del self.connection
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

# end class Session

if __name__ != "__main__" :
    MOM.DBW.SQL._Export ("*")
### __END__ MOM.DBW.SQL.Session



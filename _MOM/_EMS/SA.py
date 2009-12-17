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
#    MOM.EMS.SA
#
# Purpose
#    Entity manager strategy using SQLAlchemy session as storeage
#
# Revision Dates
#    16-Oct-2009 (MG) Creation
#    25-Oct-2009 (MG) Updated to support inheritance
#    26-Nov-2009 (CT) Use `except ... as ...` (3-compatibility)
#    03-Dec-2009 (MG) Use `MOM.DBW.SA.Q_Result`
#    10-Dec-2009 (MG) `pid` added, `load_scope` and `register_scope`
#                     implemented
#    15-Dec-2009 (MG) `__iter__` removed (has been implemented in
#                     `EMS._Manager_`)
#    16-Dec-2009 (MG) `pid_query` and `register_change` added
#    16-Dec-2009 (MG) `load_scope` update of `db_cid` added
#    17-Dec-2009 (CT) Use `change.as_pickle` instead of home-grown code
#    17-Dec-2009 (MG) Set `pid` to None during `remove`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS._Manager_
import _MOM.Entity
import _MOM._DBW._SA.Q_Result
import _TFL._Meta.Object

import _TFL.defaultdict

import itertools

from   sqlalchemy  import exc        as SA_Exception

class PID (object) :
    """PID of an entity."""

    _Attrs             = "Type_Name", "id"

    def __init__ (self, Type_Name, id) :
        self.Type_Name = Type_Name
        self.id        = id
    # end def __init__

    def __composite_values__ (self) :
        return (self.Type_Name, self.id)
    # end def __composite_values__

    def __getitem__ (self, key) :
        return getattr (self, self._Attrs [key])
    # end def __getitem__

# end class PID

class Manager (MOM.EMS._Manager_) :
    """Entity manager using hash tables to hold entities."""

    type_name = "SA"

    Q_Result  = MOM.DBW.SA.Q_Result

    def add (self, entity) :
        ses = self.session
        ses.flush () ### add all pending operations to the database transaction
        max_c = entity.max_count
        if max_c and max_c <= self.s_count (entity.Essence) :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        try :
            ses.add   (entity)
            ses.flush ()
            entity.pid = PID (entity.relevant_root.type_name, entity.id)
        except SA_Exception.IntegrityError as exc :
            ses.rollback ()
            raise MOM.Error.Name_Clash \
                (entity, self.instance (entity.__class__, entity.epk))
    # end def add

    def changes (self, * filter, ** eq_kw) :
        SA_Change = MOM.DBW.SA.SA_Change
        pid       = eq_kw.pop ("pid", None)
        if pid is not None :
            eq_kw ["_type_name"] = pid.Type_Name
            eq_kw ["_obj_id"]    = pid.id
        query     = self._query_single_root (SA_Change, SA_Change).filter \
            (* filter, ** eq_kw)
        return query
    # end def changes

    def load_scope (self) :
        self.DBW.load_scope                    (self.session, self.scope)
        self.scope.db_cid = self.session.query (MOM.DBW.SA.SA_Change).order_by \
            ("-_id").limit (1).first ().cid
    # end def load_scope

    def pid_query (self, pid, Type) :
        """Simplified query for SA."""
        return self.query (Type, id = pid.id).one ()
    # end def pid_query

    def register_change (self, change) :
        result     = self.__super.register_change (change)
        sa_change  = MOM.DBW.SA.SA_Change  (change)
        self.session.change_session.add    (sa_change)
        self.session.change_session.commit ()
        change.cid = sa_change._id
        if change.children :
            Table = sa_change._sa_table
            update = Table.update ().where \
                ( Table.c._id.in_ (c.cid for c in change.children)
                ).values (_parent_id = change.cid)
            self.session.execute (update)
        return result
    # end def register_change

    def register_scope (self) :
        """Redefine to store `guid` and `root`-info of scope in database."""
        self.DBW.register_scope (self.session, self.scope)
    # end def register_scope

    def remove (self, entity) :
        entity.pid = None
        self.session.delete (entity)
        self.session.flush  () ### needed to update auto cache roles
    # end def remove

    def rename (self, entity, new_epk, renamer) :
        old_entity = self.instance (entity.__class__, new_epk)
        if old_entity :
            raise MOM.Error.Name_Clash (entity, old_entity)
        renamer     ()
    # end def rename

    def _query_multi_root (self, Type) :
        QR = self.Q_Result
        S  = self.session
        return self.Q_Result_Composite \
            ([QR (t, S.query (t)) for t in Type.relevant_roots.itervalues ()])
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        Type = getattr (Type, "_etype", Type)
        return self.Q_Result (Type, self.session.query (Type))
    # end def _query_single_root

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.SA

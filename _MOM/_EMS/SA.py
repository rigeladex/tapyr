# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glück. All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
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
#    18-Dec-2009 (MG) Use `Q_Result_Changes`
#    21-Dec-2009 (CT) s/load_scope/load_root/
#    21-Dec-2009 (CT) `max_cid` factored
#    31-Dec-2009 (MG) `__lt__` and `__eq__` aded
#     1-Jan-2010 (CT) `PID.__hash__` added
#    26-Jan-2010 (MG) Don't commit the change session on `register_change`
#    27-Jan-2010 (MG) `Manager.add` print SA exception in `__debug__` mode
#    29-Jan-2010 (MG) `pid_from_lid`,  `pid_as_lid` added
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

    def __hash__ (self) :
        return hash ((self.Type_Name, self.id))
    # end def __hash__

    def __lt__ (self, rhs) :
        return (self.Type_Name, self.id)  < (rhs.Type_Name, rhs.id)
    # end def __lt__

    def __eq__ (self, rhs) :
        try :
            rhs = (rhs.Type_Name, rhs.id)
        except AttributeError :
            pass
        return (self.Type_Name, self.id) == rhs
    # end def __eq__

    def __str__ (self) :
        return "(%s, %s)" % (self.Type_Name, self.id)
    # end def __str__

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
            ses.add          (entity)
            ses.flush        ()
            entity.pid = PID (entity.relevant_root.type_name, entity.id)
        except SA_Exception.IntegrityError as exc :
            ses.rollback ()
            if __debug__ :
                print exc
            raise MOM.Error.Name_Clash \
                (entity, self.instance (entity.__class__, entity.epk))
    # end def add

    def changes (self, * filter, ** eq_kw) :
        SA_Change = MOM.DBW.SA.SA_Change
        query     = MOM.DBW.SA.Q_Result_Changes \
            (SA_Change, self.session.query (SA_Change)
            ).filter (* filter, ** eq_kw)
        return query
    # end def changes

    def load_root (self) :
        result = self.DBW.load_root (self.session, self.scope)
        self.scope.db_cid = self.max_cid
        return result
    # end def load_root

    @property
    def max_cid (self) :
        query = self.session.change_session.query (MOM.DBW.SA.SA_Change)
        return query.order_by ("-_id").limit (1).first ().cid
    # end def max_cid

    def pid_as_lid (self, obj, e_type) :
        pid = obj.pid
        if e_type.relevant_root :
            return pid.id
        return "%s__%s" % (pid.Type_Name, pid.id)
    # end def pid_as_lid

    def pid_from_lid (self, lid, e_type) :
        if e_type.relevant_root :
            Type_Name = e_type.relevant_root.type_name
        else :
            Type_Name, lid = lid.split ("__", 1)
        return PID (Type_Name, int (lid))
    # end def pid_from_lid

    def pid_query (self, pid, Type) :
        """Simplified query for SA."""
        return self.query (Type, id = pid.id).one ()
    # end def pid_query

    def register_change (self, change) :
        result     = self.__super.register_change (change)
        sa_change  = MOM.DBW.SA.SA_Change  (change)
        self.session.change_session.add    (sa_change)
        self.session.change_session.flush  ()
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

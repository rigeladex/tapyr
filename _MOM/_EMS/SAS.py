# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glück. All rights reserved
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
#    MOM.EMS.SAS
#
# Purpose
#    Entity manager strategy using SQL layer from SQLAlchemy
#
# Revision Dates
#    11-Feb-2010 (MG) Creation (based of MOM.EMS.SA)
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.I18N             import _, _T, _Tn

import _MOM._EMS._Manager_
import _MOM.Entity
import _MOM._DBW._SAS.Q_Result
import _TFL._Meta.Object

import _TFL.defaultdict

import itertools

from   sqlalchemy  import exc        as SAS_Exception
from   sqlalchemy  import sql

class PID (object) :
    """PID of an entity."""

    _Attrs             = "Type_Name", "id"

    def __init__ (self, Type_Name, id) :
        self.Type_Name = Type_Name
        self.id        = id
    # end def __init__

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

    type_name = "SAS"

    Q_Result  = MOM.DBW.SAS.Q_Result

    def add (self, entity) :
        ses = self.session
        ses.flush () ### add all pending operations to the database transaction
        max_c = entity.max_count
        if max_c and max_c <= self.query (entity.__class__).count () :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        try :
            ses.add   (entity)
        except SAS_Exception.IntegrityError as exc :
            ses.rollback ()
            if __debug__ :
                print exc
            raise MOM.Error.Name_Clash \
                (entity, self.instance (entity.__class__, entity.epk))
    # end def add

    def changes (self, * filter, ** eq_kw) :
        query = MOM.DBW.SAS.Q_Result_Changes \
            (MOM.SCM.Change._Change_, self.session).filter (* filter, ** eq_kw)
        return query
    # end def changes

    def load_root (self) :
        result = self.DBW.load_root (self.session, self.scope)
        self.scope.db_cid = self.max_cid
        return result
    # end def load_root

    @property
    def max_cid (self) :
        id_col   = MOM.SCM.Change._Change_._sa_table.c.cid
        last     = self.session.execute \
            ( sql.select ((id_col, )).order_by (id_col.desc ()).limit (1)
            ).fetchone ()
        return (last and last.cid) or 0
    # end def max_cid

    def pid_as_lid (self, obj, e_type) :
        pid = obj.pid
        if e_type.relevant_root :
            return str (pid.id)
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
        """Simplified query for SAS."""
        return self.query (Type, id = pid.id).one ()
    # end def pid_query

    def register_change (self, change) :
        result      = self.__super.register_change (change)
        self.session.add_change                    (change)
        ###self.session.flush  ()
        if change.children :
            Table  = MOM.SCM.Change._Change_._sa_table
            update = Table.update ().where \
                ( Table.c.cid.in_ (c.cid for c in change.children)
                ).values (parent_cid = change.cid)
            self.session.execute (update)
        self.scope.db_cid = change.cid
        return result
    # end def register_change

    def register_scope (self) :
        """Redefine to store `guid` and `root`-info of scope in database."""
        self.DBW.register_scope (self.session, self.scope)
    # end def register_scope

    def remove (self, entity) :
        self.session.delete (entity)
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
            ([QR (t, self.session) for t in Type.relevant_roots.itervalues ()])
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        Type = getattr (Type, "_etype", Type)
        return self.Q_Result (Type, self.session)
    # end def _query_single_root

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.SA

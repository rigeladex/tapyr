# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Martin Glück. All rights reserved
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
#    27-Mar-2010 (MG) `add` support for `polymorphic_epk` added
#    12-May-2010 (MG) Use new `pid_manager`, lid functions changed
#    12-May-2010 (CT) `pid_as_lid` and `pid_from_lid` removed
#    17-May-2010 (CT) Class `PID` removed
#    17-May-2010 (MG) `add` parameter `id` added
#     1-Jul-2010 (MG) `pcm` and `max_pid` added
#     5-Jul-2010 (MG) `load_root` and `register_scope` are now method's of
#                     the session
#    15-Aug-2010 (MG) `pid_query` added
#     8-Sep-2010 (MG) `register_change` call of `session.update_change` added
#    14-Sep-2010 (CT) Argument `Type` of `pid_query` made optional
#    15-Sep-2010 (CT) `Change_Summary` added to manage `pending_attr_changes`
#    16-Sep-2010 (CT) `Change_Summary`: s/clear/_clear/
#    20-Oct-2010 (CT) `Change_Summary`: s/_add_pending/add_pending/,
#                     recursion removed from `add_pending`
#    20-Oct-2010 (CT) `Change_Summary.add` redefinition removed
#    20-Oct-2010 (CT) `Manager.register_change` changed to call
#                     `uncommitted_changes.add_pending`
#     8-Jun-2011 (MG) `commit` added to release db resources
#     8-Jun-2011 (MG) `max_cid`, `register_change`: don't used `temp_connection`
#    31-Jan-2012 (MG) `Session.add` use `epk_sig_root` for `polymorphic_epk`
#    16-Apr-2012 (MG) `add` renamed to `_add` and rollback in case of
#                     Name_Clash removed (this is now handled by the
#                     _Manager_.add) method
#     2-Jul-2012 (MG) `_add` renamed back to `add`, error handling for
#                     `Name_Clash` changed
#     2-Aug-2012 (CT) Add `dependent_attrs` to `Change_Summary.add_pending`
#     4-Aug-2012 (CT) Rename `remove` to `_remove`
#     6-Aug-2012 (CT) Fix `add_pending`: use `E_Type`, not `E_Type_Manager`
#    19-Aug-2012 (MG) Keep cache during rollback due to no changes
#    11-Sep-2012 (CT) Factor `rollback_pending_change` to `MOM.Scope`
#    14-Sep-2012 (MG) Change object update handling
#    30-Jan-2013 (CT) Refactor `add` into `MOM.EMS._Manager_.add` and `_add`
#    30-Jan-2013 (MG) Remove argument from `.rollback` call in `commit`
#     3-Jun-2013 (CT) Get attribute descriptors from `.attr_prop` not by
#                     applying `getattr` to the `E_Type` itself
#    24-Jun-2013 (CT) DRY `max_pid`
#    26-Jun-2013 (CT) Add `lazy_load_p`
#     4-Jul-2013 (CT) Move table gymnastics from `register_change` to
#                     `.session.add_change`
#     5-Jul-2013 (CT) Change sig of `_query_single_root`, `_query_multi_root`
#    17-Jul-2013 (CT) Remove `db_cid`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.I18N             import _, _T, _Tn

import _MOM.Entity
import _MOM._DBW._SAS.Q_Result
import _MOM._EMS._Manager_
import _MOM._SCM.Summary
import _TFL._Meta.Object

import _TFL.defaultdict
import _TFL.multimap

import itertools

from   sqlalchemy  import exc        as SAS_Exception
from   sqlalchemy  import sql

class Change_Summary (MOM.SCM.Summary) :

    def add_pending (self, c, scope) :
        mo = c.modified_attrs
        if mo :
            ET   = scope [c.type_name].E_Type
            pacs = set (mo)
            for an in mo :
                a = ET.attr_prop (an) or getattr (ET, an, None)
                if a is not None :
                    pacs.update (d.name for d in a.dependent_attrs)
            self.pending_attr_changes [c.pid].update (pacs)
    # end def add_pending

    def _clear (self) :
        self.__super._clear ()
        self.pending_attr_changes = TFL.mm_set ()
    # end def _clear

# end class Change_Summary

class Manager (MOM.EMS._Manager_) :
    """Entity manager using hash tables to hold entities."""

    type_name           = "SAS"

    Change_Summary      = Change_Summary

    Q_Result            = MOM.DBW.SAS.Q_Result

    lazy_load_p         = True

    @property
    def max_cid (self) :
        try :
            id_col = MOM.SCM.Change._Change_._sa_table.c.cid
            last   = self.session.connection.execute \
                ( sql.select ((id_col, )).order_by (id_col.desc ()).limit (1)
                ).fetchone ()
            return (last and last.cid) or 0
        except self.session.engine.Commit_Conflict_Exception, exc:
            self.scope.rollback             ()
            raise MOM.Error.Commit_Conflict ()
    # end def max_cid

    @property
    def max_pid (self) :
        return self.pm.max_pid
    # end def max_cid

    @property
    def pcm (self) :
        return self.session
    # end def pcm

    def changes (self, * filter, ** eq_kw) :
        query = MOM.DBW.SAS.Q_Result_Changes \
            (MOM.SCM.Change._Change_, self.session).filter (* filter, ** eq_kw)
        return query
    # end def changes

    def commit (self) :
        self.__super.commit ()
        if not self.uncommitted_changes :
            ### there was no commit -> we have to issue a rollback to the
            ### session to enure that the db resources will be released
            ### properly
            self.session.rollback ()
    # end def commit

    def load_root (self) :
        result = self.session.load_root (self.scope)
        return result
    # end def load_root

    def pid_query (self, pid, Type = None) :
        pid        = int (pid)
        result     = self.session.pid_query (pid)
        if result is None :
            result = self.pm.query          (pid)
        if Type is not None and not isinstance (result, Type.Essence) :
            raise LookupError \
                ( "Pid `%r` is instance of type %s, not of type `%s`"
                % (pid, result.type_name, Type.type_name)
                )
        return result
    # end def pid_query

    def register_change (self, change) :
        self.session.add_change (change)
        uncommitted_changes = self.uncommitted_changes
        self.__super.register_change    (change)
        uncommitted_changes.add_pending (change, self.scope)
        self.session.update_change      (change)
    # end def register_change

    def register_scope (self) :
        """Redefine to store `guid` and `root`-info of scope in database."""
        self.session.register_scope (self.scope)
    # end def register_scope

    def rename (self, entity, new_epk, renamer) :
        old_entity = self.instance (entity.__class__, new_epk)
        if old_entity :
            raise MOM.Error.Name_Clash (entity, old_entity)
        renamer ()
    # end def rename

    def update (self, entity, change) :
        self.session.update (entity, change)
    # end def update

    def _add (self, entity, pid = None) :
        ses = self.session
        ses.flush () ### add all pending operations to the database transaction
        max_c = entity.max_count
        if max_c and max_c <= self.query (entity.__class__).count () :
            raise MOM.Error.Too_Many_Objects (entity, entity.max_count)
        try :
            ses.add (entity, pid)
        except SAS_Exception.IntegrityError as exc :
            raise self.Integrity_Error
    # end def _add

    def _query_multi_root (self, Type, strict = False) :
        QR = self.Q_Result
        S  = self.session
        return self.Q_Result_Composite \
            ([QR (t, self.session) for t in Type.relevant_roots.itervalues ()])
    # end def _query_multi_root

    def _query_single_root (self, Type, strict = False) :
        Type = getattr (Type, "_etype", Type)
        return self.Q_Result (Type, self.session)
    # end def _query_single_root

    def _remove (self, entity) :
        self.session.delete (entity)
    # end def _remove

# end class Manager

if __name__ != "__main__" :
    MOM.EMS._Export_Module ()
### __END__ MOM.EMS.SAS

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2009-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    MOM.EMS._Manager_
#
# Purpose
#    Base class for entity manager strategies
#
# Revision Dates
#     2-Dec-2009 (CT) Creation
#     3-Dec-2009 (CT) `count` simplified
#     4-Dec-2009 (MG) `__init__` changed to support database related
#                     parameter and to create the `session`
#    10-Dec-2009 (CT) Class methods `connect` and `new` added,
#                     `__init__` revamped
#    10-Dec-2009 (CT) Empty methods `load_scope` and `register_scope` added
#    14-Dec-2009 (CT) `__iter__` (and relevant_roots) added
#    16-Dec-2009 (MG) Add `scope` parameter to `DWB.create_database` and
#                     `DBW.connect_database`
#    16-Dec-2009 (CT) `pid_query` added
#    16-Dec-2009 (CT) `commit`, `register_change`, and `uncommitted_changes`
#                     added
#    17-Dec-2009 (CT) `async_changes` added
#    17-Dec-2009 (CT) `pid_query` fixed (needs to call `one`)
#    21-Dec-2009 (CT) s/load_scope/load_root/
#    21-Dec-2009 (CT) `relevant_roots` factored to `MOM.Scope`
#    21-Dec-2009 (CT) `commit` changed to update `scope.db_cid`
#    21-Dec-2009 (CT) `close` added
#    19-Jan-2010 (CT) `rollback` added
#    11-May-2010 (CT) `Pid_Manager` added to `__init__`
#    11-May-2010 (MG) Pass `ems` and `db_uri` to `pid_manager`
#    12-May-2010 (CT) `pid_query` rewritten to use `pm.query`
#    12-May-2010 (CT) `pid_query` changed to apply `int` to `pid`
#    17-May-2010 (CT) `register_change` changed to not set `change.user`
#    30-Jun-2010 (CT) `db_meta_data` added
#    30-Jun-2010 (CT) `change_readonly` added
#    30-Jun-2010 (CT) `pcm` added
#     1-Jul-2010 (CT) `compact` added
#    11-Aug-2010 (CT) `register_change` changed to call `change.register`
#    16-Aug-2010 (CT) `commit` changed to check for `uncommitted_changes`
#    14-Sep-2010 (CT) Use `MOM.SCM.Summary` instance instead of `list` to
#                     hold `uncommitted_changes`
#    14-Sep-2010 (CT) Argument `Type` of `pid_query` made optional
#    15-Sep-2010 (CT) `Change_Summary` defined as class variable
#    16-Sep-2010 (CT) Replace `uncommitted_changes` by new object instead of
#                     calling `clear` on the existing one
#    28-Sep-2010 (CT) `rollback` changed to use `temp_change_recorder`,
#                     `_rollback` factored
#    16-Apr-2012 (MG) `add` added
#    19-Apr-2012 (CT) Use translated `.ui_name` instead of `.type_name` for
#                     exceptions
#     2-Jul-2012 (MG) `add` removed again
#     4-Aug-2012 (CT) Add `remove` and `restored`, factor `_reset_transaction`
#     4-Aug-2012 (CT) Add `_rollback_uncommitted_changes`
#    11-Aug-2012 (CT) Allow non-root queries in `instance`
#    12-Aug-2012 (CT) Change `instance` to not use `logging.error`
#    12-Aug-2012 (CT) Add `commit_context`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _MOM._EMS
import _MOM._SCM.Summary

import _TFL._Meta.Object
import _TFL._Meta.Once_Property
import _TFL.Decorator
import _TFL.Q_Result

from   _TFL.I18N             import _, _T, _Tn

import itertools
import logging

class _Manager_ (TFL.Meta.Object) :
    """Base class for entity managers."""

    type_name          = "XXX"

    Change_Summary     = MOM.SCM.Summary

    Q_Result           = TFL.Q_Result
    Q_Result_Composite = TFL.Q_Result_Composite

    @property
    def db_meta_data (self) :
        return self.session.db_meta_data
    # end def db_meta_data

    @property
    def pcm (self) :
        return self.session.pcm
    # end def pcm

    @classmethod
    def connect (cls, scope, db_url) :
        self         = cls (scope, db_url)
        self.session = self.DBW.connect_database (db_url, scope)
        return self
    # end def connect

    @classmethod
    def new (cls, scope, db_url) :
        self         = cls (scope, db_url)
        self.session = self.DBW.create_database (db_url, scope)
        return self
    # end def new

    def __init__ (self, scope, db_url) :
        self.scope  = scope
        self.db_url = db_url
        self.DBW    = DBW = scope.app_type.DBW
        self.pm     = DBW.Pid_Manager (self, db_url)
        self._reset_transaction ()
    # end def __init__

    def async_changes (self, * filters, ** kw) :
        from _MOM.import_MOM import Q
        result = self.changes (Q.cid > self.scope.db_cid)
        if filters or kw :
            result = result.filter (* filters, ** kw)
        return result
    # end def async_changes

    def change_readonly (self, state) :
        self.session.change_readonly (state)
        self.commit                  ()
    # end def change_readonly

    def close (self) :
        if self.uncommitted_changes :
            self.commit ()
        self.session.close ()
    # end def close

    def commit (self) :
        if self.uncommitted_changes :
            self.scope.db_cid = self.max_cid
            self.session.commit     ()
            self._reset_transaction ()
    # end def commit

    @TFL.Contextmanager
    def commit_context (self) :
        ### override as necessary, e.g., to lock tables in a database
        yield
    # end def commit_context

    def compact (self) :
        if self.uncommitted_changes :
            self.commit ()
        self.session.compact ()
    # end def compact

    def count (self, Type, strict) :
        return self.query (Type, strict = strict).count ()
    # end def count

    def exists (self, Type, epk) :
        epk_dict = dict (zip (Type.epk_sig, epk))
        entities = self.query (Type).filter (** epk_dict)
        scope    = self.scope
        result   = list (getattr (scope, e.type_name) for e in entities)
        return result
    # end def exists

    def instance (self, Type, epk) :
        result   = None
        epk_dict = dict (zip (Type.epk_sig, epk))
        try :
            result = self.query (Type, ** epk_dict).one ()
        except IndexError :
            pass
        else :
            if not isinstance (result, Type.Essence) :
                result = None
        return result
    # end def instance

    def load_root (self) :
        """Redefine to load `guid`, `pid`, and `root` of scope from database."""
        raise NotImplementedError
    # end def load_root

    def pid_query (self, pid, Type = None) :
        result = self.pm.query (int (pid))
        if Type is not None and not isinstance (result, Type.Essence) :
            raise LookupError \
                ( _T ("Pid `%r` is instance of type %s, not of type `%s`")
                % (pid, _T (result.ui_name), _T (Type.ui_name))
                )
        return result
    # end def pid_query

    def query (self, Type, * filters, ** kw) :
        root   = Type.relevant_root
        strict = kw.pop ("strict", False)
        if root :
            result = self._query_single_root (Type, root)
        else :
            result = self._query_multi_root (Type)
        if filters or kw :
            result = result.filter (* filters, ** kw)
        if strict :
            result = result.filter (type_name = Type.type_name)
        return result
    # end def query

    def r_query (self, Type, rkw, * filters, ** kw) :
        return self.query (Type, * filters, ** dict (rkw, ** kw))
    # end def r_query

    def register_change (self, change) :
        if change.parent is None :
            self.uncommitted_changes.add (change)
        change.register (self.scope)
    # end def register_change

    def register_scope (self) :
        """Redefine to store `guid` and `root`-info of scope in database."""
        pass
    # end def register_scope

    def remove (self, entity) :
        self._removed_entities [entity.pid] = entity
        self._remove   (entity)
        self.pm.retire (entity)
        entity.__class__ = entity.__class__._DESTROYED_E_TYPE
    # end def remove

    def restored (self, pid) :
        result = self._removed_entities.pop (pid, None)
        if result is not None :
            result.__class__ = result.E_Type
        return result
    # end def restored

    def rollback (self) :
        with self.scope.temp_change_recorder (MOM.SCM.Ignorer) :
            self._rollback ()
        self._reset_transaction ()
    # end def rollback

    def _query_multi_root (self, Type) :
        raise NotImplementedError \
            ("%s needs to define %s" % (self.__class__, "_query_multi_root"))
    # end def _query_multi_root

    def _query_single_root (self, Type, root) :
        raise NotImplementedError \
            ("%s needs to define %s" % (self.__class__, "_query_single_root"))
    # end def _query_single_root

    def _remove (self, entity) :
        raise NotImplementedError \
            ("%s needs to define %s" % (self.__class__, "_remove"))
    # end def _remove

    def _reset_transaction (self) :
        self.uncommitted_changes = self.Change_Summary ()
        self._removed_entities   = {}
    # end def _reset_transaction

    def _rollback (self) :
        self.session.rollback ()
    # end def _rollback

    def _rollback_uncommitted_changes  (self) :
        scope = self.scope
        for c in reversed (self.uncommitted_changes) :
            if c.undoable :
                c.undo (scope)
    # end def _rollback_uncommitted_changes

    def __iter__ (self) :
        sk = TFL.Sorted_By ("pid")
        return itertools.chain \
            (* (   self._query_single_root (r, r).order_by (sk)
               for r in self.scope.relevant_roots
               )
            )
    # end def __iter__

# end class _Manager_

if __name__ != "__main__" :
    MOM.EMS._Export ("_Manager_")
### __END__ MOM.EMS._Manager_

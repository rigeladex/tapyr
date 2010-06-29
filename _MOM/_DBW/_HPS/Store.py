# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Mag. Christian Tanzer All rights reserved
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
#    MOM.DBW.HPS.Store
#
# Purpose
#    Implement on-disk store for Hash-Pickle-Store
#
# Revision Dates
#    18-Dec-2009 (CT) Creation
#    21-Dec-2009 (CT) Creation continued
#    19-Jan-2010 (CT) `_save_context` changed to save `max_pid`, too
#    20-Jan-2010 (CT) `Info.NEW` factored from `Store._create_info`
#     4-Mar-2010 (CT) `load_info` changed to allow existence of uncompressed
#                     database
#     4-Mar-2010 (CT) Classmethod `X_Uri` factored
#    19-Mar-2010 (CT) `save_objects` and `_load_store` changed to
#                     save/restore `pid`
#    30-Apr-2010 (CT) `_load_store` corrected
#    30-Apr-2010 (CT) `save_objects` changed to store all entities into a
#                     single store `by_pid` sorted by `pid`
#    12-May-2010 (CT) s/ems._pid_map/ems.pm.table/
#    17-May-2010 (CT) `scope.add_from_pickle_cargo` factored from `_load_store`
#    18-May-2010 (CT) `Change_Manager` and `load_changes` added
#    18-May-2010 (CT) `_load_pending` changed to use `.restore` instead of
#                     `.redo`
#    18-May-2010 (CT) `save_treshold` added
#    25-Jun-2010 (CT) Use `scope.db_version_hash` instead of
#                     `Version.db_version`
#    29-Jun-2010 (CT) Adapted to change of `entity.as_pickle_cargo`
#    29-Jun-2010 (CT) `Store_S` factored from `Store`
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS.Change_Manager

import _TFL._Meta.Object
import _TFL.Environment
import _TFL.Error
import _TFL.FCM
import _TFL.Filename
import _TFL.module_copy
import _TFL.open_w_lock
import _TFL.Record

from   _TFL       import sos

import contextlib
import datetime
import pickle
import zipfile            as     ZF

TZF = TFL.module_copy \
    ( "zipfile"
    , stringFileHeader = "MM\004\003"
    , stringCentralDir = "MM\002\001"
    , stringEndArchive = "MM\006\005"
    )

def _creator_info (Version, scope = None) :
    return TFL.Record \
        ( date          = datetime.datetime.now ()
        , tool          = Version.productid
        , tool_version  = Version.tuple
        , user          = getattr (scope, "user", TFL.Environment.username)
        )
# end def _creator_info

class Info (TFL.Record) :
    """Implement info object for Hash-Pickle-Store."""

    def __init__ (self, commits = None, pending = None, stores = None, ** kw) :
        return self.__super.__init__ \
            ( commits = commits if commits is not None else []
            , pending = pending if pending is not None else []
            , stores  = stores  if stores  is not None else []
            , ** kw
            )
    # end def __init__

    def FILES (self, x_uri, head = None) :
        def _ (x) :
            fn = TFL.Filename (x, x_uri)
            return fn.name, fn.base_ext
        if head is not None :
            yield _ (head)
        for s in self.stores :
            yield _ (s)
        for cid, p in self.pending :
            yield _ (p)
        for cid, c in self.commits :
            yield _ (c)
    # end def FILES

    @classmethod
    def NEW (cls, app_type, scope = None, ** kw) :
        Version = app_type.ANS.Version
        ems     = getattr (scope, "ems", TFL.Record (max_cid = 0, max_pid = 0))
        if scope is not None :
            kw.update \
                ( guid      = scope.guid
                , root_epk  = scope.root_epk
                )
        result  = cls \
            ( creator       = _creator_info (Version, scope)
            , dbv_hash      = app_type.db_version_hash
            , last_changer  = _creator_info (Version, scope)
            , max_cid       = ems.max_cid
            , max_pid       = ems.max_pid
            , ** kw
            )
        return result
    # end def NEW

# end class Info

class _TZF_ (TFL.Meta.Object) :

    ZF = TZF

# end class _TZF_

class Store (TFL.Meta.Object) :
    """Implement on-disk store for Hash-Pickle-Store."""

    ZF = ZF

    save_treshold = 3

    try :
        import zlib
    except ImportError :
        zip_compression = ZF.ZIP_STORED
    else :
        zip_compression = ZF.ZIP_DEFLATED
        del zlib

    def __init__ (self, db_uri, app_type) :
        self.app_type = app_type
        self.Version  = app_type.ANS.Version
        self.db_uri   = db_uri
        self.x_uri    = self.X_Uri (db_uri.name)
        self.info_uri = TFL.Filename ("info", self.x_uri)
        self.cm       = MOM.DBW.HPS.Change_Manager ()
    # end def __init__

    def close (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        sos.rmdir (self.x_uri.name, deletefiles = True)
    # end def close

    def create (self) :
        assert not sos.path.exists (self.db_uri.name), self.db_uri.name
        assert not sos.path.exists (self.x_uri.name), self.x_uri.name
        x_name = self.x_uri.name
        with TFL.lock_file (x_name) :
            sos.mkdir (x_name)
            self._create_info ()
    # end def create

    def load_changes (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        info  = self.info
        x_uri = self.x_uri
        with TFL.lock_file (x_uri.name) :
            for (cid, name) in info.commits :
                file_name = TFL.Filename (name, x_uri).name
                for c in self._loaded_changes (file_name) :
                    pass ### `_loaded_changes` adds the changes to `self.cm`
        self.cm.to_load = []
    # end def load_changes

    def load_info (self) :
        assert sos.path.exists (self.db_uri.name), self.db_uri.name
        x_name = self.x_uri.name
        with TFL.lock_file (x_name) :
            if not sos.path.exists (x_name) :
                sos.mkdir (x_name)
                with contextlib.closing \
                         (self.ZF.ZipFile (self.db_uri.name, "r")) as zf :
                    zf.extractall (x_name)
            self.info = self._load_info ()
    # end def load_info

    @classmethod
    def X_Uri (cls, name) :
        return TFL.Dirname (name + ".X")
    # end def X_Uri

    def _check_sync (self, info) :
        db_info = self._load_info ()
        if info.max_cid != db_info.max_cid :
            self.db_info = db_info
            raise TFL.Sync_Conflict (self)
    # end def _check_sync

    def _create_info (self) :
        uri  = self.info_uri.name
        assert not sos.path.exists (uri)
        info = self.info = self._new_info ()
        with open (uri, "wb") as file :
            pickle.dump (info, file, pickle.HIGHEST_PROTOCOL)
    # end def _create_info

    def _loaded_changes (self, name) :
        with open (name, "rb") as file :
            add     = self.cm.add
            changes = pickle.load (file)
            for cargo in changes :
                c = MOM.SCM.Change._Change_.from_pickle_cargo (cargo)
                yield c
                add (c)
                for cc in c.children :
                    add (cc)
    # end def _loaded_changes

    def _load_info (self) :
        with open (self.info_uri.name, "rb") as file :
            result = pickle.load (file)
        ### XXX Check result.dbv_hash vs. self.app_type.db_version_hash
        return result
    # end def _load_info

    def _new_info (self) :
        ### XXX `creator`, `guid`, `last_changer`, `root_epk`
        return Info.NEW (self.app_type)
    # end def _new_info

# end class Store

class Store_S (Store) :
    """Store connected to a scope."""

    def __init__ (self, db_uri, scope) :
        self.__super.__init__ (db_uri, scope.app_type)
        self.scope = scope
    # end def __init__

    def close (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        db_uri = self.db_uri
        bak    = TFL.Filename (".bak", db_uri).name
        info   = self.info
        x_name = self.x_uri.name
        self.scope.ems.commit ()
        if len (info.pending) > self.save_treshold :
            self._save_objects ()
        with TFL.lock_file (x_name) :
            self._check_sync (info)
            with TFL.open_to_replace \
                     (db_uri.name, mode = "wb", backup_name = bak) as file:
                with contextlib.closing (self.ZF.ZipFile (file, "w")) as zf :
                    for abs, rel in info.FILES (self.x_uri, self.info_uri) :
                        zf.write (abs, rel)
        self.__super.close ()
    # end def close

    def commit (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        scope = self.scope
        ucc   = scope.ems.uncommitted_changes
        if ucc :
            cargo   = [c.as_pickle_cargo (transitive = True) for c in ucc]
            info    = self.info
            max_cid = scope.ems.max_cid
            max_pid = scope.ems.max_pid
            x_name  = self.x_uri.name
            with self._save_context (x_name, scope, info, max_cid, max_pid) :
                c_name = TFL.Filename ("%d.commit" % max_cid, self.x_uri)
                with open (c_name.name, "wb") as file :
                    pickle.dump (cargo, file, pickle.HIGHEST_PROTOCOL)
                info.pending.append ((max_cid, c_name.base_ext))
    # end def commit

    def load_objects (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        info  = self.info
        x_uri = self.x_uri
        with TFL.lock_file (x_uri.name) :
            self.scope.db_errors = []
            for s in info.stores :
                self._load_store   (TFL.Filename (s, x_uri).name)
            for (cid, name) in info.pending :
                self._load_pending (TFL.Filename (name, x_uri).name)
        self.cm.to_load  = [name for (cid, name) in info.commits]
    # end def load_objects

    def _load_pending (self, name) :
        scope = self.scope
        for c in self._loaded_changes (name) :
            c.restore (scope)
    # end def _load_pending

    def _load_store (self, s) :
        with open (s, "rb") as file :
            cargo   = pickle.load (file)
            scope   = self.scope
            for tn, pid, e_cargo in cargo :
                ### XXX Add legacy lifting
                scope.add_from_pickle_cargo (tn, pid, e_cargo)
    # end def _load_store

    def _new_info (self) :
        return Info.NEW (self.app_type, self.scope)
    # end def _new_info

    @TFL.Contextmanager
    def _save_context (self, x_name, scope, info, max_cid, max_pid) :
        Version = scope.app_type.ANS.Version
        with TFL.lock_file (x_name) :
            self._check_sync (info)
            yield
            info.last_changer = _creator_info (Version, scope)
            info.max_cid      = max_cid
            info.max_pid      = max_pid
            with open (self.info_uri.name, "wb") as file :
                pickle.dump (info, file, pickle.HIGHEST_PROTOCOL)
    # end def _save_context

    def _save_objects (self) :
        scope   = self.scope
        info    = self.info
        stores  = info.stores = []
        x_name  = self.x_uri.name
        max_cid = scope.ems.max_cid
        max_pid = scope.ems.max_pid
        with self._save_context (x_name, scope, info, max_cid, max_pid) :
            sk     = TFL.Sorted_By ("pid")
            s_name = TFL.Filename ("by_pid", self.x_uri)
            cargo  = \
                [   e.as_pickle_cargo ()
                for e in sorted (scope.ems.pm.table.itervalues (), key = sk)
                ]
            with open (s_name.name, "wb") as file :
                pickle.dump (cargo, file, pickle.HIGHEST_PROTOCOL)
            stores.append   (s_name.base_ext)
            info.commits.extend (info.pending)
            info.pending = []
    # end def _save_objects

# end class Store_S

if __name__ != '__main__':
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Store

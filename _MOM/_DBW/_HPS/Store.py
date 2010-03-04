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
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS

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

def _creator_info (scope, Version) :
    return TFL.Record \
        ( date          = datetime.datetime.now ()
        , tool          = Version.productid
        , tool_version  = Version.tuple
        , user          = scope.user or TFL.Environment.username
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
    def NEW (cls, scope) :
        Version = scope.app_type.ANS.Version
        ems     = getattr (scope, "ems", TFL.Record (max_cid = 0, max_pid = 0))
        result  = cls \
            ( creator       = _creator_info (scope, Version)
            , db_version    = Version.db_version.program_version
            , guid          = scope.guid
            , last_changer  = _creator_info (scope, Version)
            , max_cid       = ems.max_cid
            , max_pid       = ems.max_pid
            , root_epk      = scope.root_epk
            )
        return result
    # end def NEW

# end class Info

class Store (TFL.Meta.Object) :
    """Implement on-disk store for Hash-Pickle-Store."""

    ZF = ZF

    try :
        import zlib
    except ImportError :
        zip_compression = ZF.ZIP_STORED
    else :
        zip_compression = ZF.ZIP_DEFLATED
        del zlib

    def __init__ (self, db_uri, scope) :
        self.Version  = Version = scope.app_type.ANS.Version
        self.db_uri   = TFL.Filename (db_uri, Version.db_version.db_extension)
        self.x_uri    = TFL.Dirname  (self.db_uri.name + ".X")
        self.info_uri = TFL.Filename ("info", self.x_uri)
        self.scope    = scope
    # end def __init__

    def close (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        db_uri = self.db_uri
        bak    = TFL.Filename (".bak", db_uri).name
        info   = self.info
        x_name = self.x_uri.name
        if info.pending :
            self.save_objects ()
        with TFL.lock_file (x_name) :
            self._check_sync (info)
            with TFL.open_to_replace \
                     (db_uri.name, mode = "wb", backup_name = bak) as file:
                with contextlib.closing (self.ZF.ZipFile (file, "w")) as zf :
                    for abs, rel in info.FILES (self.x_uri, self.info_uri) :
                        zf.write (abs, rel)
        sos.rmdir (x_name, deletefiles = True)
    # end def close

    def create (self) :
        assert not sos.path.exists (self.db_uri.name), self.db_uri.name
        assert not sos.path.exists (self.x_uri.name), self.x_uri.name
        x_name = self.x_uri.name
        with TFL.lock_file (x_name) :
            sos.mkdir         (x_name)
            self._create_info ()
    # end def create

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

    def load_objects (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        info  = self.info
        x_uri = self.x_uri
        with TFL.lock_file (x_uri.name) :
            for s in info.stores :
                self._load_store   (TFL.Filename (s, x_uri).name)
            for (cid, name) in info.pending :
                self._load_pending (TFL.Filename (name, x_uri).name)
    # end def load_objects

    def save_objects (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        scope   = self.scope
        info    = self.info
        stores  = info.stores = []
        x_name  = self.x_uri.name
        max_cid = scope.ems.max_cid
        max_pid = scope.ems.max_pid
        scope.ems.commit ()
        with self._save_context (x_name, scope, info, max_cid, max_pid) :
            sk = TFL.Sorted_By ("pid")
            for rr in scope.relevant_roots :
                tn     = rr.type_name
                Type   = scope [tn]
                s_name = TFL.Filename (tn, self.x_uri)
                cargo  = \
                    [   (e.type_name, e.as_pickle_cargo ())
                    for e in Type.query ().order_by (sk)
                    ]
                with open (s_name.name, "wb") as file :
                    pickle.dump (cargo, file, pickle.HIGHEST_PROTOCOL)
                stores.append   (s_name.base_ext)
            info.commits.extend (info.pending)
            info.pending = []
    # end def save_objects

    def _check_sync (self, info) :
        db_info = self._load_info ()
        if info.max_cid != db_info.max_cid :
            self.db_info = db_info
            raise TFL.Sync_Conflict (self)
    # end def _check_sync

    def _create_info (self) :
        uri  = self.info_uri.name
        assert not sos.path.exists (uri)
        info = self.info = Info.NEW (self.scope)
        with open (uri, "wb") as file :
            pickle.dump (info, file, pickle.HIGHEST_PROTOCOL)
    # end def _create_info

    def _load_info (self) :
        with open (self.info_uri.name, "rb") as file :
            result = pickle.load (file)
        ### Assignment to `Version.db_version` checks version compatibility
        self.Version.db_version = result.db_version
        return result
    # end def _load_info

    def _load_pending (self, name) :
        with open (name, "rb") as file :
            changes = pickle.load (file)
            scope   = self.scope
            for cargo in changes :
                c = MOM.SCM.Change._Change_.from_pickle_cargo (cargo)
                c.redo (scope)
    # end def _load_pending

    def _load_store (self, s) :
        with open (s, "rb") as file :
            cargo   = pickle.load (file)
            scope   = self.scope
            for tn, e_cargo in cargo :
                ### XXX Add legacy lifting
                Type = scope.entity_type (tn)
                if Type :
                    scope.add (Type.from_pickle_cargo (scope, e_cargo))
    # end def _load_store

    @TFL.Contextmanager
    def _save_context (self, x_name, scope, info, max_cid, max_pid) :
        Version = scope.app_type.ANS.Version
        with TFL.lock_file (x_name) :
            self._check_sync (info)
            yield
            info.last_changer = _creator_info (scope, Version)
            info.max_cid      = max_cid
            info.max_pid      = max_pid
            with open (self.info_uri.name, "wb") as file :
                pickle.dump (info, file, pickle.HIGHEST_PROTOCOL)
    # end def _save_context

# end class Store

class Store_TZF (Store) :

    ZF = TZF

# end class Store_TZF

if __name__ != '__main__':
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Store

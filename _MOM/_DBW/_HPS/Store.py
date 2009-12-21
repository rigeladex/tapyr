# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    MOM.DBW.HPS.Store
#
# Purpose
#    Implement on-disk store for Hash-Pickle-Store
#
# Revision Dates
#    18-Dec-2009 (CT) Creation
#    21-Dec-2009 (CT) Creation continued
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS

import _TFL._Meta.Object
import _TFL.Environment
import _TFL.Error
import _TFL.Filename
import _TFL.module_copy
import _TFL.open_w_lock
import _TFL.Record

from   _TFL       import sos

import datetime
import pickle
import zipfile            as     ZF

TZF = TFL.module_copy \
    ( "zipfile"
    , stringFileHeader = "MOM\004\003"
    , stringCentralDir = "MOM\002\001"
    , stringEndArchive = "MOM\006\005"
    )

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

# end class Info

class Store (TFL.Meta.Object) :
    """Implement on-disk store for Hash-Pickle-Store."""

    ZF = TZF

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
            info    = self.info
            cargo   = [c.as_pickle_cargo (transitive = True) for c in ucc]
            max_cid = scope.ems.max_cid
            x_name  = self.x_uri.name
            Version = scope.app_type.ANS.Version
            with TFL.lock_file (x_name) :
                db_info = self._load_info ()
                if info ["max_cid"] != db_info ["max_cid"] :
                    self.db_info = db_info
                    raise TFL.Sync_Conflict (self)
                c_name = TFL.Filename ("%d.commit" % max_cid, self.x_uri).name
                with open (c_name, "wb") as file :
                    pickle.dump (cargo, file, pickle.HIGHEST_PROTOCOL)
                info.last_changer = self._creator (scope, Version)
                info.max_cid      = max_cid
                info.pending.append ((max_cid, c_name))
                with open (self.info_uri.name, "wb") as file :
                    pickle.dump (info, file, pickle.HIGHEST_PROTOCOL)
    # end def commit

    def load_info (self) :
        assert sos.path.exists (self.db_uri.name), self.db_uri.name
        assert not sos.path.exists (self.x_uri.name), self.x_uri.name
        x_name = self.x_uri.name
        with TFL.lock_file (x_name) :
            sos.mkdir      (x_name)
            with contextlib.closing \
                     (self.ZF.ZipFile (self.db_uri.name, "r")) as zf :
                zf.extractall (x_name)
            self.info = info = self._load_info ()
            ### Assignment to `Version.db_version` checks version compatibility
            Version.db_version = info.db_version
    # end def load_info

    def load_objects (self) :
        assert sos.path.exists (self.x_uri.name), self.x_uri.name
        x_name = self.x_uri.name
        with TFL.lock_file (x_name) :
            for s in info ["stores"] :
                self._load_store (s)
            for (cid, name) in info ["pending"] :
                self._load_pending (p)
    # end def load_objects

    def _create_info (self) :
        uri     = self.info_uri.name
        assert not sos.path.exists (uri)
        scope   = self.scope
        ems     = getattr (scope, "ems", TFL.Record (max_cid = 0, max_pid = 0))
        Version = self.Version
        info    = self.info = Info \
            ( creator       = self._creator (scope, Version)
            , db_version    = Version.db_version.program_version
            , guid          = scope.guid
            , last_changer  = self._creator (scope, Version)
            , max_cid       = ems.max_cid
            , max_pid       = ems.max_pid
            , root_epk      = scope.root_epk
            )
        with open (uri, "wb") as file :
            pickle.dump (info, file, pickle.HIGHEST_PROTOCOL)
    # end def _create_info

    def _creator (self, scope, Version) :
        return TFL.Record \
            ( date          = datetime.datetime.now ()
            , tool          = Version.productid
            , tool_version  = Version.tuple
            , user          = scope.user or TFL.Environment.username
            )
    # end def _creator

    def _load_info (self) :
        with open (self.info_uri.name, "rb") as file :
            result = pickle.load (file)
        return result
    # end def _load_info

    def _load_pending (self, cid, name) :
        with open (name, "rb") as file :
            changes = pickle.load (file)
            scope   = self.scope
            for c in changes :
                r.redo (scope)
    # end def _load_pending

    def _load_store (self, s) :
        pass ### XXX
    # end def _load_store

# end class Store

if __name__ != '__main__':
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Store

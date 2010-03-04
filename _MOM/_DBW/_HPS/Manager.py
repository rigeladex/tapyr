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
#    MOM.DBW.HPS.Manager
#
# Purpose
#    Database wrapper for Hash-Pickle-Store
#
# Revision Dates
#    18-Dec-2009 (CT) Creation
#    21-Dec-2009 (CT) Creation continued
#    19-Jan-2010 (CT) `rollback` added
#    20-Jan-2010 (CT) Provide `info` even if there is no `store`
#     2-Feb-2010 (CT) `commit` changed to update `info.max_cid`  even if
#                     there is no `store`
#     4-Mar-2010 (CT) `_new_manager` factored; `delete_database` added
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS.Store
import _MOM._DBW._Manager_

from   _TFL import sos

import _TFL.Accessor
import _TFL.Filename

class _M_HPS_Manager_ (MOM.DBW._Manager_.__class__) :
    """Meta class for MOM.DBW.HPS.Manager"""

    def create_database (cls, db_uri, scope) :
        return cls._new_manager (db_uri, scope, TFL.Method.create)
    # end def create_database

    def connect_database (cls, db_uri, scope) :
        return cls._new_manager (db_uri, scope, TFL.Method.load_info)
    # end def connect_database

    def delete_database (cls, db_uri, db_ext) :
        uri = cls._db_uri (db_uri, db_ext).name
        if sos.path.exists (uri) :
            sos.unlink (uri)
        x_uri = MOM.DBW.HPS.Store.X_Uri (uri).name
        if sos.path.exists (x_uri) :
            sos.rmdir (x_uri, True)
    # end def delete_database

    def _db_uri (cls, uri, ext) :
        return TFL.Filename (uri, ext)
    # end def _db_uri

    def _new_manager (cls, db_uri, scope, store_fct) :
        store = None
        if db_uri is not None :
            ext   = scope.app_type.ANS.Version.db_version.db_extension
            store = MOM.DBW.HPS.Store (cls._db_uri (db_uri, ext), scope)
            store_fct (store)
        return cls (store, scope)
    # end def _get_store

# end class _M_HPS_Manager_

class Manager (MOM.DBW._Manager_) :
    """Database wrapper for Hash-Pickle-Store."""

    __metaclass__ = _M_HPS_Manager_

    type_name     = "HPS"

    def __init__ (self, store, scope) :
        self.store = store
        self.scope = scope
        if store is None :
            self._info = MOM.DBW.HPS.Info.NEW (scope)
    # end def __init__

    def close (self) :
        if self.store is not None :
            self.store.close ()
    # end def close

    def commit (self) :
        if self.store is not None :
            self.store.commit ()
        else :
            info         = self._info
            ems          = self.scope.ems
            info.max_cid = ems.max_cid
            info.max_pid = ems.max_pid
    # end def commit

    @property
    def info (self) :
        if self.store is not None :
            return self.store.info
        else :
            return self._info
    # end def info

    def load_objects (self) :
        if self.store is not None :
            self.store.load_objects ()
    # end def load_objects

    def rollback (self) :
        pass ### Nothing needs to be done here
    # end def rollback

# end class Manager

if __name__ != '__main__':
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Manager

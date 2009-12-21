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
#    MOM.DBW.HPS.Manager
#
# Purpose
#    Database wrapper for Hash-Pickle-Store
#
# Revision Dates
#    18-Dec-2009 (CT) Creation
#    21-Dec-2009 (CT) Creation continued
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS.Store
import _MOM._DBW._Manager_

class _M_HPS_Manager_ (MOM.DBW._Manager_.__class__) :
    """Meta class for MOM.DBW.HPS.Manager"""

    def create_database (cls, db_uri, scope) :
        store = None
        if db_uri is not None :
            store = MOM.DBW.HPS.Store (db_uri, scope)
            store.create ()
        return cls (store, scope)
    # end def create_database

    def connect_database (cls, db_uri, scope) :
        store = None
        if db_uri is not None :
            store = MOM.DBW.HPS.Store (db_uri, scope)
            store.load_info ()
        return cls (store, scope)
    # end def connect_database

# end class _M_HPS_Manager_

class Manager (MOM.DBW._Manager_) :
    """Database wrapper for Hash-Pickle-Store."""

    __metaclass__ = _M_HPS_Manager_

    type_name     = "HPS"

    def __init__ (self, store, scope) :
        self.store = store
        self.scope = scope
    # end def __init__

    def commit (self) :
        if self.store :
            self.store.commit ()
    # end def commit

    @property
    def info (self) :
        if self.store :
            return self.store.info
    # end def info

    def load_objects (self) :
        if self.store :
            self.store.load_objects ()
    # end def load_objects

# end class Manager

if __name__ != '__main__':
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Manager

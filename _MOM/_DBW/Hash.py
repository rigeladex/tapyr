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
#    MOM.DBW.Hash
#
# Purpose
#    Database wrapper for hash-based entity management
#
# Revision Dates
#     3-Dec-2009 (CT) Creation
#     4-Dec-2009 (MG) Renamed from `Session` to `Manager`
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._Manager_

class _M_Hash_Manager_ (MOM.DBW._Manager_.__class__) :
    """Meta class for MOM.DBW.Hash"""

    def create_database (cls, db_uri) :
        assert db_uri is None
        ### maybe we need to return an instance of a Session (depends on the
        ### database implementation)
        return cls ()
    # end def create_database

    def connect_database (cls, db_uri) :
        assert db_uri is None
        ### maybe we need to return an instance of a Session (depends on the
        ### database implementation)
        return cls ()
    # end def connect_database

# end class _M_Hash_Manager_

class Manager (MOM.DBW._Manager_) :
    """Database wrapper for hash-based entity management."""

    __metaclass__ = _M_Hash_Manager_

    type_name     = "Hash"

    ### right now we use the Hash class as a session as well -> therefore we
    ### need to provide the commit interface
    def commit (self) :
        pass ### XXX
    # end def commit

# end class Manager

if __name__ != '__main__':
    MOM.DBW._Export ("*")
### __END__ MOM.DBW.Hash

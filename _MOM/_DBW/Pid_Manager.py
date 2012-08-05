# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.DBW.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.Pid_Manager
#
# Purpose
#    Base class for database backend specific manager for permanent ids
#
# Revision Dates
#    11-May-2010 (CT) Creation
#    11-May-2010 (MG) `__init__` added
#    12-May-2010 (CT) `retire` added
#    17-May-2010 (MG) `kw` added to `__call__`
#     4-Aug-2012 (CT) Remove implementation of `retire`
#    ««revision-date»»···
#--

from   _TFL       import TFL
from   _MOM       import MOM

import _MOM._DBW

import _TFL._Meta.Object

class _Pid_Manager_ (TFL.Meta.Object) :
    """Base class for database backend specific manager for permanent ids."""

    _real_name = "Pid_Manager"

    def __init__ (self, ems, db_url) :
        self.ems = ems
    # end def __init__

    def __call__ (self, entity, pid = None, ** kw) :
        if pid is None :
            pid = self.new (entity, ** kw)
        else :
            self.reserve (entity, pid, ** kw)
        return pid
    # end def __call__

    def new (self, entity) :
        """Return a new `pid` to be used for `entity`."""
        raise NotImplementedError
    # end def new

    def query (self, pid) :
        """Return entity with `pid`."""
        raise NotImplementedError
    # end def query

    def reserve (self, entity, pid) :
        """Reserve `pid` for use for `entity.` `pid` must not be already used
           for any other entity.
        """
        raise NotImplementedError
    # end def reserve

    def retire (self, entity) :
        """Retire any resources held for `entity` (but `entity.pid` won't get
           reused, ever).
        """
        raise NotImplementedError
    # end def retire

Pid_Manager = _Pid_Manager_ # end class

if __name__ != "__main__" :
    MOM.DBW._Export ("*")
### __END__ MOM.DBW.Pid_Manager

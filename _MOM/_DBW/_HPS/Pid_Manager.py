# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.DBW.HPS.
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
#    MOM.DBW.HPS.Pid_Manager
#
# Purpose
#    HPS specific manager for permanent ids
#
# Revision Dates
#    11-May-2010 (CT) Creation
#    11-May-2010 (MG) `ems` and `db_uri` added
#    12-May-2010 (CT) `retire` added
#    12-May-2010 (CT) `reserve` corrected (corner cases)
#    ««revision-date»»···
#--

"""
Pid manager for Hash-Pickle-Store::

    >>> from _TFL.Record import Record as R
    >>> pm = Pid_Manager ()
    >>> pm.new (R ())
    1
    >>> pm.new (R ())
    2
    >>> pm.reserve (R (), 5)
    5
    >>> pm.reserve (R (), 5)
    Traceback (most recent call last):
      ...
    ValueError: Cannot reserve pid 5, already used by object `Record (pid = 5)`
    >>> pm.new (R ())
    6
    >>> pm.max_pid
    6

"""

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS
import _MOM._DBW.Pid_Manager

class Pid_Manager (MOM.DBW.Pid_Manager) :
    """HPS specific manager for permanent ids."""

    def __init__ (self, ems = None, db_url = None) :
        self.__super.__init__ (ems, db_url)
        self.max_pid = 0
        self.table   = {}
    # end def __init__

    def new (self, entity) :
        self.max_pid += 1
        result = self.max_pid
        if entity is not None :
            self.table [result] = entity
            entity.pid = result
        return result
    # end def new

    def query (self, pid) :
        return self.table [pid]
    # end def query

    def reserve (self, entity, pid) :
        table = self.table
        if pid in table :
            if table [pid] is not entity :
                raise ValueError \
                    ( "Cannot reserve pid %s, already used by object `%r`"
                    % (pid, table [pid])
                    )
        else :
            self.max_pid = max (pid, self.max_pid)
            if entity is not None :
                table [pid] = entity
                entity.pid  = pid
        return pid
    # end def reserve

    def retire (self, entity) :
        if entity.pid in self.table :
            del self.table [entity.pid]
        entity.pid = None
    # end def retire

# end class Pid_Manager

if __name__ != "__main__" :
    MOM.DBW.HPS._Export ("*")
### __END__ MOM.DBW.HPS.Pid_Manager

# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Martin Glueck All rights reserved
# Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package MOM.DBW.SAS.
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
#    MOM.DBW.SAS.Pid_Manager
#
# Purpose
#    SAS specific manager for permanent ids
#
# Revision Dates
#    11-May-2010 (MG) Creation
#    12-May-2010 (MG) Support for PostgreSQL sequences added
#    17-May-2010 (CT) `reserve` changed to `insert` for postgresql, too
#    17-May-2010 (MG) `new_context` replaced by `context`
#    24-Jun-2010 (CT) `commit`, `reserve`, and `rollback` factored to `dbs`
#     1-Jul-2010 (MG) `max_pid` and `__iter__` added, `type_name` factored
#    15-Jul-2010 (MG) `close` added
#    29-Jul-2010 (CT) `transaction = None` added to `Pid_Manager`
#    10-Jun-2011 (MG) Handling of database connection changed to allow better
#                     support for sqlite
#     4-Aug-2012 (CT) Add stub for `retire`
#     5-Aug-2012 (MG) Fix `reserve_pid`
#    19-Jan-2013 (MG) Fix column name for type-name
#    28-May-2013 (CT) Use `type_name`, not `Type_Name`, as column name
#     6-Jun-2013 (CT) Fix argument to `ValueError` in `reserve`
#     6-Jun-2013 (CT) Improve exception message from `query`
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS
import _MOM._DBW.Pid_Manager

class Pid_Manager (MOM.DBW.Pid_Manager) :
    """SAS specific manager for permanent ids."""

    transaction = None

    def __init__ (self, ems, db_url) :
        self.__super.__init__ (ems, db_url)
        sa_table     = self.ems.DBW.sa_pid
        self.insert  = sa_table.insert ()
        self.select  = sa_table.select ()
        self.pid_col = sa_table.c.pid
        self.tn_col  = sa_table.c.type_name
        self.dbs     = self.ems.DBW.DBS_map [db_url.scheme]
    # end def __init__

    def commit (self) :
        self.dbs.commit_pid (self)
    # end def commit

    @TFL.Meta.Once_Property
    def connection (self) :
        return self.dbs.connection_pid (self)
    # end def connection

    @TFL.Contextmanager
    def context (self, entity, pid) :
        try :
            yield self (entity, pid, commit = False)
        except Exception :
            self.rollback ()
            raise
        else :
            self.commit   ()
    # end def new_context

    def close (self) :
        self.rollback ()
    # end def close

    @property
    def max_pid (self) :
        result = self.connection.execute \
            (self.select.limit (1).order_by (self.pid_col.desc ()))
        row = result.fetchone ()
        if row :
            return row.pid
        return 0
    # end def max_pid

    def new (self, entity, commit = True) :
        type_name = None
        if entity :
            type_name = entity.type_name
        sql    = self.insert.values      (type_name = type_name)
        result = self.connection.execute (sql)
        if commit :
            self.commit ()
        pid = int (result.inserted_primary_key [0])
        if entity :
            entity.pid = pid
        return pid
    # end def new

    def query (self, pid) :
        type_name = self.type_name (pid)
        try :
            return self.ems.scope [type_name].query (pid = pid).one ()
        except Exception :
            raise LookupError \
                ("No %s object with pid `%d` found" % (type_name, pid))
    # end def query

    def reserve (self, entity, pid, commit = True) :
        self.dbs.reserve_pid (self.connection, pid)
        type_name = None
        if entity :
            type_name  = entity.type_name
            entity.pid = pid
        result = self.connection.execute \
            (self.select.where (self.pid_col == pid)).fetchone ()
        if result :
            if type_name and result.type_name != type_name :
                raise ValueError \
                    ( "Try to reserve pid %d with changed type_name %s != %s"
                    % (pid, result.type_name, type_name)
                    )
        else :
            sql    = self.insert.values      (type_name = type_name, pid = pid)
            result = self.connection.execute (sql)
            if commit :
                self.commit ()
        return pid
    # end def reserve

    def retire (self, entity) :
        pass ### XXX
    # end def retire

    def rollback (self) :
        self.dbs.rollback_pid (self)
    # end def rollback

    def type_name (self, pid) :
        result = self.connection.execute \
            (self.select.where (self.pid_col == pid))
        found  = result.fetchone ()
        self.commit              ()
        if found and found.type_name :
            return found.type_name
        raise LookupError ("No object with pid `%d` found" % (pid, ))
    # end def type_name

    def __iter__ (self) :
        result = self.connection.execute \
            (self.select.order_by (self.pid_col.asc ()))
        for row in result :
            if row.type_name :
                yield row.pid, row.type_name
    # end def __iter__

# end class Pid_Manager

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Pid_Manager

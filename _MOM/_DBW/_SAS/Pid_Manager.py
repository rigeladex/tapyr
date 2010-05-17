# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Martin Glueck All rights reserved
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
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _MOM._DBW._HPS
import _MOM._DBW.Pid_Manager

class Pid_Manager (MOM.DBW.Pid_Manager) :
    """SAS specific manager for permanent ids."""

    def __init__ (self, ems, db_uri) :
        self.__super.__init__ (ems, db_uri)
        db_uri            = db_uri or "sqlite://"
        self.is_postgres  = db_uri.startswith ("postgresql://")
        if db_uri.startswith ("sqlite://") :
            self.commit   = self.rollback = lambda : None
        sa_table          = self.ems.DBW.sa_pid
        self.insert       = sa_table.insert ()
        self.select       = sa_table.select ()
        self.pid_col      = sa_table.c.pid
        self.tn_col       = sa_table.c.Type_Name
    # end def __init__

    def commit (self) :
        self.transaction.commit     ()
        self.connection.close       ()
        del self.connection
    # end def commit

    @TFL.Meta.Once_Property
    def connection (self) :
        result           = self.ems.session.engine.connect ()
        self.transaction = result.begin                    ()
        return result
    # end def connection

    def new (self, entity, commit = True) :
        Type_Name = None
        if entity :
            Type_Name = entity.type_name
        sql    = self.insert.values      (Type_Name = Type_Name)
        result = self.connection.execute (sql)
        if commit :
            self.commit ()
        pid = int (result.inserted_primary_key [0])
        if entity :
            entity.pid = pid
        return pid
    # end def new

    @TFL.Contextmanager
    def new_context (self, entity) :
        try :
            yield self.new (entity, commit = False)
        except :
            self.rollback ()
            raise
        else :
            self.commit   ()
    # end def new_context

    def query (self, pid) :
        result = self.connection.execute \
            (self.select.where (self.pid_col == pid))
        found  = result.fetchone ()
        self.commit              ()
        if found :
            try :
                return self.ems.scope [found.type_name].query (pid = pid).one ()
            except StandardError : ### XXX
                pass
        raise LookupError ("No object with pid `%d` found" % (pid, ))
    # end def query

    def reserve (self, entity, pid) :
        if self.is_postgres :
            self.connection.execute \
                ("ALTER SEQUENCE pid_seq RESTART WITH %d" % (pid + 1, ))
        Type_Name = None
        if entity :
            Type_Name  = entity.type_name
            entity.pid = pid
        sql    = self.insert.values      (Type_Name = Type_Name, pid = pid)
        result = self.connection.execute (sql)
        self.commit ()
        return pid
    # end def reserve

    def rollback (self) :
        if self.transaction :
            self.transaction.rollback ()
            self.connection.close     ()
            del self.connection
    # end def rollback

# end class Pid_Manager

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.Pid_Manager



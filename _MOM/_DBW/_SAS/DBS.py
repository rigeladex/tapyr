# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
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
#    MOM.DBW.SAS.DBS
#
# Purpose
#    Encapsulate db-specific functionality for SAS
#
# Revision Dates
#    23-Jun-2010 (CT) Creation
#    24-Jun-2010 (CT) `pid` related methods added
#    15-Jul-2010 (MG) `Postgresql.Connection` added and used
#    29-Jul-2010 (CT) `MySQL.create_database` changed (`encoding`, exception
#                     handling)
#    29-Jul-2010 (CT) `IF EXISTS` and `IF NOT EXISTS` added to `MySQL`
#    ««revision-date»»···
#--

from   _MOM                      import MOM
from   _TFL                      import TFL

import _MOM._DBW._DBS_

import contextlib
import sqlalchemy

class _NFB_ (MOM.DBW._DBS_) :
    """Base class for non-file based databases."""

    @classmethod
    def commit_pid (cls, pm) :
        pm.transaction.commit   ()
        pm.connection.close     ()
        del pm.connection
    # end def commit_pid

    @classmethod
    def rollback_pid (cls, pm) :
        pm.transaction.rollback ()
        pm.connection.close     ()
        del pm.connection
    # end def rollback_pid

    @classmethod
    def Url (cls, value, ANS, default_path = None) :
        if default_path :
            default_path = TFL.Filename (default_path).base
        return super (_NFB_, cls).Url (value, ANS, default_path)
    # end def Url

# end class _NFB_

class MySQL (_NFB_) :
    """DB-specific functionality for MySQL."""

    scheme = "mysql"

    @classmethod
    def create_database (cls, db_url, manager, encoding = "utf8") :
        try :
            engine = manager._create_engine (db_url.scheme_auth)
            engine.execute \
                ( "CREATE DATABASE IF NOT EXISTS %s character set %s"
                % (db_url.path, encoding)
                )
        except sqlalchemy.exc.OperationalError :
            pass
    # end def create_database

    @classmethod
    def delete_database (cls, db_url, manager) :
        try :
            engine = manager._create_engine (db_url.scheme_auth)
            engine.execute ("DROP DATABASE IF EXISTS %s" % (db_url.path, ))
        except sqlalchemy.exc.OperationalError :
            pass
    # end def delete_database

# end class MySQL

class Postgresql (_NFB_) :
    """DB-specific functionality for Postgresql."""

    scheme = "postgresql"

    class Connection (object) :

        def __init__ (self, db_url, manager) :
            import psycopg2.extensions as PE
            engine = manager._create_engine (db_url.scheme_auth + "/postgres")
            conn   = engine.connect ()
            conn.connection.connection.set_isolation_level \
                (PE.ISOLATION_LEVEL_AUTOCOMMIT)
            self.engine = engine
            self.conn   = conn
        # end def __init__

        def execute (self, * args, ** kw) :
            return self.conn.execute (* args, ** kw)
        # end def execute

        def close (self) :
            self.conn.close          ()
            self.engine.pool.dispose ()
        # end def close

    # end class Connection

    @classmethod
    def create_database \
            ( cls, db_url, manager
            , encoding = "utf8"
            , template = "template0"
            ) :
        conn = cls.Connection (db_url, manager)
        with contextlib.closing (conn) :
            conn.execute \
                ( "CREATE DATABASE %s ENCODING='%s' TEMPLATE %s"
                % (db_url.path, encoding, template)
                )
    # end def create_database

    @classmethod
    def delete_database (cls, db_url, manager) :
        conn = cls.Connection (db_url, manager)
        with contextlib.closing (conn) :
            try :
                conn.execute ("DROP DATABASE %s" % (db_url.path, ))
            except sqlalchemy.exc.ProgrammingError :
                pass
    # end def delete_database

    @classmethod
    def reserve_pid (cls, connection, pid) :
        connection.execute \
            ("ALTER SEQUENCE pid_seq RESTART WITH %d" % (pid + 1, ))
    # end def reserve_pid

# end class Postgresql

class Sqlite (MOM.DBW._DBS_) :
    """DB-specific functionality for Sqlite ."""

    scheme = "sqlite"

    @classmethod
    def commit_pid (cls, pm) :
        pass
    # end def commit_pid

    @classmethod
    def rollback_pid (cls, pm) :
        pass
    # end def rollback_pid

# end class Sqlite

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.DBS

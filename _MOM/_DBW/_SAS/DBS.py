# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2012 Mag. Christian Tanzer All rights reserved
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
#     2-Aug-2010 (MG) Support for dropping the tables instead of droping the
#                     database added
#     3-Aug-2010 (MG) Handle error of `meta.reflect` in `delete_database`
#    10-Aug-2010 (MG) `Postgresql._drop_database_content` fixed
#    16-Aug-2010 (MG) `MySQL._drop_database` fixed to suppress the nasty warning
#     2-Sep-2010 (CT) Pass `db_url.path` through `str` to aovid::
#            ProgrammingError: (ProgrammingError) type "u" does not exist
#            LINE 1: SELECT datname FROM pg_database WHERE datname = u'regtest'                                                                       ^
#             "SELECT datname FROM pg_database WHERE datname = u'regtest'" {}
#    30-Nov-2010 (CT) `Fatal_Exceptions` added
#    22-Mar-2011 (MG) `_SAS_DBS_` added, `create_engine` for Postgresql
#                     redefined
#     9-Jun-2011 (MG) `query_last_cid_on_update` added
#    10-Jun-2011 (MG) `*_pid` function changes, `connection_pid` added
#    14-Jun-2011 (MG) `commit_pid`, `connection_pid`, `rollback_pid` fixed
#                     `MySQL._drop_database`: only swollow the `Unknown
#                     database` error message
#    22-Jul-2011 (MG) `Sqlite.create_engine`: `PRAGMA case_sensitive_like`
#                     added
#     8-Sep-2011 (CT) s/SQLError/DBAPIError/
#                     (SQLError doesn't exist in SQLAlchemy 0.7)
#    27-Apr-2012 (MG) `reserve_cid` implemented for Postgresql, `reserve_pid`
#                     changed
#    ««revision-date»»···
#--

from   _MOM                      import MOM
from   _TFL                      import TFL
import _TFL._Meta.Property

import _MOM._DBW._DBS_

import contextlib
import sqlalchemy
from   sqlalchemy            import engine        as SQL_Engine
from   sqlalchemy.interfaces import PoolListener

class _SAS_DBS_ (MOM.DBW._DBS_) :
    """Base class for all databases using sqlalchemy as db interface."""

    Engine_Parameter          = dict (pool_recycle = 900, echo = False)
    echo                      = TFL.Meta.Alias_Property ("_sa_engine.echo")
    Commit_Conflict_Exception = sqlalchemy.exc.DBAPIError
    query_last_cid_on_update  = False

    def __init__ (self, sa_engine) :
        self._sa_engine = sa_engine
    # end def __init__

    def connect (self) :
        return self._sa_engine.connect ()
    # end def connect

    def commit (self, transaction, connection) :
        transaction.commit ()
        connection.close   ()
    # end def commit

    def close (self) :
        self._sa_engine.pool.dispose ()
        self._sa_engine = None
    # end def close

    @classmethod
    def create_engine (cls, db_url) :
        return cls \
            ( SQL_Engine.create_engine
                (db_url.value or "sqlite:///:memory:", ** cls.Engine_Parameter)
            )
    # end def create_engine

    def create_tables (self, metadata) :
        metadata.create_all (self._sa_engine)
    # end def create_tables

    def rollback (self, transaction, connection) :
        transaction.rollback ()
        connection.close     ()
    # end def rollback

    def __getattr__ (self, name) :
        return getattr (self._sa_engine, name)
    # end def __getattr__

# end class _SAS_DBS_

class _NFB_ (_SAS_DBS_) :
    """Base class for non-file based databases."""

    Fatal_Exceptions = (sqlalchemy.exc.OperationalError, )
    pm               = None

    @classmethod
    def commit_pid (cls, pm) :
        if cls.pm :
            cls.pm ["transaction"].commit ()
            cls.pm ["connection"].close   ()
            cls.pm = None
            del pm.connection
    # end def commit_pid

    @classmethod
    def connection_pid (cls, pm) :
        if not cls.pm :
            cls.pm = {}
            cls.pm ["connection" ] = conn = pm.ems.session.engine.connect ()
            cls.pm ["transaction"] = conn.begin                           ()
        return cls.pm ["connection"]
    # end def connection_pid

    @classmethod
    def delete_database (cls, db_url, manager) :
        try :
            cls._drop_database (db_url, manager)
        except sqlalchemy.exc.DBAPIError as e:
            ### looks like we don't have the permissions to drop the database
            ### -> let's delete all tables we find using the reflection
            ### mechanism of sqlalchemy
            engine = cls.create_engine    (db_url)
            meta   = sqlalchemy.MetaData  (bind = engine)
            try :
                meta.reflect                   ()
                if meta.tables :
                    cls._drop_database_content (engine, meta)
            except sqlalchemy.exc.DBAPIError :
                pass
            engine.close ()
    # end def delete_database

    @classmethod
    def _drop_database_content (cls, engine, meta) :
        meta.drop_all ()
    # end def _drop_database_content

    @classmethod
    def rollback_pid (cls, pm) :
        if cls.pm :
            cls.pm ["transaction"].rollback ()
            cls.pm ["connection"].close     ()
            cls.pm = None
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

    scheme                    = "mysql"
    query_last_cid_on_update  = True

    @classmethod
    def create_database (cls, db_url, manager, encoding = "utf8") :
        try :
            engine = cls.create_engine (TFL.Url (db_url.scheme_auth))
            engine.execute \
                ( "CREATE DATABASE IF NOT EXISTS %s character set %s"
                % (str (db_url.path), encoding)
                )
        except sqlalchemy.exc.OperationalError :
            pass
    # end def create_database

    @classmethod
    def create_engine (cls, db_url) :
        engine = cls \
            ( SQL_Engine.create_engine
                (db_url.value or "sqlite:///:memory:", ** cls.Engine_Parameter)
            )
        #engine.execute ("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        return engine
    # end def create_engine

    @classmethod
    def _drop_database (cls, db_url, manager) :
        engine = cls.create_engine (TFL.Url (db_url.scheme_auth))
        ### This is necessary to avoid a nasty Warning that the database does
        ### not exist (even using the IF EXISTS clause)
        try :
            engine.execute ("use %s" % (str (db_url.path), ))
        except sqlalchemy.exc.OperationalError, exc :
            if (  '(1049, "Unknown database \'%s\'")' % (db_url.path, )
               not in exc.message
               ) :
                raise
        else :
            engine.execute ("DROP DATABASE IF EXISTS %s" % (str (db_url.path), ))
    # end def _drop_database

# end class MySQL

try :
    import psycopg2.extensions as PE
except ImportError :
    PE = None ### looks like PostgreSQL python adapter is not installed

class Postgresql (_NFB_) :
    """DB-specific functionality for Postgresql."""

    scheme                 = "postgresql"
    ISOLATION_AUTO_COMMIT  = getattr (PE, "ISOLATION_LEVEL_AUTOCOMMIT",   -1)
    ISOLATION_SERIALIZABLE = getattr (PE, "ISOLATION_LEVEL_SERIALIZABLE", -1)

    class SAS_Pool_Listener (PoolListener) :
        """Modify newly created connections to update the postgresql
           isolcation level.
        """
        def __init__ (self, isolation_level) :
            self.isolation_level = isolation_level
        # end def __init__

        def connect (self, connection, * args) :
            connection.set_isolation_level (self.isolation_level)
        # end def connect

    # end class SAS_Pool_Listener

    class Connection (object) :

        def __init__ (self, db_url, dbs) :
            engine = dbs.create_engine \
                ( TFL.Url (db_url.scheme_auth + "/postgres")
                , isolation_level = dbs.ISOLATION_AUTO_COMMIT
                )
            self.engine = engine
            self.conn   = engine.connect ()
        # end def __init__

        def execute (self, * args, ** kw) :
            return self.conn.execute (* args, ** kw)
        # end def execute

        def close (self) :
            self.conn.close          ()
            self.engine.close        ()
        # end def close

    # end class Connection

    @classmethod
    def create_database \
            ( cls, db_url, manager
            , encoding = "utf8"
            , template = "template0"
            ) :
        conn = cls.Connection (db_url, cls)
        with contextlib.closing (conn) :
            ### before we try to create the database let's check if it does
            ### not already exist
            result = conn.execute \
                ( "SELECT datname FROM pg_database WHERE datname = %r"
                % (str (db_url.path), )
                ).fetchall ()
            if not result :
                ### database does not exist -> create it
                conn.execute \
                    ( "CREATE DATABASE %s ENCODING='%s' TEMPLATE %s"
                    % (str (db_url.path), encoding, template)
                    )
    # end def create_database

    @classmethod
    def create_engine (cls, db_url, isolation_level = None) :
        if isolation_level is None :
            isolation_level = cls.ISOLATION_SERIALIZABLE
        return cls \
            ( SQL_Engine.create_engine
                ( db_url.value or "sqlite:///:memory:"
                , listeners = (cls.SAS_Pool_Listener (isolation_level), )
                , ** cls.Engine_Parameter
                )
            )
    # end def create_engine

    @classmethod
    def _drop_database (cls, db_url, manager) :
        conn = cls.Connection (db_url, cls)
        with contextlib.closing (conn) :
            conn.execute ("DROP DATABASE %s" % (str (db_url.path), ))
    # end def _drop_database

    @classmethod
    def _drop_database_content (cls, engine, meta) :
        super (Postgresql, cls)._drop_database_content (engine, meta)
        ### now we need to drop everything we created with the
        ### knowledge of sqlalchemy
        engine.execute ("DROP SEQUENCE pid_seq")
    # end def _drop_database_content

    @classmethod
    def reserve_cid (cls, connection, cid) :
        connection.execute \
            ("SELECT setval('change_history_cid_seq', %d)" % (cid, ))
    # end def reserve_cid

    @classmethod
    def reserve_pid (cls, connection, pid) :
        connection.execute \
            ("SELECT setval('pid_seq', %d)" % (pid, ))
    # end def reserve_pid

# end class Postgresql

class Sqlite (_SAS_DBS_) :
    """DB-specific functionality for Sqlite ."""

    scheme = "sqlite"

    @classmethod
    def commit_pid (cls, pm) :
        if hasattr (pm, "connection") :
            del pm.connection
    # end def commit_pid

    @classmethod
    def connection_pid (cls, pm) :
        ### sqlite does not support a multiple connection per thread -> we
        ### reuse the connection of the session
        return pm.ems.session.connection
    # end def connection_pid

    @classmethod
    def create_engine (cls, db_url, isolation_level = None) :
        engine = super (Sqlite, cls).create_engine (db_url)
        engine.execute ("PRAGMA case_sensitive_like = true;")
        return engine
    # end def create_engine

    @classmethod
    def rollback_pid (cls, pm) :
        if hasattr (pm, "connection") :
            del pm.connection
    # end def rollback_pid

# end class Sqlite

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.DBS

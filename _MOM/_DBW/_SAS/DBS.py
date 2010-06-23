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
#    ««revision-date»»···
#--

from   _MOM                      import MOM
from   _TFL                      import TFL

import _MOM._DBW._DBS_

import contextlib

class MySQL (MOM.DBW._DBS_) :
    """DB-specific functionality for MySQL."""

    scheme = "mysql"

    @classmethod
    def create_database (cls, db_url, manager) :
        engine = manager._create_engine (db_url.scheme_auth)
        engine.execute ("CREATE DATABASE %s" % (db_url.path, ))
    # end def create_database

    @classmethod
    def delete_database (cls, db_url, manager) :
        try :
            engine  = manager._create_engine (db_url.scheme_auth)
            engine.execute ("DROP DATABASE %s" % (db_url.path, ))
        except sqlalchemy.exc.OperationalError :
            pass
    # end def delete_database

# end class MySQL

class Postgresql (MOM.DBW._DBS_) :
    """DB-specific functionality for Postgresql."""

    scheme = "postgresql"

    @classmethod
    def create_connection (cls, db_url, manager) :
        import psycopg2.extensions as PE
        engine = manager._create_engine (db_url.scheme_auth + "/postgres")
        conn   = engine.connect ()
        conn.connection.connection.set_isolation_level \
            (PE.ISOLATION_LEVEL_AUTOCOMMIT)
        return conn, engine
    # end def create_connection

    @classmethod
    def create_database \
            ( cls, db_url, manager
            , encoding = "utf8"
            , template = "template0"
            ) :
        conn, engine = cls.create_connection (db_url, manager)
        with contextlib.closing (conn) :
            conn.execute \
                ( "CREATE DATABASE %s ENCODING='%s' TEMPLATE %s"
                % (db_url.path, encoding, template)
                )
    # end def create_database

    @classmethod
    def delete_database (cls, db_url, manager) :
        conn, engine = cls.create_connection (db_url, manager)
        with contextlib.closing (conn) :
            try :
                conn.execute ("DROP DATABASE %s" % (db_url.path, ))
            except sqlalchemy.exc.ProgrammingError :
                pass
    # end def delete_database

# end class Postgresql

class Sqlite (MOM.DBW._DBS_) :
    """DB-specific functionality for Sqlite ."""

    scheme = "sqlite"

# end class Sqlite

if __name__ != "__main__" :
    MOM.DBW.SAS._Export ("*")
### __END__ MOM.DBW.SAS.DBS

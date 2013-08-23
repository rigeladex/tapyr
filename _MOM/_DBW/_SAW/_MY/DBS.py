# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.MY.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    MOM.DBW.SAW.MY.DBS
#
# Purpose
#    Encapsulate mySQL-specific functionality for SAW
#
# Revision Dates
#    24-Jun-2013 (CT) Creation
#    17-Jul-2013 (CT) Remove dependency on `MOM.DBW.SAS`
#    23-Aug-2013 (CT) Remove SAS-compatibility kludge `sa_scheme`
#    ««revision-date»»···
#--

from   __future__          import division, print_function
from   __future__          import absolute_import, unicode_literals

from   _MOM                import MOM
from   _TFL                import TFL

from   _TFL.pyk            import pyk

from   _MOM._DBW._SAW      import SA

import _MOM._DBW._SAW.DBS

class MY_DBS (MOM.DBW.SAW._NFB_DBS_) :
    """Encapsulate mySQL-specific functionality for SAW"""

    _real_name                = "DBS"

    query_last_cid_on_update  = True
    scheme                    = "mysql"
    table_kw                  = dict \
        ( mysql_engine        = "InnoDB"
        , mysql_charset       = "utf8"
        , mysql_collation     = "utf8_bin"
        )

    @classmethod
    def create_database (cls, db_url, manager, encoding  = "utf8") :
        try :
            engine = cls.create_engine (TFL.Url (db_url.scheme_auth))
            engine.execute \
                ( "CREATE DATABASE IF NOT EXISTS %s "
                    "DEFAULT CHARACTER SET %s "
                    "DEFAULT COLLATE %s_bin"
                % (str (db_url.path), encoding, encoding)
                )
        except SA.Exception.OperationalError as exc :
            pass
    # end def create_database

    @classmethod
    def create_engine (cls, db_url) :
        result = super (MY_DBS, cls).create_engine (db_url)
        ### XXX is this needed / wanted ???
        #result.execute ("SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        return result
    # end def create_engine

    @classmethod
    def _drop_database (cls, db_url, manager) :
        engine = cls.create_engine (TFL.Url (db_url.scheme_auth))
        ### This is necessary to avoid a nasty Warning that the database does
        ### not exist (even using the IF EXISTS clause)
        try :
            engine.execute ("use %s" % (str (db_url.path), ))
        except SA.Exception.OperationalError, exc :
            if (  '(1049, "Unknown database \'%s\'")' % (db_url.path, )
               not in exc.message
               ) :
                raise
        else :
            engine.execute \
                ("DROP DATABASE IF EXISTS %s" % (str (db_url.path), ))
    # end def _drop_database

DBS = MY_DBS # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.MY._Export ("*")
### __END__ MOM.DBW.SAW.MY.DBS

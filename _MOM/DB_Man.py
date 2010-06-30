# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.
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
#    MOM.DB_Man
#
# Purpose
#    Manager for data bases of MOM
#
# Revision Dates
#    30-Jun-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _TFL._Meta.Object

class DB_Man (TFL.Meta.Object) :
    """Manager for data bases of MOM."""

    attr_changes = {}
    ilk          = "PC"
    src          = None

    ### DB_Man creation methods
    @classmethod
    def connect (cls, db_url, app_type) :
        self     = cls.__new__ (db_url, app_type)
        self.ems = app_type.EMS.connect (self, db_url)
        return self
    # end def connect

    @classmethod
    def create (cls, db_url, app_type, from_db_man, chunk_size = 10000) :
        self            = cls.__new__ (db_url, app_type)
        self.src        = from_db_man
        self.ems        = app_type.EMS.new (self, db_url)
        self.chunk_size = chunk_size
        self._migrate (chunk_size)
        return self
    # end def create

    def __init__ (self) :
        raise TypeError \
            ( "Use {name}.connect or {name}.create to create "
                "new database managers".format (name = self.__class__.__name__)
            )
    # end def __init__

    def __new__ (cls, db_url, app_type) :
        self          = super (DB_Man, cls).__new__ (cls)
        self.db_url   = db_url
        self.app_type = app_type
        return self
    # end def __new__

    ### DB_Man instance methods

    def change_readonly (self, state) :
        """Change `readonly` state of database to `state`."""
        self.ems.change_readonly (state)
    # end def change_readonly

    @property
    def db_meta_data (self) :
        return self.ems.db_meta_data
    # end def db_meta_data

    def _migrate (self, chunk_size) :
        self.ems.pcm.consume \
            ( self.src.ems.produce_entities ()
            , self.src.ems.produce_changes  ()
            , chunk_size
            )
    # end def _migrate

# end class DB_Man

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.DB_Man

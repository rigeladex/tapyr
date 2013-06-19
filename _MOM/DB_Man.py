# -*- coding: iso-8859-15 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
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
#    12-Jul-2010 (CT) Signature changed from `db_url, app_type` to
#                     `app_type, db_url`
#    12-Jul-2010 (CT) `destroy` added
#    15-Jul-2010 (MG) `__str__` added
#    19-Jan-2013 (MG) Add support for `legacy_lifter`
#     7-Jun-2013 (CT) Pass `src.db_meta_data` to `consume`
#    ««revision-date»»···
#--

from   _MOM                  import MOM
from   _TFL                  import TFL

import _TFL._Meta.Object
import _TFL.Record
import _MOM.Legacy_Lifter

class DB_Man (TFL.Meta.Object) :
    """Manager for data bases of MOM."""

    uncommitted_changes    = TFL.Record (pending_attr_changes = {})
    ilk                    = "PC"
    src                    = None

    db_meta_data           = property (TFL.Getter.ems.db_meta_data)
    max_cid                = property (TFL.Getter.ems.max_cid)
    max_pid                = property (TFL.Getter.ems.max_pid)
    max_surrs              = property (TFL.Getter.ems.max_surrs)
    readonly               = property (TFL.Getter.ems.db_meta_data.readonly)

    ### DB_Man creation methods
    @classmethod
    def connect (cls, app_type, db_url) :
        db_url   = app_type.Url (db_url)
        self     = cls.__new__  (cls, app_type, db_url)
        self.ems = app_type.EMS.connect (self, db_url)
        return self
    # end def connect

    @classmethod
    def create ( cls, app_type, db_url, from_db_man
               , chunk_size    = 10000
               , legacy_lifter = None
               ) :
        db_url          = app_type.Url (db_url)
        self            = cls.__new__  (cls, app_type, db_url)
        self.src        = from_db_man
        self.ems        = app_type.EMS.new (self, db_url)
        self.chunk_size = chunk_size
        self._migrate (chunk_size, legacy_lifter)
        return self
    # end def create

    def __init__ (self) :
        raise TypeError \
            ( "Use {name}.connect or {name}.create to create "
                "new database managers".format (name = self.__class__.__name__)
            )
    # end def __init__

    def __new__ (cls, app_type, db_url) :
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

    def destroy (self) :
        self.ems.close ()
        self.__dict__.clear ()
    # end def destroy

    def _migrate (self, chunk_size, legacy_lifter) :
        ll = MOM.Legacy_Lifter (legacy_lifter)
        self.ems.pcm.consume \
            ( ll.entity_iter (self, self.src.ems.pcm.produce_entities ())
            , ll.change_iter (self, self.src.ems.pcm.produce_changes  ())
            , chunk_size
            , self.src.db_meta_data
            )
    # end def _migrate

    def __str__ (self) :
        return "%s <%s>" % (self.__class__.__name__, self.db_url)
    # end def __str__

# end class DB_Man

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.DB_Man

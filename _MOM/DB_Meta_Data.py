# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.
#
# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this script. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DB_Meta_Data
#
# Purpose
#    Provide meta data for MOM data base
#
# Revision Dates
#    30-Jun-2010 (CT) Creation (factored from `MOM.DBW.HPS.DB_Meta_Data`)
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _TFL.Environment
import _TFL.Record

import datetime

class _MOM_DB_Meta_Data_ (TFL.Record) :
    """Provide meta data for MOM data base."""

    _real_name = "DB_Meta_Data"

    @classmethod
    def COPY (cls, other) :
        return cls (** other._kw)
    # end def COPY

    @classmethod
    def NEW (cls, app_type, scope = None, ** kw) :
        Version = app_type.Version
        creator = TFL.Record \
            ( date          = datetime.datetime.now ()
            , tool_version  = Version.id
            , user          = getattr (scope, "user", TFL.Environment.username)
            )
        result  = cls \
            ( creator       = creator
            , dbv_hash      = app_type.db_version_hash
            , guid          = getattr (scope, "guid", None)
            , readonly      = False
            , root_epk      = getattr (scope, "root_epk", ())
            , ** kw
            )
        return result
    # end def NEW

DB_Meta_Data = _MOM_DB_Meta_Data_ # end class

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.DB_Meta_Data

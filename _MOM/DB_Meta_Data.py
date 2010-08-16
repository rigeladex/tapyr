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
#    13-Aug-2010 (CT) `COPY` changed to set `readonly` to `False`
#    16-Aug-2010 (CT) `COPY` changed to use `_copy_ignore` and `NEW`
#    16-Aug-2010 (CT) `NEW`  changed to pop from `kw`
#    ««revision-date»»···
#--

from   _MOM       import MOM
from   _TFL       import TFL

import _TFL.Environment
import _TFL.Record

import datetime

class _MOM_DB_Meta_Data_ (TFL.Record) :
    """Provide meta data for MOM data base."""

    _real_name   = "DB_Meta_Data"
    _copy_ignore = set (( "readonly", "dbv_hash"))

    @classmethod
    def COPY (cls, other, app_type, scope = None) :
        ignore = cls._copy_ignore | other._copy_ignore
        kw     = other._kw
        return cls.NEW \
            ( app_type, scope
            , ** dict ((k, kw [k]) for k in kw if k not in ignore)
            )
    # end def COPY

    @classmethod
    def NEW (cls, app_type, scope = None, ** _kw) :
        kw      = dict (_kw)
        Version = app_type.Version
        result  = cls \
            ( creator       = kw.pop ("creator", None) or TFL.Record
                ( date          = datetime.datetime.now ()
                , tool_version  = Version.id
                , user          =
                    getattr (scope, "user", TFL.Environment.username)
                )
            , dbv_hash      = app_type.db_version_hash
            , guid          =
                kw.pop ("guid", None) or getattr (scope, "guid", None)
            , readonly      = kw.pop ("readonly", False)
            , root_epk      =
                kw.pop ("root_epk", None) or getattr (scope, "root_epk", ())
            , ** kw
            )
        return result
    # end def NEW

DB_Meta_Data = _MOM_DB_Meta_Data_ # end class

if __name__ != "__main__" :
    MOM._Export ("*")
### __END__ MOM.DB_Meta_Data

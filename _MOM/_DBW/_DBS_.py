# -*- coding: iso-8859-1 -*-
# Copyright (C) 2010 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# ****************************************************************************
# This module is part of the package MOM.DBW.
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
#    MOM.DBW._DBS_
#
# Purpose
#    Encapsulate db-specific functionality
#
# Revision Dates
#    23-Jun-2010 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM                      import MOM
from   _TFL                      import TFL
from   _TFL                      import sos

import _MOM._DBW._Manager_

import _TFL._Meta.Object
import _TFL.Url

class _M_DBS_ (TFL.Meta.Object.__class__) :
    """Meta class for DBS classes."""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if not name.startswith ("_") :
            MOM.DBW._Manager_.DBS_map [cls.scheme] = cls
    # end def __init__

# end class _M_DBS_

class _DBS_ (TFL.Meta.Object) :
    """Base class for DBS classes."""

    __metaclass__ = _M_DBS_

    @classmethod
    def create_database (cls, db_url, manager) :
        pass
    # end def create_database

    @classmethod
    def delete_database (cls, db_url, manager) :
        try :
            sos.unlink (db_url.path)
        except OSError :
            pass
    # end def delete_database

    @classmethod
    def reserve_pid (cls, connection, pid) :
        pass
    # end def reserve_pid

    @classmethod
    def Url (cls, value, ANS, default_path = None) :
        result = TFL.Url (value, fs_path = True)
        if not result.path and default_path is not None :
            result = TFL.Url.new (result, path = default_path, fs_path = True)
        result.scheme_auth = "://".join ((result.scheme, result.authority))
        result.create = False
        return result
    # end def Url

# end class _DBS_

if __name__ != "__main__" :
    MOM.DBW._Export ("_DBS_")
### __END__ MOM.DBW._DBS_

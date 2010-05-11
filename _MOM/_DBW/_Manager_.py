# -*- coding: iso-8859-1 -*-
# Copyright (C) 2009-2010 Martin Glueck. All rights reserved
# Langstrasse 4, 2244 Spannberg, Austria. martin@mangari.org
# ****************************************************************************
# This module is part of the package _MOM.
#
# This module is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW._Manager_
#
# Purpose
#    Base class for database backend specific _Manager_ classes
#
# Revision Dates
#    19-Oct-2009 (MG) Creation
#    30-Nov-2009 (CT) `update_etype` added
#     4-Dec-2009 (MG) Renamed from `Session` to `_Manager_`
#    16-Dec-2009 (MG) `_Manager_.prepare` added
#    27-Jan-2010 (MG) `update_etype` parameter `app_type` added
#    11-May-2010 (CT) `Pid_Manager` added
#    ««revision-date»»···
#--

from   _TFL       import TFL
from   _MOM       import MOM

import _MOM._DBW
import _MOM._DBW.Pid_Manager

import _TFL._Meta.Object

class _M_Manager_ (TFL.Meta.Object.__class__) :
    """Backend independent _Manager_, describes the common interface."""

    def create_database (cls, db_uri, scope) :
        raise NotImplementedError
    # end def create_database

    def connect_database (cls, db_uri, scope) :
        raise NotImplementedError
    # end def connect_database

    def etype_decorator (cls, e_type) :
        return e_type
    # end def etype_decorator

    def prepare (self) :
        pass
    # end def prepare

    def update_etype (cls, e_type, app_type) :
        pass
    # end def update_etype

# end class _M_Manager_

class _Manager_ (TFL.Meta.Object) :
    """Base class for database backend specific _Manager_ classes"""

    __metaclass__ = _M_Manager_

    Pid_Manager   = MOM.DBW.Pid_Manager

    type_name     = "Bare"

    def commit (self) :
        raise NotImplementedError
    # end def commit

# end class _Manager_

if __name__ != '__main__':
    MOM.DBW._Export ("_Manager_")
### __END__ MOM.DBW._Manager_

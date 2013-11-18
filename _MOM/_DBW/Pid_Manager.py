# -*- coding: utf-8 -*-
# Copyright (C) 2010-2013 Mag. Christian Tanzer All rights reserved
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
#    MOM.DBW.Pid_Manager
#
# Purpose
#    Base class for database backend specific manager for permanent ids
#
# Revision Dates
#    11-May-2010 (CT) Creation
#    11-May-2010 (MG) `__init__` added
#    12-May-2010 (CT) `retire` added
#    17-May-2010 (MG) `kw` added to `__call__`
#     4-Aug-2012 (CT) Remove implementation of `retire`
#     6-Jun-2013 (CT) Use `@subclass_responsibility`
#    26-Aug-2013 (CT) Move `__call__` to `HPS`
#    ««revision-date»»···
#--

from   _TFL              import TFL
from   _MOM              import MOM

import _MOM._DBW

from   _TFL.Decorator    import subclass_responsibility
import _TFL._Meta.Object

class _Pid_Manager_ (TFL.Meta.Object) :
    """Base class for database backend specific manager for permanent ids."""

    _real_name = "Pid_Manager"

    def __init__ (self, ems, db_url) :
        self.ems = ems
    # end def __init__

    @subclass_responsibility
    def new (self, entity) :
        """Return a new `pid` to be used for `entity`."""
    # end def new

    @subclass_responsibility
    def query (self, pid) :
        """Return entity with `pid`."""
    # end def query

    @subclass_responsibility
    def reserve (self, entity, pid) :
        """Reserve `pid` for use for `entity.` `pid` must not be already used
           for any other entity.
        """
    # end def reserve

    @subclass_responsibility
    def retire (self, entity) :
        """Retire any resources held for `entity` (but `entity.pid` won't get
           reused, ever).
        """
    # end def retire

Pid_Manager = _Pid_Manager_ # end class

if __name__ != "__main__" :
    MOM.DBW._Export ("*")
### __END__ MOM.DBW.Pid_Manager

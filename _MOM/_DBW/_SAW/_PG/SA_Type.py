# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.PG.
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
#    MOM.DBW.SAW.PG.SA_Type
#
# Purpose
#    Encapsulate SQLalchemy types for PostgreSQL
#
# Revision Dates
#     2-Aug-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

from   _MOM._DBW._SAW        import SA
import _MOM._DBW._SAW.SA_Type

import sqlalchemy.dialects.postgresql

class M_SA_Type_PG (MOM.DBW.SAW.SA_Type.__class__) :

    _real_name = "M_SA_Type"

    def __getattr__ (cls, name) :
        try :
            return cls.__m_super.__getattr__ (name)
        except AttributeError :
            result = getattr (sqlalchemy.dialects.postgresql, name.upper ())
            setattr (cls, name, result)
            return result
    # end def __getattr__

M_SA_Type = M_SA_Type_PG # end class

class _PG_SA_Type_ \
        (TFL.Meta.BaM (MOM.DBW.SAW.SA_Type, metaclass = M_SA_Type_PG)) :
    """Encapsulate SQLalchemy types for PostgreSQL"""

    _real_name   = "SA_Type"

SA_Type = _PG_SA_Type_ # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.PG._Export ("SA_Type")
### __END__ MOM.DBW.SAW.PG.SA_Type

# -*- coding: utf-8 -*-
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
#    MOM.DBW.SAW.PG.Manager
#
# Purpose
#    Database wrapper for PostgreSQL accessed by sqlalchemy wrapped by SAW
#
# Revision Dates
#    21-Jun-2013 (CT) Creation
#    28-Jul-2013 (CT) Add import for `...PG.Sequence`
#     2-Aug-2013 (CT) Add import for `...PG.SA_Type`
#    ««revision-date»»···
#--

from   __future__                 import division, print_function
from   __future__                 import absolute_import, unicode_literals

from   _MOM                       import MOM
from   _TFL                       import TFL

from   _TFL.pyk                   import pyk

from   _MOM._DBW._SAW             import SA

import _MOM._DBW._SAW.Manager
class _M_SAW_PG_Manager_ (MOM.DBW.SAW.Manager.__class__) :
    """Meta class of MOM.DBW.SAW.PG.Manager"""

# end class _M_SAW_PG_Manager_

class _SAW_PG_Manager_ \
          (TFL.Meta.BaM (MOM.DBW.SAW.Manager, metaclass = _M_SAW_PG_Manager_)) :
    """Database wrapper for SAW-wrapped sqlalchemy-PostgreSQL"""

    _real_name    = "Manager"

    PNS           = MOM.DBW.SAW.PG

Manager = _SAW_PG_Manager_ # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.PG._Export ("*")

    ### The following modules dispatch on `Manager.__class__` and therefore
    ### needs to import `Manager`. Due to the cycle we need to import them
    ### after defining and exporting `Manager`
    import _MOM._DBW._SAW._PG.Attr
    import _MOM._DBW._SAW._PG.DBS
    import _MOM._DBW._SAW._PG.E_Type_Wrapper
    import _MOM._DBW._SAW._PG.Pid_Manager
    import _MOM._DBW._SAW._PG.SA_Type
    import _MOM._DBW._SAW._PG.Sequence
### __END__ MOM.DBW.SAW.PG.Manager

# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.SAW.SQ.
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
#    MOM.DBW.SAW.SQ.Manager
#
# Purpose
#    Database wrapper for SQLite accessed by sqlalchemy wrapped by SAW
#
# Revision Dates
#    21-Jun-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__          import division, print_function
from   __future__          import absolute_import, unicode_literals

from   _MOM                import MOM
from   _TFL                import TFL
from   _TFL.pyk            import pyk

from   _MOM._DBW._SAW      import SA

import _MOM._DBW._SAW.Manager
import _MOM._DBW._SAW._SQ.DBS
import _MOM._DBW._SAW._SQ.Pid_Manager
import _MOM._DBW._SAW._SQ.SA_Type
import _MOM._DBW._SAW._SQ.Sequence
import _MOM._DBW._SAW._SQ.Session

class _M_SAW_SQ_Manager_ (MOM.DBW.SAW.Manager.__class__) :
    """Meta class of MOM.DBW.SAW.SQ.Manager"""

# end class _M_SAW_SQ_Manager_

class _SAW_SQ_Manager_ \
          (TFL.Meta.BaM (MOM.DBW.SAW.Manager, metaclass = _M_SAW_SQ_Manager_)) :
    """Database wrapper for SAW-wrapped sqlalchemy-SQLite"""

    _real_name    = "Manager"

    PNS           = MOM.DBW.SAW.SQ

Manager = _SAW_SQ_Manager_ # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.SQ._Export ("*")

    ### The following modules dispatch on `Manager.__class__` and therefore
    ### needs to import `Manager`. Due to the cycle we need to import them
    ### after defining and exporting `Manager`
    import _MOM._DBW._SAW._SQ.Attr
    import _MOM._DBW._SAW._SQ.E_Type_Wrapper
### __END__ MOM.DBW.SAW.SQ.Manager

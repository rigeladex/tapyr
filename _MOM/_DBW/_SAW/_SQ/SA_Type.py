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
#    MOM.DBW.SAW.SQ.SA_Type
#
# Purpose
#    Encapsulate SQLalchemy types for SQLite
#
# Revision Dates
#    18-Jul-2013 (CT) Creation
#    ««revision-date»»···
#--

from   __future__ import division, print_function
from   __future__ import absolute_import, unicode_literals

from   _MOM                  import MOM
from   _TFL                  import TFL
from   _TFL.pyk              import pyk

from   _MOM._DBW._SAW        import SA
import _MOM._DBW._SAW.SA_Type

class _SQ_SA_Type_ (MOM.DBW.SAW.SA_Type) :
    """Encapsulate SQLalchemy types for SQLite"""

    _real_name   = "SA_Type"

SA_Type = _SQ_SA_Type_ # end class

if __name__ != "__main__" :
    MOM.DBW.SAW.SQ._Export ("SA_Type")
### __END__ MOM.DBW.SAW.SQ.SA_Type

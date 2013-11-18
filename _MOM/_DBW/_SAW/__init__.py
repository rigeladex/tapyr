# -*- coding: utf-8 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package MOM.DBW.
#
# This package is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This package is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this package.  If not, see <http://www.gnu.org/licenses/>.
# ****************************************************************************
#
#++
# Name
#    MOM.DBW.SAW.__init__
#
# Purpose
#    Base database wrapper for databases accessed via sqlalchemy
#
# Revision Dates
#    28-May-2013 (CT) Creation
#    ««revision-date»»···
#--

from   _MOM._DBW              import DBW
from   _TFL.Package_Namespace import Package_Namespace

SAW = Package_Namespace ()
DBW._Export ("SAW")

del Package_Namespace

__doc__ = """
.. moduleauthor:: Christian Tanzer <tanzer@swing.co.at>

`MOM.DBW.SAW` provides a database wrapper for databases accessed via
SQLAlchemy.

"""

### __END__ MOM.DBW.SAW.__init__
